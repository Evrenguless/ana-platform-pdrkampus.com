# PDR Kampüs — 500 Rehber İlk Toplu İçerik Denetimi

Tarih: 12 Ekim 2026  
Dal: `feature/500-konu-icerik-sistemi`  
Kapsam: 500 rehberin veri paketleri ve mevcut üretim/denetim kodları. **Canlıya yayın onayı değildir.**

## Sayısal durum
- Kullanıcının başarılı yerel üretim çıktısı: **500 HTML rehber**, **1.766 kaynak kartı**, `structural_gate: passed`, `publication_approved: false`.
- 5 başlangıç rehberi + `data/pdr-editorial-batch-02.json` … `batch-22.json` dosyalarında 495 rehber.
- Veri paketleri 02–14: 295 rehber. Veri paketleri 15–22: 200 rehber.
- Son 200 rehberin **tamamında aynı beş bölüm başlığı** ve **aynı ikinci SSS cevabı** kullanılıyor.
- Son 200 rehberin tüm örnek olayları aynı `Öğrenci veya öğretmen okul ortamında …` kalıbıyla başlıyor.
- Son 200 rehberde **beş ana bölümün toplamı ortalama 79 kelime** (en az 72, en çok 87); gerçek bir kapsamlı rehber için yetersiz.
- Önceki paketlerin bölüm derinliği de sınırlı: paket 05 ortalama 38, 06 ortalama 35, 07 ortalama 26, 08 ortalama 29, 11 ortalama 27 kelime (beş bölüm toplamı).
- Paket 05–14 arası paketlerin her birinde aynı beş bölüm başlığından oluşan tek bir ortak başlık seti var (paket 02–04 konu bazında daha çeşitli).

## Öncelikli sorunlar
### P0 — Yayın öncesi içerik yetersizliği
- `structural_gate: passed` yalnızca HTML/SEO iskeletini kontrol ediyor; özgünlük ve uzmanlık değerlendirmiyor.
- Öncelik: 15–22 paketlerindeki **200 şablonlu sayfanın** konuya özgü açıklama, gerçekçi senaryo, karar adımları ve özgün SSS ile yeniden yazılması.
- Risk içeren rehberler (intihar ifadesi, ihmal/istismar, kriz, mahremiyet) ayrıca uzman ve güncel mevzuat kontrolünden geçmeli.

### P1 — Eski paketlerde yetersiz metin derinliği
| Paket | Rehber | Beş bölüm ortalama kelime |
|---|---:|---:|
| 02 | 10 | 73 |
| 03 | 14 | 65 |
| 04 | 21 | 40 |
| 05 | 20 | 38 |
| 06 | 30 | 35 |
| 07 | 25 | 26 |
| 08 | 25 | 29 |
| 09 | 25 | 68 |
| 10 | 25 | 72 |
| 11 | 25 | 27 |
| 12 | 25 | 73 |
| 13 | 25 | 73 |
| 14 | 25 | 73 |
| 15–22 | 200 | 79 |

Bu değerler yalnızca `sections` alanlarının kelime sayısıdır; örnek olay, kontrol listesi, SSS, kaynak kartları ve ortak sayfa şablonu dahil değildir.

### P1 — Kaynak kartları
- Yerel çıktı: toplam 1.766 kart, çok sayıda rehberde hiç kart yok.
- Mevcut kod gerçek `/kutuphane/` veya `/kaynak/` detay sayfasına yönlendirmeye çalışıyor. Bu, **konusal uygunluğu kanıtlamıyor**.
- Kaynak kartları sayfa başlığı/etiket aramasıyla otomatik öneriliyor; belge içeriği elle doğrulanmadı.
- Kaynak yoksa yanlış PDF linki eklemek yerine kütüphane araması korunmalı.

### P1 — SEO ve bilgi mimarisi
- Başlık/meta benzersizliği mevcut betiklerde temel düzeyde kontrol ediliyor.
- Benzer niyetli sayfalar arasındaki yamyamlaşma (`canonical`/birleştirme ihtiyacı) ayrıca kontrol edilmeli.
- İçerik yetersizliği çözümlenmeden 500 sayfayı indeksletmek önerilmez.

### P2 — Tarayıcı ve dış URL kontrolleri
- Mobil kırılımlar, görsel taşmalar, sayfa performansı henüz gerçek cihazda incelenmedi.
- Dış bağlantılar/uzak belgeler ve güncel resmî kaynaklar topluca doğrulanmadı.

## Önerilen düzeltme sırası
1. **Şablon kırma:** Paket 15–22 / 200 rehberde gerçek konu bazlı beş özgün bölüm, uygulanabilir örnek ve benzersiz SSS.
2. **Metin derinliği:** Paket 04–11'i okul PDR uygulamalarına özel somut ölçüt, görüşme örneği ve değerlendirme adımlarıyla genişletme.
3. **Riskli konular:** Ayrı etik/mevzuat/uzman kontrolü.
4. **Kaynak uygunluğu:** Eşleşmeleri başlığa göre değil kaynak belgesinin gerçek amacı ve seviyesine göre değerlendirme.
5. **SEO birleştirme haritası:** Aynı arama niyetine yanıt verenleri tespit, tek güçlü sayfa veya anlamlı alt rehber ayrımı.
6. **Mobil ve teknik:** Gerçek tarayıcıdan uçtan uca kontrol, ondan sonra kademeli canlı yayın.

## Sınırlar
Bu denetim ilk **veri ve kod temelli içerik taramasıdır**. Her kaynağın içeriği, tüm 500 HTML'in mobil sunumu, dış bağlantıların HTTP yanıtı ve uzman doğruluğu henüz değerlendirilmedi. Tüm değişiklikler taslak dalındadır; canlıya yayın yapılmadı.
