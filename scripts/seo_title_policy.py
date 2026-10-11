# -*- coding: utf-8 -*-
"""PDR Kampüs: onaylanmış SEO başlıklarını koruma politikası."""

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "seo" / "approved-page-titles.json"

@lru_cache(maxsize=1)
def approved_titles():
    if not MANIFEST.exists():
        return {}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data.get("titles", {})

def approved_title(route, proposed_title):
    """
    Daha önce gözden geçirilmiş bir başlık varsa onu koru.

    Yeni bir URL için üreticinin özgün başlığını kullan.
    Ayırt edici bilgileri otomatik olarak silme.
    """
    if not route:
        return proposed_title

    route = "/" + str(route).strip("/") + "/"
    return approved_titles().get(route, proposed_title)
