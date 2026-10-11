#!/usr/bin/env python3
"""Match all planned PDR topics to existing local catalogue pages, without publishing."""
import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from topic_source_aliases import TOPIC_ALIASES

ROOT = Path(__file__).resolve().parents[1]
STOP = {"rehberlik","ogrenci","okul","icin","formu","form","sunumu","sunum","etkinligi","etkinlik","nasil","nedir","ile","ve","bir","ornegi","hazirlama","calismalari","gorusme","dosyasi","pdf","word","meb"}

def normalize(value):
    s = str(value or "").translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"))
    return unicodedata.normalize("NFKD", s).casefold()

def tokens(value):
    return set(re.findall(r"[a-z0-9]{3,}", normalize(value))) - STOP

def read(name):
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected list: {name}")
    return data

def local_page(url):
    if not isinstance(url, str) or not url.startswith("/") or url.startswith("//"):
        return False
    if "?" in url or "#" in url or ".." in Path(url).parts:
        return False
    path = (ROOT / url.lstrip("/")).resolve()
    if ROOT.resolve() not in path.parents:
        return False
    if path.is_dir() or url.endswith("/"):
        path = path / "index.html"
    return path.is_file()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--min-score", type=float, default=0.72)
    p.add_argument("--limit-per-topic", type=int, default=8)
    p.add_argument("--output", default="seo/icerik-plani/500-konu-kaynak-eslesmeleri.json")
    args = p.parse_args()
    if not 0.5 <= args.min_score <= 1 or not 1 <= args.limit_per_topic <= 20:
        p.error("Invalid matching thresholds")
    plan = read("seo/icerik-plani/500-konu-listesi.json")
    rows = []
    seen_ids = set()
    for filename in ("data/library.json", "data/collected-resources.json",
                     "data/new-resources-batch.json", "data/library-reviewed-batch-20261010.json"):
        for row in read(filename):
            rid = str(row.get("id", ""))
            if not rid or rid in seen_ids:
                continue
            seen_ids.add(rid)
            rows.append(row)
    links_txt = (ROOT / "src/resource-page-links.js").read_text(encoding="utf-8")
    links = dict(re.findall(r'"([^"]+)"\s*:\s*"(/[^"]+)"', links_txt))
    output = (ROOT / args.output).resolve()
    if ROOT.resolve() not in output.parents or output.suffix != ".json":
        p.error("Output must be a JSON file inside checkout")
    results = []
    stats = Counter()
    distinct_selected = set()
    stats["catalogue_unique_ids"] = len(rows)
    stats["catalogue_with_pagePath"] = sum(bool(row.get("pagePath")) for row in rows)
    stats["catalogue_with_file"] = sum(bool(row.get("file")) for row in rows)
    stats["catalogue_with_topic"] = sum(bool(row.get("topic")) for row in rows)
    stats["topics_with_curated_aliases"] = 0
    stats["matched_subject_before_link_check"] = 0
    stats["matched_subject_distinct_topics"] = 0
    for item in plan:
        label = str(item.get("baslik", ""))
        slug = str(item.get("slug", ""))
        # Use the canonical root concept, when present, rather than the whole long-tail title.
        parent = str(item.get("ana_konu", "")).strip()
        generic_parent = parent in ("/konular.html", "/konular.html/", "/", "")
        main_words = tokens(parent.strip("/").split("/")[-1].replace("-", " ")) if parent.startswith("/") else tokens(parent)
        title_words = tokens(label)
        if generic_parent:
            main_words = title_words
        if not main_words:
            main_words = title_words
        concept = normalize(parent.strip('/').split('/')[-1].replace('-', ' ')) if not generic_parent else ""
        alias_phrases = TOPIC_ALIASES.get(concept, [])
        alias_words = [tokens(phrase) for phrase in alias_phrases if tokens(phrase)]
        if alias_words:
            stats["topics_with_curated_aliases"] += 1
        if generic_parent:
            stats["topics_with_generic_parent"] += 1
        candidates = []
        used = set()
        subject_matches = 0
        for row in rows:
            rid = str(row.get("id", ""))
            title = str(row.get("title", ""))
            tagged = tokens(row.get("topic", ""))
            headline = tokens(title)
            if not main_words:
                continue
            subject_match = main_words <= tagged or main_words <= headline
            if generic_parent:
                # Require two meaningful title terms to avoid matching broad single words.
                subject_match = len(main_words) >= 2 and len(main_words & (tagged | headline)) >= 2 and len(main_words & (tagged | headline)) / len(main_words) >= 0.55
            if not subject_match:
                subject_match = any(alias <= tagged or alias <= headline for alias in alias_words)
            if not subject_match and len(main_words) >= 2:
                subject_match = len(main_words & (tagged | headline)) / len(main_words) >= 0.75
            if not subject_match:
                continue
            detail_score = len(title_words & (headline | tagged)) / max(1, len(title_words))
            score = 0.8 + 0.2 * detail_score
            if score < args.min_score:
                continue
            subject_matches += 1
            url = row.get("pagePath") or links.get(rid, "")
            if not local_page(url):
                stats["matched_but_no_local_page"] += 1
                continue
            if url in used:
                continue
            used.add(url)
            candidates.append((score, {"baslik": title, "tur": row.get("type", "Materyal"), "sayfa": url, "eslesme_puani": round(score, 3), "belge_icerigi_dogrulandi": False}))
        stats["matched_subject_before_link_check"] += subject_matches
        if subject_matches:
            stats["matched_subject_distinct_topics"] += 1
        candidates.sort(key=lambda x: (-x[0], x[1]["baslik"]))
        chosen = [x[1] for x in candidates[:args.limit_per_topic]]
        if chosen: stats["topics_with_candidates"] += 1
        else: stats["topics_without_candidates"] += 1
        stats["candidate_links"] += len(chosen)
        distinct_selected.update(x["sayfa"] for x in chosen)
        results.append({"id": item["id"], "slug": slug, "kaynak_adaylari": chosen})
    stats["unique_selected_resource_pages"] = len(distinct_selected)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"topics": len(plan), **dict(stats), "report": str(output), "published": 0}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
