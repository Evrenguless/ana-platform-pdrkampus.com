#!/usr/bin/env python3
"""Publication-readiness evidence for the complete 500-guide DRAFT preview.

No production changes. Standard library only. Regenerate previews first.
This is editorial triage, not specialist/legal review or approval to publish.
"""
import collections
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "drafts/pdr-ilk-paket"
OUT = ROOT / "seo/icerik-plani/500-rehber-yayin-oncesi-denetim.json"
WORD = re.compile(r"[\wçğıöşüÇĞİÖŞÜ]+", re.UNICODE)
RISK = ("kriz-", "intihar", "istismar", "ihmal", "siddet", "zarar-verme",
        "kendine-zarar", "risk-bildirim", "istenmeyen-temas")
class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = collections.Counter()
        self.title, self.h1, self.desc, self.robots, self.canonical = "", [], [], [], []
        self.meta, self.links = {}, []
        self.text = []
        self.section_depth = 0
        self.section_text = []
        self.sections = []
        self.example = ""
        self.in_title = self.in_h1 = False
        self.h1_buffer = ""
        self.in_main = False
        self.in_example = False
        self.in_materials = False
        self.in_faq = False
        self.materials_cards = 0
        self.library_material_cards = 0
        self.faq_count = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] += 1
        if tag == "title": self.in_title = True
        if tag == "h1": self.in_h1 = True; self.h1_buffer = ""
        if tag == "main": self.in_main = True
        if tag == "section" and "topic-section" in a.get("class", "").split():
            self.section_depth += 1
            self.section_text.append([])
            if a.get("id") == "ornek": self.in_example = True
        if tag == "section" and a.get("id") == "materyaller": self.in_materials = True
        if tag == "details": self.faq_count += 1; self.in_faq = True
        if tag == "a":
            self.links.append(a.get("href", ""))
            if "guide2-card" in a.get("class", "").split():
                self.materials_cards += 1
                if a.get("href", "").startswith(("/kutuphane/", "/kaynak/")):
                    self.library_material_cards += 1
        if tag == "link" and "canonical" in a.get("rel", "").split(): self.canonical.append(a.get("href", ""))
        if tag == "meta":
            name = a.get("name", "").lower()
            if name == "description": self.desc.append(a.get("content", ""))
            if name == "robots": self.robots.append(a.get("content", ""))
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_h1: self.h1_buffer += data
        if self.section_depth and self.section_text: self.section_text[-1].append(data)
        if self.in_example: self.example += data
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "h1": self.in_h1 = False; self.h1.append(self.h1_buffer.strip())
        if tag == "section" and self.section_depth:
            self.sections.append(" ".join(self.section_text.pop()))
            self.section_depth -= 1
            if self.in_example: self.in_example = False
        if tag == "details": self.in_faq = False

def words(s): return WORD.findall(s.casefold())
def normalized(s): return " ".join(words(html.unescape(s)))
def shingles(text, k=8):
    w = words(text)
    return set(tuple(w[i:i+k]) for i in range(len(w)-k+1))

def main():
    pages = sorted(p for p in DRAFT.glob("*.html") if p.name != "index.html")
    if len(pages) != 500:
        raise SystemExit(f"Expected 500 draft HTML pages, got {len(pages)}; run prepare_first_50.py")
    records = []
    content_shingles = {}
    titles = collections.defaultdict(list)
    descriptions = collections.defaultdict(list)
    repeated_texts = collections.defaultdict(list)
    for path in pages:
        src = path.read_text(encoding="utf-8")
        r = Reader()
        r.feed(src)
        slug = path.stem
        issues = []
        if len(r.h1) != 1 or not r.h1[0].strip(): issues.append("invalid_h1_count")
        if not r.title.strip(): issues.append("missing_seo_title")
        if len(r.desc) != 1 or not r.desc[0].strip(): issues.append("invalid_description_count")
        if len(r.canonical) != 1 or r.canonical[0] != f"https://pdrkampus.com/konu/{slug}/":
            issues.append("canonical_missing_or_mismatch")
        if not any("noindex" in value.lower() for value in r.robots):
            issues.append("preview_indexing_risk")
        if r.faq_count < 2: issues.append("short_faq")
        if r.materials_cards == 0: issues.append("no_direct_source_cards")
        if r.library_material_cards == 0: issues.append("no_library_material_cards")
        if "Katalog başlık ve etiketlerinden seçilen aday kaynaklardır" in src:
            issues.append("candidate_sources_not_editorially_verified")
        # The page contains many non-manuscript sections (checklist, FAQ, footnote).
        # The original guide chapters are before the example id. Extract the exact
        # authored chapter text from section id=adim-N, excluding page furniture.
        chapters = re.findall(
            r'<section class="topic-section" id="adim-\d+">\s*<h2>.*?</h2>\s*<p>(.*?)</p>',
            src, flags=re.S
        )
        chapters = [html.unescape(re.sub(r"<[^>]*>", " ", c)) for c in chapters]
        chapter_words = sum(len(words(c)) for c in chapters)
        if not chapters: issues.append("missing_chapter_markup")
        if chapter_words < 125: issues.append("main_text_under_125")
        if chapter_words < 250: issues.append("main_text_under_250")
        if len(chapters) < 5: issues.append("fewer_than_five_manuscript_chapters")
        for i, text in enumerate(chapters):
            if len(words(text)) < 15: issues.append("chapter_under_15_words")
            if len(words(text)) >= 15: repeated_texts[normalized(text)].append(slug)
        if len(words(r.example)) < 20: issues.append("short_example_or_example_missing")
        if any(x in slug for x in RISK): issues.append("specialist_review_required")
        main_text = " ".join(chapters)
        content_shingles[slug] = shingles(main_text)
        titles[normalized(r.title)].append(slug)
        if r.desc: descriptions[normalized(r.desc[0])].append(slug)
        records.append({"slug":slug,"title":r.title,"chapter_count":len(chapters),
                        "main_text_words":chapter_words,"example_words":len(words(r.example)),
                        "resource_cards":r.materials_cards,
                        "library_material_cards":r.library_material_cards,
                        "issues":sorted(set(issues))})
    by_slug = {r["slug"]:r for r in records}
    for key,bucket in (("duplicate_title",titles),("duplicate_description",descriptions)):
        for slugs in bucket.values():
            if len(slugs) > 1:
                for slug in slugs: by_slug[slug]["issues"].append(key)
    duplicated = [{"slugs":sorted(set(slugs)),"sample":text[:180]}
                  for text,slugs in repeated_texts.items() if len(set(slugs)) > 1]
    duplicated.sort(key=lambda x:-len(x["slugs"]))
    # Approximate paragraph-content similarity only: 8-token shingles; small
    # documents may share template wording and should be reviewed, not auto-deleted.
    candidates = []
    slugs = sorted(content_shingles)
    for i, a in enumerate(slugs):
        sa = content_shingles[a]
        if not sa: continue
        for b in slugs[i+1:]:
            sb = content_shingles[b]
            if not sb: continue
            intersect = len(sa & sb)
            if intersect < 12: continue
            overlap = intersect / min(len(sa),len(sb))
            if overlap >= 0.45:
                candidates.append({"a":a,"b":b,"shared_eight_word_phrases":intersect,
                                   "smaller_text_overlap":round(overlap,3)})
    candidates.sort(key=lambda p:-p["smaller_text_overlap"])
    kinds = collections.Counter(issue for r in records for issue in set(r["issues"]))
    summary = {
        "pages_checked":len(records),"draft_only":True,"publication_approved":False,
        "main_text_avg_words":round(sum(r["main_text_words"] for r in records)/len(records),1),
        "main_text_min_words":min(r["main_text_words"] for r in records),
        "under_125":sum(r["main_text_words"]<125 for r in records),
        "under_250":sum(r["main_text_words"]<250 for r in records),
        "pages_without_source_cards":sum(r["resource_cards"]==0 for r in records),
        "pages_without_library_material_cards":sum(r["library_material_cards"]==0 for r in records),
        "library_material_cards_total":sum(r["library_material_cards"] for r in records),
        "candidate_duplicate_pairs":len(candidates),
        "identical_chapter_groups":len(duplicated),
        "issues_by_kind":dict(kinds)
    }
    report = {"summary":summary,"duplicate_candidates":candidates[:500],
              "reused_complete_chapters":duplicated[:200],
              "limitations":[
                  "8-token phrase similarity is a triage heuristic, not semantic originality proof.",
                  "No web request or remote PDF/content relevance verification was performed.",
                  "No clinical, child-protection or legal specialist validation was performed.",
                  "No mobile/visual device testing was performed.",
                  "Source-card counts are not proof of document appropriateness or availability."
              ],"pages":records}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == "__main__":main()
