#!/usr/bin/env python3
"""Read-only editorial quality audit for 500 PDR guide manuscripts.

Only writes a JSON report in seo/icerik-plani/. Never edits drafts or live pages.
Run after scripts/prepare_first_50.py when checking rendered previews too.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "seo/icerik-plani/500-rehber-derin-icerik-denetimi.json"
DRAFTS = ROOT / "drafts/pdr-ilk-paket"
WORD_RE = re.compile(r"\b[\wçğıöşüÇĞİÖŞÜ]+\b", re.UNICODE)
HIGH_RISK = ("kriz-", "intihar", "istismar", "ihmal", "kendine-zarar", "siddet", "zarar-verme", "risk-bildirimi")
def count(s):
    return len(WORD_RE.findall(s))
def norm(s):
    return re.sub(r"\s+", " ", s.casefold()).strip()
def group_range(n):
    return "<75" if n < 75 else "75-124" if n < 125 else "125-199" if n < 200 else "200-299" if n < 300 else "300+"
def main():
    rows = []
    files = []
    for n in range(2, 23):
        path = ROOT / f"data/pdr-editorial-batch-{n:02d}.json"
        if not path.is_file():
            raise SystemExit(f"Missing source data: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        files.append({"batch": n, "count": len(data)})
        for r in data:
            rows.append((n, r))
    by_slug = defaultdict(list)
    by_title = defaultdict(list)
    by_faq = defaultdict(list)
    by_heading_set = defaultdict(list)
    by_paragraph = defaultdict(list)
    per_page = []
    bins = Counter()
    for batch, r in rows:
        slug = r["slug"]
        sections = r.get("sections", [])
        text = " ".join(x[1] for x in sections)
        core_words = count(text)
        total_words = core_words + count(r.get("summary", "")) + count(r.get("example", ""))
        total_words += sum(count(s) for s in r.get("check", []))
        total_words += sum(count(q) + count(a) for q, a in r.get("faq", []))
        bins[group_range(core_words)] += 1
        issues = []
        if core_words < 125:
            issues.append("short_main_text_under_125_words")
        if core_words < 75:
            issues.append("very_short_main_text_under_75_words")
        if len(sections) < 5:
            issues.append("fewer_than_5_sections")
        if any(count(t) < 15 for _, t in sections):
            issues.append("section_under_15_words")
        if count(r.get("example", "")) < 20:
            issues.append("example_under_20_words")
        if len(r.get("faq", [])) < 2:
            issues.append("fewer_than_2_faq")
        if len(r.get("check", [])) < 3:
            issues.append("fewer_than_3_checklist")
        preview_path = DRAFTS / (slug + ".html")
        if not preview_path.is_file():
            issues.append("missing_local_preview_or_not_built")
        else:
            raw = preview_path.read_text(encoding="utf-8")
            if 'name="robots" content="noindex' not in raw:
                issues.append("preview_not_noindex")
        if any(k in slug for k in HIGH_RISK):
            issues.append("mandatory_specialist_review")
        by_slug[slug].append(slug)
        by_title[norm(r["title"])].append(slug)
        by_heading_set["|".join(norm(h) for h, _ in sections)].append(slug)
        for question, answer in r.get("faq", []):
            by_faq[norm(answer)].append(slug)
        for heading, paragraph in sections:
            if count(paragraph) >= 12:
                by_paragraph[norm(paragraph)].append(slug)
        per_page.append({"slug": slug, "batch": batch, "title": r["title"],
                         "main_section_words": core_words, "editorial_total_words": total_words,
                         "section_lengths": [count(t) for _, t in sections],
                         "issues": issues})
    def repeated(index):
        return [{"count": len(slugs), "slugs": slugs[:35], "sample": term[:180]}
                for term, slugs in index.items() if len(set(slugs)) > 1]
    repeated_faq = sorted(repeated(by_faq), key=lambda x: -x["count"])
    repeated_heads = sorted(repeated(by_heading_set), key=lambda x: -x["count"])
    repeated_paragraphs = sorted(repeated(by_paragraph), key=lambda x: -x["count"])
    duplicates = [{"key": key, "slugs": v} for key, v in by_title.items() if len(v) > 1]
    issues_by_kind = Counter(issue for page in per_page for issue in page["issues"])
    result = {
        "audit": "Source manuscript, structural heuristics; not a professional content approval",
        "expected_total": 500, "json_manuscripts_checked": len(rows),
        "initial_hardcoded_guides_not_in_json": 5,
        "draft_html_count": len(list(DRAFTS.glob("*.html"))) - (DRAFTS / "index.html").is_file() if DRAFTS.exists() else 0,
        "batch_counts": files,
        "core_word_buckets": dict(sorted(bins.items())),
        "core_word_avg": round(sum(x["main_section_words"] for x in per_page) / len(per_page), 1),
        "under_125_main_words": sum(x["main_section_words"] < 125 for x in per_page),
        "under_75_main_words": sum(x["main_section_words"] < 75 for x in per_page),
        "duplicate_seo_titles": duplicates,
        "reused_faq_answers": repeated_faq[:50],
        "reused_heading_patterns": repeated_heads[:50],
        "reused_full_section_paragraphs": repeated_paragraphs[:50],
        "issues_by_kind": dict(issues_by_kind),
        "publication_approved": False,
        "limitations": [
            "Initial five hardcoded guides require separate review in builder source and rendered HTML.",
            "Counts are based on JSON author text; rendered shared page templates are excluded.",
            "No external resource URLs or source relevance were verified.",
            "No clinical, legal, or professional accuracy approval has been performed.",
            "Mobile layout requires real browser/device inspection.",
            "Topic-intent overlap and semantic similarity need human editorial review."
        ],
        "pages": per_page
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("pages", "reused_faq_answers", "reused_heading_patterns", "reused_full_section_paragraphs",
                                   "batch_counts", "duplicate_seo_titles")}, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
