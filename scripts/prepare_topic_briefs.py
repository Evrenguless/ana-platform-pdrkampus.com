#!/usr/bin/env python3
"""Prepare source-backed editorial briefs for the 500-topic plan.

Read only: plan and candidate matches. Writes briefs outside tracked published
content. Does not manufacture article text or assert that linked sources are verified.
"""
import argparse
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "seo/icerik-plani/500-konu-listesi.json"
MATCHES = ROOT / "seo/icerik-plani/500-konu-kaynak-eslesmeleri.json"
DEFAULT_OUT = ROOT / "drafts/topic-briefs"

def read(path):
    if not path.is_file():
        raise SystemExit(f"Missing input: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"Expected JSON list: {path}")
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--refresh-sources", action="store_true")
    args = parser.parse_args()
    if not (1 <= args.limit <= 500 and args.start >= 0):
        parser.error("Invalid range")
    plan = read(PLAN)
    matches = {str(x.get("id")): x for x in read(MATCHES)}
    output = Path(args.output).expanduser().resolve()
    if not (output == ROOT or ROOT in output.parents):
        parser.error("Output must be within checkout")
    if output in (ROOT, ROOT / "konu", ROOT / "seo"):
        parser.error("Unsafe output location")
    output.mkdir(parents=True, exist_ok=True)
    statuses = Counter()
    for item in plan[args.start:args.start + args.limit]:
        code = str(item.get("id", "")).strip()
        slug = str(item.get("slug", "")).strip()
        if not code or not slug or "/" in slug or ".." in slug or "/" in code or ".." in code:
            raise SystemExit(f"Unsafe plan entry: {code}, {slug}")
        path = output / f"{code}-{slug}.json"
        if path.exists() and not args.refresh_sources:
            statuses["preserved"] += 1
            continue
        candidate = matches.get(code, {}).get("kaynak_adaylari", [])
        sources = [
            {"baslik": str(x.get("baslik", "")), "sayfa": str(x.get("sayfa", "")),
             "tur": str(x.get("tur", "")), "belge_icerigi_dogrulandi": False}
            for x in candidate if isinstance(x, dict) and x.get("sayfa")
        ]
        if path.exists():
            brief = json.loads(path.read_text(encoding="utf-8"))
            if brief.get("id") != code or brief.get("slug") != slug:
                raise SystemExit(f"Brief identity mismatch: {path}")
            prior = {x.get("sayfa"): x for x in brief.get("kaynak_adaylari", []) if isinstance(x, dict)}
            for source in sources:
                if prior.get(source["sayfa"], {}).get("belge_icerigi_dogrulandi") is True:
                    source["belge_icerigi_dogrulandi"] = True
            if brief.get("kaynak_adaylari") == sources:
                statuses["unchanged"] += 1
                continue
            brief["kaynak_adaylari"] = sources
            path.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            statuses["refreshed_sources"] += 1
            continue
        existing = ROOT / "konu" / slug / "index.html"
        brief = {
            "id": code, "slug": slug, "baslik": item.get("baslik", ""),
            "kategori": item.get("kategori", ""), "ana_konu": item.get("ana_konu", ""),
            "hedef_url": f"/konu/{slug}/",
            "mevcut_sayfa": existing.is_file(),
            "kaynak_adaylari": sources,
            "arama_niyeti": "", "ozgun_aciklama": "",
            "okul_uygulama_adimlari": [], "dikkat_edilecek_noktalar": [],
            "sik_sorulan_sorular": [], "ilgili_konular": [],
            "editor_onayi": False,
            "yayina_hazir": False,
            "not": "Bu dosya editoryal çalışma fişidir; boş alanlar hazır içerik değildir."
        }
        path.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        statuses["new_brief"] += 1
        if not sources: statuses["without_source_candidates"] += 1
        if existing.is_file(): statuses["already_published_path"] += 1
    print(json.dumps({"plan_total": len(plan), "range": [args.start, args.start+args.limit],
                      "results": dict(statuses), "output": str(output),
                      "published_pages_created": 0}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
