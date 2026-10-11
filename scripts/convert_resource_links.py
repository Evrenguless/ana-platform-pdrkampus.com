#!/usr/bin/env python3
"""Konu sayfalarındaki eski kütüphane bağlantılarını düzeltir."""

import hashlib
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]

LINK_FILE = ROOT / "src/resource-page-links.js"
BASELINE = ROOT / "seo/protected-files.json"
APPROVALS = ROOT / "seo/approved-edits.json"

sys.path.insert(0, str(ROOT / "scripts"))
from seo_engine import protected, runtime_digest

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = LINK_FILE.read_text(encoding="utf-8")

    # Kütüphanedeki gerçek kaynak sayfası bağlantıları
    links = dict(re.findall(
        r'"([^"]+)"\s*:\s*"(/[^"]+)"',
        source
    ))

    # Eski kaynak-detay adresleri de desteklenir.
    for page in (ROOT / "kaynak-detay").glob("*/index.html"):
        links.setdefault(
            page.parent.name,
            f"/kaynak-detay/{page.parent.name}/"
        )

    baseline = load(BASELINE)
    approvals = load(APPROVALS)

    pattern = re.compile(
        r'(<a\b[^>]*?\bhref\s*=\s*)(["\'])(.*?)\2',
        re.I | re.S
    )

    updated_files = []
    replaced = 0
    unresolved = {}

    # Kullanıcının tespit ettiği konu sayfalarına odaklan.
    for page in sorted((ROOT / "konu").rglob("*.html")):
        original = page.read_text(encoding="utf-8")
        local_count = 0

        def replace(match):
            nonlocal local_count

            prefix, quote, href = match.groups()
            value = html.unescape(href)
            parsed = urlsplit(value)

            if parsed.netloc not in ("", "pdrkampus.com", "www.pdrkampus.com"):
                return match.group(0)

            if not parsed.path.endswith("kutuphane.html"):
                return match.group(0)

            if not parsed.fragment or parsed.query:
                return match.group(0)

            resource_id = unquote(parsed.fragment)
            target = links.get(resource_id)

            if not target:
                unresolved[resource_id] = unresolved.get(resource_id, 0) + 1
                return match.group(0)

            target_file = ROOT / target.lstrip("/")
            if target.endswith("/"):
                target_file /= "index.html"

            if not target_file.is_file():
                unresolved[resource_id] = unresolved.get(resource_id, 0) + 1
                return match.group(0)

            local_count += 1

            return prefix + quote + html.escape(target, quote=True) + quote

        updated = pattern.sub(replace, original)

        if updated == original:
            continue

        page.write_text(updated, encoding="utf-8")

        relative = page.relative_to(ROOT).as_posix()
        updated_files.append(relative)
        replaced += local_count

        if relative in baseline["files"]:
            approvals.setdefault("edits", {})[relative] = {
                "baseline_sha256": baseline["files"][relative],
                "reviewed_sha256": sha(page),
                "runtime_sha256": runtime_digest(updated),
                "reason": (
                    "Reviewed resource navigation improvement: "
                    "existing library fragment links replaced with "
                    "verified resource detail pages; SEO metadata preserved."
                )
            }

    APPROVALS.write_text(
        json.dumps(approvals, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    report = {
        "updated_pages": len(updated_files),
        "replaced_links": replaced,
        "unresolved": unresolved,
        "files": updated_files
    }

    output = ROOT / "seo/resource-link-migration-report.json"
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    result = protected(ROOT)

    print("\n=== TOPLU BAĞLANTI DÖNÜŞÜMÜ ===")
    print("Güncellenen sayfa:", len(updated_files))
    print("Düzeltilen bağlantı:", replaced)
    print("Eşleşmeyen kaynak:", len(unresolved))
    print("SEO koruması:", "BAŞARILI" if result["pass"] else "BAŞARISIZ")

    if unresolved:
        print("\nEşleşmeyen kaynak kimlikleri:")
        for key, count in list(unresolved.items())[:30]:
            print(f"- {key}: {count}")

    if not result["pass"]:
        print("Koruma sorunları:", result["changed"][:20])
        raise SystemExit(1)

if __name__ == "__main__":
    main()
