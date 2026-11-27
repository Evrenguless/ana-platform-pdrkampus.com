"""Index policy: keep only proven or hand-curated pages in Google's index.

Background (Search Console, 27 Nov 2026): after ~8.700 pages were published in
three weeks, Google demoted the whole site on 26 Oct 2026 (average position
9 -> 30, impressions 6.600/day -> <100/day) and left 4.650 crawled pages
unindexed. Mass-produced template pages drag down the site-wide quality
signal, so this script marks every bulk resource/topic page `noindex,follow`
unless it is:

  * listed in seo/index-allowlist.txt (pages that earned Search impressions,
    exported from Search Console), or
  * a protected, hand-curated page in seo/protected-files.json, or
  * a library catalogue hub page (/kutuphane/katalog/...).

Pages stay online and linked; only Google indexing changes. Redirect stubs
are skipped. To promote a page back into the index after it gets real,
unique content, add its path to seo/index-allowlist.txt and re-run.

Usage: python scripts/apply_index_policy.py [--check]
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ('kutuphane', 'konu')
INDEX = '<meta name="robots" content="index,follow,max-image-preview:large">'
NOINDEX = '<meta name="robots" content="noindex,follow">'
ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>', re.I)


def explicit_allowlist():
    keep = set()
    for line in (ROOT / 'seo/index-allowlist.txt').read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            keep.add(line.strip('/'))
    return keep


def allowlist():
    keep = explicit_allowlist()
    protected = json.loads((ROOT / 'seo/protected-files.json').read_text(encoding='utf-8'))['files']
    for name in protected:
        if name.endswith('/index.html'):
            keep.add(name[:-len('/index.html')])
    return keep


def apply(route, source, keep, explicit):
    """Return the page source with the index policy applied.

    Kept pages are left as they are (an explicitly allow-listed page that was
    noindexed by this policy is switched back to index); every other bulk page
    gets noindex,follow. Redirect stubs and pages outside SECTIONS are untouched.
    """
    if not route.startswith(tuple(s + '/' for s in SECTIONS)) or 'http-equiv="refresh"' in source:
        return source
    if route in keep or route.startswith('kutuphane/katalog'):
        if route in explicit and NOINDEX in source:
            return source.replace(NOINDEX, INDEX, 1)
        return source
    if ROBOTS_RE.search(source):
        return ROBOTS_RE.sub(NOINDEX, source, count=1)
    return source.replace('</head>', NOINDEX + '</head>', 1)


def apply_outputs(outputs):
    """Apply the policy to a generator's {relative path: html} outputs."""
    keep, explicit = allowlist(), explicit_allowlist()
    for key, source in list(outputs.items()):
        if key.endswith('/index.html'):
            outputs[key] = apply(key[:-len('/index.html')], source, keep, explicit)
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    keep, explicit = allowlist(), explicit_allowlist()
    changed, noindexed, total = [], 0, 0
    for section in SECTIONS:
        for path in sorted((ROOT / section).glob('*/index.html')):
            route = str(path.parent.relative_to(ROOT))
            source = path.read_text(encoding='utf-8')
            updated = apply(route, source, keep, explicit)
            if 'http-equiv="refresh"' in source:
                continue
            total += 1
            noindexed += NOINDEX in updated
            if updated != source:
                changed.append(str(path.relative_to(ROOT)))
                if not args.check:
                    path.write_text(updated, encoding='utf-8')
    print(json.dumps({'pages': total, 'noindex': noindexed, 'indexable': total - noindexed,
                      'changed': len(changed)}, ensure_ascii=False))
    if args.check and changed:
        raise SystemExit('Index policy drift; run python scripts/apply_index_policy.py: ' + ', '.join(changed[:10]))


if __name__ == '__main__':
    main()
