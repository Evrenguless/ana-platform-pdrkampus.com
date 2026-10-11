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

SCHOOL_RULES = [
    ("bireyi-tanima", ("sosyometri", "gözlem", "bireyi tanı", "anket", "envanter")),
    ("sosyal-duygusal-gelisim", ("öz güven", "özgüven", "öz saygı", "duygu", "empati", "öz düzenleme", "arkadaşlık", "iletişim beceri", "problem çözme", "öfke")),
    ("sinif-rehberligi", ("sınıf rehber", "sınıf etkinlik", "sınıf yönet", "grup rehber")),
    ("okula-uyum", ("okula uyum", "okul aidiyet", "uyum haftası", "okula başlama")),
    ("rehberlik-planlama", ("rehberlik plan", "yıllık plan", "çerçeve plan", "rehberlik program", "eylem plan")),
    ("sinav-ve-calisma", ("ders çalışma", "akademik motivasyon", "öğrenme stratej", "sınav kayg", "zaman yönet", "çalışma beceri")),
    ("koruyucu-onleyici", ("şiddet", "risk", "güvenli okul", "önleyici", "ihmal", "istismar", "bağımlılık")),
]
OABT_RULES = [
    ("oabt-gelisim-psikolojisi", ("gelişim psikoloj", "gelişim dönem", "piaget", "erikson", "kohlberg", "bağlanma", "ahlak geliş", "ergenlik")),
    ("oabt-ogrenme-psikolojisi", ("öğrenme psikoloj", "koşullanma", "pekiştirme", "davranışçı", "bandura", "bilişsel öğrenme")),
    ("oabt-danisma-kuramlari", ("danışma kuram", "psikanaliz", "bilişsel davranışçı", "gestalt", "roger", "adler", "varoluşçu", "gerçeklik terap")),
    ("oabt-olcme-degerlendirme", ("ölçme", "değerlendirme", "geçerlik", "güvenirlik", "test geliştirme", "madde analizi")),
    ("oabt-mesleki-rehberlik", ("mesleki rehber", "kariyer", "holland", "super", "meslek seç")),
    ("oabt-psikolojik-danisma", ("psikolojik danışma", "danışma beceri", "görüşme teknik", "grupla danışma")),
    ("oabt-rehberlik-ve-etik", ("etik", "rehberlik hizmet", "meslek eti", "gizlilik", "konsültasyon")),
]
def classify(title, category, original):
    if original.startswith("/konu/"):
        return original.strip("/").split("/")[-1], "existing_parent", []
    primary = OABT_RULES if category == "PDR ÖABT alan konuları" else SCHOOL_RULES if category == "Okul PDR uygulamaları" else []
    matches = [key for key, terms in primary if any(term in title for term in terms)]
    if not matches and not primary:
        matches = [key for key, terms in TOPIC_RULES if any(term in title for term in terms)]
    if len(matches) == 1:
        return matches[0], "specialized_rule", matches
    return CATEGORIES.get(category, "inceleme-gerekli"), "ambiguous" if len(matches) > 1 else "category_fallback", matches

def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    proposed = []
    groups = Counter()
    weak = []
    for item in plan:
        category = str(item.get("kategori", ""))
        title = str(item.get("baslik", "")).casefold()
        original = str(item.get("ana_konu", ""))
        subject, origin, matched = classify(title, category, original)
        if origin in ("ambiguous", "category_fallback") and subject in ("okul-pdr", "pdr-oabt", "inceleme-gerekli"):
            weak.append(item.get("id"))
        groups[subject] += 1
        proposed.append({
            "id": item.get("id"), "slug": item.get("slug"), "baslik": item.get("baslik"),
            "kategori": category, "ana_konu_eski": original, "konu_kumesi_onerisi": subject,
            "siniflandirma_yontemi": origin, "eslesen_kumeler": matched, "editor_onayi": False,
        })
    duplicates = {key: count for key, count in Counter(x.get("slug") for x in plan).items() if count > 1}
    output = {
        "total": len(plan), "generic_parents": sum(x.get("ana_konu")=="/konular.html" for x in plan),
        "proposed_groups": dict(groups), "ambiguous_ids": weak,
        "duplicate_slugs": duplicates, "review_required_count": len(weak), "entries": proposed,
        "notice": "Heuristic grouping only. This does not rewrite the approved 500-topic plan."
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="entries"},ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
