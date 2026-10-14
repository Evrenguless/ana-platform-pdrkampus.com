#!/usr/bin/env python3
"""Build the user-authorized 500-guide release; --check verifies public outputs.

Source identity checks remain distinct from specialist review. Existing live
routes outside this package are never overwritten. Drafts stay noindex.
"""
import argparse
import contextlib
import hashlib
import html
import io
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
import build_first_editorial_batch as builder
from seo_engine import Page, runtime_digest
from sitemap_tools import TAG, read_urlset, eligible_outputs

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://pdrkampus.com'
START = '<!-- EDITORIAL-500-START -->'
END = '<!-- EDITORIAL-500-END -->'
E = html.escape


def shared_card(url, title, description, category, visual=None, action='Rehberi aç'):
    cover = visual or '<span class="resource-format-tile">REHBER<small>'+E(category)+'</small></span>'
    return ('<article class="document-card library-document resource-card surface-card" data-editorial-card>'
            '<a class="resource-card-cover" href="'+E(url, quote=True)+'" aria-label="'+E(title+' — '+action, quote=True)+'">'+cover+'</a>'
            '<div class="resource-content"><div class="document-card-meta"><span>'+E(category)+'</span><span>Uygulama rehberi</span></div>'
            '<h3><a href="'+E(url, quote=True)+'">'+E(title)+'</a></h3><p class="library-source">PDR Kampüs</p>'
            '<p class="resource-detail">'+E(description)+'</p></div><div class="resource-actions"><a href="'+E(url, quote=True)+'">'+E(action)+' →</a></div></article>')


def library_card(match):
    url, body = match.groups()
    title = re.search(r'<strong>(.*?)</strong>', body, re.S).group(1)
    meta = re.search(r'<span class="guide2-meta">(.*?)</span>', body, re.S).group(1)
    small = re.findall(r'<small>(.*?)</small>', body, re.S)
    image = re.search(r'<img\b[^>]*>', body)
    cover = image.group() if image else '<span class="resource-format-tile">KAYNAK<small>'+meta+'</small></span>'
    return ('<article class="document-card library-document resource-card surface-card">'
            '<a class="resource-card-cover" href="'+url+'" aria-label="'+E(html.unescape(title)+' kaynağını aç', quote=True)+'">'+cover+'</a>'
            '<div class="resource-content"><div class="document-card-meta"><span>'+meta+'</span></div>'
            '<h3><a href="'+url+'">'+title+'</a></h3>'+''.join('<p class="library-source">'+s+'</p>' for s in small)+
            '</div><div class="resource-actions"><a href="'+url+'">Kaynağı incele →</a></div></article>')


def production_page(source, guide):
    url = BASE+'/konu/'+guide['slug']+'/'
    source = re.sub(r'<meta\s+name="robots"[^>]*>', '', source, flags=re.I)
    source = re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', source, flags=re.S|re.I)
    source = re.sub(r'<meta\s+name="twitter:[^"]+"[^>]*>', '', source, flags=re.I)
    source = source.replace('Bu sayfa PDR Kampüs editoryal taslağıdır.', 'Bu sayfa PDR Kampüs eğitim ve uygulama rehberidir.')
    source = re.sub(r'<a class="guide2-card" href="([^"]+)"\s*>(.*?)</a>', library_card, source, flags=re.S)
    source = source.replace('class="guide2-grid"', 'class="library-results"')
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'WebPage','@id':url+'#page','url':url,'name':guide['title'],'description':guide['summary'],'inLanguage':'tr'},
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'PDR Kampüs','item':BASE+'/'},
            {'@type':'ListItem','position':2,'name':'Konular','item':BASE+'/konular.html'},
            {'@type':'ListItem','position':3,'name':guide['title'],'item':url}]}]}
    additions = ('<link rel="stylesheet" href="/src/resource-catalog.css"><link rel="stylesheet" href="/src/resource-design.css">'
                 '<link rel="stylesheet" href="/src/visual-refresh.css"><link rel="stylesheet" href="/src/editorial-guides.css?v=20261014">'
                 '<meta name="twitter:card" content="summary"><meta name="twitter:title" content="'+E(guide['title'],quote=True)+'"><meta name="twitter:description" content="'+E(guide['summary'],quote=True)+'">'
                 '<meta property="og:url" content="'+url+'"><meta property="og:title" content="'+E(guide['title'],quote=True)+'">'
                 '<meta property="og:description" content="'+E(guide['summary'],quote=True)+'">'
                 '<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>')
    source = source.replace('</head>', additions+'</head>',1)
    source = source.replace('<body', '<body data-resource-design="editorial"',1)
    page = Page(source)
    if page.noindex or page.canonicals != [url] or len(page.primary_h1) != 1 or not page.title or not page.description:
        raise ValueError('Invalid public metadata: '+guide['slug'])
    if 'guide2-card"' in source or 'editoryal taslağıdır' in source:
        raise ValueError('Draft presentation survived: '+guide['slug'])
    return source


def grouping(guide):
    slug = guide['slug']
    for prefix, label, cat in [
        ('bep-', 'Özel eğitim ve BEP','cat-guidance'), ('ozel-egitim-', 'Özel eğitim ve BEP','cat-guidance'),
        ('kriz-', 'Kriz ve güvenlik','cat-risk-safety'), ('zorbalik-', 'Akran zorbalığı','cat-risk-safety'),
        ('sinav-', 'Sınav rehberliği','cat-academic'), ('kariyer-', 'Kariyer ve mesleki rehberlik','cat-career'),
        ('veliyle-', 'Aile ve veli çalışmaları','cat-family'), ('veli-', 'Aile ve veli çalışmaları','cat-family'),
        ('ilkokul-', 'İlkokul','cat-guidance'), ('ortaokul-', 'Ortaokul','cat-guidance'), ('lise-', 'Lise','cat-guidance'),
        ('sinifta-', 'Sınıf rehberliği','cat-guidance'), ('rehberlik-', 'Rehberlik servisi','cat-guidance')]:
        if slug.startswith(prefix): return label, cat
    return 'Okul PDR uygulamaları', 'cat-guidance'


def build():
    # Generate and validate source manifests against the current main catalogue.
    if len(builder.GUIDES) != 5:
        raise ValueError('Run publisher in a fresh process')
    with contextlib.redirect_stdout(io.StringIO()): builder.main()
    guides = builder.GUIDES
    if len(guides) != 500 or len({g['slug'] for g in guides}) != 500:
        raise ValueError('Expected exactly 500 distinct manuscripts')
    topics = json.loads((ROOT/'data/topics.json').read_text())
    slugs = {g['slug'] for g in guides}
    old_rows = [t for t in topics['topics'] if t['slug'] not in slugs]
    existing_rows = {t['slug']:t for t in topics['topics'] if t['slug'] in slugs}
    if any(t.get('editorialCollection') != 'editorial-500' for t in existing_rows.values()):
        raise ValueError('Existing topic dictionary collision')
    outputs = {}; cards = []; groups = set()
    for guide in guides:
        slug = guide['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug): raise ValueError('Unsafe slug')
        key = 'konu/'+slug+'/index.html'
        if (ROOT/key).exists() and slug not in existing_rows:
            raise ValueError('Existing public route collision: '+key)
        outputs[key] = production_page((builder.OUTPUT/(slug+'.html')).read_text(),guide)
        label, cat = grouping(guide); groups.add(label)
        card = shared_card('/konu/'+slug+'/',guide['title'],guide['summary'],label)
        cards.append(card.replace('data-editorial-card', 'data-editorial-card data-guide-group="'+E(label,quote=True)+'"',1))
        old_rows.append({'id':'topic_'+slug.replace('-','_'),'slug':slug,'name':guide['title'],
            'categoryId':cat,'aliases':[],'useCases':['Okul PDR uygulaması'], 'indexable':True,
            'contentStatus':'published','canonicalPath':'/konu/'+slug+'/','editorialCollection':'editorial-500',
            'seo':{'title':guide['title']+' | PDR Kampüs','description':guide['summary'],'primaryQuery':guide['title']},
            'relatedTopics':[]})
    topics['topics'] = old_rows; topics['updatedAt']='2026-10-14'
    outputs['data/topics.json'] = json.dumps(topics,ensure_ascii=False,indent=2)+'\n'
    options = ''.join('<option value="'+E(g,quote=True)+'">'+E(g)+'</option>' for g in sorted(groups))
    listing = (START+'\n<section id="uygulama-rehberleri" class="editorial-guides" data-resource-design="editorial" aria-labelledby="editorial-title">'
       '<h2 id="editorial-title">500 uygulama rehberi</h2><p>Okulda karşılaştığın konuya göre rehberleri ara; uygulama adımlarını, örnekleri ve ilgili kaynakları incele.</p>'
       '<div class="editorial-controls" hidden><div class="library-discovery"><label for="guide-search">Rehberlerde ara</label>'
       '<input id="guide-search" type="search" placeholder="Örneğin: BEP, sınav kaygısı, veli görüşmesi" aria-controls="editorial-results"></div>'
       '<div><label for="guide-group">Konu alanı</label><select id="guide-group" aria-controls="editorial-results"><option value="">Bütün alanlar</option>'+options+'</select></div></div>'
       '<p id="guide-count" role="status" aria-live="polite">500 rehber</p><div id="editorial-results" class="library-results">'+''.join(cards)+'</div>'
       '<p id="guide-empty" hidden>Bu aramayla eşleşen rehber bulunamadı. Başka bir sözcük veya konu alanı deneyebilirsin.</p>'
       '<button id="guide-more" class="editorial-more" type="button" hidden>Daha fazla rehber göster</button></section>\n'+END)
    source = (ROOT/'konular.html').read_text()
    if START in source:
        source = source[:source.index(START)]+listing+source[source.index(END)+len(END):]
    else:
        source = source.replace('<nav class="topic-discovery-nav"', listing+'\n<nav class="topic-discovery-nav"',1)
        source = source.replace('</head>','<link rel="stylesheet" href="/src/resource-catalog.css"><link rel="stylesheet" href="/src/resource-design.css"><link rel="stylesheet" href="/src/visual-refresh.css"><link rel="stylesheet" href="/src/editorial-guides.css?v=20261014"><script src="/src/editorial-guides.js?v=20261014" defer></script></head>',1)
    outputs['konular.html'] = source
    tree = read_urlset(ROOT).getroot()
    for guide in guides:
        node = ET.SubElement(tree,TAG+'url'); ET.SubElement(node,TAG+'loc').text = BASE+'/konu/'+guide['slug']+'/'
    maps, excluded = eligible_outputs(ROOT,tree,outputs)
    added = {BASE+'/konu/'+g['slug']+'/' for g in guides}
    lost = added & set(excluded)
    if lost: raise ValueError('New guides rejected by sitemap: '+str({u:excluded[u] for u in lost}))
    old = {n.text for n in read_urlset(ROOT).getroot().iter(TAG+'loc')}
    included = {n.text for content in maps.values() for n in ET.fromstring(content).iter(TAG+'loc')}
    if old-included: raise ValueError('Existing sitemap routes lost: '+str(old-included))
    outputs.update(maps)
    return outputs


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=build()
    if args.check:
        for key, value in outputs.items():
            if not (ROOT/key).is_file() or (ROOT/key).read_text() != value: raise SystemExit('Regenerate editorial release: '+key)
    else:
        for key,value in outputs.items():
            path=ROOT/key;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
        baseline=json.loads((ROOT/'seo/protected-files.json').read_text())['files']
        approvals=json.loads((ROOT/'seo/approved-edits.json').read_text())
        for key,value in outputs.items():
            if key in baseline:
                record={'baseline_sha256':baseline[key],'reviewed_sha256':hashlib.sha256(value.encode()).hexdigest(),
                    'reason':'User authorized publishing the 500 editorial guides to Konular on 2026-10-14; metadata, routes and existing inventory verified. This is not specialist approval.'}
                if key.endswith('.html'):record['runtime_sha256']=runtime_digest(value)
                approvals.setdefault('edits',{})[key]=record
        (ROOT/'seo/approved-edits.json').write_text(json.dumps(approvals,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'guides':500,'public_topic_total':len(json.loads(outputs['data/topics.json'])['topics']),'checked':args.check,'outputs':len(outputs)},ensure_ascii=False))

if __name__=='__main__': main()
