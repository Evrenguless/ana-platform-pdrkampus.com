# PDR Kampüs — öncelikli editoryal düzeltme raporu

118 rehberin konuya özgü içeriği düzeltildi; tüm 500 taslak aynı denetim betikleriyle yeniden oluşturulup incelendi. Bu çalışma 500 rehberin tüm editoryal eksiklerinin bittiğini veya uzman onayını ifade etmez.

**Dal:** `feature/500-konu-icerik-sistemi`. **Tarih:** 14 Ekim 2026. **Yayın onayı:** hayır.

Depo adı çalışma sırasında `Evrenguless/ana-platform-pdrkampus.com` olarak değişmişti. GitHub depo kimliği **1387603040** aynı kaldı; eski adres aynı depoya yönleniyor.

Başlangıç: commit `60e4051949b86cf54477d9bb112b5531c3c355e5`, Actions run **38435919059**, artifact **11832837160**. Yerel feature dalı bu commit ile birebir aynıydı. Önce ölçümleri indirilen orijinal rapordan, sonra ölçümleri yeniden oluşturulan taslakların aynı denetiminden alınmıştır.

## 500 rehberin önce/sonra ölçümleri

| Ölçüt | Önce | Sonra |
|---|---:|---:|
| Ortalama ana metin kelimesi | 249.6 | 261.7 |
| En kısa ana metin | 123 | 142 |
| 125 kelimenin altı | 1 | 0 |
| 250 kelimenin altı | 286 | 221 |
| Kaynak kartı olmayan rehber | 229 | 137 |
| Benzerlik adayı çift | 1450 | 840 |
| Birebir ortak bölüm grubu | 8 | 2 |
| 15 kelimeden kısa bölüm sorunu olan rehber | 176 | 135 |
| Kısa/eksik örnek sorunu olan rehber | 93 | 49 |

Benzerlik sayısı 8 kelimelik ortak dizilerin %45 eşiğine dayalı bir tarama sonucudur; çift sayısı ayrı hatalı rehber sayısı değildir. Bölüm sorunu sayısı da bölüm adedi değil ilgili soruna sahip rehber sayısıdır.

## Düzenlenen 118 rehber

- Kritik risk denetiminin işaretlediği 33 rehberin tamamı.
- 34 BEP/özel eğitim rehberinin tamamı.
- Tekrarı yoğun 25 kariyer rehberi.
- En kısa 25 rehber; yukarıdaki gruplarla bir rehber çakışır.
- Birebir ortak bölümü olan nakil uyumu ve yalnızlık rehberleri.

| Öncelikli grup ölçütü | Önce | Sonra |
|---|---:|---:|
| Ortalama kelime | 239.0 | 290.4 |
| En kısa ana metin | 123 | 254 |
| 250 kelimenin altı | 65 | 0 |
| Kaynak kartı olmayan | 92 | 0 |
| Kısa bölüm sorunu | 41 | 0 |
| Kısa örnek sorunu | 44 | 0 |
| 118 rehber arasında benzerlik adayı | 602 | 0 |

Krizlerde anlık güvenlik, güvenli veli teması, olgusal kayıt, bilgi mahremiyeti ve yetkili devir farklı olay türlerine göre açıklandı. Kendine zarar/intihar ifadelerinde sakinleşme veya söz verme tek güvenlik kanıtı sayılmıyor; okul rolü uzman değerlendirmesiyle ayrılıyor. İstismar ve ihmalde okulun soruşturma yürütmemesi, gerekli bildirimin kanıt veya veli görüşmesi beklenerek ertelenmemesi vurgulandı.

BEP grubunda ortak ve kendi kendini tekrar eden açıklamalar yerine somut görev, ipucu düzeyi, bağımsız performans, ekip sorumlusu ve izlem kararı eklendi. Kariyer grubunda bölüm koşulu, ders planı, günlük iş görevi, maliyet, değer ve tanıtım doğrulama ayrı araştırma görevleriyle ele alındı. Kısa rehberlerde konuya özgü uygulama ve takip açıklamaları eklendi; 15 kelimeden kısa parçalar içerik sırası korunarak anlamlı bölümlerle birleştirildi.

## Kaynakların sınırı

12 kurumsal kaynak için 118 rehbere açık eşleme yapıldı; başlık taramasıyla rastgele kaynak eklenmedi. Yeni 165 kaynak kartı mevcut kart düzenini kullanır ve yayımlayan kurumun sayfasına açılır. Kaynağın sınırlı kapsamı kartta; kontrol kanıtı kaynak manifestinde bulunur.

Kaynak kayıtlarında MEB BEP kılavuzu/yönerge gibi doğrudan okunan belgeler ile arama indeksinde görülen içerik ayrılır. YÖK Atlas ve NICE için doğrudan erişim denemelerindeki başarısızlık kayda geçirilmiştir. Çocuk Koruma Kanunu için Bakanlığın resmî bağlantı dizini görüldü; bağlı PDF tam metninin güncellik onayı verilmedi. O*NET ABD bağlamındadır; Türkiye için yetki, ücret veya istihdam garantisi olarak kullanılmaz. Kaynak kartı bulunması rehberdeki her önerinin belgede yer aldığını ya da uzman tarafından onaylandığını göstermez.

## Doğrulama

- 2 mevcut denetçi testi + 5 yeni öncelikli içerik/kaynak testi geçti.
- Mevcut 46 JavaScript testi geçti.
- Derleme kontrolü, 500 taslak oluşturma ve mevcut yapısal kapı geçti.
- Derin içerik ve yayın öncesi denetim yeniden çalıştı: 500 benzersiz slug, her rehberde en az 5 bölüm, boş ana metin yok, yayın onayı false.
- Geniş Python keşfinde localhost izni ve openpyxl eksikliğine bağlı iki çevre hatası çıktı. Etkilenen iki modül uygun ortamda yeniden çalıştırıldı: 6 + 6 test geçti. Pilot dosyalar bulunmadığı için 4 ilgisiz test atlandı.
- Git diff boşluk kontrolü geçti. Canlı /konu sayfaları, kataloglar, sitemap ve yayın ayarları değiştirilmedi.

## Kalan iş

221 rehber hâlâ 250 kelimenin altında; 137 rehberde kaynak kartı yok. 840 benzerlik adayı ve sınav/zorbalık gruplarında iki birebir ortak bölüm grubu kalıyor. 33 kritik rehberin uzman inceleme gereksinimi sürüyor. Mevcut katalog kaynaklarının 500 rehber için konu uygunluğu otomatik denetimle doğrulanmış sayılmıyor. Yayın, tüm belge içeriğinin doğrulanması ve görsel/mobil onay bu commit kapsamı dışında.

## Commit kapsamındaki kesin dosya listesi

- `.github/workflows/draft-500-quality-audit.yml`
- `data/pdr-editorial-batch-02.json`
- `data/pdr-editorial-batch-04.json`
- `data/pdr-editorial-batch-05.json`
- `data/pdr-editorial-batch-06.json`
- `data/pdr-editorial-batch-07.json`
- `data/pdr-editorial-batch-08.json`
- `data/pdr-editorial-batch-09.json`
- `data/pdr-editorial-batch-10.json`
- `data/pdr-editorial-batch-11.json`
- `data/pdr-editorial-batch-15.json`
- `data/pdr-editorial-batch-18.json`
- `data/pdr-editorial-batch-20.json`
- `data/pdr-editorial-batch-22.json`
- `data/pdr-editorial-primary-sources.json`
- `scripts/build_first_editorial_batch.py`
- `scripts/test_editorial_priority_guides.py`
- `seo/icerik-plani/500-rehber-derin-icerik-denetimi.json`
- `seo/icerik-plani/500-rehber-yayin-oncesi-denetim.json`
- `seo/icerik-plani/ilk-50-kalite-raporu.json`
- `seo/icerik-plani/ilk-50-yayin-kapisi.json`
- `seo/icerik-plani/ilk-500-toplu-durum.json`
- `seo/icerik-plani/priority-editorial-remediation-2026-10-14.json`
- `seo/icerik-plani/priority-editorial-remediation-2026-10-14.md`

Oluşturulan `drafts/pdr-ilk-paket/` HTML önizlemeleri yereldir ve commit kapsamına alınmaz; aynı betikle yeniden üretilebilir.

## Rehber bazında ölçümler

| Rehber slug | Ana metin önce → sonra | Kaynak kartı önce → sonra |
|---|---:|---:|
| `bep-ders-uyarlamasi` | 234 → 370 | 0 → 1 |
| `bep-guclu-yonler` | 133 → 279 | 0 → 1 |
| `bep-hazirlama-okul-ekibi` | 187 → 261 | 9 → 10 |
| `bep-hedef-izleme-toplantisi` | 222 → 359 | 0 → 1 |
| `bep-ogrenci-katilimi` | 238 → 375 | 0 → 1 |
| `bep-olculebilir-hedef` | 191 → 335 | 0 → 1 |
| `bep-toplantisi-gundemi` | 216 → 354 | 9 → 10 |
| `cocukta-guvenli-yardim-isteme` | 137 → 278 | 5 → 7 |
| `ergenlik-veli-rehberligi` | 138 → 286 | 9 → 10 |
| `ilkokul-arkadas-anlasmazligi` | 139 → 278 | 0 → 1 |
| `ilkokul-isbirlikci-oyun` | 137 → 285 | 1 → 2 |
| `ilkokul-istenmeyen-temasa-hayir-deme` | 251 → 384 | 1 → 2 |
| `kariyer-aile-meslek-beklentisi` | 349 → 275 | 0 → 2 |
| `kariyer-bolum-ders-planini-okuma` | 365 → 275 | 0 → 2 |
| `kariyer-bolum-tanitiminda-bilgi-dogrulama` | 383 → 290 | 0 → 2 |
| `kariyer-coklu-ilgi-alani-olan-ogrenci` | 358 → 287 | 0 → 2 |
| `kariyer-egitim-yolu-arastirma` | 370 → 278 | 0 → 2 |
| `kariyer-gelecek-mesleklerini-arastirma` | 342 → 271 | 0 → 2 |
| `kariyer-guclu-yon-ve-beceri-eslestirme` | 367 → 275 | 0 → 2 |
| `kariyer-ilgi-envanteri-sonuclarini-konusma` | 382 → 279 | 0 → 2 |
| `kariyer-is-ortami-tercihleri` | 355 → 273 | 0 → 2 |
| `kariyer-kariyer-kararinda-belirsizlik` | 349 → 276 | 0 → 2 |
| `kariyer-kariyer-plani-donemlik-izleme` | 356 → 278 | 0 → 2 |
| `kariyer-meslek-seciminde-akran-etkisi` | 367 → 275 | 0 → 2 |
| `kariyer-meslek-seciminde-tek-dogru-yanilgisi` | 363 → 287 | 0 → 2 |
| `kariyer-meslek-tanitim-semineri` | 356 → 277 | 1 → 3 |
| `kariyer-meslek-uzmanina-soru-hazirlama` | 368 → 282 | 0 → 2 |
| `kariyer-mesleki-degerleri-karsilastirma` | 358 → 274 | 0 → 2 |
| `kariyer-mesleki-karar-secenek-tablosu` | 366 → 277 | 0 → 2 |
| `kariyer-mesleklere-iliskin-onyargi` | 361 → 274 | 0 → 2 |
| `kariyer-mesleklerin-gunluk-gorevleri` | 383 → 282 | 0 → 2 |
| `kariyer-mezuniyet-sonrasi-alternatifler` | 362 → 279 | 0 → 2 |
| `kariyer-ogrenim-maliyetini-arastirma` | 370 → 281 | 0 → 2 |
| `kariyer-resm-program-kosullari` | 357 → 269 | 0 → 2 |
| `kariyer-sehir-ve-ulasim-kosullari` | 354 → 276 | 0 → 2 |
| `kariyer-staj-ve-gonulluluk-firsatlari` | 357 → 274 | 0 → 2 |
| `kariyer-universite-yasami-beklentileri` | 346 → 270 | 0 → 2 |
| `kriz-acil-guvenlik-degerlendirmesi` | 200 → 303 | 0 → 1 |
| `kriz-afet-sonrasi-okula-donus` | 196 → 308 | 0 → 2 |
| `kriz-aile-ici-siddet-anlatimi` | 206 → 309 | 0 → 2 |
| `kriz-gorusmede-ayrinti-zorlamama` | 185 → 291 | 0 → 2 |
| `kriz-guvenilir-yetiskin-destegi` | 182 → 294 | 0 → 1 |
| `kriz-guvenli-uzman-yonlendirme` | 188 → 291 | 0 → 1 |
| `kriz-guvenlik-planini-guncelleme` | 180 → 293 | 0 → 2 |
| `kriz-ihmal-suphesini-bildirme` | 190 → 292 | 0 → 2 |
| `kriz-istismar-suphesinde-yaklasim` | 203 → 301 | 0 → 2 |
| `kriz-izlem-ve-destek-devri` | 183 → 295 | 0 → 1 |
| `kriz-kaybedilen-yakin-sonrasi-okul` | 184 → 291 | 0 → 2 |
| `kriz-kendine-zarar-ifadesi` | 209 → 313 | 0 → 2 |
| `kriz-kriz-sonrasi-devamsizlik` | 177 → 284 | 0 → 1 |
| `kriz-kriz-sonrasi-sinif-rutini` | 189 → 305 | 0 → 1 |
| `kriz-krizde-ogrenci-mahremiyeti` | 182 → 286 | 0 → 2 |
| `kriz-krizde-ogretmen-koordinasyonu` | 181 → 287 | 0 → 1 |
| `kriz-krizde-veli-bilgilendirme` | 189 → 292 | 0 → 1 |
| `kriz-kurum-ici-acil-gorevler` | 181 → 285 | 0 → 1 |
| `kriz-ogrenciye-acil-yardim-yolu` | 173 → 282 | 0 → 1 |
| `kriz-okulda-zarar-verme-riski` | 186 → 292 | 0 → 1 |
| `kriz-risk-bildirimini-kaydetme` | 184 → 287 | 0 → 2 |
| `kriz-supheli-olayda-bilgi-guvenligi` | 174 → 287 | 0 → 2 |
| `kriz-tehdit-iceren-akran-davranisi` | 189 → 297 | 0 → 1 |
| `kriz-zorlayici-olay-sonrasi-sinif` | 195 → 301 | 0 → 2 |
| `kriz-zorlayici-olayda-soylenti` | 182 → 292 | 0 → 1 |
| `lgs-kaygi-grup-calismasi` | 135 → 274 | 0 → 1 |
| `nakille-gelen-ogrenci-uyumu` | 232 → 254 | 0 → 1 |
| `ogrenci-hedef-belirleme-gorusmesi` | 128 → 268 | 9 → 10 |
| `ogrenci-intihar-ifadesinde-acil-destek` | 267 → 409 | 0 → 2 |
| `ogrenci-risk-bildirimi-ilk-adim` | 153 → 302 | 0 → 1 |
| `ogretmen-zorbalik-gozlem-formu` | 134 → 274 | 9 → 11 |
| `ogretmenle-ogrenci-vaka-gorusmesi` | 130 → 272 | 1 → 2 |
| `okul-aidiyetini-gelistirme` | 138 → 281 | 1 → 2 |
| `okulda-ihmal-istismar-bildirimi` | 237 → 384 | 9 → 11 |
| `okulda-ihmal-suphesinde-ilk-adim` | 258 → 395 | 0 → 2 |
| `okulda-kriz-ilk-degerlendirme` | 242 → 389 | 9 → 10 |
| `okulda-kriz-sonrasi-rutin` | 162 → 307 | 9 → 10 |
| `okulda-kriz-sonrasi-sinif-bilgilendirmesi` | 245 → 375 | 0 → 1 |
| `okulda-yalnizlik-ogrenci-gorusmesi` | 219 → 285 | 1 → 2 |
| `ortaokul-akran-baskisi` | 138 → 277 | 2 → 3 |
| `oz-saygi-sinif-etkinligi` | 137 → 282 | 0 → 1 |
| `ozel-egitim-ailenin-gozlem-katkisi` | 288 → 269 | 0 → 1 |
| `ozel-egitim-aileyle-donemlik-hedef` | 288 → 278 | 0 → 1 |
| `ozel-egitim-akran-katiliminin-guvenligi` | 282 → 273 | 0 → 1 |
| `ozel-egitim-alternatif-katilim-yontemi` | 276 → 259 | 0 → 1 |
| `ozel-egitim-bep-degerlendirme-kaydi` | 286 → 269 | 0 → 1 |
| `ozel-egitim-bep-ekibi-gorev-dagilimi` | 299 → 277 | 0 → 1 |
| `ozel-egitim-bep-hedef-olcutu` | 288 → 267 | 0 → 1 |
| `ozel-egitim-bep-kazanim-izleme` | 282 → 272 | 0 → 1 |
| `ozel-egitim-bep-performans-gozlemi` | 278 → 266 | 0 → 1 |
| `ozel-egitim-bep-toplanti-gundemi` | 288 → 278 | 0 → 1 |
| `ozel-egitim-destek-egitim-koordinasyonu` | 282 → 283 | 0 → 1 |
| `ozel-egitim-duyusal-gereksinime-duyarlilik` | 286 → 270 | 0 → 1 |
| `ozel-egitim-egitimde-erisilebilir-materyal` | 282 → 262 | 0 → 1 |
| `ozel-egitim-farkli-yanit-verme-yollari` | 291 → 277 | 0 → 1 |
| `ozel-egitim-gecislerde-ongorulebilirlik` | 283 → 267 | 0 → 1 |
| `ozel-egitim-gorev-suresi-uyarlamasi` | 288 → 276 | 0 → 1 |
| `ozel-egitim-gorsel-yonerge-uyarlamasi` | 284 → 270 | 0 → 1 |
| `ozel-egitim-islevsel-iletisim-firsatlari` | 289 → 273 | 0 → 1 |
| `ozel-egitim-kapsayici-grup-etkinligi` | 290 → 276 | 0 → 1 |
| `ozel-egitim-kaynastirma-sinif-destegi` | 228 → 365 | 9 → 10 |
| `ozel-egitim-ogrencinin-guclu-yonleri` | 286 → 275 | 0 → 1 |
| `ozel-egitim-okul-ici-kurum-is-birligi` | 286 → 278 | 0 → 1 |
| `ozel-egitim-olumlu-davranis-destegi` | 278 → 271 | 0 → 1 |
| `ozel-egitim-ram-degerlendirmesi-sonrasi` | 288 → 281 | 0 → 1 |
| `ozel-egitim-sinif-ici-destek-duzeni` | 287 → 272 | 0 → 1 |
| `ozel-egitim-uyarlama-ise-yariyor-mu` | 281 → 271 | 0 → 1 |
| `ozel-egitim-veli-isbirligi` | 169 → 305 | 9 → 10 |
| `ram-yonlendirme-gorusmesi` | 132 → 271 | 0 → 1 |
| `rehberlik-faaliyet-raporu` | 142 → 286 | 9 → 11 |
| `rehberlik-servisine-basvuru` | 136 → 281 | 9 → 10 |
| `sinav-oz-bakim-plani` | 135 → 284 | 0 → 1 |
| `sinav-sonrasi-geri-bildirim` | 133 → 273 | 1 → 2 |
| `sinif-rehberlik-etkinligi-tasarimi` | 142 → 285 | 9 → 10 |
| `sosyal-duygusal-hedef-yazma` | 123 → 268 | 2 → 3 |
| `uyku-ve-ogrenme-ogrenci` | 141 → 284 | 9 → 10 |
| `veli-iletisim-etkinligi` | 131 → 268 | 9 → 10 |
| `veli-toplantisinda-gizlilik` | 126 → 271 | 0 → 2 |
| `yas-sonrasi-veli-iletisimi` | 139 → 284 | 0 → 2 |
| `yks-bolum-meslek-arastirmasi` | 139 → 288 | 0 → 2 |
| `zorbalik-veli-ilk-bilgilendirme` | 136 → 276 | 9 → 11 |

Her rehberin kaynak dosyası, bölüm/örnek kelime sayıları, sorunları ve birincil kaynak kimlikleri eşlik eden JSON raporunda bulunur.
