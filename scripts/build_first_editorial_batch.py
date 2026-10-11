#!/usr/bin/env python3
"""First editorial production batch: 5 distinct, reviewable PDR guides.

Creates HTML previews under drafts/pdr-ilk-paket/. Never overwrites live pages,
existing 499 drafts, sitemap, source catalogues or the 500-topic plan.
"""
import html
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REFERENCE=ROOT/"konu/akran-zorbaligi/index.html"
OUTPUT=ROOT/"drafts/pdr-ilk-paket"
GUIDES=[
{
"slug":"ogrenme-motivasyonu-okul-rehberligi",
"title":"Öğrenme Motivasyonu: Okulda Rehberlik Uygulamaları",
"summary":"Öğrenmeye katılımı azaltan etkenleri anlamak, ulaşılabilir hedefler belirlemek ve öğrencinin ilerlemesini izlemek için okul temelli uygulama rehberi.",
"sections":[
("Motivasyonu tek bir nedene bağlamayın","Öğrencinin derslere katılımını değerlendirirken uyku düzenini, dersin güçlük düzeyini, önceki başarı deneyimlerini, akran ilişkilerini ve sınıf ortamını ayrı ayrı ele alın. Düşük performansı tek başına isteksizlik olarak yorumlamayın."),
("İlk görüşmede ne sorulur?","Öğrenciden son iki haftada kendisini derse yakın hissettiği ve uzak hissettiği anları anlatmasını isteyin. Güçlü bulduğu dersleri, zorlandığı etkinlikleri ve kendi seçtiği hedefleri birlikte belirleyin."),
("Uygulanabilir küçük hedefler","Bir haftalık süreç için öğrencinin kontrol edebileceği tek bir davranış belirleyin: örneğin ders başında beş dakikalık hazırlık ya da tamamlanabilir bir çalışma adımı. Sonucu yalnızca notla değil, çaba ve süreçle birlikte değerlendirin."),
("Öğretmen ve aileyle iş birliği","Öğretmenle geri bildirimin somut ve yargısız olmasını, veliyle ise karşılaştırma ve baskı yerine düzenli destek sağlanmasını konuşun. Öğrencinin mahremiyetini koruyun."),
("İzleme ve yeniden değerlendirme","Bir veya iki hafta sonra öğrencinin seçtiği hedefi, karşılaştığı engelleri ve işe yarayan yöntemleri gözden geçirin. Süreğen güçlüklerde daha kapsamlı okul değerlendirmesi ve gerektiğinde uygun uzmana yönlendirme yapın.")
]},
{
"slug":"dikkat-odaklanma-okulda-destek",
"title":"Dikkat ve Odaklanma: Okulda Destek Adımları",
"summary":"Ders ortamında dikkatini sürdürmekte zorlanan öğrenciler için gözleme dayalı, damgalamayan ve izlenebilir destek yaklaşımı.",
"sections":[
("Güçlüğün koşullarını belirleyin","Zorlanmanın tüm derslerde mi, belirli görevlerde mi, günün bazı saatlerinde mi ortaya çıktığını öğretmen gözlemleri ve öğrencinin anlatımıyla inceleyin. Dikkat güçlüğünden tanı sonucu çıkarmayın."),
("Görevi daha yönetilebilir hâle getirin","Uzun yönergeleri kısa parçalara ayırmak, önemli adımları görünür kılmak ve kısa kontrol noktaları belirlemek öğrenme sürecini destekleyebilir. Düzenlemeyi öğrenciyle birlikte deneyin."),
("Çevresel etkenleri değerlendirin","Gürültü, oturma düzeni, uyku, duygusal zorlanma ve görevin anlaşılabilirliği gibi etkenleri inceleyin. Öğrenciye tek bir açıklama dayatmayın."),
("Öğretmenle ortak izleme ölçütü belirleyin","Yalnızca 'dikkatliydi' demek yerine göreve başlama süresi veya tamamlanan adımlar gibi gözlenebilir göstergeler seçin. Ölçütlerin öğrenciyi etiketlemek için kullanılmamasına dikkat edin."),
("Gerektiğinde yönlendirme","Güçlük birden fazla ortamda sürüyor ve günlük işlevselliği etkiliyorsa aileyle gizliliğe uygun görüşün; değerlendirme gereksinimini ilgili uzmanlarla ele alın.")
]},
{
"slug":"bep-hazirlama-okul-ekibi",
"title":"BEP Hazırlama: Okul Ekibi İçin Uygulama Rehberi",
"summary":"Bireyselleştirilmiş Eğitim Programı hazırlarken öğrencinin mevcut performansını, ölçülebilir hedefleri ve ekip koordinasyonunu düzenleme rehberi.",
"sections":[
("Başlangıç: mevcut performansı yazın","Öğrencinin yapabildiklerini ve destek gereksinimlerini somut gözlem ve değerlendirme verisiyle açıklayın. Genel yargılar yerine öğretim açısından anlamlı örnekler kullanın."),
("Ölçülebilir hedef oluşturun","Her hedefte beklenen davranışın, koşulun ve başarı ölçütünün anlaşılır olmasına dikkat edin. Hedeflerin öğrencinin mevcut düzeyi ve eğitim ortamıyla uyumunu kontrol edin."),
("Uyarlamaları somutlaştırın","Materyal, süre, yönerge, ortam ve ölçme yönteminde ihtiyaç duyulan düzenlemeleri ayrı ayrı belirtin. Aynı uyarlamanın her öğrenciye uygun olacağını varsaymayın."),
("Ekip rollerini netleştirin","Öğretmen, aile, rehberlik servisi ve ilgili diğer personelin görev paylaşımını belirleyin. Öğrencinin görüşünün alınabileceği uygun fırsatları değerlendirin."),
("İlerlemeyi belgeleyin","Belirlenen aralıklarla öğrenme örneklerini gözden geçirin. Hedefler işlevsel değilse verilere dayalı değişiklikleri BEP geliştirme süreçleri içinde ele alın. Güncel mevzuat ve kurum usullerini esas alın.")
]},
{
"slug":"okula-uyum-ilk-haftalar",
"title":"Okula Uyum: İlk Haftalar İçin Rehberlik Planı",
"summary":"Okula yeni başlayan veya okul değiştiren öğrencilerin güven, aidiyet ve katılımını desteklemek için uygulanabilir ilk haftalar planı.",
"sections":[
("Uyum ihtiyacını belirleyin","Öğrencinin önceki okul deneyimini, güçlü yönlerini, yeni ortamda merak ettiklerini ve kaygılarını anlamaya çalışın. Yeni gelen her öğrenciyi aynı hızda uyum sağlayacak kabul etmeyin."),
("Güvenli karşılama düzenleyin","Okulun temel alanlarını, ulaşılabilecek yetişkinleri ve günlük rutinleri yaşa uygun biçimde tanıtın. Soru sormayı kolaylaştıran kısa ve düşük baskılı etkinlikler kullanın."),
("Akran desteğini planlayın","Gönüllü akran rehberliği ve iş birliğine dayalı sınıf etkinlikleri düzenleyin. Öğrencinin katılmak istemediği sosyal etkinliklerde zorlayıcı davranmayın."),
("Veli ve öğretmen geri bildirimini birleştirin","İlk haftaların sonunda devam, sınıf katılımı, teneffüs deneyimi ve yardım isteme davranışlarını değerlendirin. Mahremiyet ilkeleri doğrultusunda bilgi paylaşın."),
("Uyum güçlüğü sürerse","Çekilme, yoğun kaygı veya devamsızlık gibi belirtiler devam ederse bireysel görüşme ve okulun uygun destek/yönlendirme süreçlerini planlayın.")
]},
{
"slug":"veli-gorusmesi-hazirlik-izleme",
"title":"Veli Görüşmesi: Hazırlık, Görüşme ve Takip",
"summary":"Okul rehberlik servisinde veli görüşmesini amaçlı, iş birlikçi ve gizliliğe uygun biçimde yürütmek için adım adım uygulama rehberi.",
"sections":[
("Görüşme amacını netleştirin","Veliye görüşmenin neden planlandığını ve hangi konuların ele alınacağını açıkça bildirin. Çocuğa ilişkin bilgileri yalnızca görüşme amacıyla sınırlı ve gerekli düzeyde kullanın."),
("Yargısız başlangıç yapın","Velinin gözlemlerini kesintiye uğratmadan dinleyin. Suçlayıcı ifadeler yerine belirli okul gözlemlerini paylaşın ve farklı bakış açılarını anlamaya çalışın."),
("Somut destek adımları belirleyin","Evde ve okulda uygulanabilecek az sayıda, gerçekçi adım üzerinde anlaşın. Her adım için sorumluluğu ve yeniden görüşme zamanını netleştirin."),
("Kayıt ve mahremiyet","Görüşme kaydını kurumun güncel usullerine uygun ve asgari veri ilkesiyle tutun. Öğrencinin özel paylaşımlarını gereksiz yere aktarmayın."),
("Takip görüşmesi planlayın","Kararlaştırılan adımların işe yarayıp yaramadığını somut örneklerle değerlendirin. Destek ihtiyacı devam ederse okul içi iş birliğini ve gerekli yönlendirmeleri gözden geçirin.")
]}
]
def esc(s):
    return html.escape(str(s),quote=True)

SEARCH_TERMS = {
 "ogrenme-motivasyonu-okul-rehberligi": ["motivasyon", "verimli ders çalışma", "çalışma becerileri"],
 "dikkat-odaklanma-okulda-destek": ["dikkat", "odaklan", "öğrenme güçlüğ"],
 "bep-hazirlama-okul-ekibi": ["bep", "bireyselleştirilmiş", "özel eğitim"],
 "okula-uyum-ilk-haftalar": ["okula uyum", "uyum", "okul öncesi"],
 "veli-gorusmesi-hazirlik-izleme": ["veli görüş", "veli rehberliği", "aile iletişimi"],
}
EXTRA = {
 "ogrenme-motivasyonu-okul-rehberligi": {
 "example": "Öğrenci ödevleri başlatamadığını söylüyor. İlk hafta hedefi her akşam 15 dakika çalışmak değil; seçtiği iki gün, kendi belirlediği bir derste yalnızca ilk soruya başlamak olabilir. Görüşmede neyin işe yaradığını öğrenci anlatır.",
 "check": ["Hedef öğrencinin kendi kontrol edebileceği bir davranış mı?", "Çalışmayı zorlaştıran koşullar öğrenciyle birlikte belirlendi mi?", "Öğretmen ve veli geri bildirimi karşılaştırma içermiyor mu?", "İlerlemeyi konuşmak için tarih belirlendi mi?"],
 "faq": [("Motivasyonu düşük öğrenciyi nasıl tanırız?", "Tek başına not düşüşü yeterli değildir. Öğrencinin katılımı, okul deneyimi ve güçlük yaşadığı durumlar birlikte değerlendirilir."), ("Ödül kullanmak gerekli mi?", "Her öğrenci için tek yöntem yoktur. Öğrencinin anlamlı bulduğu hedefler, özerklik ve yeterlik deneyimini destekleyen geri bildirim önceliklidir.")]},
 "dikkat-odaklanma-okulda-destek": {
 "example": "Öğrenci uzun yazılı yönergelerde görevden kopuyor ama sözlü kısa yönergeleri izliyor. Öğretmen bir hafta boyunca yönergeleri üç görünür adıma böler, görev başlangıcını gözler ve öğrenciyle yararlılığını değerlendirir.",
 "check": ["Gözlem birden fazla ders ve ortamı kapsıyor mu?", "Öğrenci için erişilebilir yönerge ve mola düzeni denendi mi?", "Verilen destek damgalamadan uygulanıyor mu?", "Süreğen güçlüklerde uygun değerlendirme kanalı açık mı?"],
 "faq": [("Dikkat dağınıklığı tanı anlamına gelir mi?", "Hayır. Sınıf içi gözlem klinik tanı koymaz; gerekirse uygun uzman değerlendirmesi istenir."), ("Öğretmen ilk olarak ne yapabilir?", "Görevleri küçük parçalara ayırabilir, yönergeleri netleştirebilir ve öğrenciyle hangi düzenlemenin işe yaradığını gözden geçirebilir.")]},
 "bep-hazirlama-okul-ekibi": {
 "example": "‘Okuduğunu anlar’ hedefi yerine başlangıç performansı ölçülür ve öğrencinin düzeyine uygun metinde belirlenmiş soruları hangi destekle, hangi başarı ölçütünde yanıtlayacağı açıklanır. Örnek ölçüt öğrenci verilerine göre belirlenir.",
 "check": ["Performans tanımı gözlenebilir veriye dayanıyor mu?", "Hedefin koşulu ve başarı ölçütü açık mı?", "Uyarlamalar öğretmenin uygulayabileceği kadar somut mu?", "İzleme kanıtı ve gözden geçirme tarihi belirlendi mi?"],
 "faq": [("Her öğrenci için aynı BEP şablonu yeterli mi?", "Hayır. Belgenin düzeni kurumun güncel usullerine uygun olsa da performans, hedef ve destekler öğrenciye göre belirlenir."), ("Hedef gerçekleşmiyorsa ne yapılmalı?", "Öğretim yöntemi, ortam ve hedefin ulaşılabilirliği ekipçe veriye dayanarak gözden geçirilir.")]},
 "okula-uyum-ilk-haftalar": {
 "example": "Okul değiştiren öğrenci teneffüste yalnız kalıyor. Öğrencinin onayıyla bir sınıf arkadaşı okul alanlarını tanıtıyor; ilk hafta sonunda öğrenci kendini güvende hissettiği alanları ve zorlandığı anları anlatıyor.",
 "check": ["Öğrencinin görüşü alındı mı?", "Okuldaki güvenilir yetişkinler tanıtıldı mı?", "Akran desteği gönüllülük temelinde mi?", "İlk haftalar için takip görüşmesi planlandı mı?"],
 "faq": [("Uyum ne kadar sürer?", "Tek bir süre herkes için geçerli değildir. Öğrencinin yaşına, deneyimine ve okul ortamına göre izleme planlanır."), ("Çekingen öğrenciyi etkinliğe zorlamalı mıyız?", "Hayır. Katılımı destekleyen düşük baskılı seçenekler ve öğrencinin sınırlarına saygı esastır.")]},
 "veli-gorusmesi-hazirlik-izleme": {
 "example": "Veli ‘çocuğum ders çalışmıyor’ diyerek geliyor. Görüşmede taraflar gözlenen iki durumu netleştiriyor: çalışma başlangıcı ve ev ödevi bitirme güçlüğü. Bir ev ve bir okul desteği belirleyerek iki hafta sonrasına takip koyuyor.",
 "check": ["Görüşmenin amacı ve sınırı açıklandı mı?", "Veli görüşüne yeterince yer verildi mi?", "Çocuğun özel bilgileri gereksiz yere paylaşılmadı mı?", "Kararlar, sorumlular ve takip zamanı net mi?"],
 "faq": [("Veliye öğrencinin tüm görüşme notları verilir mi?", "Hayır. Gizlilik, çocuğun yararı ve yürürlükteki yükümlülükler doğrultusunda yalnızca gerekli bilgiler paylaşılır."), ("Veliyle anlaşma sağlanamazsa?", "Ortak hedefleri yeniden tanımlayın, somut gözlemleri paylaşın ve uygun okul içi iş birliği süreçlerini değerlendirin.")]},
}
def resources(slug):
    terms=SEARCH_TERMS[slug]
    rows=[]
    seen=set()
    for name in ("data/library.json","data/collected-resources.json","data/new-resources-batch.json","data/library-reviewed-batch-20261010.json"):
        file=ROOT/name
        if not file.exists(): continue
        for row in json.loads(file.read_text(encoding="utf-8")):
            rid=str(row.get("id",""))
            if not rid or rid in seen:continue
            seen.add(rid)
            hay=(" "+str(row.get("title",""))+" "+str(row.get("topic",""))).casefold()
            score=max((3 if term in str(row.get("title","")).casefold() else 1 if term in hay else 0) for term in terms)
            if score: rows.append((score,row))
    # Favor direct title matches; a broad category tag alone is not enough
    # to present an unrelated item as a recommended document.
    rows.sort(key=lambda item:(-item[0],str(item[1].get("title",""))))
    strong=[row for score,row in rows if score>=3]
    return strong[:9]
def source_cards(slug):
    cards=[]
    count=0
    for r in resources(slug):
        title=esc(r.get("title","Kaynak"))
        rid=str(r.get("id",""))
        url=r.get("pagePath","")
        if not (isinstance(url,str) and url.startswith("/") and (ROOT/url.lstrip("/")).exists()):
            # A genuine file is preferable to a fabricated local landing page.
            url=r.get("file","")
        if not (isinstance(url,str) and url.startswith(("https://","http://","/"))):continue
        preview=r.get("previewImage") or r.get("preview") or ""
        if not preview:
            files=list((ROOT/"assets/resource-previews").glob(rid+"-*.jpg"))
            if not files:files=list((ROOT/"assets/resource-previews").glob(rid+"*.png"))
            if files:preview="/"+str(files[0].relative_to(ROOT))
        if isinstance(preview,str) and preview.startswith("/") and not (ROOT/preview.lstrip("/")).is_file():preview=""
        visual=f'<img src="{esc(preview)}" alt="{title} belge önizlemesi" loading="lazy">' if preview else '<span class="guide2-card-fallback" aria-hidden="true">PDF / MATERYAL</span>'
        cards.append(f'<a class="guide2-card" href="{esc(url)}" target="_blank" rel="noopener noreferrer"><span class="guide2-visual">{visual}</span><span class="guide2-card-body"><span class="guide2-meta">{esc(r.get("level",""))} · {esc(r.get("type","Materyal"))}</span><strong>{title}</strong><small>{esc(r.get("source","Kaynak kurum"))}</small><span class="guide2-action">Kaynağı incele →</span></span></a>')
        count+=1
    return '<div class="guide2-grid">'+"".join(cards)+'</div>' if cards else '<p>Bu konu için belge düzeyinde uygun materyal henüz doğrulanmadı.</p>'
def load_editorial_batches():
    """Append new, topic-specific manuscripts; preserve existing first five guides."""
    for filename in ("data/pdr-editorial-batch-02.json", "data/pdr-editorial-batch-03.json", "data/pdr-editorial-batch-04.json"):
        path = ROOT / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        for record in json.loads(path.read_text(encoding="utf-8")):
            slug = record["slug"]
            if any(existing["slug"] == slug for existing in GUIDES):
                raise ValueError("Duplicate editorial slug: " + slug)
            if len(record["sections"]) < 5 or len(record["faq"]) < 2 or len(record["check"]) < 3:
                raise ValueError("Incomplete editorial guide: " + slug)
            GUIDES.append({key: record[key] for key in ("slug", "title", "summary", "sections")})
            EXTRA[slug] = {key: record[key] for key in ("example", "check", "faq")}
            SEARCH_TERMS[slug] = record["search_terms"]

def main():
    load_editorial_batches()
    source=REFERENCE.read_text(encoding="utf-8")
    if '<main' not in source or '</main>' not in source:raise SystemExit("Missing main in reference")
    head,tail=source.split("<main",1)
    _,foot=tail.split("</main>",1)
    style_match=re.search(r'<style>[^<]*\\.guide2-grid.*?</style>',source,flags=re.S)
    theme_style=style_match.group(0) if style_match else ""
    OUTPUT.mkdir(parents=True,exist_ok=True)
    report=[]
    for g in GUIDES:
        slug=g["slug"];t=g["title"];desc=g["summary"];extra=EXTRA[slug]
        h=re.sub(r'<title>.*?</title>',f'<title>{esc(t)} | PDR Kampüs</title>',head,count=1,flags=re.S)
        h=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m.group(1)+esc(desc)+m.group(2),h,count=1)
        h=re.sub(r'(<link rel="canonical" href=")[^"]*(")',lambda m:m.group(1)+'https://pdrkampus.com/konu/'+slug+'/'+m.group(2),h,count=1)
        h=re.sub(r'<script type="application/ld\\+json">.*?</script>','',h,flags=re.S)
        h=re.sub(r'<meta property="og:[^"]+"[^>]*>','',h)
        h=h.replace('</head>','<meta name="robots" content="noindex,follow">'+theme_style+'''<style>
        .topic-article .topic-section p{line-height:1.85}
        .topic-article .guide2{margin-top:24px}
        .guide2-card-fallback{display:grid;place-items:center;min-height:130px;background:#ecf3ed;color:#315c49;font-weight:700;letter-spacing:.1em}
        .guide2-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:14px}
        .guide2-card{display:flex;flex-direction:column;border:1px solid #dbe7dd;border-radius:14px;overflow:hidden;background:#fff;text-decoration:none}
        .guide2-card-body{padding:15px;display:grid;gap:8px}
        .guide2-visual img{width:100%;height:160px;object-fit:cover}
        .topic-quick ul{line-height:1.85}
        .pdr-sidebar{display:flex;flex-direction:column;gap:16px;min-width:0}
        .pdr-sidebar .topic-card{margin:0;padding:18px;border:1px solid #dce7de;border-radius:16px;background:#fff}
        .pdr-sidebar .pdr-side-note:nth-child(even){background:#f1f7f2}
        .pdr-sidebar h3{font-size:17px;line-height:1.4;margin:0 0 8px}
        .pdr-sidebar p{font-size:14px;line-height:1.7;margin:0}
        .pdr-side-note small{font-size:11px;letter-spacing:.09em;color:#317459;font-weight:700}
        .pdr-side-links .topic-links{display:grid;gap:8px}
        @media(max-width:850px){.pdr-sidebar{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}}
        @media(max-width:560px){.pdr-sidebar{grid-template-columns:1fr}}
        </style></head>''',1)

        from urllib.parse import quote
        search='/kutuphane.html?q='+quote(t.split(':')[0])
        rail_note_data = {
            "ogrenme-motivasyonu-okul-rehberligi": ["Öğrencinin güçlü yönlerini öğren.", "Küçük bir haftalık hedef seç.", "İlerlemeyi bir hafta sonra izle."],
            "dikkat-odaklanma-okulda-destek": ["Zorlanmanın hangi görevlerde oluştuğunu gözle.", "Yönergeleri görünür adımlara böl.", "Sınıf gözleminden tanı çıkarma."],
            "bep-hazirlama-okul-ekibi": ["Mevcut performansı somut yaz.", "Hedefin başarı ölçütünü belirt.", "Ekibin görevlerini birlikte netleştir."],
            "okula-uyum-ilk-haftalar": ["Güvenilir yetişkinleri tanıt.", "Gönüllü akran desteği düzenle.", "İlk haftaları birlikte değerlendir."],
            "veli-gorusmesi-hazirlik-izleme": ["Görüşmenin amacını açıkla.", "Yargı yerine gözlem paylaş.", "Takip tarihini birlikte kararlaştır."],
        }
        notes = "".join('<div class="topic-card pdr-side-note"><small>UYGULAMA İPUCU</small><h3>Adım '+str(i)+'</h3><p>'+esc(note)+'</p></div>' for i,note in enumerate(rail_note_data.get(slug, [section[1] for section in g["sections"][:3]]),1))
        quick = '<div class="topic-card pdr-side-links"><h3>Hızlı erişim</h3><div class="topic-links"><a href="#adim-1">Uygulama adımları</a><a href="#ornek">Örnek senaryo</a><a href="#materyaller">Kaynak önizlemeleri</a><a href="'+esc(search)+'">Kütüphanede ara</a></div></div>'
        sidebar_cards = quick + notes
        toc=''.join(f'<li><a href="#adim-{i}">{esc(a)}</a></li>' for i,(a,_) in enumerate(g["sections"],1))
        sections=''.join(f'<section class="topic-section" id="adim-{i}"><h2>{esc(a)}</h2><p>{esc(b)}</p></section>' for i,(a,b) in enumerate(g["sections"],1))
        checklist=''.join('<li>'+esc(x)+'</li>' for x in extra["check"])
        faq=''.join('<details class="topic-section"><summary><strong>'+esc(q)+'</strong></summary><p>'+esc(a)+'</p></details>' for q,a in extra["faq"])

        page=f'''<main class="topic-shell">
        <nav class="topic-breadcrumb" aria-label="İçerik haritası"><a href="/">PDR Kampüs</a><span>/</span><a href="/konular.html">Konular</a><span>/</span>{esc(t)}</nav>
        <section class="topic-hero"><div><p class="topic-kicker">OKUL PDR · UYGULAMA REHBERİ</p><h1>{esc(t)}</h1><p class="topic-lead">{esc(desc)}</p><div class="topic-actions"><a class="primary" href="{esc(search)}">Kütüphanede ara</a></div></div><aside class="topic-quick"><strong>Bu sayfada</strong><ul><li>Okulda uygulama adımları</li><li>Somut örnek senaryo</li><li>Kontrol listesi ve sık sorulanlar</li><li>Materyal ve önizleme kartları</li></ul></aside></section>
        <section class="topic-content"><article class="topic-article">
        <nav class="guide-toc" aria-label="Bu rehberde"><strong>Bu rehberde</strong><ul>{toc}<li><a href="#ornek">Uygulama örneği</a></li><li><a href="#materyaller">İlgili kaynaklar</a></li></ul></nav>
        {sections}
        <section class="topic-section" id="ornek"><h2>Okuldan örnek uygulama</h2><p>{esc(extra["example"])}</p></section>
        <section class="topic-section"><h2>Uygulama kontrol listesi</h2><ul>{checklist}</ul></section>
        <section class="topic-section"><h2>Sık sorulan sorular</h2>{faq}</section>
        <section class="guide2" id="materyaller"><h2>İlgili kütüphane materyalleri</h2><p class="guide2-intro">Katalog başlık ve etiketlerinden seçilen aday kaynaklardır. İçerikleri tek tek incelenmeden konuya tam uygunlukları kesinleştirilmiş sayılmaz.</p>{source_cards(slug)}<p><a href="{esc(search)}">Kütüphanedeki diğer materyalleri gör →</a></p></section>
        <section class="topic-section"><h2>İçerik ve kullanım notu</h2><p>Bu sayfa PDR Kampüs editoryal taslağıdır. Kurumun güncel mevzuatı, öğrenci güvenliği, gizlilik ve gerekli uzman yönlendirmesi esastır.</p></section>
        </article><aside class="topic-sidebar pdr-sidebar">{sidebar_cards}<div class="topic-card"><h3>İlgili sayfalar</h3><div class="topic-links"><a href="/konular.html">Bütün konu rehberleri</a><a href="{esc(search)}">Kütüphane kaynakları</a><a href="/materyaller/sunumlar/">Rehberlik sunumları</a></div></div></aside></section>
        </main>'''
        dest=OUTPUT/(slug+".html")
        dest.write_text(h+page+foot,encoding="utf-8")
        report.append({"slug":slug,"state":"updated","sections":len(g["sections"]),"candidate_sources":len(resources(slug))})
    print(json.dumps({"batch_size":len(GUIDES),"results":report,"live_pages_changed":0,"preview_folder":str(OUTPUT)},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
