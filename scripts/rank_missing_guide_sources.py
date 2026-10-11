#!/usr/bin/env python3
"""Rank candidate documents for the five gaps; no publication or automatic approval."""
import json,re,unicodedata
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"seo/icerik-plani/ilk-50-eksik-kaynak-adaylari.json"
OUTPUT=ROOT/"seo/icerik-plani/ilk-50-kaynak-oncelik-raporu.json"
KEYWORDS={
"aile-okul-iletisimi-zor-gorusmeler":["veli görüş","aile iletişim","zor veli","ebeveyn iletişim"],
"cocuklarda-dijital-mahremiyet":["dijital mahremiyet","kişisel veri","güvenli internet","dijital güvenlik","siber güvenlik"],
"ogrenci-izleme-formu-hazirlama":["öğrenci izleme","izleme form","takip form","görüşme takip","öğrenci takip"],
"okulda-ihmal-istismar-bildirimi":["ihmal","istismar","çocuk koruma","bildirim","çocuk güvenliği"],
"rehberlik-servisi-evrak-duzeni":["rehberlik evrak","belge düzen","dosyalama","rehberlik form","rehberlik plan"],
}
def norm(s):
    s=str(s or "").casefold().replace("ı","i")
    s=unicodedata.normalize("NFKD",s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))
def safe_url(u):
    if not isinstance(u,str):return False
    p=urlparse(u)
    return p.scheme=="https" and bool(p.netloc) or u.startswith("/") and not u.startswith("//") and ".." not in u.split("/")
def local_preview(p):
    return isinstance(p,str) and p.startswith("/") and not p.startswith("//") and (ROOT/p.lstrip("/")).is_file()
def main():
    raw=json.loads(SOURCE.read_text(encoding="utf-8"))
    result={}
    for slug,rows in raw.items():
        ranked=[]
        for row in rows:
            title=norm(row.get("title"))
            terms=[norm(x) for x in KEYWORDS.get(slug,[])]
            hit=[t for t in terms if t in title]
            direct=len(hit)>0
            page=row.get("pagePath")
            file=row.get("file")
            preview=row.get("preview")
            # The HTML builder can discover previews by resource ID even if
            # the catalogue has no previewImage field.
            if not local_preview(preview):
                rid=str(row.get("id") or "")
                if rid and re.fullmatch(r"[a-zA-Z0-9_-]+",rid):
                    folder=ROOT/"assets/resource-previews"
                    matches=sorted(folder.glob(rid+"-*.jpg"))+sorted(folder.glob(rid+"*.png"))
                    if matches:preview="/"+str(matches[0].relative_to(ROOT))
            ranked.append({
                "id":row.get("id"),"title":row.get("title"),"topic":row.get("topic"),
                "direct_title_match":direct,"matching_phrases":hit,
                "file_link_present":safe_url(file),
                "local_page_present":bool(page and isinstance(page,str) and page.startswith("/") and (ROOT/page.lstrip("/")).is_file()),
                "local_preview_present":local_preview(preview),
                "source":row.get("source"),"file":file,"pagePath":page,"preview":preview,
                "editor_approval_required":True,
            })
        ranked.sort(key=lambda r:(not r["direct_title_match"],not r["local_preview_present"],not r["local_page_present"],str(r["title"])))
        result[slug]={"total_candidates":len(ranked),"direct_title_matches":sum(x["direct_title_match"] for x in ranked),"candidates":ranked}
    OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"per_topic":{k:{"candidates":v["total_candidates"],"direct_title_matches":v["direct_title_matches"],"with_local_previews":sum(x["local_preview_present"] for x in v["candidates"])} for k,v in result.items()},"report":str(OUTPUT),"published":0},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
