#!/usr/bin/env python3
"""Read-only audit for 50 preview HTML guides. No publishing or mutation."""
import json, re, html
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/"drafts/pdr-ilk-paket"
OUTPUT=ROOT/"seo/icerik-plani/ilk-50-kalite-raporu.json"

class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.images=[]; self.ids=set(); self.headings=[]; self.meta={}; self.title=""; self._title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="a":self.links.append(a.get("href",""))
        if tag=="img":self.images.append(a.get("src",""))
        if a.get("id"):self.ids.add(a["id"])
        if tag=="meta" and a.get("name"):self.meta[a["name"]]=a.get("content","")
        if tag=="title":self._title=True
    def handle_data(self,data):
        if self._title:self.title+=data
    def handle_endtag(self,tag):
        if tag=="title":self._title=False

def local_exists(url):
    p=urlsplit(url)
    if p.scheme or p.netloc or not p.path:return True
    path=unquote(p.path)
    if path.startswith("//"):return False
    dest=(ROOT/path.lstrip("/")).resolve() if path.startswith("/") else None
    if dest is None:return None
    if not (dest==ROOT or ROOT in dest.parents):return False
    if path.endswith("/"):dest=dest/"index.html"
    return dest.is_file()

def main():
    files=sorted(FOLDER.glob("*.html"))
    findings=[]; overview=Counter()
    for p in files:
        src=p.read_text(encoding="utf-8")
        reader=Reader();reader.feed(src)
        problems=[]
        for link in reader.links:
            if link.startswith("#") and link[1:] not in reader.ids:problems.append("broken_anchor:"+link)
            elif link.startswith("/") and local_exists(link) is False:problems.append("missing_local_link:"+link)
        for image in reader.images:
            if image.startswith("/") and local_exists(image) is False:problems.append("missing_local_image:"+image)
        if not reader.meta.get("robots","").startswith("noindex"):problems.append("missing_preview_noindex")
        if src.count('class="guide2-card"')==0:problems.append("no_resource_cards")
        if "belge önizlemesi" not in src:problems.append("no_preview_images")
        if src.count('class="topic-section"')<7:problems.append("limited_content_sections")
        if len(re.findall(r'<details',src))<2:problems.append("limited_faq")
        if "Katalog başlık ve etiketlerinden seçilen aday kaynaklardır" in src:problems.append("source_relevance_unverified")
        if "Örnek uygulama: Okul ekibi bu konuda bir ihtiyaç belirlediğinde" in src:problems.append("formulaic_example")
        if len(set(problems))!=len(problems):problems=list(dict.fromkeys(problems))
        overview.update(x.split(":",1)[0] for x in problems)
        findings.append({"file":str(p.relative_to(ROOT)),"title":html.unescape(reader.title),"issues":problems,"resource_cards":src.count('class="guide2-card"'),"preview_images":src.count("belge önizlemesi")})
    needs_attention=[{"file":x["file"],"issues":[issue for issue in x["issues"] if issue in ("no_resource_cards","no_preview_images")]} for x in findings if any(issue in ("no_resource_cards","no_preview_images") for issue in x["issues"])]
    output={"files_checked":len(files),"issues_by_kind":dict(overview),"source_gaps":needs_attention,"publish_ready_claimed":0,
        "note":"External URLs and PDF content were not checked; source relevancy remains editorial review.",
        "pages":findings}
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k!="pages"},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
