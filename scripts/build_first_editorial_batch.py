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
def main():
    source=REFERENCE.read_text(encoding="utf-8")
    if "<main" not in source or "</main>" not in source:
        raise SystemExit("Reference template missing <main>")
    head,remaining=source.split("<main",1)
    _,foot=remaining.split("</main>",1)
    OUTPUT.mkdir(parents=True,exist_ok=True)
    report=[]
    for guide in GUIDES:
        target=OUTPUT/(guide["slug"]+".html")
        if target.exists():
            report.append({"slug":guide["slug"],"state":"preserved"})
            continue
        title=guide["title"]
        desc=guide["summary"]
        h=re.sub(r"<title>.*?</title>",f"<title>{esc(title)} | PDR Kampüs</title>",head,count=1,flags=re.S)
        h=re.sub(r'(<meta name="description" content=")[^"]*(")',lambda m:m.group(1)+esc(desc)+m.group(2),h,count=1)
        h=re.sub(r'(<link rel="canonical" href=")[^"]*(")',lambda m:m.group(1)+"https://pdrkampus.com/konu/"+guide["slug"]+"/"+m.group(2),h,count=1)
        h=re.sub(r'<script type="application/ld\+json">.*?</script>',"",h,flags=re.S)
        h=re.sub(r'<meta property="og:[^"]+"[^>]*>',"",h)
        h=h.replace("</head>",'<meta name="robots" content="noindex,follow"></head>',1)
        sections="".join(f'<section class="topic-section"><h2>{esc(a)}</h2><p>{esc(b)}</p></section>' for a,b in guide["sections"])
        body=f'''<main class="topic-shell">
<nav class="topic-breadcrumb" aria-label="İçerik haritası"><a href="/">PDR Kampüs</a> / <a href="/konular.html">Konular</a> / {esc(title)}</nav>
<section class="topic-hero"><div><p class="topic-kicker">PDR KAMPÜS · REHBER TASLAĞI</p><h1>{esc(title)}</h1><p class="topic-lead">{esc(desc)}</p></div></section>
<section class="topic-content"><article class="topic-article">{sections}
<section class="topic-section"><h2>İlgili materyalleri inceleyin</h2><p>Bu taslakta belge düzeyinde doğrulanmamış kaynak kartları gösterilmez. Konuya uygun materyalleri <a href="/kutuphane.html">PDR Kampüs Kütüphane</a> bölümünde inceleyebilirsiniz.</p></section>
<section class="topic-section"><h2>Uygulama notu</h2><p>İçerik okul temelli rehberlik çalışmaları için editoryal taslaktır. Öğrencinin güvenliği, gizlilik ve güncel kurum süreçleri önceliklidir; uzman değerlendirmesinin yerini almaz.</p></section>
</article></section></main>'''
        target.write_text(h+body+foot,encoding="utf-8")
        report.append({"slug":guide["slug"],"state":"created","sections":len(guide["sections"])})
    print(json.dumps({"batch_size":len(GUIDES),"results":report,"live_pages_changed":0,"preview_folder":str(OUTPUT)},ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
