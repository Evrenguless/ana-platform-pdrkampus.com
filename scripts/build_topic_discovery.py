"""One topic catalogue: existing centers and editorial guides share topic cards."""
import html
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=html.escape


def normalized(text):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFKD',text.casefold().replace('ı','i')) if not unicodedata.combining(c))


def card(row, group, editorial=False):
    marker=' data-editorial-card' if editorial else ''
    return ('<article class="topic-resource" data-topic-card'+marker+' data-guide-group="'+E(group,quote=True)+'">'
            '<div class="topic-resource-art" aria-hidden="true">'+row['icon']+'</div>'
            '<small>'+E(row['label'])+'</small><h3><strong>'+E(row['title'])+'</strong></h3>'
            '<p>'+E(row['description'])+'</p><a href="'+E(row['url'],quote=True)+'">Konuyu incele</a></article>')


def render(source, guides, grouping):
    centers=json.loads((ROOT/'data/topic-discovery-centers.json').read_text())
    by_url={r['url']:r for r in centers}
    # Reuse the actual illustrations in the existing topic cards, never covers.
    rules=[
        (('bep','ozel-egitim'),'/konu/ogrenciyi-tanima/'),
        (('sinav','sınav'),'/konu/sinav-kaygisi/'),
        (('zorbalik','zorbalık'),'/konu/akran-zorbaligi/'),
        (('kariyer','meslek','alan-sec','universite'),'/konu/kariyer-gelisimi/'),
        (('veli','aile'),'/konu/veli-gorusmesi/'),
        (('kriz','intihar','zarar','yas-ve','kayip','travma'),'/kriz/'),
        (('istismar','ihmal','koruma','mahremiyet','beden-guven'),'/cocuk-koruma/'),
        (('sosyometri','gozlem','tanima'),'/konu/sosyometri/'),
        (('motivasyon','erteleme','ogrenme','ders-cal'),'/konu/akademik-motivasyon/'),
        (('devamsiz','okul-reddi'),'/konu/devamsizlik/'),
        (('uyum','okula-bas','okula-yeni','okul-degis','yeni-ortam'),'/konu/okula-uyum/'),
        (('dijital','internet','ekran','teknoloji'),'/konu/dijital-denge/'),
        (('rehberlik','etik','randevu','kayit','evrak'),'/konu/rehberlik-hizmetleri/'),
        (('goruşme','gorusme','dinleme','danisma'),'/konu/bireysel-gorusme/'),
        (('sinif','duygu','empati','iletisim','arkadas','akran'),'/konu/sinif-rehberligi-etkinlikleri/')]
    buckets={r['url']:[] for r in centers};groups=set();center_groups={}
    for row in centers:
        group,_=grouping({'slug':row['url'].strip('/').split('/')[-1]})
        center_groups[row['url']]=group;groups.add(group)
    for guide in guides:
        group,_=grouping(guide);groups.add(group)
        route=next((route for terms,route in rules if any(t in normalized(guide['slug']) for t in terms)), '/konu/sinif-rehberligi-etkinlikleri/')
        center=by_url[route]
        row={'url':'/konu/'+guide['slug']+'/','title':guide['title'],'description':guide['summary'],'label':group,'icon':center['icon']}
        buckets[route].append(card(row,group,True))
    # Show related guide cards alongside the topic centers from the first page.
    cards=[];remaining=[]
    for center in centers:
        related=buckets[center['url']]
        cards.append(card(center,center_groups[center['url']]))
        cards.extend(related[:2]);remaining.extend(related[2:])
    cards.extend(remaining)
    if len(cards)!=len(centers)+len(guides):raise ValueError('Topic catalogue lost entries')
    options=''.join('<option value="'+E(g,quote=True)+'">'+E(g)+'</option>' for g in sorted(groups))
    section=('<section class="topic-content topic-discovery" id="topicCards" aria-labelledby="topic-discovery-title">'
       '<span id="uygulama-rehberleri" aria-hidden="true"></span><div class="topic-article">'
       '<h2 id="topic-discovery-title">Konuları keşfet</h2><p>Öğrenciyi tanımadan veli iletişimine, okul uyumundan kariyer gelişimine: konu merkezlerini ve uygulama rehberlerini birlikte keşfet.</p>'
       '<div class="editorial-controls" hidden><div class="library-discovery"><label for="guide-search">Konularda ara</label>'
       '<input id="guide-search" type="search" placeholder="Örneğin: BEP, sınav kaygısı, veli görüşmesi" aria-controls="editorial-results"></div>'
       '<div><label for="guide-group">Konu alanı</label><select id="guide-group" aria-controls="editorial-results"><option value="">Bütün alanlar</option>'+options+'</select></div></div>'
       '<p id="guide-count" role="status" aria-live="polite">'+str(len(cards))+' konu ve rehber</p>'
       '<div id="editorial-results" class="topic-section topic-index-grid">'+''.join(cards)+'</div>'
       '<p id="guide-empty" hidden>Bu aramayla eşleşen konu bulunamadı. Başka bir sözcük veya konu alanı deneyebilirsin.</p>'
       '<button id="guide-more" class="editorial-more" type="button" hidden>Daha fazla konu göster</button></div>'
       '<aside class="topic-sidebar"><div class="topic-card"><h3>Kütüphaneye geç</h3><p>Bir kavramın açıklamasından doğrudan ilgili form ve materyallere ulaş.</p><div class="topic-links"><a href="/kutuphane.html?q=sosyometri">Sosyometri kaynakları</a><a href="/kutuphane.html">Tüm kütüphane</a></div></div></aside></section>')
    source=re.sub(r'<section id="uygulama-rehberleri".*?</section>','',source,flags=re.S)
    source=source.replace('<!-- EDITORIAL-500-START -->','').replace('<!-- EDITORIAL-500-END -->','')
    source,n=re.subn(r'<section class="topic-content(?: topic-discovery)?" id="topicCards"[^>]*>.*?</section>',lambda m:section,source,count=1,flags=re.S)
    if n!=1:raise ValueError('Expected one existing topic catalogue')
    # Only the index assets need a new cache key; guide pages are unchanged.
    source=source.replace('/src/editorial-guides.js?v=20261014"','/src/editorial-guides.js?v=20261014-unified"')
    source=source.replace('/src/editorial-guides.css?v=20261014"','/src/editorial-guides.css?v=20261014-unified"')
    return source
