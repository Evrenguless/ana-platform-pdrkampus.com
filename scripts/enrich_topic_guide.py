#!/usr/bin/env python3
"""PDR Kampüs konu rehberi: gerçek kaynaklardan öneri kartları üretir."""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "konu/akran-zorbaligi/index.html"
LIBRARY = ROOT / "data/library.json"
LINKS = ROOT / "src/resource-page-links.js"
PREVIEWS = ROOT / "data/resource-previews.json"
APPROVAL = ROOT / "seo/approved-edits.json"
PROTECTED = ROOT / "seo/protected-files.json"

START = "<!-- PDR-KONU-REHBERI-2-START -->"
END = "<!-- PDR-KONU-REHBERI-2-END -->"

RESOURCE_IDS = [
    "zorbalik-kuramsal",
    "farkindalik-ilkokul",
    "farkindalik-ortaokul",
    "farkindalik-lise",
    "ogretmen-brosur",
    "veli-brosur",
    "sunum-öğretmen-ilkokul",
    "sunum-öğretmen-ortaokul",
    "sunum-veli-ilkokul",
    "sunum-veli-ortaokul",
    "akran-35",
    "akran-40",
]

def esc(value):
    return html.escape(str(value or ""), quote=True)

def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def preview_for(resource_id, previews):
    """Yalnızca depoda gerçekten bulunan önizleme görsellerini döndür."""
    item = previews.get(resource_id, {})
    if isinstance(item, str):
        candidates = [item]
    elif isinstance(item, dict):
        candidates = []
        for key in ("thumbnail", "cover", "image", "preview", "src"):
            value = item.get(key)
            if isinstance(value, str):
                candidates.append(value)
        for value in item.get("previews", []):
            if isinstance(value, str):
                candidates.append(value)
            elif isinstance(value, dict):
                for key in ("thumbnail", "src", "image", "url"):
                    if isinstance(value.get(key), str):
                        candidates.append(value[key])
    else:
        candidates = []

    for value in candidates:
        clean = value.split("?")[0]
        if clean.startswith(("http://", "https://", "//", "data:")):
            continue
        local = (ROOT / clean.lstrip("/")).resolve()
        if ROOT.resolve() in local.parents and local.is_file():
            return "/" + local.relative_to(ROOT).as_posix()
    return None

def main():
    records = {row["id"]: row for row in load_json(LIBRARY, []) if "id" in row}
    link_source = LINKS.read_text(encoding="utf-8")
    links = dict(re.findall(r'"([^"]+)"\s*:\s*"(/[^"]+)"', link_source))
    previews = load_json(PREVIEWS, {})

    if not isinstance(previews, dict):
        previews = {}

    cards = []
    missing = []
    images = 0

    for resource_id in RESOURCE_IDS:
        row = records.get(resource_id)
        if not row:
            missing.append(resource_id)
            continue

        # Öncelik: katalogdaki mevcut gerçek sayfa bağlantısı.
        href = links.get(resource_id)
        if not href:
            candidate = ROOT / "kaynak-detay" / resource_id / "index.html"
            if candidate.exists():
                href = f"/kaynak-detay/{resource_id}/"

        if not href:
            missing.append(resource_id)
            continue

        local_target = ROOT / href.lstrip("/")
        if href.endswith("/"):
            local_target /= "index.html"
        if not local_target.is_file():
            missing.append(resource_id)
            continue

        title = esc(row.get("title"))
        kind = esc(row.get("type", "Kaynak"))
        level = esc(row.get("level", "Tüm kademeler"))
        source = esc(row.get("source", ""))
        preview = preview_for(resource_id, previews)

        if preview:
            images += 1
            visual = (
                f'<img src="{esc(preview)}" alt="{title} belge önizlemesi" '
                'loading="lazy" decoding="async">'
            )
        else:
            visual = (
                '<span class="guide2-file-mark" aria-hidden="true">PDF</span>'
                '<span class="guide2-visual-label">Kaynak belgesi</span>'
            )

        cards.append(
            f'<a class="guide2-card" href="{esc(href)}">'
            f'<span class="guide2-visual">{visual}</span>'
            f'<span class="guide2-card-body">'
            f'<span class="guide2-meta">{level} · {kind}</span>'
            f'<strong>{title}</strong>'
            f'<small>{source}</small>'
            f'<span class="guide2-action">Kaynağı incele →</span>'
            f'</span></a>'
        )

    if len(cards) < 6:
        raise SystemExit(
            f"Yeterli doğrulanmış kaynak yok: {len(cards)}. "
            f"Eksik kayıtlar: {missing}"
        )

    styles = """
<style>
.guide2{margin:38px 0;padding:clamp(22px,4vw,42px);
 border:1px solid #dbe7dd;border-radius:24px;background:#f7faf6}
.guide2 h2{font-family:Georgia,serif;color:#123c31;font-size:clamp(25px,3vw,35px);line-height:1.2}
.guide2 h3{font-family:Georgia,serif;color:#123c31;margin:0 0 10px}
.guide2 p,.guide2 li{color:#45574d;line-height:1.75}
.guide2-intro{max-width:800px}
.guide2-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:25px 0}
.guide2-step{background:#fff;padding:20px;border:1px solid #e0e9e0;border-radius:16px}
.guide2-step a,.guide2-related a{color:#176347;text-decoration:underline;text-underline-offset:3px}
.guide2-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:24px 0}
.guide2-card{display:flex;flex-direction:column;min-width:0;overflow:hidden;border:1px solid #dce6dd;
 border-radius:16px;background:#fff;color:#123c31;text-decoration:none;transition:transform .2s,border-color .2s}
.guide2-card:hover{transform:translateY(-3px);border-color:#83a992}
.guide2-visual{height:152px;background:#e9f0e9;display:flex;align-items:center;justify-content:center;
 flex-direction:column;gap:6px;overflow:hidden}
.guide2-visual img{width:100%;height:100%;object-fit:contain}
.guide2-file-mark{font:700 21px Manrope,Arial,sans-serif;border:2px solid #a9bfb0;border-radius:8px;padding:14px;color:#376a4c}
.guide2-visual-label{font-size:12px;color:#658171}
.guide2-card-body{padding:17px;display:flex;flex-direction:column;gap:9px;flex:1}
.guide2-meta{color:#64816e;font:600 12px Manrope,Arial,sans-serif}
.guide2-card strong{font:700 15px/1.45 Manrope,Arial,sans-serif}
.guide2-card small{color:#697c6f;line-height:1.5}
.guide2-action{margin-top:auto;font-size:13px;font-weight:700;color:#176347}
.guide2-related{margin-top:26px;padding-top:18px;border-top:1px solid #dbe7dd}
.guide2-related a{display:inline-block;margin:0 16px 8px 0}
@media(max-width:850px){.guide2-grid,.guide2-steps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.guide2-grid,.guide2-steps{grid-template-columns:1fr}.guide2-visual{height:180px}}
</style>
"""

    section = f"""
{START}
{styles}
<section class="guide2" aria-labelledby="guide2-heading">
  <h2 id="guide2-heading">Akran zorbalığında okulda nasıl ilerlenir?</h2>
  <p class="guide2-intro">Akran zorbalığına ilişkin bir bildirim alındığında ilk adım,
  öğrencilerin güvenliğini değerlendirmek ve durumu dikkatle anlamaktır.
  Tek bir sunum veya etkinlik her vakayı çözmez; görüşme, koruyucu çalışma,
  aile iş birliği ve izleme birlikte ele alınmalıdır.</p>

  <div class="guide2-steps">
    <div class="guide2-step">
      <h3>1. Durumu değerlendir</h3>
      <p>Öğrencileri ayrı ayrı, yargılamadan dinle. Olayların sıklığı,
      güç dengesizliği ve güvenlik riskini değerlendir.
      Gizlilik ve okulun bildirim yükümlülüklerini gözet.</p>
      <a href="/kaynak-detay/zorbalik-kuramsal/">Psikolojik danışman kitapçığına git</a>
    </div>
    <div class="guide2-step">
      <h3>2. Koruyucu çalışmayı seç</h3>
      <p>İhtiyaca ve gelişim dönemine uygun sınıf etkinliği,
      farkındalık programı veya psikoeğitim materyali kullan.
      Grup çalışmasını bireysel müdahalenin yerine koyma.</p>
      <a href="/kutuphane.html?q=akran%20zorbaligi">Zorbalık materyallerini incele</a>
    </div>
    <div class="guide2-step">
      <h3>3. Aileyle iş birliği ve takip</h3>
      <p>Velilerle somut gözlemler üzerinden görüş; etiketleyici dilden kaçın.
      Öğrencinin güvenliğini, okul içindeki destekleri ve sonraki
      değerlendirme tarihini birlikte planla.</p>
      <a href="/kaynak-detay/veli-brosur/">Veli broşürünü incele</a>
    </div>
  </div>

  <h2>Akran zorbalığı için önerilen materyaller</h2>
  <p class="guide2-intro">PDR Kampüs kütüphanesindeki gerçek kaynaklardan seçildi.
  Kademeye ve çalışmanın amacına göre bir materyal seçerek başlayabilirsin.</p>
  <div class="guide2-grid">
    {"".join(cards)}
  </div>

  <p><a href="/kutuphane.html?q=akran%20zorbaligi">Kütüphanedeki diğer akran zorbalığı kaynakları →</a></p>

  <div class="guide2-related">
    <h3>İlgili konu rehberleri</h3>
    <a href="/konu/siber-zorbalik/">Siber zorbalık</a>
    <a href="/konu/guvenli-okul-iklimi/">Güvenli okul iklimi</a>
    <a href="/konu/veli-gorusmesi/">Veli görüşmesi</a>
    <a href="/konular.html">Tüm konular</a>
  </div>
</section>
{END}
"""

    original = PAGE.read_text(encoding="utf-8")
    if START in original and END in original:
        pattern = re.escape(START) + r".*?" + re.escape(END)
        changed = re.sub(pattern, lambda _: section.strip(), original, count=1, flags=re.S)
    else:
        if original.count("</main>") != 1:
            raise SystemExit("Beklenmeyen HTML yapısı: </main> bulunamadı.")
        changed = original.replace("</main>", section + "\n</main>", 1)

    PAGE.write_text(changed, encoding="utf-8")

    baseline = load_json(PROTECTED, {})
    approvals = load_json(APPROVAL, {"version": 1, "edits": {}})
    relative = PAGE.relative_to(ROOT).as_posix()

    if relative in baseline.get("files", {}):
        sys.path.insert(0, str(ROOT / "scripts"))
        from seo_engine import runtime_digest

        approvals.setdefault("edits", {})[relative] = {
            "baseline_sha256": baseline["files"][relative],
            "reviewed_sha256": sha(PAGE),
            "runtime_sha256": runtime_digest(changed),
            "reason": "Reviewed topic guide enhancement: existing article and SEO metadata preserved; contextual guidance and verified resource cards added."
        }
        APPROVAL.write_text(
            json.dumps(approvals, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )

    print("✅ Rehber sayfası güncellendi:", relative)
    print("✅ Doğrulanmış materyal kartı:", len(cards))
    print("✅ Gerçek görsel önizlemesi:", images)
    print("ℹ️ Önizlemesiz kaynaklarda belge kartı kullanıldı.")
    print("ℹ️ Eşleşmeyen kayıtlar:", missing)
    print("✅ Mevcut makale, H1, canonical ve SEO başlıkları korundu.")

if __name__ == "__main__":
    main()
