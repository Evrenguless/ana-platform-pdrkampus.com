# Kütüphane materyal eşleştirmesi — 14 Ekim 2026

212 rehbere mevcut kütüphanedeki 86 farklı materyal bağlandı; 400 yeni kart bağlantısı eklendi. İçerik metinleri değiştirilmedi. Çalışma yalnızca `feature/500-konu-icerik-sistemi` dalındadır; yayın onayı yoktur.

| Ölçüt | Önce | Sonra |
|---|---:|---:|
| Kütüphane materyali olmayan rehber | 229 | 17 |
| Kütüphane materyal kartı | 1766 | 2166 |
| Hiç kaynak kartı olmayan rehber | 137 | 12 |

Kütüphane materyali ve dış kurumun birincil başvuru bağlantısı ayrı sayılıyor. Bu nedenle 17 rehberde kütüphane materyali yokken bunların 5 tanesinde birincil kaynak kartı bulunuyor.

Başlık araması bazı ilgili belgeleri bulamıyordu. Yeni manifest belge kimliğini, başlığını, konusunu, kademesini ve kaynağını sabitliyor. Her rehber için kullanım amacı kayıtlı ve sayfada gösteriliyor. Kartlar ham dosyaya değil mevcut kütüphane detay sayfasına açılıyor; kapaklar mevcut katalog önizlemelerinden geliyor. Belge kimliği/kapsamı değişirse veya detay sayfası kaybolursa işlem hata veriyor.

Kütüphane kayıtlarının konu ve hedef kitle bilgileri eşleştirme dayanağıdır; bütün belgelerin tam metni bu turda uzman tarafından doğrulanmış sayılmaz. Önizleme ve kaynak inceleme açıklamaları korunur.

## Doğrulama

- 11 ilgili Python testi geçti (2 denetçi, 5 öncelikli içerik/kaynak, 4 kütüphane bağlantısı testi).
- 500 taslağın yapısal kontrolü ve yayın öncesi denetimi geçti; yayın kapısı false.
- 500 rehberin ana metin, örnek ve bölüm sayıları önceki commit ile birebir aynı.
- Yeni materyal almayan 288 rehberin toplam kart sayıları değişmedi.
- 212 rehberdeki kartlar mevcut yerel kütüphane detay sayfalarına gidiyor.
- Tarayıcıda örnek BEP kartı doğru MEB kılavuzuna ve görünür 102 sayfalık belge önizlemesine açıldı.

## Kalan 17 rehber

- `etik-ikilem-okul-psikolojik-danisma` — Mesleki etik ikilemi için belge içeriği uygunluğu henüz doğrulanmadı; öğrenci etik davranış materyali kullanılmadı.
- `kariyer-ogrenim-maliyetini-arastirma` — Güncel bütçe, burs ve barınma maliyeti için doğrudan uygun kütüphane materyali bulunamadı; birincil başvuru bağlantıları korunuyor.
- `kariyer-sehir-ve-ulasim-kosullari` — Şehir ve ulaşım koşulları için doğrudan uygun kütüphane materyali bulunamadı; birincil başvuru bağlantıları korunuyor.
- `kariyer-staj-ve-gonulluluk-firsatlari` — Staj/gönüllülük izin ve güvenlik koşullarını kapsayan doğrudan uygun kütüphane belgesi bulunamadı.
- `kariyer-universite-yasami-beklentileri` — Barınma, ulaşım ve üniversite yaşam hizmetleri için doğrudan uygun kütüphane belgesi bulunamadı; birincil başvuru bağlantıları korunuyor.
- `lise-gonullu-toplumsal-katki` — Katalogdaki doğrudan toplum hizmeti kılavuzunun kapsamı ortaokuldur; lise için doğrudan uygun belge seçilemedi.
- `lise-gunluk-yasam-ve-uyku-dengesi` — Katalogdaki okul öncesi uyku hikâyesi lise rehberine bağlanmadı.
- `lise-meslek-golgeleme-etkinligi` — Meslek gölgelemede izin/güvenlik ve gözlem kapsamına uygun doğrudan belge bulunamadı.
- `lise-okul-kulubunde-sorumluluk` — Doğrudan bulunan toplum hizmeti kılavuzu ortaokul kapsamındadır; lise kulüp usulleri için ayrı belge gerekir.
- `lise-staj-ve-gozlem-deneyimi` — Staj/gözlem izin ve güvenlik koşullarına uygun doğrudan belge bulunamadı.
- `okulda-ogrenci-oz-degerlendirme` — Projeye ilişkin öğrenci öz değerlendirme amacı için uygun doğrudan materyal seçilemedi; genel öğrenci tanıma formu bunun yerine kullanılmadı.
- `okulda-ogrenci-ozgecmisi` — Öğrenci özgeçmiş hazırlığına uygun doğrudan örnek veya kılavuz bulunamadı.
- `sinav-oz-bakim-plani` — Uyku, dinlenme ve öz bakım gereksinimini doğrudan ele alan uygun kademe belgesi bulunamadı.
- `sinav-uyku-ve-dinlenme-plani` — Yaşa uygun doğrudan uyku/dinlenme materyali bulunamadı; okul öncesi hikâye bağlanmadı.
- `sinifta-ozel-gunler-hassasiyet` — Farklı bakım verenler ve aile yapıları odağında doğrudan materyal seçilemedi; yas belgesi tek başına bu rehbere bağlanmadı.
- `veliyle-uyku-duzeni` — Katalogdaki doğrudan uyku materyali okul öncesi hikâyesidir; tüm kademelere uygun aile/uyku belgesi bulunamadı.
- `veliyle-yalan-soyleme` — Doğrudan ilgili aile bilgilendirme belgesi bulunamadı.

## Değişen dosyalar

- `.github/workflows/draft-500-quality-audit.yml`
- `data/pdr-editorial-library-links.json`
- `scripts/audit_500_publication_readiness.py`
- `scripts/build_first_editorial_batch.py`
- `scripts/test_editorial_library_links.py`
- `scripts/test_editorial_priority_guides.py`
- `seo/icerik-plani/500-rehber-yayin-oncesi-denetim.json`
- `seo/icerik-plani/ilk-50-kalite-raporu.json`
- `seo/icerik-plani/ilk-50-yayin-kapisi.json`
- `seo/icerik-plani/ilk-500-toplu-durum.json`
- `seo/icerik-plani/kutuphane-materyal-eslestirme-2026-10-14.json`
- `seo/icerik-plani/kutuphane-materyal-eslestirme-2026-10-14.md`

## Rehber bazında eklenen materyaller

| Rehber | Materyaller |
|---|---|
| `bep-ders-uyarlamasi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `bep-guclu-yonler` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `bep-hedef-izleme-toplantisi` | BEP Değerlendirme Raporu · 1. Dönem Sonu; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `bep-ogrenci-katilimi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `bep-olculebilir-hedef` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `cocuklarda-kisisel-sinirlar` | Sınır Koyma · Sınıf Rehberlik Tek Etkinlik Örnekleri · 2026-2027; Mahremiyet Eğitimi · Öğretmen Sunumu · 2026 |
| `devamsizlik-ogrenci-ilk-gorusme` | Devamsızlık Takip Formu · Düzenlenebilir Word; Devamsızlık Nedenleri Anketi ve Uygulama Yönergesi |
| `guclu-yon-kesfi-sinifta` | GÜÇLÜ YÖNLERİ BULMAYA YÖNELİK ANKET |
| `guvenli-internet-veliler-icin` | Aileler İçin Güvenli İnternet Rehberi · 2025; Bilinçli Teknoloji ve Güvenli İnternet Kullanımı · Veli Sunumu |
| `ilkokul-arkadas-anlasmazligi` | Sosyal Duygusal Beceriler – İlkokul Oyun Kitabı; Rehber Öğretmen/Psikolojik Danışman Sosyal Duygusal Beceri Kitapçığı |
| `kariyer-aile-meslek-beklentisi` | Mesleki Karar Verme Yetkinliği ve Ailelerin Meslek Gelişimine Desteği · Araştırma; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-bolum-ders-planini-okuma` | YÖK Atlas · Üniversite ve Tercih Referans Sistemi; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-bolum-tanitiminda-bilgi-dogrulama` | YÖK Atlas · Üniversite ve Tercih Referans Sistemi; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-coklu-ilgi-alani-olan-ogrenci` | Mesleki Değer ve Yeteneklerimiz · Öğrenci Kitapçığı; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-egitim-yolu-arastirma` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-gelecek-mesleklerini-arastirma` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-guclu-yon-ve-beceri-eslestirme` | Mesleki Değer ve Yeteneklerimiz · Öğrenci Kitapçığı; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-ilgi-envanteri-sonuclarini-konusma` | Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı; Kariyer Gelişimi ve Planlama Psikoeğitim Programı (KAGEP) |
| `kariyer-is-ortami-tercihleri` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-kariyer-kararinda-belirsizlik` | Kariyer Karar Verme Öz-Yeterliği, Gelecek Beklentisi ve Mesleki Sonuç Beklentisi · Araştırma Raporu · 2026; Karar Verme ve Eleştirel Düşünme · Öğrenci Bülteni |
| `kariyer-kariyer-plani-donemlik-izleme` | Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı; Kariyer Gelişimi ve Planlama Psikoeğitim Programı (KAGEP) |
| `kariyer-meslek-seciminde-akran-etkisi` | Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı; Kariyer Gelişimi ve Planlama Psikoeğitim Programı (KAGEP) |
| `kariyer-meslek-seciminde-tek-dogru-yanilgisi` | Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı; Kariyer Gelişimi ve Planlama Psikoeğitim Programı (KAGEP) |
| `kariyer-meslek-uzmanina-soru-hazirlama` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-mesleki-degerleri-karsilastirma` | Mesleki Değer ve Yeteneklerimiz · Öğrenci Kitapçığı; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-mesleki-karar-secenek-tablosu` | Kariyer Karar Verme Öz-Yeterliği, Gelecek Beklentisi ve Mesleki Sonuç Beklentisi · Araştırma Raporu · 2026; Karar Verme ve Eleştirel Düşünme · Öğrenci Bülteni |
| `kariyer-mesleklere-iliskin-onyargi` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-mesleklerin-gunluk-gorevleri` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-mezuniyet-sonrasi-alternatifler` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kariyer-resm-program-kosullari` | YÖK Atlas · Üniversite ve Tercih Referans Sistemi; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `kriz-acil-guvenlik-degerlendirmesi` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-afet-sonrasi-okula-donus` | Psikososyal Güçlendirici Destek Programı – Doğal Afet; Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası |
| `kriz-aile-ici-siddet-anlatimi` | Öğretmenler İçin Çocuk İstismarına Müdahale Rehberi; İhmal-İstismar Sürecinde Yasal Sorumluluklar · TCK ve ÇKK · 2026 |
| `kriz-gorusmede-ayrinti-zorlamama` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-guvenilir-yetiskin-destegi` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-guvenli-uzman-yonlendirme` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-guvenlik-planini-guncelleme` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-ihmal-suphesini-bildirme` | Öğretmenler İçin Çocuk İstismarına Müdahale Rehberi; İhmal-İstismar Sürecinde Yasal Sorumluluklar · TCK ve ÇKK · 2026 |
| `kriz-istismar-suphesinde-yaklasim` | Öğretmenler İçin Çocuk İstismarına Müdahale Rehberi; İhmal-İstismar Sürecinde Yasal Sorumluluklar · TCK ve ÇKK · 2026 |
| `kriz-izlem-ve-destek-devri` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-kaybedilen-yakin-sonrasi-okul` | Çocuk ve Ergenlerde Kayıp-Yas · Öğretmenler İçin Bilgilendirme Rehberi; Psikososyal Güçlendirici Destek Programı – Ölüm-Yas |
| `kriz-kendine-zarar-ifadesi` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-kriz-sonrasi-devamsizlik` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-kriz-sonrasi-sinif-rutini` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-krizde-ogrenci-mahremiyeti` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `kriz-krizde-ogretmen-koordinasyonu` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-krizde-veli-bilgilendirme` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-kurum-ici-acil-gorevler` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-ogrenciye-acil-yardim-yolu` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-okulda-zarar-verme-riski` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-risk-bildirimini-kaydetme` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-supheli-olayda-bilgi-guvenligi` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `kriz-tehdit-iceren-akran-davranisi` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-zorlayici-olay-sonrasi-sinif` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `kriz-zorlayici-olayda-soylenti` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `lgs-kaygi-grup-calismasi` | Sınav Kaygısı ile Baş Etme · Psikoeğitim Grubu Programı; Sınav Kaygısı · Öğrenci Bilgilendirme Kitapçığı |
| `lgs-son-hafta-ogrenci-destegi` | LGS Sınav Stratejileri; LGS Kaygı ve Motivasyon Rehberi |
| `lgs-sonrasi-okula-uyum` | Okula Uyum Süreci · Kılavuz · 2025; Okula Uyum · Öğretmen Broşürü · 2025 |
| `lgs-veli-tercih-bilgilendirme` | LGS Tercih Süreci · Öğrenci ve Veli Bilgilendirme Kılavuzu · 2026; LGS Tercih Dönemi Rehber Öğretmen/Psikolojik Danışman Eğitim Sunumu · 2026 |
| `lise-aile-kariyer-beklentisi` | Mesleki Karar Verme Yetkinliği ve Ailelerin Meslek Gelişimine Desteği · Araştırma; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `lise-akademik-ilgi-haritasi` | Mesleki Değer ve Yeteneklerimiz · Öğrenci Kitapçığı; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `lise-akranla-akademik-kiyaslama` | Sınav Kaygısı ile Baş Etme · Psikoeğitim Grubu Programı; Sınav Kaygısı · Öğrenci Bilgilendirme Kitapçığı |
| `lise-alan-secimini-degerlendirme` | YÖK Atlas · Üniversite ve Tercih Referans Sistemi; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `lise-bolum-karsilastirma-cizelgesi` | YÖK Atlas · Üniversite ve Tercih Referans Sistemi; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `lise-ders-programi-esnekligi` | YKS Verimli Ders Çalışma Rehberi; TYT-AYT Deneme Takip Çizelgesi ve Haftalık Planlayıcı |
| `lise-dijital-guvenlik-ve-mahremiyet` | Bilinçli Teknoloji ve Güvenli İnternet · Öğrenci Bilgilendirme Kitapçığı; Güvenli İnternet Kullanımı · Modüler Pano |
| `lise-etkili-deneme-geri-bildirimi` | TYT-AYT Deneme Takip Çizelgesi; Verimli Ders Çalışma Kontrol Listesi |
| `lise-farkli-goruslere-saygi` | Sosyal Duygusal Beceriler – Lise Öğretmen Sunumu; Sosyal Duygusal Beceriler – Lise Öğrenci Farkındalık Programı |
| `lise-gelecek-belirsizligiyle-bas-etme` | Kariyer Karar Verme Öz-Yeterliği, Gelecek Beklentisi ve Mesleki Sonuç Beklentisi · Araştırma Raporu · 2026; Karar Verme ve Eleştirel Düşünme · Öğrenci Bülteni |
| `lise-guvenilir-yetiskine-basvuru` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `lise-kendini-ifade-etme-becerisi` | İletişim Becerileri · Sunum; Sosyal Duygusal Beceriler – Lise Öğretmen Sunumu |
| `lise-mesleki-deger-kesfi` | Mesleki Değer ve Yeteneklerimiz · Öğrenci Kitapçığı; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `lise-mezuniyet-sonrasi-secenekler` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `lise-sinav-donemi-aile-iletisimi` | Sınav Döneminde Anne Baba Olmak; Sınav Kaygısı · Veli Bilgilendirme Kitapçığı |
| `lise-sinav-sonuclarini-yorumlama` | TYT-AYT Deneme Takip Çizelgesi; Verimli Ders Çalışma Kontrol Listesi |
| `lise-sosyal-iliskilerde-riza` | Sınır Koyma · Lise Öğretmen Broşürü; Sınır Koyma · Lise Öğrenci Sunumu |
| `lise-universite-arastirma-plani` | YÖK Atlas · Üniversite ve Tercih Referans Sistemi; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `lise-uzun-vadeli-hedef-bolme` | Hedef Belirleme · Ortaokul-Lise Broşürü; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `lise-yeni-ortama-gecis-hazirligi` | Okula Uyum Süreci · Kılavuz · 2025; Okula Uyum · Öğretmen Broşürü · 2025 |
| `mesleki-karar-yanilgilari` | Karar Verme ve Eleştirel Düşünme · Öğrenci Bülteni; Etkili Karar Verme İpuçları · Afiş |
| `nakille-gelen-ogrenci-uyumu` | Okula Uyum Süreci · Kılavuz · 2025; Okula Uyum · Öğretmen Broşürü · 2025 |
| `ogrenci-gorusmesinde-gizlilik` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `ogrenci-gorusmesinde-sessizlik` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `ogrenci-ile-gizlilik-siniri-anlatma` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `ogrenci-intihar-ifadesinde-acil-destek` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `ogrenci-risk-bildirimi-ilk-adim` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `ogrencide-karar-verme-etkinligi` | Karar Verme ve Eleştirel Düşünme · Öğrenci Bülteni; Etkili Karar Verme İpuçları · Afiş |
| `ogrencide-sosyal-sorumluluk` | Okul Öğrenci Kulüpleri Sosyal Sorumluluk Ve Toplum Hizmeti Çalışmaları Uygulama Projesi Kılavuzu |
| `ogrencilerde-dijital-iz-farkindaligi` | Bilinçli Teknoloji ve Güvenli İnternet · Öğrenci Bilgilendirme Kitapçığı; Güvenli İnternet Kullanımı · Modüler Pano |
| `ogrencilerde-gelecek-kaygisi` | Kariyer Karar Verme Öz-Yeterliği, Gelecek Beklentisi ve Mesleki Sonuç Beklentisi · Araştırma Raporu · 2026; Karar Verme ve Eleştirel Düşünme · Öğrenci Bülteni |
| `ogrencilerde-zaman-yonetimi` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `ogrenciye-yapici-geri-bildirim` | İletişim Becerileri · Öğretmen Bilgilendirme Kitapçığı |
| `okulda-aile-ici-catismayi-bildiren-ogrenci` | Öğretmenler İçin Çocuk İstismarına Müdahale Rehberi; İhmal-İstismar Sürecinde Yasal Sorumluluklar · TCK ve ÇKK · 2026 |
| `okulda-bep-aile-katilimi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `okulda-donem-sonu-rehberlik-degerlendirme` | Rehberlik Faaliyet Değerlendirme Formu · Düzenlenebilir Word; Özel Eğitim ve Rehberlik Hizmetleri Uygulama Rehberi · 2026 |
| `okulda-duygu-termometresi` | Rehber Öğretmen/Psikolojik Danışman Sosyal Duygusal Beceri Kitapçığı |
| `okulda-gizli-bilgi-paylasimi` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `okulda-guvenilir-yetiskin-haritasi` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `okulda-guvenli-basvuru-yollari` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `okulda-ihmal-suphesinde-ilk-adim` | Öğretmenler İçin Çocuk İstismarına Müdahale Rehberi; İhmal-İstismar Sürecinde Yasal Sorumluluklar · TCK ve ÇKK · 2026 |
| `okulda-kariyer-farkindaligi` | Önlisans Meslek Tanıtımları · 2024-2025; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `okulda-kriz-sonrasi-sinif-bilgilendirmesi` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `okulda-motivasyon-dalgalanmasi` | Hedef Belirleme ve Motivasyon · Öğretmen Broşürü · 2026-2027; Motivasyon ve Verimli Ders Çalışma Teknikleri · Sunum |
| `okulda-ogrenci-davranis-hedefi` | Zaman Yönetimi · Hedefler Çalışma Kağıdı; Hedef Belirleme ve Motivasyon · Öğretmen Broşürü · 2026-2027 |
| `okulda-ogrenci-guvenligi-gozlem-notu` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `okulda-ogrenci-katilim-hakki` | Çocuk Katılımı El Kitabı · UNICEF 2026 |
| `okulda-ogrenci-motivasyon-gorusmesi` | Hedef Belirleme ve Motivasyon · Öğretmen Broşürü · 2026-2027; Motivasyon ve Verimli Ders Çalışma Teknikleri · Sunum |
| `okulda-oz-yeterlik` | Özgüven Geliştirme · Öğretmen Broşürü · 2026-2027 |
| `okulda-psikososyal-destek-basvurusu` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `okulda-sosyal-kaygi-gozlemi` | Sosyal Kaygı · Eğitim ve Kültür Dergisi İçeriği |
| `okulda-veli-ogretmen-iletisim-plani` | İletişim Becerileri · Öğretmen Bilgilendirme Kitapçığı |
| `ortaokulda-duygulari-ifade-etme` | Sosyal Duygusal Beceriler – Ortaokul Öğretmen Sunumu; Sosyal Duygusal Beceriler – Ortaokul Öğrenci Farkındalık Programı |
| `ortaokulda-guvenli-arkadas-secimi` | Sosyal Duygusal Beceriler – Ortaokul Öğretmen Sunumu; Sosyal Duygusal Beceriler – Ortaokul Öğrenci Farkındalık Programı |
| `oz-saygi-sinif-etkinligi` | Özgüven Geliştirme · Öğretmen Broşürü · 2026-2027 |
| `ozel-egitim-ailenin-gozlem-katkisi` | Eğitsel Performans ve BEP · Düzenlenebilir Form; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-aileyle-donemlik-hedef` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-akran-katiliminin-guvenligi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-alternatif-katilim-yontemi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-bep-degerlendirme-kaydi` | BEP Değerlendirme Raporu · 1. Dönem Sonu; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-bep-ekibi-gorev-dagilimi` | BEP Geliştirme Birimi · 1. Toplantı Tutanağı; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-bep-hedef-olcutu` | BEP Değerlendirme Raporu · 1. Dönem Sonu; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-bep-kazanim-izleme` | BEP Değerlendirme Raporu · 1. Dönem Sonu; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-bep-performans-gozlemi` | Eğitsel Performans ve BEP · Düzenlenebilir Form; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-bep-toplanti-gundemi` | BEP Geliştirme Birimi · 1. Toplantı Tutanağı; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-destek-egitim-koordinasyonu` | BEP Geliştirme Birimi · 1. Toplantı Tutanağı; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-duyusal-gereksinime-duyarlilik` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-egitimde-erisilebilir-materyal` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-farkli-yanit-verme-yollari` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-gecislerde-ongorulebilirlik` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-gorev-suresi-uyarlamasi` | Eğitsel Performans ve BEP · Düzenlenebilir Form; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-gorsel-yonerge-uyarlamasi` | Eğitsel Performans ve BEP · Düzenlenebilir Form; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-islevsel-iletisim-firsatlari` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-kapsayici-grup-etkinligi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-ogrencinin-guclu-yonleri` | Eğitsel Performans ve BEP · Düzenlenebilir Form; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-okul-ici-kurum-is-birligi` | BEP Geliştirme Birimi · 1. Toplantı Tutanağı; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ozel-egitim-olumlu-davranis-destegi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-ram-degerlendirmesi-sonrasi` | Eğitsel Değerlendirme ve Tanılama Süreci · Broşür; Özel Eğitim ve Rehberlik Hizmetleri Uygulama Rehberi · 2026 |
| `ozel-egitim-sinif-ici-destek-duzeni` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `ozel-egitim-uyarlama-ise-yariyor-mu` | Eğitsel Performans ve BEP · Düzenlenebilir Form; Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası |
| `ram-basvuru-sureci-bilgilendirmesi` | Eğitsel Değerlendirme ve Tanılama Süreci · Broşür; Özel Eğitim ve Rehberlik Hizmetleri Uygulama Rehberi · 2026 |
| `ram-raporu-okuma-rehberi` | Eğitsel Değerlendirme ve Tanılama Süreci · Broşür; Özel Eğitim ve Rehberlik Hizmetleri Uygulama Rehberi · 2026 |
| `ram-sonrasi-okul-destegi` | Eğitsel Değerlendirme ve Tanılama Süreci · Broşür; Özel Eğitim ve Rehberlik Hizmetleri Uygulama Rehberi · 2026 |
| `ram-yonlendirme-gorusmesi` | Eğitsel Değerlendirme ve Tanılama Süreci · Broşür; Özel Eğitim ve Rehberlik Hizmetleri Uygulama Rehberi · 2026 |
| `ram-yonlendirme-oncesi-ogretmen-gozlemi` | Eğitsel Değerlendirme ve Tanılama Süreci · Broşür; Özel Eğitim ve Rehberlik Hizmetleri Uygulama Rehberi · 2026 |
| `rehberlikte-grup-calismasi-gonulluluk` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `rehberlikte-kayit-guvenligi` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `saglikli-sinav-hedefleri` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-aile-deneme-sonucu-iletisimi` | Sınav Döneminde Anne Baba Olmak; Sınav Kaygısı · Veli Bilgilendirme Kitapçığı |
| `sinav-deneme-analizi-gorusmesi` | TYT-AYT Deneme Takip Çizelgesi; Verimli Ders Çalışma Kontrol Listesi |
| `sinav-dusuk-puan-sonrasi-destek` | Sınav Kaygısı ile Baş Etme · Psikoeğitim Grubu Programı; Sınav Kaygısı · Öğrenci Bilgilendirme Kitapçığı |
| `sinav-gercekci-net-hedefi` | Hedef Belirleme · Ortaokul-Lise Broşürü; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-hazirliginda-gercekci-program` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-kiyaslama-dilini-azaltma` | Sınav Döneminde Anne Baba Olmak; Sınav Kaygısı · Veli Bilgilendirme Kitapçığı |
| `sinav-konu-eksiklerini-belirleme` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-kucuk-calisma-oturumlari` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-lgs-yerlestirme-bilgisi` | LGS Tercih Süreci · Öğrenci ve Veli Bilgilendirme Kılavuzu · 2026; LGS Tercih Dönemi Rehber Öğretmen/Psikolojik Danışman Eğitim Sunumu · 2026 |
| `sinav-ogrenme-stratejisi-secme` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-okul-ve-kurs-yuk-dengesi` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-program-kosulu-inceleme` | YKS Tercih Süreci · Öğrenci ve Veli Bilgilendirme Kılavuzu · 2026; YÖK Atlas · Üniversite ve Tercih Referans Sistemi |
| `sinav-sinav-gunu-hazirligi` | Sınav Stratejileri · Öğrenci Broşürü |
| `sinav-sinav-kaygisi-erken-belirtiler` | Sınav Kaygısı ile Baş Etme · Psikoeğitim Grubu Programı; Sınav Kaygısı · Öğrenci Bilgilendirme Kitapçığı |
| `sinav-sinav-oncesi-kaygi-dusunceleri` | Sınav Kaygısı ile Baş Etme · Psikoeğitim Grubu Programı; Sınav Kaygısı · Öğrenci Bilgilendirme Kitapçığı |
| `sinav-sinav-sonrasi-belirsizlik` | Sınav Kaygısı ile Baş Etme · Psikoeğitim Grubu Programı; Sınav Kaygısı · Öğrenci Bilgilendirme Kitapçığı |
| `sinav-sinav-sonucunu-aileye-aciklama` | Sınav Döneminde Anne Baba Olmak; Sınav Kaygısı · Veli Bilgilendirme Kitapçığı |
| `sinav-sinavda-yardim-isteme` | 2026 YKS · Sınav Kılavuzu; LGS 2026 · Merkezî Sınav Başvuru ve Uygulama Kılavuzu |
| `sinav-tekrara-baslama-stratejisi` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-tercih-bilgi-kaynagi` | YKS Tercih Süreci · Öğrenci ve Veli Bilgilendirme Kılavuzu · 2026; YÖK Atlas · Üniversite ve Tercih Referans Sistemi |
| `sinav-yanlis-sorulari-siniflandirma` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-yeni-doneme-gecis-hedefi` | Hedef Belirleme · Ortaokul-Lise Broşürü; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinav-yks-tercih-sirasi-degerlendirme` | YKS Tercih Süreci · Öğrenci ve Veli Bilgilendirme Kılavuzu · 2026; YÖK Atlas · Üniversite ve Tercih Referans Sistemi |
| `sinav-yuksek-beklenti-baskisi` | Sınav Döneminde Anne Baba Olmak; Sınav Kaygısı · Veli Bilgilendirme Kitapçığı |
| `sinav-zaman-baskisini-yonetme` | Verimli Ders Çalışma Kontrol Listesi; Zaman Yönetimi · Hedefler Çalışma Kağıdı |
| `sinif-iklimi-anketi` | Sosyal Kabulü ve Olumlu Sınıf İklimini Sağlama · Öğretmen Rehber Kitabı |
| `sinifta-akran-destegi-planlama` | Rehber Öğretmen/Psikolojik Danışman Sosyal Duygusal Beceri Kitapçığı |
| `sinifta-aktif-dinleme-oyunu` | Empati ve Etkili Dinleme Sunusu; İletişim Becerileri · Öğretmen Bilgilendirme Kitapçığı |
| `sinifta-guvenli-sosyal-medya` | Bilinçli Teknoloji ve Güvenli İnternet · Öğretmen Etkinlik Örnekleri; Bilinçli Teknoloji ve Güvenli İnternet · Öğrenci Bilgilendirme Kitapçığı |
| `sinifta-yardim-isteyen-ogrenci` | Okul Temelli Psikososyal Koruma, Önleme ve Krize Müdahalede Bir Yol Haritası; Psikososyal Destek Programı Uygulama Kılavuzu |
| `uzun-devamsizlik-sonrasi-donus` | Devamsızlık Takip Formu · Düzenlenebilir Word; Devamsızlık Nedenleri Anketi ve Uygulama Yönergesi |
| `veli-gorusmesinde-ogrencinin-sesi` | Çocuk Katılımı El Kitabı · UNICEF 2026 |
| `veli-ile-ekran-suresi-catismasi` | Aileler İçin Güvenli İnternet Rehberi · 2025; Bilinçli Teknoloji ve Güvenli İnternet Kullanımı · Veli Sunumu |
| `veli-toplantisinda-gizlilik` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `veli-toplantisinda-zor-sorular` | Aile İçi İletişim ve Anne-Baba Tutumları · Veli Bilgilendirme Kitapçığı; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-akran-dislama` | Akran Zorbalığı · Psikolojik Danışman Kitapçığı; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-arkadas-secimi` | Akran Zorbalığı · Psikolojik Danışman Kitapçığı; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-cocuk-guclu-yonleri` | Aile İçi İletişim ve Anne-Baba Tutumları · Veli Bilgilendirme Kitapçığı; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-ders-basarisizligi` | Verimli Ders Çalışma Teknikleri · Veli Sunumu · 2025; Verimli Ders Çalışma Kontrol Listesi |
| `veliyle-ergen-mahremiyeti` | Ergen Çocuğunuzla İletişim Kurmanın Yolları · Veli Sunumu; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-erteleme-gorusmesi` | Verimli Ders Çalışma Teknikleri · Veli Sunumu · 2025; Verimli Ders Çalışma Kontrol Listesi |
| `veliyle-kardes-kiskancligi` | Kardeş Kıskançlığına Karşı Aileler İçin Öneriler · 2025 |
| `veliyle-lise-gecis-kaygisi` | Okula Uyum · Veli Broşürü · 2025; Okula Uyum Süreci · Kılavuz · 2025 |
| `veliyle-odev-yardim-siniri` | Aile İçi İletişim ve Anne-Baba Tutumları · Veli Bilgilendirme Kitapçığı; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-ogretmen-sikayeti` | Aile İçi İletişim ve Anne-Baba Tutumları · Veli Bilgilendirme Kitapçığı; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-okul-korkusu` | Okula Uyum · Veli Broşürü · 2025; Okula Uyum Süreci · Kılavuz · 2025 |
| `veliyle-okul-nakli` | Okula Uyum · Veli Broşürü · 2025; Okula Uyum Süreci · Kılavuz · 2025 |
| `veliyle-okula-gec-kalma` | Okula Uyum · Veli Broşürü · 2025; Okula Uyum Süreci · Kılavuz · 2025 |
| `veliyle-oyun-kurallari` | Sosyal Duygusal Beceriler – İlkokul Veli Broşürü; Sosyal Duygusal Beceriler – İlkokul Oyun Kitabı |
| `veliyle-ozel-egitim-isbirligi` | Bireyselleştirilmiş Eğitim Programı · Tüm Öğretmenler İçin Yol Haritası; BEP Örnek Formatı · Word |
| `veliyle-ozgurluk-sinirlar` | Ergen Çocuğunuzla İletişim Kurmanın Yolları · Veli Sunumu; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
| `veliyle-rehberlik-gizlilik` | RAM Rehberlik Hizmetleri Kılavuzu · Bireysel Görüşme Süreci |
| `veliyle-siber-zorbalik` | Aileler İçin Güvenli İnternet Rehberi · 2025; Bilinçli Teknoloji ve Güvenli İnternet Kullanımı · Veli Sunumu |
| `veliyle-sinav-karsilastirmasi` | Sınav Döneminde Anne Baba Olmak; Sınav Kaygısı · Veli Bilgilendirme Kitapçığı |
| `veliyle-sinif-degisimi` | Okula Uyum · Veli Broşürü · 2025; Okula Uyum Süreci · Kılavuz · 2025 |
| `veliyle-sorumluluk-paylasimi` | Hak ve Sorumluluk Gelişimi · Veli Kitapçığı; Sorumluluk Bilinci · Veli Bülteni · Kasım 2025 |
| `veliyle-sosyal-duygusal-destek` | Sosyal Duygusal Beceriler – Ortaokul Veli Broşürü; Sosyal Duygusal Beceriler – Lise Veli Broşürü |
| `veliyle-teknoloji-bagimlilik-endisesi` | Aileler İçin Güvenli İnternet Rehberi · 2025; Bilinçli Teknoloji ve Güvenli İnternet Kullanımı · Veli Sunumu |
| `yas-sonrasi-veli-iletisimi` | Çocuk ve Ergenlerde Kayıp-Yas · Aileler İçin Bilgilendirme Rehberi; Çocuk ve Ergenlerde Kayıp-Yas · Öğretmenler İçin Bilgilendirme Rehberi |
| `yas-yasayan-ogrenciye-okul-destegi` | Çocuk ve Ergenlerde Kayıp-Yas · Öğretmenler İçin Bilgilendirme Rehberi; Psikososyal Güçlendirici Destek Programı – Ölüm-Yas |
| `yks-bolum-meslek-arastirmasi` | YÖK Atlas · Üniversite ve Tercih Referans Sistemi; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `yks-deneme-analizi-rehberi` | TYT-AYT Deneme Takip Çizelgesi; Verimli Ders Çalışma Kontrol Listesi |
| `yks-tercih-karar-tablosu` | YKS Tercih Süreci · Öğrenci ve Veli Bilgilendirme Kılavuzu · 2026; YÖK Atlas · Üniversite ve Tercih Referans Sistemi |
| `yks-tercihinde-aile-baskisi` | Mesleki Karar Verme Yetkinliği ve Ailelerin Meslek Gelişimine Desteği · Araştırma; Okulda Bireysel Kariyer Psikolojik Danışmanlığı El Kitabı |
| `zor-veli-gorusmesi` | Aile İçi İletişim ve Anne-Baba Tutumları · Veli Bilgilendirme Kitapçığı; Aile İçi İletişim, Çocuk Hakları ve Çocuk Kıymeti · Veli Broşürü |
