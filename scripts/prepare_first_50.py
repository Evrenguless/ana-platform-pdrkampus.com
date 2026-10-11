#!/usr/bin/env python3
"""One-command build of the complete 50-guide editorial review package.

Writes ONLY under drafts/pdr-ilk-paket and seo/icerik-plani.
Never changes /konu, main, sitemap, robots, or existing live pages.
"""
import contextlib
import html
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DRAFTS=ROOT/"drafts/pdr-ilk-paket"
REPORT=ROOT/"seo/icerik-plani"
EXPECTED=50

def run(script, *args):
    command=[sys.executable,str(ROOT/"scripts"/script),*args]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    if result.returncode:
        print(result.stdout)
        print(result.stderr,file=sys.stderr)
        raise SystemExit(f"Failed: {script}")
    try:return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"Unexpected JSON output from {script}")

def main():
    generated=run("build_first_editorial_batch.py")
    if generated.get("batch_size")!=EXPECTED:
        raise SystemExit(f"Expected {EXPECTED} guides, got {generated.get('batch_size')}")
    results=generated.get("results",[])
    slugs=[r["slug"] for r in results]
    if len(slugs)!=len(set(slugs)):raise SystemExit("Duplicate slugs")
    for slug in slugs:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",slug):
            raise SystemExit("Unsafe slug: "+slug)
        path=DRAFTS/(slug+".html")
        if not path.is_file():raise SystemExit("Missing generated HTML: "+slug)
        if 'name="robots" content="noindex' not in path.read_text(encoding="utf-8"):
            raise SystemExit("Draft lacks noindex: "+slug)
    quality=run("audit_first_50_guides.py")
    seo=run("audit_first_50_publication.py")
    if quality.get("files_checked")!=EXPECTED or seo.get("pages_checked")!=EXPECTED:
        raise SystemExit("Audit did not cover all 50 guides")
    serious={"broken_anchor","missing_local_link","missing_local_image",
             "missing_preview_noindex","limited_content_sections","limited_faq",
             "formulaic_example","h1_count_invalid","canonical_mismatch",
             "duplicate_seo_title","duplicate_meta_description","preview_indexing_risk"}
    issues=set(quality.get("issues_by_kind",{}))|set(seo.get("issues_by_kind",{}))
    if issues & serious:raise SystemExit("Structural gate failed: "+", ".join(sorted(issues & serious)))
    # Not an approval to publish: PDFs, source relevance and mobile UI still need review.
    detailed_seo=json.loads((REPORT/"ilk-50-yayin-kapisi.json").read_text(encoding="utf-8"))
    cards={p["slug"]:p["source_cards"] for p in detailed_seo["pages"]}
    items=[]
    for index,slug in enumerate(slugs,1):
        page=DRAFTS/(slug+".html")
        text=page.read_text(encoding="utf-8")
        match=re.search(r"<h1[^>]*>(.*?)</h1>",text,re.S)
        heading=re.sub(r"<[^>]+>","",match.group(1)) if match else slug
        title=html.escape(html.unescape(heading))
        count=cards.get(slug,0)
        label=f"{count} kaynak adayı" if count else "Kütüphane araması"
        items.append(f'<li><a href="./{slug}.html">{title}</a><small>{label}</small></li>')
    page='''<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>50 PDR Rehberi · Editoryal Önizleme</title>
<style>body{font-family:system-ui,sans-serif;background:#f6f8f4;color:#183c30;margin:0}
main{max-width:1020px;margin:44px auto;padding:0 20px}h1{font-family:Georgia,serif;font-size:clamp(30px,5vw,48px)}
p{line-height:1.65}ul{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(285px,1fr));gap:13px}
li{background:white;border:1px solid #dde7dd;padding:18px;border-radius:15px;display:grid;gap:12px}
a{color:#174e3c;font-weight:700;text-decoration:none}a:hover{text-decoration:underline}
small{color:#557263}aside{background:white;border-left:3px solid #527d65;padding:15px;margin:24px 0}</style></head>
<body><main><p>PDR KAMPÜS · EDİTORYAL ÖNİZLEME</p><h1>İlk 50 uygulama rehberi</h1>
<p>Bu bağlantılar yalnızca inceleme taslaklarını açar. Canlı sitede yayınlanmamıştır.</p>
<aside>Kaynak kartları katalog eşleşmesidir; belge içeriği, erişilebilirlik ve profesyonel uygunluk ayrıca incelenmelidir.</aside>
<ul>'''+''.join(items)+'''</ul></main></body></html>'''
    (DRAFTS/"index.html").write_text(page,encoding="utf-8")
    manifest={"pages":EXPECTED,"preview_index":str((DRAFTS/"index.html").relative_to(ROOT)),
              "source_cards":sum(cards.values()),
              "without_source_cards":[k for k,v in cards.items() if not v],
              "structural_gate":"passed",
              "publication_approved":False,
              "remaining_reviews":["Document relevance","Remote access","Mobile visual inspection"]}
    (REPORT/"ilk-50-toplu-durum.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
