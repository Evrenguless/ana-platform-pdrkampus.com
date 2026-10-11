#!/usr/bin/env python3
"""Publication gate for fifty HTML previews. Does not publish or alter HTML."""
import json, re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
DRAFTS=ROOT/"drafts/pdr-ilk-paket"
REPORT=ROOT/"seo/icerik-plani/ilk-50-yayin-kapisi.json"

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=""; self.description=[]; self.robots=[]; self.canonical=[]
        self.h1=[]; self.links=[]; self.images=[]; self.ids=[]
        self._title=False; self._h1=False; self._h1text=""
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="title":self._title=True
        if tag=="h1":self._h1=True;self._h1text=""
        if tag=="meta" and a.get("name","").lower()=="description":self.description.append(a.get("content",""))
        if tag=="meta" and a.get("name","").lower()=="robots":self.robots.append(a.get("content",""))
        if tag=="link" and a.get("rel")=="canonical":self.canonical.append(a.get("href",""))
        if tag=="a":self.links.append(a.get("href",""))
        if tag=="img":self.images.append(a.get("src",""))
        if a.get("id"):self.ids.append(a["id"])
    def handle_data(self,data):
        if self._title:self.title+=data
        if self._h1:self._h1text+=data
    def handle_endtag(self,tag):
        if tag=="title":self._title=False
        if tag=="h1":self._h1=False;self.h1.append(self._h1text.strip())

def main():
    files=sorted(p for p in DRAFTS.glob("*.html") if p.name != "index.html")
    all_titles=defaultdict(list);all_descriptions=defaultdict(list)
    per_page=[];totals=Counter();external=Counter()
    for path in files:
        raw=path.read_text(encoding="utf-8")
        page=Page();page.feed(raw)
        problems=[]
        if not page.title.strip():problems.append("missing_title")
        if len(page.h1)!=1:problems.append("h1_count_invalid")
        if len(page.description)!=1 or not page.description[0].strip():problems.append("meta_description_missing_or_duplicate")
        if len(page.canonical)!=1:problems.append("canonical_missing_or_duplicate")
        elif page.canonical[0]!="https://pdrkampus.com/konu/"+path.stem+"/":problems.append("canonical_mismatch")
        if not any("noindex" in x.casefold() for x in page.robots):problems.append("preview_indexing_risk")
        duplicate_ids=[k for k,v in Counter(page.ids).items() if v>1]
        if duplicate_ids:problems.append("duplicate_html_ids")
        for url in page.links:
            parsed=urlsplit(url)
            if parsed.scheme in ("http","https"):
                external[parsed.netloc.lower()]+=1
            elif parsed.scheme and parsed.scheme not in ("mailto","tel"):problems.append("unusual_link_scheme")
        if "Katalog başlık ve etiketlerinden seçilen aday kaynaklardır" in raw:problems.append("document_relevance_not_verified")
        # A card is not proof that its remote PDF exists or matches the article.
        if 'class="guide2-card"' not in raw:problems.append("no_resource_cards")
        all_titles[page.title.strip().casefold()].append(path.stem)
        if page.description:all_descriptions[page.description[0].strip().casefold()].append(path.stem)
        problems=list(dict.fromkeys(problems))
        totals.update(problems)
        per_page.append({"slug":path.stem,"title":page.title,"h1":page.h1,"description_length":len(page.description[0]) if page.description else 0,"source_cards":raw.count('class="guide2-card"'),"issues":problems})
    for bucket,label in ((all_titles,"duplicate_seo_title"),(all_descriptions,"duplicate_meta_description")):
        for slugs in bucket.values():
            if len(slugs)>1:
                totals[label]+=len(slugs)
                for page in per_page:
                    if page["slug"] in slugs:page["issues"].append(label)
    report={"pages_checked":len(files),"issues_by_kind":dict(totals),
            "external_domains_with_link_counts":dict(external.most_common(30)),
            "limitations":["Remote destinations were not requested or verified.",
                           "Document contents and professional accuracy require editorial review.",
                           "Mobile layout needs browser/device inspection."],
            "publish_approved":False,"pages":per_page}
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="pages"},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
