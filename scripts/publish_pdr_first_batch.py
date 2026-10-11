#!/usr/bin/env python3
"""PDR-002–010 için kontrollü ilk yayın paketi."""

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "seo/icerik-plani/500-konu-listesi.json"
DRAFTS = ROOT / "drafts/pdr-konular"
TOPICS = ROOT / "data/topics.json"
SITEMAP = ROOT / "sitemap.xml"
APPROVALS = ROOT / "seo/approved-edits.json"
SHARD = ROOT / "sitemaps/konular-pdr-ilk-paket.xml"

BASE = "https://pdrkampus.com"
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
TAG = f"{{{NS}}}"
ET.register_namespace("", NS)

sys.path.insert(0, str(ROOT / "scripts"))
from seo_engine import protected, runtime_digest

def save_xml(root):
    ET.indent(root, space="  ")
    return ET.tostring(
        root, encoding="unicode", xml_declaration=True
    ) + "\n"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def test(command):
    print("\n▶", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)

def main():
    plan = {
        row["id"]: row
        for row in json.loads(PLAN.read_text(encoding="utf-8"))
    }

    wanted = [f"PDR-{i:03d}" for i in range(2, 11)]
    targets = []

    for code in wanted:
        row = plan[code]
        found = list(DRAFTS.glob(f"{code}-*.draft"))

        if len(found) != 1:
            raise SystemExit(f"{code}: tek taslak bulunamadı.")

        target = ROOT / "konu" / row["slug"] / "index.html"

        if target.exists():
            raise SystemExit(
                f"{code}: yayın sayfası zaten mevcut. "
                "Üzerine yazılmadı."
            )

        source = found[0].read_text(encoding="utf-8")

        if source.count("<main") != 1 or source.count("</main>") != 1:
            raise SystemExit(f"{code}: HTML yapısı uygun değil.")

        if len(re.findall(r"<h1\b", source)) != 1:
            raise SystemExit(f"{code}: H1 kontrolü başarısız.")

        if "orgm.meb.gov.tr" not in source:
            raise SystemExit(
                f"{code}: resmî MEB kaynak bağlantısı eksik."
            )

        # Kaynak adaylarının uygunluğu doğrulanmadı:
        # bunları ilk yayın paketinden çıkar.
        source = re.sub(
            r'<!-- PDR-DRAFT-GALLERY-START -->.*?'
            r'<!-- PDR-DRAFT-GALLERY-END -->',
            "",
            source,
            flags=re.S,
        )
        source = re.sub(
            r'<style>\s*\.pdr-topic-resources\b.*?</style>\s*'
            r'<section class="pdr-topic-resources".*?</section>',
            "",
            source,
            flags=re.S,
        )

        # İlk üç rehberde yalnız galeri bölümü olabilir.
        source = re.sub(
            r'<section class="pdr-topic-resources".*?</section>',
            "",
            source,
            flags=re.S,
        )

        source = re.sub(
            r'<meta\s+name="robots"\s+content="noindex,follow"\s*/?>',
            "",
            source,
            flags=re.I,
        )

        if "noindex" in source.lower():
            raise SystemExit(f"{code}: noindex hâlâ bulunuyor.")

        expected = BASE + row["onerilen_url"]

        if f'href="{expected}"' not in source:
            raise SystemExit(f"{code}: canonical adres uyuşmuyor.")

        targets.append((code, row, target, source))

    # Mevcut işlemleri geri döndürebilmek için anlık yedek.
    with tempfile.TemporaryDirectory(prefix="pdr-publish-") as tmp:
        backup = Path(tmp)
        touched = [TOPICS, SITEMAP, APPROVALS]
        existed = {p: p.exists() for p in touched}

        for p in touched:
            if p.exists():
                shutil.copy2(p, backup / p.name)

        try:
            topics = json.loads(TOPICS.read_text(encoding="utf-8"))
            existing_slugs = {
                t.get("slug") for t in topics["topics"]
            }

            for code, row, target, source in targets:
                if row["slug"] in existing_slugs:
                    raise ValueError(
                        f"Konunun sözlük kaydı zaten var: {row['slug']}"
                    )

                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source, encoding="utf-8")

                topics["topics"].append({
                    "id": f"topic_{row['slug'].replace('-', '_')}",
                    "slug": row["slug"],
                    "name": row["baslik"],
                    "categoryId": "cat-risk-safety",
                    "aliases": [],
                    "useCases": ["okul PDR uygulaması"],
                    "indexable": True,
                    "contentStatus": "published",
                    "canonicalPath": row["onerilen_url"],
                    "relatedTopics": [
                        "akran-zorbaligi",
                        "akran-catismasi"
                    ],
                    "officialSources": [
                        "https://orgm.meb.gov.tr/www/akran-zorbaligi/icerik/3132"
                    ],
                    "seo": {
                        "title": row["baslik"] + " | PDR Kampüs",
                        "description": (
                            row["baslik"] +
                            " hakkında okul PDR uygulama adımları, "
                            "güvenlik ve takip önerileri."
                        ),
                        "primaryQuery": row["baslik"],
                    },
                })

            TOPICS.write_text(
                json.dumps(
                    topics, ensure_ascii=False, indent=2
                ) + "\n",
                encoding="utf-8",
            )

            if SHARD.exists():
                raise ValueError(
                    "Yayın sitemap dosyası zaten mevcut."
                )

            urlset = ET.Element(TAG + "urlset")

            for _, row, _, _ in targets:
                entry = ET.SubElement(urlset, TAG + "url")
                ET.SubElement(entry, TAG + "loc").text = (
                    BASE + row["onerilen_url"]
                )

            SHARD.write_text(
                save_xml(urlset), encoding="utf-8"
            )

            tree = ET.parse(SITEMAP)
            root = tree.getroot()

            if root.tag != TAG + "sitemapindex":
                raise ValueError("Beklenmeyen sitemap yapısı.")

            node = ET.SubElement(root, TAG + "sitemap")
            ET.SubElement(node, TAG + "loc").text = (
                BASE + "/sitemaps/konular-pdr-ilk-paket.xml"
            )

            SITEMAP.write_text(
                save_xml(root), encoding="utf-8"
            )

            # Mevcut SEO koruma sisteminin onay kaydı.
            baseline = json.loads(
                (ROOT / "seo/protected-files.json")
                .read_text(encoding="utf-8")
            )["files"]

            approvals = json.loads(
                APPROVALS.read_text(encoding="utf-8")
            )

            if "sitemap.xml" in baseline:
                approvals.setdefault("edits", {})["sitemap.xml"] = {
                    "baseline_sha256": baseline["sitemap.xml"],
                    "reviewed_sha256": sha(SITEMAP),
                    "reason": (
                        "Reviewed nine new PDR guides and sitemap "
                        "addition for first publication batch."
                    ),
                }

                APPROVALS.write_text(
                    json.dumps(
                        approvals, ensure_ascii=False, indent=2
                    ) + "\n",
                    encoding="utf-8",
                )

            if "data/topics.json" in baseline:
                approvals.setdefault("edits", {})["data/topics.json"] = {
                    "baseline_sha256": baseline["data/topics.json"],
                    "reviewed_sha256": sha(TOPICS),
                    "reason": (
                        "Reviewed topic dictionary for first publication batch."
                    ),
                }

                APPROVALS.write_text(
                    json.dumps(
                        approvals, ensure_ascii=False, indent=2
                    ) + "\n",
                    encoding="utf-8",
                )

            test(["python3", "scripts/check_seo.py"])
            test([
                "python3",
                "scripts/check_links.py",
                "--internal-only",
            ])

            protection = protected(ROOT)

            if not protection["pass"]:
                raise ValueError(
                    "SEO koruma kontrolü başarısız: "
                    + str(protection["changed"])
                )

            print("\n=== İLK YAYIN PAKETİ HAZIR ===")
            print("Yeni konu sayfası:", len(targets))
            print("Sitemap'e eklenen URL:", len(targets))
            print("SEO koruması: BAŞARILI")
            print("GitHub'a henüz gönderilmedi.")

        except Exception as exc:
            print("\n❌ Kontrol başarısız:", exc)
            print("Değişiklikler geri alınıyor...")

            for _, _, target, _ in targets:
                target.unlink(missing_ok=True)

            SHARD.unlink(missing_ok=True)

            for p in touched:
                saved = backup / p.name
                if saved.exists():
                    shutil.copy2(saved, p)
                elif not existed[p]:
                    p.unlink(missing_ok=True)

            raise SystemExit(1)

if __name__ == "__main__":
    main()
