#!/usr/bin/env python3
"""PDR Kampus: existing topic pages' resource coverage and preview builder.

No page, sitemap, source catalogue or shared stylesheet is modified by default.
Only existing topic pages are candidates. Missing/weak matches are reported.
Use --apply explicitly to insert marked resource sections into eligible pages.
"""
from __future__ import annotations
import argparse
import html
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MARK_START = "<!-- PDR-BATCH-RESOURCE-START -->"
MARK_END = "<!-- PDR-BATCH-RESOURCE-END -->"
STOP = {"okul", "icin", "ile", "ve", "bir", "form", "pdf", "ppt", "meb", "ogrenci", "rehberlik", "calisma", "etkinlik", "rehberi", "sunum", "ornek", "nasil", "yapilir"}
SPECIAL = {"akran-zorbaligi"}  # Curated reference stays untouched.


def load(relative, fallback):
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return fallback


def norm(value):
    value = str(value or "").translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"))
    return unicodedata.normalize("NFKD", value).casefold()


def words(value):
    return {w for w in re.findall(r"[a-z]{3,}", norm(value)) if w not in STOP}


def topic_terms(slug, metadata):
    names = [slug.replace("-", " ")]
    if metadata:
        names += [metadata.get("name", ""), *metadata.get("aliases", [])]
    return names


def resource_url(row, links):
    rid = str(row.get("id", ""))
    candidates = [row.get("pagePath", ""), links.get(rid, ""), "/kaynak-detay/" + rid + "/"]
    for candidate in candidates:
        if not isinstance(candidate, str) or not candidate.startswith("/"):
            continue
        path = ROOT / candidate.lstrip("/") / "index.html" if candidate.endswith("/") else ROOT / candidate.lstrip("/")
        if path.is_file() and path.suffix == ".html":
            return candidate
    return None


def preview_path(rid, previews):
    item = previews.get(rid, {})
    values = [item] if isinstance(item, str) else []
    if isinstance(item, dict):
        values += [item.get(k) for k in ("thumbnail", "cover", "image", "preview", "src")]
        for p in item.get("previews", []):
            values.append(p if isinstance(p, str) else p.get("src") if isinstance(p, dict) else "")
    for val in values:
        if not isinstance(val, str):
            continue
        clean = val.split("?")[0]
        if clean.startswith("/") and ".." not in Path(clean).parts and (ROOT / clean.lstrip("/")).is_file():
            return clean
        if clean and not urlparse(clean).scheme and ".." not in Path(clean).parts and (ROOT / clean).is_file():
            return "/" + clean
    return None


def get_matches(slug, metadata, rows, links, previews, limit):
    term_sets = [words(term) for term in topic_terms(slug, metadata)]
    term_sets = [s for s in term_sets if s]
    found = []
    used = set()
    for row in rows:
        title = str(row.get("title", ""))
        haystack = words(" ".join(str(row.get(k, "")) for k in ("title", "topic", "category", "description")))
        score = max((len(term & haystack) / len(term) for term in term_sets), default=0)
        if score < 0.75:
            continue
        href = resource_url(row, links)
        if not href or href in used:
            continue
        used.add(href)
        found.append((score, title, href, preview_path(str(row.get("id", "")), previews)))
    return sorted(found, key=lambda m: (-m[0], m[1]))[:limit]


def section(matches):
    cards = []
    for _, title, href, image in matches:
        visual = ('<img loading="lazy" src="' + html.escape(image, quote=True) + '" alt="">' if image else '<span aria-hidden="true">Kaynak</span>')
        cards.append('<a class="pdr-batch-card" href="' + html.escape(href, quote=True) + '"><span class="pdr-batch-visual">' + visual + '</span><strong>' + html.escape(title) + '</strong><span class="pdr-batch-action">Kaynağı incele</span></a>')
    return MARK_START + '''
<section class="pdr-batch-resources" aria-labelledby="pdr-batch-title">
  <h2 id="pdr-batch-title">İlgili kaynaklar ve materyaller</h2>
  <p>Kütüphanede bu konuyla eşleşen kaynakları inceleyin.</p>
  <div class="pdr-batch-grid">''' + "".join(cards) + '''</div>
</section>
<style>
.pdr-batch-resources{margin:36px 0;padding:clamp(20px,4vw,36px);background:#f7faf6;border:1px solid #dbe7dd;border-radius:24px}
.pdr-batch-resources h2{font-family:Georgia,serif;color:#123c31}
.pdr-batch-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:20px}
.pdr-batch-card{display:flex;flex-direction:column;gap:10px;padding:14px;border:1px solid #dce6dd;background:white;border-radius:16px;text-decoration:none;color:#123c31}
.pdr-batch-card strong{font:700 15px/1.5 Manrope,Arial,sans-serif}
.pdr-batch-visual{height:150px;display:grid;place-items:center;background:#e9f0e9;border-radius:9px;overflow:hidden;color:#376a4c}
.pdr-batch-visual img{width:100%;height:100%;object-fit:contain}
.pdr-batch-action{margin-top:auto;color:#176347;font:700 13px Manrope,Arial,sans-serif}
@media(max-width:800px){.pdr-batch-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:540px){.pdr-batch-grid{grid-template-columns:1fr}}
</style>
''' + MARK_END


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true", help="Update eligible existing pages only")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--min-resources", type=int, default=3)
    p.add_argument("--report", default="/tmp/pdr-topic-batch-report.json")
    args = p.parse_args()
    if not (1 <= args.limit <= 500 and 1 <= args.min_resources <= 12):
        p.error("Invalid limit or min-resources")
    topic_data = load("data/topics.json", {})
    metadata = {x["slug"]: x for x in topic_data.get("topics", []) if x.get("slug")}
    rows = load("data/library.json", []) + load("data/collected-resources.json", [])
    if not isinstance(rows, list):
        raise SystemExit("Resource catalogue is not a list")
    previews = load("data/resource-previews.json", {})
    if not isinstance(previews, dict):
        previews = {}
    source = (ROOT / "src/resource-page-links.js").read_text(encoding="utf-8")
    links = dict(re.findall(r'"([^"]+)"\s*:\s*"(/[^"]+)"', source))
    report = []
    changed = 0
    for page in sorted((ROOT / "konu").glob("*/index.html")):
        if len(report) >= args.limit:
            break
        slug = page.parent.name
        if slug in SPECIAL:
            continue
        original = page.read_text(encoding="utf-8")
        if '<link rel="canonical"' not in original or "PDR-KONU-REHBERI-2-START" in original or "TOPIC-RESOURCE-CARDS-START" in original:
            continue
        matches = get_matches(slug, metadata.get(slug), rows, links, previews, 9)
        state = "insufficient_sources" if len(matches) < args.min_resources else "ready"
        if MARK_START in original and MARK_END in original:
            state = "already_generated"
        if args.apply and state == "ready":
            insertion = section(matches)
            if "</main>" not in original:
                state = "missing_main"
            else:
                updated = original.replace("</main>", insertion + "</main>", 1)
                page.write_text(updated, encoding="utf-8")
                changed += 1
                state = "updated"
        report.append({"slug": slug, "state": state, "matched": len(matches), "resources": [m[2] for m in matches]})
    target = Path(args.report).expanduser().resolve()
    if target == ROOT or ROOT in target.parents:
        raise SystemExit("Report must be outside repository")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"applied": args.apply, "changed": changed, "scanned": len(report), "pages": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from collections import Counter
    print(json.dumps({"scanned": len(report), "changed": changed, "states": dict(Counter(x["state"] for x in report)), "report": str(target)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
