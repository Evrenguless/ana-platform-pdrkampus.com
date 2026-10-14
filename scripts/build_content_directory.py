#!/usr/bin/env python3
"""Expose every published canonical content page through ordinary HTML links."""
import argparse,html,json,re
from pathlib import Path
from collections import defaultdict
from sitemap_tools import read_urlset,render_sitemaps
from seo_engine import Page
from campus_tools import navigation, footer as campus_footer, switcher
ROOT=Path(__file__).resolve().parents[1];BASE='https://pdrkampus.com';SIZE=80
LABELS={'kaynaklar':'Kütüphane kaynakları','konular':'Rehberlik konuları','sayfalar':'Rehberler ve araçlar'}
E=html.escape

def build():
 template=(ROOT/'kutuphane/katalog/index.html').read_text()
 header=re.search(r'<header.*?</header>.*?</nav>',template,re.S).group()
 header=header.replace('<a href="https://analiz.pdrkampus.com/">AGS/PDR Puan Hesaplama</a><a href="https://norm.pdrkampus.com/">PDR Norm Analizi</a>',switcher('platform'),1)
 footer=re.search(r'<footer.*?</footer>',template,re.S).group()
 styles=''.join(re.findall(r'<link[^>]+rel="stylesheet"[^>]*>',template))
 groups=defaultdict(list)
 urls={n.text for n in read_urlset(ROOT).getroot().iter() if n.tag.endswith('loc') and n.text and not n.text.startswith(BASE+'/icerikler/')}
 for url in sorted(urls):
  if url.startswith(BASE+'/icerikler/'):continue
  rel=url.removeprefix(BASE+'/');file=ROOT/(rel+'index.html' if not rel or rel.endswith('/') else rel)
  page=Page(file.read_text())
  if page.noindex or page.canonicals!=[url]:continue
  group='kaynaklar' if rel.startswith(('kutuphane/','kaynak/','kaynak-detay/')) else 'konular' if rel.startswith('konu/') else 'sayfalar'
  groups[group].append((url,page.title,page.description))
 outputs={}
 def page(path,title,description,body,items):
  url=BASE+path
  schema={'@context':'https://schema.org','@graph':[{'@type':'CollectionPage','url':url,'name':title,'description':description,'inLanguage':'tr-TR'},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'PDR Kampüs','item':BASE+'/'},{'@type':'ListItem','position':2,'name':title,'item':url}]},{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':t,'url':u} for i,(u,t,_) in enumerate(items)]}]}
  outputs[path.lstrip('/')+'index.html']=f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | PDR Kampüs</title><meta name="description" content="{E(description,quote=True)}"><link rel="canonical" href="{url}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">'+styles+'<link rel="stylesheet" href="/assets/campus-tools.css?v=20261014-integrated"><script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script></head><body id="top">'+header+navigation('platform')+'<main class="catalog-shell"><p class="catalog-kicker"><a href="/">Ana sayfa</a> / <a href="/icerikler/">Kampüs içerikleri</a></p><h1>'+E(title)+'</h1><p class="catalog-lead">'+E(description)+'</p>'+body+'</main>'+campus_footer('platform')+footer+'<script src="/src/menu.js?v=20261013" defer></script></body></html>'
 cards=[]
 for group,label in LABELS.items():
  items=groups[group];chunks=[items[i:i+SIZE] for i in range(0,len(items),SIZE)]
  def route(i):return '/icerikler/'+group+'/' + (str(i)+'/' if i>1 else '')
  cards.append((BASE+route(1),label,str(len(items))+' yayımlanmış içerik'))
  for i,chunk in enumerate(chunks,1):
   description=f'{label}: yayımlanmış {len(items)} içerik arasından {i}. sayfadaki kaynakları incele. Başlıklara dokunarak özgün içerik sayfasına ulaş.'
   body='<div class="catalog-grid">'+''.join('<article class="catalog-card"><p class="catalog-kicker">'+E(label)+'</p><h2><a href="'+u.removeprefix(BASE)+'">'+E(t.removesuffix(' | PDR Kampüs'))+'</a></h2><p>'+E(d)+'</p><a href="'+u.removeprefix(BASE)+'">İçeriği incele →</a></article>' for u,t,d in chunk)+'</div>'
   body+='<nav class="catalog-pagination" aria-label="İçerik sayfaları">'+(' <a rel="prev" href="'+route(i-1)+'">← Önceki</a>' if i>1 else '')+f' <span>Sayfa {i} / {len(chunks)}</span> '+('<a rel="next" href="'+route(i+1)+'">Sonraki →</a>' if i<len(chunks) else '')+'</nav>'
   page(route(i),label+f' · Sayfa {i}',description,body,chunk)
 body='<div class="catalog-grid">'+''.join('<article class="catalog-card"><h2><a href="'+u.removeprefix(BASE)+'">'+E(t)+'</a></h2><p>'+E(d)+'</p><a href="'+u.removeprefix(BASE)+'">Listeyi aç →</a></article>' for u,t,d in cards)+'</div><section class="catalog-card"><h2>PDR Kampüs çalışma araçları</h2><p>Kütüphane kaynaklarından sonra sınav hazırlığı ve okul verileriyle ilgili çalışma alanlarına geçebilirsin.</p><p><a href="https://norm.pdrkampus.com/okullar/">Okul ve kurum kayıtları</a> · <a href="https://analiz.pdrkampus.com/pdr-oabt/">PDR ÖABT puan ve sıralama rehberleri</a> · <a href="https://cikmissorular.pdrkampus.com/yillar/">Yıllara göre çıkmış sorular</a></p></section>'
 page('/icerikler/','Kampüs içerikleri','Kütüphane kaynaklarını, rehberlik konularını ve araçları tüm yayımlanmış içerikler listesinde keşfet. Kaynaklar sayfalara ayrılmıştır; her başlık kendi özgün adresini açar.',body,cards)
 urls.update(BASE+'/'+key[:-10] for key in outputs)
 outputs.update(render_sitemaps(urls,BASE))
 return outputs

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();outputs=build()
 for key,s in outputs.items():
  p=ROOT/key
  if args.check:
   if not p.is_file() or p.read_text()!=s:raise SystemExit('Regenerate content directory: '+key)
  else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 print('Content directory:',sum(k.endswith('.html') for k in outputs),'pages')
if __name__=='__main__':main()
