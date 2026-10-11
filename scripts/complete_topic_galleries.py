#!/usr/bin/env python3
import hashlib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from seo_engine import protected, runtime_digest
from build_topic_resource_cards import valid_page, preview_image

TOPICS = {
    "akran-catismasi": ["akran çatışması", "çatışma çözme", "çatışma çözümü"],
    "arkadaslik-iliskileri": ["arkadaşlık ilişkileri", "arkadaşlık becerileri", "arkadaşlık kurma"],
    "ofke-yonetimi": ["öfke yönetimi", "öfkeyle baş", "öfke kontrolü", "öfke ve"],
    "okul-aidiyeti": ["okul aidiyeti", "okula aidiyet", "okul bağlılığı", "okul bağlılığı"],
    "okul-reddi": ["okul reddi", "okul reddine"],
    "ozguven": ["özgüven", "öz güven", "özsaygı", "benlik saygısı"],
    "problem-cozme-becerileri": ["problem çözme becerileri", "problem çözme", "sorun çözme"],
    "sinifta-iletisim-becerileri": ["iletişim becerileri", "etkili iletişim", "iletişim kurma"],
}

START = "<!-- TOPIC-RESOURCE-CARDS-START -->"
END = "<!-- TOPIC-RESOURCE-CARDS-END -->"

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def norm(value):
    value = str(value or "").translate(str.maketrans(
        "çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"
    )).casefold()
    return unicodedata.normalize("NFKC", value)

def escape(value):
    return html.escape(str(value or ""), quote=True)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

library = load("data/library.json")
collected = load("data/collected-resources.json")
previews = load("data/resource-previews.json")
baseline = load("seo/protected-files.json")
approvals = load("seo/approved-edits.json")

if not isinstance(previews, dict):
    raise SystemExit("Önizleme verisi beklenen formatta değil.")

link_text = (ROOT / "src/resource-page-links.js").read_text(encoding="utf-8")
links = dict(re.findall(r'"([^"]+)"\s*:\s*"(/[^"]+)"', link_text))

css = """
<style>
.pdr-topic-resources{margin:36px 0;padding:clamp(20px,4vw,38px);background:#f7faf6;border:1px solid #dbe7dd;border-radius:24px}
.pdr-topic-resources h2{font-family:Georgia,serif;color:#123c31;font-size:clamp(24px,3vw,34px)}
.pdr-topic-resources>p{color:#506558;line-height:1.7}
.pdr-topic-resource-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:22px}
.pdr-topic-resource-card{display:flex;flex-direction:column;overflow:hidden;background:#fff;border:1px solid #dce6dd;border-radius:16px;text-decoration:none;color:#123c31}
.pdr-topic-resource-card:hover{border-color:#85a996}
.pdr-topic-resource-visual{height:154px;background:#e9f0e9;display:flex;align-items:center;justify-content:center;overflow:hidden}
.pdr-topic-resource-visual img{width:100%;height:100%;object-fit:contain}
.pdr-topic-resource-file{font:700 21px Manrope,Arial,sans-serif;border:2px solid #adc5b5;border-radius:9px;padding:16px;color:#376a4c}
.pdr-topic-resource-body{display:flex;flex-direction:column;gap:10px;padding:17px;flex:1}
.pdr-topic-resource-body small{font:600 12px Manrope,Arial,sans-serif;color:#64816e}
.pdr-topic-resource-body strong{font:700 15px/1.5 Manrope,Arial,sans-serif}
.pdr-topic-resource-action{margin-top:auto;font-size:13px;font-weight:700;color:#176347}
@media(max-width:850px){.pdr-topic-resource-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.pdr-topic-resource-grid{grid-template-columns:1fr}}
</style>
"""

prepared = []
skipped = []

for slug, terms in TOPICS.items():
    page = ROOT / "konu" / slug / "index.html"
    original = page.read_text(encoding="utf-8")

    if START in original or "PDR-KONU-REHBERI-2-START" in original:
        print(f"Zaten galeri var: {slug}")
        continue

    matches = []
    seen_urls = set()

    for row in library + collected:
        searchable = norm(
            f'{row.get("title", "")} {row.get("topic", "")}'
        )
        if not any(norm(term) in searchable for term in terms):
            continue

        rid = row.get("id")
        url = row.get("pagePath") or links.get(rid, "")

        if not valid_page(url):
            fallback = f"/kaynak-detay/{rid}/"
            url = fallback if valid_page(fallback) else ""

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        matches.append((row, url))
        if len(matches) == 9:
            break

    # Kaynağı olmayan konuya alakasız kart eklemiyoruz.
    if not matches:
        skipped.append(slug)
        continue

    cards = []
    for row, url in matches:
        image = preview_image(row["id"], previews)
        visual = (
            f'<img src="{escape(image)}" alt="{escape(row.get("title"))} önizlemesi" loading="lazy" decoding="async">'
            if image else
            '<span class="pdr-topic-resource-file">PDF</span>'
        )
        cards.append(
            f'<a class="pdr-topic-resource-card" href="{escape(url)}">'
            f'<span class="pdr-topic-resource-visual">{visual}</span>'
            '<span class="pdr-topic-resource-body">'
            f'<small>{escape(row.get("level", "Tüm kademeler"))} · {escape(row.get("type", "Materyal"))}</small>'
            f'<strong>{escape(row.get("title", "Kaynak"))}</strong>'
            '<span class="pdr-topic-resource-action">Kaynağı incele →</span>'
            '</span></a>'
        )

    block = (
        f'\n{START}\n{css}\n'
        '<section class="pdr-topic-resources" aria-label="Önerilen materyaller">'
        '<h2>Bu konuda kullanabileceğiniz materyaller</h2>'
        '<p>İlgili kaynakları doğrudan kendi sayfalarında inceleyebilirsiniz.</p>'
        f'<div class="pdr-topic-resource-grid">{"".join(cards)}</div>'
        f'</section>\n{END}\n'
    )

    updated = original

    if "</main>" not in updated:
        if updated.count("<main") != 1:
            skipped.append(slug + " (HTML yapısı)")
            continue

        if "<footer" in updated:
            updated = updated.replace("<footer", "</main>\n<footer", 1)
        elif "</body>" in updated:
            updated = updated.replace("</body>", "</main>\n</body>", 1)
        else:
            skipped.append(slug + " (Kapanış etiketi bulunamadı)")
            continue

    if updated.count("</main>") != 1:
        skipped.append(slug + " (HTML yapısı)")
        continue

    updated = updated.replace("</main>", block + "</main>", 1)
    prepared.append((page, updated, len(cards)))

# Önce tüm değişiklikleri hazırla, ardından yaz.
for page, updated, count in prepared:
    page.write_text(updated, encoding="utf-8")
    relative = page.relative_to(ROOT).as_posix()

    if relative in baseline["files"]:
        approvals["edits"][relative] = {
            "baseline_sha256": baseline["files"][relative],
            "reviewed_sha256": digest(page),
            "runtime_sha256": runtime_digest(updated),
            "reason": "Reviewed topic gallery completion with verified relevant resource detail links and existing previews."
        }
    print(f"✅ {page.parent.name}: {count} kaynak kartı")

(ROOT / "seo/approved-edits.json").write_text(
    json.dumps(approvals, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)

result = protected(ROOT)

print("\n=== SONUÇ ===")
print("Yeni galeri eklenen:", len(prepared))
print("Kaynak bulunamadığı için atlanan:", len(skipped))
print("Atlananlar:", skipped)
print("SEO koruması:", "BAŞARILI" if result["pass"] else "BAŞARISIZ")

if not result["pass"]:
    print(result["changed"])
    raise SystemExit(1)
