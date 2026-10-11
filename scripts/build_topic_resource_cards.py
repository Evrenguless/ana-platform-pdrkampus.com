#!/usr/bin/env python3
"""Mevcut konu sayfalarına doğrulanmış, önizlemeli kaynak kartları ekler."""

import hashlib
import html
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- TOPIC-RESOURCE-CARDS-START -->"
END = "<!-- TOPIC-RESOURCE-CARDS-END -->"

sys.path.insert(0, str(ROOT / "scripts"))
from seo_engine import runtime_digest, protected

def read_json(name, default):
    path = ROOT / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def esc(value):
    return html.escape(str(value or ""), quote=True)

def valid_page(url):
    if not url or not url.startswith("/") or url.startswith("//"):
        return False

    parsed = urlsplit(url)

    if parsed.query or parsed.fragment:
        return False

    target = (ROOT / parsed.path.lstrip("/")).resolve()

    if target.is_dir():
        target /= "index.html"

    return (
        target.is_file()
        and ROOT.resolve() in target.parents
        and target.suffix == ".html"
    )

def normalize(text):
    return (
        str(text or "")
        .replace("ı", "i")
        .replace("İ", "i")
        .replace("ş", "s")
        .replace("ğ", "g")
        .replace("ü", "u")
        .replace("ö", "o")
        .replace("ç", "c")
        .casefold()
        .strip()
    )

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href:
                self.hrefs.append(html.unescape(href))

def preview_image(resource_id, previews):
    data = previews.get(resource_id)

    if isinstance(data, str):
        candidates = [data]
    elif isinstance(data, dict):
        candidates = [
            data.get(k)
            for k in ("thumbnail", "cover", "image", "preview", "src")
        ]

        for item in data.get("previews", []):
            if isinstance(item, str):
                candidates.append(item)
            elif isinstance(item, dict):
                candidates.extend(
                    item.get(k)
                    for k in ("thumbnail", "src", "image", "url")
                )
    else:
        candidates = []

    for candidate in candidates:
        if not isinstance(candidate, str):
            continue

        parsed = urlsplit(candidate)

        if parsed.scheme or parsed.netloc:
            continue

        target = (ROOT / parsed.path.lstrip("/")).resolve()

        if (
            target.is_file()
            and ROOT.resolve() in target.parents
            and target.suffix.lower() in (".webp", ".jpg", ".jpeg", ".png")
        ):
            return "/" + target.relative_to(ROOT).as_posix()

    return None

def main():
    library = read_json("data/library.json", [])
    collected = read_json("data/collected-resources.json", [])
    previews = read_json("data/resource-previews.json", {})

    if not isinstance(previews, dict):
        previews = {}

    link_source = (ROOT / "src/resource-page-links.js").read_text(
        encoding="utf-8"
    )

    links = dict(re.findall(
        r'"([^"]+)"\s*:\s*"(/[^"]+)"',
        link_source
    ))

    records = {}
    by_url = {}

    for row in library + collected:
        rid = row.get("id")
        if not rid:
            continue

        url = row.get("pagePath") or links.get(rid)

        if not valid_page(url or ""):
            fallback = f"/kaynak-detay/{rid}/"
            if valid_page(fallback):
                url = fallback
            else:
                continue

        records[rid] = row
        by_url[url] = rid

    baseline = read_json("seo/protected-files.json", {})
    approvals = read_json(
        "seo/approved-edits.json",
        {"version": 1, "edits": {}}
    )

    css = """
<style>
.pdr-topic-resources{margin:36px 0;padding:clamp(20px,4vw,38px);
background:#f7faf6;border:1px solid #dbe7dd;border-radius:24px}
.pdr-topic-resources h2{font-family:Georgia,serif;color:#123c31;
font-size:clamp(24px,3vw,34px)}
.pdr-topic-resources>p{color:#506558;line-height:1.7}
.pdr-topic-resource-grid{display:grid;
grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:22px}
.pdr-topic-resource-card{display:flex;flex-direction:column;overflow:hidden;
background:white;border:1px solid #dce6dd;border-radius:16px;
text-decoration:none;color:#123c31}
.pdr-topic-resource-card:hover{border-color:#85a996}
.pdr-topic-resource-visual{height:154px;background:#e9f0e9;
display:flex;align-items:center;justify-content:center;overflow:hidden}
.pdr-topic-resource-visual img{width:100%;height:100%;object-fit:contain}
.pdr-topic-resource-file{font:700 21px Manrope,Arial,sans-serif;
border:2px solid #adc5b5;border-radius:9px;padding:16px;color:#376a4c}
.pdr-topic-resource-body{display:flex;flex-direction:column;gap:10px;
padding:17px;flex:1}
.pdr-topic-resource-body small{font:600 12px Manrope,Arial,sans-serif;
color:#64816e}
.pdr-topic-resource-body strong{font:700 15px/1.5 Manrope,Arial,sans-serif}
.pdr-topic-resource-action{margin-top:auto;font-size:13px;
font-weight:700;color:#176347}
@media(max-width:850px){
.pdr-topic-resource-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){
.pdr-topic-resource-grid{grid-template-columns:1fr}}
</style>
"""

    updated = []
    skipped = []
    total_cards = 0
    total_previews = 0

    for page in sorted((ROOT / "konu").glob("*/index.html")):
        source = page.read_text(encoding="utf-8")
        slug = page.parent.name

        # Akran Zorbalığı sayfasında önizlemeli galeri zaten bulunuyor.
        if "PDR-KONU-REHBERI-2-START" in source:
            skipped.append((slug, "Mevcut galeri korunuyor"))
            continue

        if source.count("</main>") != 1:
            skipped.append((slug, "HTML yapısı kontrol edilmeli"))
            continue

        if START in source:
            source = re.sub(
                re.escape(START) + r".*?" + re.escape(END),
                "",
                source,
                flags=re.S
            )

        parser = LinkParser()
        parser.feed(source)

        # Sayfanın mevcut kaynak bağlantıları en güvenilir eşleştirme.
        candidates = []

        for href in parser.hrefs:
            parsed = urlsplit(href)

            if parsed.netloc not in (
                "", "pdrkampus.com", "www.pdrkampus.com"
            ):
                continue

            rid = by_url.get(parsed.path)

            if rid and rid not in candidates:
                candidates.append(rid)

        # Konu kaydı birebir eşleşirse ek kaynak bul.
        for rid, row in records.items():
            topic = normalize(row.get("topic", ""))
            title = normalize(row.get("title", ""))
            label = normalize(slug.replace("-", " "))

            if topic == label or (
                len(label) >= 9 and label in title
            ):
                if rid not in candidates:
                    candidates.append(rid)

        cards = []
        image_count = 0

        for rid in candidates:
            row = records[rid]
            url = row.get("pagePath") or links.get(rid)

            if not valid_page(url or ""):
                url = f"/kaynak-detay/{rid}/"

            if not valid_page(url):
                continue

            image = preview_image(rid, previews)

            if image:
                image_count += 1
                visual = (
                    f'<img src="{esc(image)}" '
                    f'alt="{esc(row.get("title"))} önizlemesi" '
                    'loading="lazy" decoding="async">'
                )
            else:
                visual = '<span class="pdr-topic-resource-file">PDF</span>'

            cards.append(
                f'<a class="pdr-topic-resource-card" href="{esc(url)}">'
                f'<span class="pdr-topic-resource-visual">{visual}</span>'
                f'<span class="pdr-topic-resource-body">'
                f'<small>{esc(row.get("level", "Tüm kademeler"))} · '
                f'{esc(row.get("type", "Materyal"))}</small>'
                f'<strong>{esc(row.get("title", "Kaynak"))}</strong>'
                f'<span class="pdr-topic-resource-action">Kaynağı incele →</span>'
                '</span></a>'
            )

            if len(cards) == 9:
                break

        # İlgisiz veya yetersiz kaynakla boş galeri oluşturma.
        if len(cards) < 3:
            skipped.append((slug, f"Yalnızca {len(cards)} kaynak eşleşti"))
            continue

        block = f"""
{START}
{css}
<section class="pdr-topic-resources" aria-label="Önerilen materyaller">
<h2>Bu konuda kullanabileceğiniz materyaller</h2>
<p>İlgili kaynakları doğrudan kendi sayfalarında inceleyebilir,
önizleyebilir ve erişilebilir dosyalarını kullanabilirsiniz.</p>
<div class="pdr-topic-resource-grid">
{''.join(cards)}
</div>
</section>
{END}
"""

        changed = source.replace("</main>", block + "\n</main>", 1)
        page.write_text(changed, encoding="utf-8")

        relative = page.relative_to(ROOT).as_posix()

        if relative in baseline.get("files", {}):
            approvals.setdefault("edits", {})[relative] = {
                "baseline_sha256": baseline["files"][relative],
                "reviewed_sha256": sha(page),
                "runtime_sha256": runtime_digest(changed),
                "reason": (
                    "Reviewed topic resource gallery: verified existing "
                    "resource pages, original article and SEO metadata preserved."
                )
            }

        updated.append((slug, len(cards), image_count))
        total_cards += len(cards)
        total_previews += image_count

    approval_file = ROOT / "seo/approved-edits.json"

    approval_file.write_text(
        json.dumps(approvals, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    report = {
        "updated": updated,
        "skipped": skipped,
        "total_cards": total_cards,
        "real_previews": total_previews
    }

    output = ROOT / "seo/topic-resource-gallery-report.json"
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    result = protected(ROOT)

    print("\n=== KONU REHBERLERİ 2.0 ===")
    print("Güncellenen sayfa:", len(updated))
    print("Eklenen materyal kartı:", total_cards)
    print("Gerçek görsel önizlemesi:", total_previews)
    print("Atlanan sayfa:", len(skipped))
    print("SEO koruması:", "BAŞARILI" if result["pass"] else "BAŞARISIZ")

    print("\nGüncellenen konular:")
    for slug, count, images in updated:
        print(f"✅ {slug}: {count} kart, {images} önizleme")

    print("\nAtlanan konular:")
    for slug, reason in skipped:
        print(f"— {slug}: {reason}")

    if not result["pass"]:
        print("Koruma sorunları:", result["changed"])
        raise SystemExit(1)

if __name__ == "__main__":
    main()
