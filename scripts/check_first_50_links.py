#!/usr/bin/env python3
"""Parallel verification of the first three document links on every draft page.

Network requests are made to remote sites. Nothing is published or modified
except the JSON report under seo/icerik-plani/.
"""
import concurrent.futures
import json
import re
import time
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
DRAFTS=ROOT/"drafts/pdr-ilk-paket"
REPORT=ROOT/"seo/icerik-plani/ilk-50-baglanti-denetimi.json"

class Cards(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards=[]
    def handle_starttag(self,tag,attrs):
        if tag!="a":return
        a=dict(attrs)
        if "guide2-card" in a.get("class","").split():
            self.cards.append(a.get("href",""))

def check(url):
    if url.startswith("/"):
        path=(ROOT/url.lstrip("/")).resolve()
        if ROOT not in path.parents:return {"status":"unsafe_local"}
        if path.is_dir():path=path/"index.html"
        return {"status":"local_ok" if path.is_file() else "local_missing"}
    parsed=urlparse(url)
    if parsed.scheme not in ("http","https") or not parsed.netloc:
        return {"status":"invalid_url"}
    for method in ("HEAD","GET"):
        try:
            headers={"User-Agent":"Mozilla/5.0 (compatible; PDRKampusContentQA/1.0)","Accept":"*/*"}
            if method=="GET":headers["Range"]="bytes=0-0"
            with urlopen(Request(url,headers=headers,method=method),timeout=9) as response:
                code=response.status
                return {"status":"http_ok" if 200<=code<400 else "http_error","code":code,
                        "final_url":response.geturl(),"method":method}
        except HTTPError as exc:
            if method=="HEAD" and exc.code in (403,405,429,501):continue
            return {"status":"http_restricted" if exc.code in (401,403,429) else "http_error","code":exc.code,"method":method}
        except (URLError,TimeoutError,OSError) as exc:
            if method=="HEAD":continue
            return {"status":"network_error","error":str(exc)[:180]}
    return {"status":"network_error"}

def main():
    targets=[]
    for path in sorted(DRAFTS.glob("*.html")):
        parser=Cards();parser.feed(path.read_text(encoding="utf-8"))
        for i,url in enumerate(parser.cards[:3],1):
            targets.append({"slug":path.stem,"position":i,"url":url})
    unique=sorted(set(t["url"] for t in targets))
    print(f"Checking {len(unique)} unique links used in {len(targets)} cards across 50 guides...",flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results=dict(zip(unique,pool.map(check,unique)))
    rows=[dict(t,**results[t["url"]]) for t in targets]
    summary=dict(Counter(x["status"] for x in rows))
    blocked=[x for x in rows if x["status"] not in ("http_ok","local_ok")]
    output={"guides":len({x["slug"] for x in rows}),"cards_checked":len(rows),
            "unique_urls_checked":len(unique),"status_counts":summary,"needs_review":blocked,
            "limitations":["HTTP 403 and 429 may be access restrictions rather than broken links.",
                           "HTTP success does not establish document relevance, PDF quality, or content accuracy.",
                           "Mobile rendering still requires a browser check."],"approved_for_publication":False}
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in output.items() if k not in ("needs_review","limitations")},ensure_ascii=False,indent=2))
    print("Report:",REPORT)
if __name__=="__main__":main()
