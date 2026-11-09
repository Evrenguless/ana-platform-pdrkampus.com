#!/usr/bin/env python3
"""PDR Kampüs: kütüphane sayfalarında kısa başlık, paylaşım görseli ve yayın tarihi.

İdempotent: tekrar çalıştırmak aynı sonucu verir. Kısaltılan başlıklar
seo/approved-page-titles.json'a yazılır, böylece üreticiler aynı başlığı korur.
Yönlendirme ve noindex sayfalarına dokunulmaz.
"""
import argparse, glob, html, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://pdrkampus.com'
BRAND = ' | PDR Kampüs'
MAX = 60
FALLBACK_IMAGE = '/assets/logo.png'


def indexable(src):
    return 'http-equiv="refresh"' not in src and not re.search(r'<meta name="robots" content="[^"]*noindex', src)


def first_added_dates():
    out = subprocess.run(['git', 'log', '--diff-filter=A', '--format=@%cs', '--name-only', '--', 'kutuphane/*/index.html'],
                         cwd=ROOT, text=True, capture_output=True, check=True).stdout
    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith('@'):
            current = line[1:]
        elif line.strip():
            dates[line.strip()] = current  # log is newest first; keep the oldest add
    return dates


def title_of(src):
    m = re.search(r'<title>(.*?)</title>', src, re.S)
    return html.unescape(m.group(1)) if m else ''


def h1_of(src):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', m.group(1)))).strip() if m else ''


def preview_image(src, previews):
    m = re.search(r'id="resourcePreviewData"[^>]*>(.*?)</script>', src, re.S)
    if not m:
        return None
    try:
        rid = json.loads(m.group(1)).get('id')
    except ValueError:
        return None
    entry = previews.get(rid) or {}
    img = (entry.get('previews') or [None])[0] or entry.get('thumbnail')
    return img if img and (ROOT / img.lstrip('/')).is_file() else None


def set_meta(src, attr, key, value):
    tag = '<meta ' + attr + '="' + key + '" content="' + html.escape(value, quote=True) + '">'
    pattern = r'<meta ' + attr + '="' + re.escape(key) + r'" content="[^"]*">'
    if re.search(pattern, src):
        return re.sub(pattern, lambda _: tag, src, count=1)
    return src.replace('</head>', tag + '</head>', 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    previews = json.loads((ROOT / 'data/resource-previews.json').read_text(encoding='utf-8'))
    manifest_path = ROOT / 'seo/approved-page-titles.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    approved = manifest.setdefault('titles', {})
    dates = first_added_dates()

    pages = {}
    for f in glob.glob(str(ROOT / '**/*.html'), recursive=True):
        rel = Path(f).relative_to(ROOT).as_posix()
        if rel.startswith(('_staging/', 'inventory-review/', 'node_modules/', 'drafts/')):
            continue
        src = Path(f).read_text(encoding='utf-8')
        if indexable(src):
            pages[rel] = src
    used = {}
    for rel, src in pages.items():
        used.setdefault(title_of(src), set()).add(rel)

    changed = {}
    stats = {'titles': 0, 'images': 0, 'large_images': 0, 'dates': 0}
    for rel in sorted(pages):
        if not (rel.startswith('kutuphane/') and rel.endswith('/index.html')) or rel.startswith('kutuphane/katalog/'):
            continue
        src = original = pages[rel]
        route = '/' + rel[:-len('index.html')]
        # 1) Kısa ve benzersiz başlık
        old = title_of(src)
        # Aynı başlığı paylaşan sayfalar editoryal inceleme bekliyor; ayrıştırmayı başlıkla yapma.
        if len(old) > MAX and used.get(old, set()) == {rel}:
            h1 = h1_of(src)
            for cand in (h1 + BRAND, h1):
                if h1 and len(cand) <= MAX and not (used.get(cand, set()) - {rel}):
                    used.get(old, set()).discard(rel)
                    used.setdefault(cand, set()).add(rel)
                    src = re.sub(r'<title>.*?</title>', lambda _: '<title>' + html.escape(cand, quote=False) + '</title>', src, count=1, flags=re.S)
                    src = set_meta(src, 'property', 'og:title', cand)
                    approved[route] = cand
                    stats['titles'] += 1
                    break
        # 2) Paylaşım / Keşfet görseli
        img = preview_image(src, previews)
        src = set_meta(src, 'property', 'og:image', BASE + (img or FALLBACK_IMAGE))
        src = set_meta(src, 'name', 'twitter:card', 'summary_large_image' if img else 'summary')
        if not re.search(r'<meta name="robots"', src):
            src = src.replace('</head>', '<meta name="robots" content="index,follow,max-image-preview:large">' + '</head>', 1)
        stats['images'] += 1
        stats['large_images'] += bool(img)
        # 3) Yayın tarihi (ilk eklendiği commit)
        published = dates.get(rel)
        if published and '"datePublished"' not in src:
            src, n = re.subn(r'("@type":\s*"CreativeWork")', lambda m: m.group(1) + ',"datePublished":"' + published + '"', src, count=1)
            stats['dates'] += n
        if src != original:
            changed[rel] = src

    manifest['count'] = len(approved)
    new_manifest = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        stale = [rel for rel in changed] + (['seo/approved-page-titles.json'] if new_manifest != manifest_path.read_text(encoding='utf-8') else [])
        if stale:
            raise SystemExit('Run scripts/enhance_seo_meta.py: ' + ', '.join(stale[:5]))
        print('SEO meta verified.')
        return
    for rel, src in changed.items():
        (ROOT / rel).write_text(src, encoding='utf-8')
    manifest_path.write_text(new_manifest, encoding='utf-8')
    print(json.dumps({**stats, 'files_changed': len(changed)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
