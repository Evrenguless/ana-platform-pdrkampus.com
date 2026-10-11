#!/usr/bin/env python3
"""İlk dokuz PDR sayfasını mevcut konu rehberlerinin görsel düzenine tamamlar."""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_topic_resource_cards import preview_image, valid_page

PLAN = json.loads(
    (ROOT / "seo/icerik-plani/500-konu-listesi.json")
    .read_text(encoding="utf-8")
)

LIBRARY = {
    str(row["id"]): row
    for row in json.loads(
        (ROOT / "data/library.json").read_text(encoding="utf-8")
    )
    if row.get("id")
}

PREVIEWS = json.loads(
    (ROOT / "data/resource-previews.json").read_text(encoding="utf-8")
)

LINK_SOURCE = (
    ROOT / "src/resource-page-links.js"
).read_text(encoding="utf-8")

LINKS = dict(re.findall(
    r'"([^"]+)"\s*:\s*"(/[^"]+)"',
    LINK_SOURCE
))

# Sayfa amacına göre seçilmiş, katalogda mevcut kaynak kimlikleri.
SELECTED = {
    "PDR-002": [
        "zorbalik-kuramsal",
        "farkindalik-ortaokul",
        "farkindalik-lise",
    ],
    "PDR-003": [
        "zorbalik-kuramsal",
        "akranzorbaligi-psikoegitim-isparta-2025",
    ],
    "PDR-004": [
        "veli-brosur",
        "nevsehir-veli-akran-zorbaligi",
        "zorbalik-kuramsal",
    ],
    "PDR-005": [
        "zorbalik-kuramsal",
        "farkindalik-ilkokul",
        "farkindalik-ortaokul",
        "farkindalik-lise",
    ],
    "PDR-006": [
        "farkindalik-ilkokul",
        "zorbalik-kuramsal",
    ],
    "PDR-007": [
        "farkindalik-ortaokul",
        "zorbalik-kuramsal",
    ],
    "PDR-008": [
        "farkindalik-lise",
        "zorbalik-kuramsal",
    ],
    "PDR-009": [
        "zorbalik-kuramsal",
        "farkindalik-ilkokul",
        "farkindalik-ortaokul",
        "farkindalik-lise",
    ],
    "PDR-010": [
        "zorbalik-kuramsal",
        "farkindalik-ortaokul",
        "farkindalik-lise",
    ],
}

START = "<!-- PDR-COMPLETE-GUIDE-START -->"
END = "<!-- PDR-COMPLETE-GUIDE-END -->"

def esc(value):
    return html.escape(str(value or ""), quote=True)

def resource_url(rid):
    row = LIBRARY.get(rid, {})
    candidates = [
        row.get("pagePath"),
        LINKS.get(rid),
        f"/kaynak-detay/{rid}/",
    ]

    for url in candidates:
        if valid_page(url or ""):
            return url

    return None

def resource_card(rid):
    row = LIBRARY.get(rid)

    if not row:
        return None

    url = resource_url(rid)

    if not url:
        return None

    image = preview_image(rid, PREVIEWS)

    if image:
        visual = (
            f'<img src="{esc(image)}" '
            f'alt="{esc(row["title"])} önizlemesi" '
            'loading="lazy" decoding="async">'
        )
    else:
        visual = '<span class="pdr-topic-resource-file">PDF</span>'

    card = (
        f'<a class="pdr-topic-resource-card" href="{esc(url)}">'
        f'<span class="pdr-topic-resource-visual">{visual}</span>'
        '<span class="pdr-topic-resource-body">'
        f'<small>{esc(row.get("level", ""))} · '
        f'{esc(row.get("type", "Materyal"))}</small>'
        f'<strong>{esc(row["title"])}</strong>'
        f'<small>{esc(row.get("source", ""))}</small>'
        '<span class="pdr-topic-resource-action">'
        'Kaynağı incele →</span>'
        '</span></a>'
    )

    return card, bool(image)

CSS = """
<style>
.pdr-complete-related {
  margin: 22px 0 30px;
  padding: 23px;
  background: #f7faf6;
  border: 1px solid #dbe7dd;
  border-radius: 20px;
}
.pdr-complete-related h2 {
  font-family: Georgia,serif;
  color: #123c31;
  margin: 0 0 14px;
}
.pdr-complete-related-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.pdr-complete-related-links a {
  padding: 10px 14px;
  border: 1px solid #dbe7dd;
  border-radius: 12px;
  background: #fff;
  color: #123c31;
  text-decoration: none;
  font-weight: 600;
}
.pdr-complete-related-links a:hover {
  border-color: #85a996;
}
.pdr-topic-resources {
  margin: 36px 0;
  padding: clamp(20px,4vw,38px);
  background: #f7faf6;
  border: 1px solid #dbe7dd;
  border-radius: 24px;
}
.pdr-topic-resources h2 {
  font-family: Georgia,serif;
  color: #123c31;
  font-size: clamp(24px,3vw,34px);
}
.pdr-topic-resource-grid {
  display: grid;
  grid-template-columns: repeat(3,minmax(0,1fr));
  gap: 16px;
  margin-top: 22px;
}
.pdr-topic-resource-card {
  display: flex;
  flex-direction: column;
  background: white;
  border: 1px solid #dce6dd;
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  color: #123c31;
}
.pdr-topic-resource-card:hover {
  border-color: #85a996;
}
.pdr-topic-resource-visual {
  height: 154px;
  background: #e9f0e9;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.pdr-topic-resource-visual img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
.pdr-topic-resource-file {
  font: 700 21px Manrope,Arial,sans-serif;
  color: #376a4c;
}
.pdr-topic-resource-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 10px;
  padding: 17px;
}
.pdr-topic-resource-body small {
  color: #64816e;
}
.pdr-topic-resource-body strong {
  font-weight: 700;
  line-height: 1.5;
}
.pdr-topic-resource-action {
  margin-top: auto;
  color: #176347;
  font-weight: 700;
}
@media(max-width:850px) {
  .pdr-topic-resource-grid {
    grid-template-columns: repeat(2,minmax(0,1fr));
  }
}
@media(max-width:560px) {
  .pdr-topic-resource-grid {
    grid-template-columns: 1fr;
  }
}
</style>
"""

BY_ID = {row["id"]: row for row in PLAN}
changed = []
total_cards = 0
total_previews = 0

for code, ids in SELECTED.items():
    row = BY_ID[code]
    page = ROOT / "konu" / row["slug"] / "index.html"

    if not page.is_file():
        raise SystemExit(f"Eksik yayın sayfası: {code}")

    source = page.read_text(encoding="utf-8")

    if START in source:
        print(f"↪ {code}: Zaten tamamlanmış.")
        continue

    if source.count("</main>") != 1:
        raise SystemExit(f"HTML yapısı beklenenden farklı: {code}")

    cards = []
    image_count = 0

    for rid in ids:
        result = resource_card(rid)

        if not result:
            print(f"⚠️ {code}: Detay sayfası bulunamadı: {rid}")
            continue

        card, has_image = result
        cards.append(card)
        image_count += int(has_image)

    if not cards:
        raise SystemExit(f"{code}: Geçerli kaynak bulunamadı.")

    other_links = [
        (
            f'/konu/{other["slug"]}/',
            other["baslik"]
        )
        for other_code, other in BY_ID.items()
        if other_code in SELECTED and other_code != code
        and (
            ROOT / "konu" / other["slug"] / "index.html"
        ).is_file()
    ]

    other_links = other_links[:5]

    related = [
        ("/konu/akran-zorbaligi/", "Akran Zorbalığı Ana Rehberi"),
        ("/konu/akran-catismasi/", "Akran Çatışması"),
    ] + other_links

    related_html = "".join(
        f'<a href="{esc(url)}">{esc(title)}</a>'
        for url, title in related
    )

    block = (
        START + "\n" + CSS +
        '<nav class="pdr-complete-related" '
        'aria-label="İlgili konu rehberleri">'
        '<h2>İlgili konu rehberleri</h2>'
        '<div class="pdr-complete-related-links">'
        + related_html +
        '</div></nav>'
        '<section class="pdr-topic-resources" '
        'aria-label="İlgili kaynaklar">'
        '<h2>Bu konuda kullanabileceğiniz materyaller</h2>'
        '<p>Kaynakları kendi detay sayfalarında '
        'önizleyebilir ve inceleyebilirsiniz.</p>'
        '<div class="pdr-topic-resource-grid">'
        + "\n".join(cards) +
        '</div></section>\n' + END + "\n"
    )

    updated = source.replace("</main>", block + "</main>", 1)

    page.write_text(updated, encoding="utf-8")

    changed.append(code)
    total_cards += len(cards)
    total_previews += image_count

    print(
        f"✅ {code}: {len(cards)} kaynak kartı, "
        f"{image_count} görsel önizleme"
    )

print("\n=== İLK 9 REHBER TAMAMLAMA ===")
print("Güncellenen sayfa:", len(changed))
print("Eklenen kaynak kartı:", total_cards)
print("Gerçek görsel önizlemesi:", total_previews)
print("Mevcut makaleler: KORUNDU")
print("Yeni sitemap URL'si: EKLENMEDİ")
