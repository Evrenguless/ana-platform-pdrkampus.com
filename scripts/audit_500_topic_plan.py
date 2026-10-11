#!/usr/bin/env python3
"""Non-destructive 500-topic plan audit. Never overwrites the original plan."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "seo/icerik-plani/500-konu-listesi.json"
OUT = ROOT / "seo/icerik-plani/500-konu-plan-denetimi.json"
CATEGORIES = {
    "Okul PDR uygulamaları": "okul-pdr",
    "PDR ÖABT alan konuları": "pdr-oabt",
    "AGS hazırlık konuları": "ags",
    "Sınav stratejileri ve analiz": "sinav-stratejileri",
    "Atama, Akademi ve norm": "atama-norm",
}
TOPIC_RULES = [
    ("akran-zorbaligi", ("zorbal", "akran çatış")),
    ("ozel-egitim", ("özel eğitim", "bep", "kaynaştır", "ram ", "öğrenme güçlüğ")),
    ("veli-gorusmesi", ("veli", "ebeveyn", "aile")),
    ("devamsizlik", ("devamsız", "okul redd", "okul terk")),
    ("kriz-mudahale", ("kriz", "intihar", "istismar", "yas ", "travma")),
    ("kariyer", ("kariyer", "meslek", "tercih", "yöneltme")),
    ("sinav-kaygisi", ("sınav kayg", "sınav stres")),
    ("dijital-denge", ("dijital", "teknoloji", "siber", "ekran süres")),
    ("rehberlik-planlama", ("yıllık plan", "çerçeve plan", "rehberlik plan")),
    ("ogrenci-gorusmeleri", ("öğrenci görüş", "bireysel görüş")),
]
def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    proposed = []
    groups = Counter()
    weak = []
    for item in plan:
        category = str(item.get("kategori", ""))
        title = str(item.get("baslik", "")).casefold()
        original = str(item.get("ana_konu", ""))
        if original.startswith("/konu/"):
            subject = original.strip("/").split("/")[-1]
            origin = "existing_parent"
        else:
            matched = [key for key, terms in TOPIC_RULES if any(term in title for term in terms)]
            subject = matched[0] if len(matched) == 1 else CATEGORIES.get(category, "inceleme-gerekli")
            origin = "title_rule" if len(matched) == 1 else "category_fallback"
            if len(matched) > 1 or subject == "inceleme-gerekli":
                weak.append(item.get("id"))
        groups[subject] += 1
        proposed.append({
            "id": item.get("id"), "slug": item.get("slug"), "baslik": item.get("baslik"),
            "kategori": category, "ana_konu_eski": original, "konu_kumesi_onerisi": subject,
            "siniflandirma_yontemi": origin, "editor_onayi": False,
        })
    duplicates = {key: count for key, count in Counter(x.get("slug") for x in plan).items() if count > 1}
    output = {
        "total": len(plan), "generic_parents": sum(x.get("ana_konu")=="/konular.html" for x in plan),
        "proposed_groups": dict(groups), "ambiguous_ids": weak,
        "duplicate_slugs": duplicates, "entries": proposed,
        "notice": "Heuristic grouping only. This does not rewrite the approved 500-topic plan."
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="entries"},ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
