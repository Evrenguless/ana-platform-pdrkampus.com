# Teknik SEO — 11 Ekim 2026

Canlı başlangıç denetimi: robots.txt ve sitemap.xml 200; rastgele olmayan adres 404. 4.179 sitemap URL'sinden katalog sayfa 36–40 dosyaları bulunmuyordu (örnek canlı URL de 404). Kamu kaynak ve konu örneklerinin içeriği ve canonical etiketi ilk HTML yanıtında mevcut. Parametreli kütüphane araması temiz /kutuphane.html canonical adresini kullanıyor; kişisel profil noindex.

Yeni sitemap.xml üç bölümlü bir sitemap index: kaynaklar, konular, diğer kamu sayfaları. Mevcut yayın envanterinden 4.067 gerçek self-canonical URL dahil edilir. Sadece dosyası bulunan, noindex olmayan ve statik ana içeriği, tek bir görünür H1'i, başlık/açıklaması bulunan adresler kabul edilir. Parametreler, fragmentler, başka hostlar ve dizin dışına çıkış reddedilir. Her parça 50.000 URL ve açılmış UTF-8 50 MiB sınırlarında bölünür. Kaynak değişim tarihi doğrulanmadığı için lastmod uydurulmaz.

Başlangıç dışlamaları seo/sitemap-review.json içinde: 5 eksik dosya; dosya türü/alan adı başlıklı 3 içerik; 104 ayırt edilemeyen başlıklı kaynak. Üç zayıf başlıklı sayfa noindex,follow'dur. Aynı başlık farklı belgelerde görülebildiğinden diğer 104 adres silinmez, redirect/canonical birleştirmesi yapılmaz ve otomatik noindex uygulanmaz; sitemap tanıtımı kaynak belgeye dayalı sürüm başlığı/özeti incelemesine kadar tutulur. Sitemap dışında olmak indekslemeyi tek başına engellemez. Yapısal eşik ve metadata özgünlüğü editoryal kaliteyi, kaynak doğruluğunu veya Google indekslemesini garanti etmez.

227 ortak açıklama görünür kaynak kurum/kademe bilgisiyle ayrıştırıldı. Dokuz konu sayfasına mevcut keşif gezinmesinden statik bağlantılar eklendi. Materyal düğmeleri ara redirect adresi yerine mevcut canonical kaynak adresine bağlanır. Kaynak/konu tasarımı, CSS, uygulama/auth scriptleri ve özgün veri dosyaları değişmez.

Tüm mevcut katalog, materyal, kariyer ve yeni kaynak yayıncıları sitemap index okuyabilir/yazabilir. Katalog oluşturucu incelenmiş sayfaları yeniden süsleyip iç içe çoğaltmadan korur. SEO Audit iş akışında bölme ve canonical testleri vardır. Yeni veri eklenmesi otomatik editoryal onay anlamına gelmez.

Doğrulama:

- python scripts/test_sitemaps.py
- python scripts/build_sitemaps.py --check
- python scripts/check_seo.py
- python scripts/build_library_catalog.py --check
- python scripts/build_material_hubs.py --check
- python scripts/build_career_pages.py --check
- python scripts/test_seo_engine.py
- python -m unittest discover -s scripts -p test_resource_publication.py
- node --test tests/*.mjs

Koruma kaydı başlangıçtaki mevcut redirect ve canonical bağlantı eşlemeleri için eksikti; ilgili kamu sunum dosyaları incelenip kesin hash'leri kaydedildi. Veri/CSV/SQL koruması gevşetilmedi. Testlerde kaynak PDF dosyaları bulunmadığından dört PDF pilot testi açıkça atlanır.

Search Console erişimi bu çalışmada mevcut değil. Domain mülkünde veya https://pdrkampus.com/ URL-prefix mülkünde https://pdrkampus.com/sitemap.xml gönderilmeli; konu/kaynak/hub örneklerinde canlı URL denetimi, kullanıcı canonical / Google canonical ve indeksleme nedeni karşılaştırılmalı. Gerçek Googlebot erişimi ve indeks kapsamı yalnız Search Console verisinden doğrulanabilir.
