#!/usr/bin/env python3
"""Audit local bulk topic drafts before any publish step.

Fails if generic four-section template survives, resource placeholders dominate,
or drafts contain invalid basic SEO. Never changes any files.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERIC = (
    "önce öğrencinin ihtiyacını ve çalışmanın hedefini",
    "ilgili öğrenci ve okul koşullarını değerlendirin",
    "çalışmaya amaç ve sınırları açıklayarak başlayın",
    "çalışmanın ardından hangi adımların işe yaradığını",
)

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.headings = []
        self.links = []
        self.title = ""
        self._in_title = False
        self.canonical = []
        self.robots = []
        self.images = 0
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in_title = True
        if tag == "link" and d.get("rel") == "canonical":
            self.canonical.append(d.get("href", ""))
        if tag == "meta" and d.get("name") == "robots":
            self.robots.append(d.get("content", ""))
        if tag == "a":
            self.links.append(d.get("href", ""))
        if tag == "img":
            self.images += 1
    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
    def handle_data(self, data):
        if self._in_title:
            self.title += data

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--folder", default="drafts/pdr-konular")
    p.add_argument("--report", default="/tmp/pdr-draft-quality.json")
    args = p.parse_args()
    folder = (ROOT / args.folder).resolve()
    if not folder.is_dir() or not (folder == ROOT or ROOT in folder.parents):
        p.error("Draft folder must exist inside checkout")
    rows = []
    fingerprints = collections.defaultdict(list)
    for path in sorted(folder.glob("*.draft")):
        raw = path.read_text(encoding="utf-8")
        parser = Inspect()
        parser.feed(raw)
        problems = []
        if parser.h1 != 1: problems.append("h1_count")
        if len(parser.canonical) != 1: problems.append("canonical_count")
        if not parser.title.strip(): problems.append("missing_title")
        if not any("noindex" in value for value in parser.robots): problems.append("draft_not_noindex")
        if "<main" not in raw or "</main>" not in raw: problems.append("missing_main")
        normalized = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw)).casefold()
        shared = sum(text in normalized for text in GENERIC)
        if shared >= 3: problems.append("repeated_generic_guide")
        if "pdr-topic-resource-file\">KAYNAK" in raw: problems.append("placeholder_resource_card")
        if not parser.links: problems.append("no_links")
        if "İlgili kaynak adayları" in raw: problems.append("unverified_source_gallery")
        # Detect exact duplicates of main article text, ignoring shared header/footer.
        body = raw.split('<article class="topic-article">', 1)
        if len(body) == 2:
            content = body[1].split("</article>", 1)[0]
            clean = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", content)).strip()
            fingerprints[hashlib.sha256(clean.encode()).hexdigest()].append(path.name)
        rows.append({"file": path.name, "problems": problems, "images": parser.images})
    duplicates = [group for group in fingerprints.values() if len(group) > 1]
    report = Path(args.report).expanduser().resolve()
    if report == ROOT or ROOT in report.parents:
        p.error("Report must be outside checkout")
    report.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "drafts": len(rows),
        "flagged": sum(bool(x["problems"]) for x in rows),
        "exact_article_duplicate_groups": duplicates,
        "issues": dict(collections.Counter(y for x in rows for y in x["problems"])),
        "pages": rows,
    }
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k,v in result.items() if k != "pages"}, ensure_ascii=False, indent=2))
    print("Report:", report)
    if result["flagged"] or duplicates:
        raise SystemExit("QUALITY GATE FAILED: do not publish these drafts.")

if __name__ == "__main__":
    main()
