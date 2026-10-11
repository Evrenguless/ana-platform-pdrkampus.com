#!/usr/bin/env python3
"""Non-destructive consolidation proposal for repetitive SEO pages.

Keeps the original 500-topic plan untouched. Does not publish content.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"seo/icerik-plani/500-konu-listesi.json"
TARGET=ROOT/"seo/icerik-plani/500-konu-birlestirme-onerisi.json"
PATTERNS={
 "ags": re.compile(r": (Temel Kavramlar|Konu Anlatımı|Örnek Soru Çözüm Yaklaşımları|Sık Karıştırılan Kavramlar|Çalışma ve Tekrar Rehberi)$",re.I),
 "oabt": re.compile(r": (Temel Kavramlar|Kuram ve Yaklaşımlar|Konu Anlatımı|Kavram Karşılaştırmaları|Soru Çözüm Stratejileri)$",re.I),
 "norm": re.compile(r": (Temel Bilgiler|Hesaplama ve Değerlendirme|Sık Sorulan Sorular)$",re.I),
}
GROUP_CATEGORIES={
 "AGS hazırlık konuları":"ags",
 "PDR ÖABT alan konuları":"oabt",
 "Atama, Akademi ve norm":"norm",
}
def main():
    plan=json.loads(SOURCE.read_text(encoding="utf-8"))
    groups=defaultdict(list)
    untouched=[]
    for row in plan:
        title=str(row.get("baslik","")).strip()
        category=str(row.get("kategori",""))
        kind=GROUP_CATEGORIES.get(category)
        match=PATTERNS[kind].search(title) if kind else None
        if match:
            base=title[:match.start()].strip()
            groups[(category,base)].append(row)
        else:
            untouched.append(row)
    proposals=[]
    for (category,base),items in sorted(groups.items()):
        if len(items)<2:
            untouched.extend(items)
            continue
        proposals.append({
            "category":category,"proposed_canonical_title":base,
            "source_ids":[x.get("id") for x in items],
            "existing_slugs":[x.get("slug") for x in items],
            "sections":[PATTERNS[GROUP_CATEGORIES[category]].search(x["baslik"]).group(1) for x in items],
            "editor_review_required":True,
            "action":"merge_proposal_only",
        })
    output={
        "original_count":len(plan),
        "merge_groups":len(proposals),
        "potentially_redundant_pages":sum(len(p["source_ids"])-1 for p in proposals),
        "unmodified_standalone_topics":len(untouched),
        "proposals":proposals,
        "untouched_ids":[x.get("id") for x in untouched],
        "warning":"No URLs were changed. Do not redirect or delete before checking distinct search intent and existing indexing."
    }
    TARGET.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k not in ("proposals","untouched_ids")},ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
