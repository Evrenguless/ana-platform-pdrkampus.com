#!/usr/bin/env python3
"""Review-only source shortlist for five gaps; no output is published."""
import json
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
TOPICS={
 "aile-okul-iletisimi-zor-gorusmeler":["Aile iletişimi","Veli rehberliği","Veli görüşmeleri"],
 "cocuklarda-dijital-mahremiyet":["Dijital güvenlik","Dijital yaşam","Teknoloji bağımlılığı"],
 "ogrenci-izleme-formu-hazirlama":["Rehberlik planlaması","Bireyi tanıma","Rehberlik materyali"],
 "okulda-ihmal-istismar-bildirimi":["Kriz müdahalesi","Çocuk koruma","İhmal ve istismar"],
 "rehberlik-servisi-evrak-duzeni":["Rehberlik planlaması","Rehberlik materyali","Rehberlik evrakları"],
}
def main():
    rows={}
    for name in ("library.json","collected-resources.json","new-resources-batch.json","library-reviewed-batch-20261010.json"):
        path=ROOT/"data"/name
        if not path.exists():continue
        for row in json.loads(path.read_text(encoding="utf-8")):
            if row.get("id"):rows.setdefault(str(row["id"]),row)
    results={}
    for slug,categories in TOPICS.items():
        pool=[r for r in rows.values() if str(r.get("topic","")).casefold() in [x.casefold() for x in categories]]
        results[slug]=[{"id":r.get("id"),"title":r.get("title"),"topic":r.get("topic"),"source":r.get("source"),"pagePath":r.get("pagePath"),"file":r.get("file"),"preview":r.get("previewImage") or r.get("preview"),"reviewed":False} for r in pool]]
    report=ROOT/"seo/icerik-plani/ilk-50-eksik-kaynak-adaylari.json"
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"catalogue_records":len(rows),"candidate_counts":{slug:len(group) for slug,group in results.items()},"report":str(report),"published":0},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
