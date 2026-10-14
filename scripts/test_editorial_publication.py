"""Verify public metadata, complete manuscript preservation and discovery routes."""
import html
import json
import re
import unittest
from pathlib import Path
import build_first_editorial_batch as builder
from publish_editorial_guides import production_page
from seo_engine import Page, protected
from sitemap_tools import read_urlset, TAG
ROOT=Path(__file__).resolve().parents[1]

class ProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if len(builder.GUIDES)==5:builder.load_editorial_batches()
        cls.rows=json.loads((ROOT/'data/topics.json').read_text())['topics']
        cls.urls={n.text for n in read_urlset(ROOT).getroot().iter(TAG+'loc')}
        cls.listing=(ROOT/'konular.html').read_text()

    def test_all_500_manuscripts_are_published_and_discoverable(self):
        self.assertEqual(len(builder.GUIDES),500)
        published={r['slug']:r for r in self.rows if r.get('editorialCollection')=='editorial-500'}
        self.assertEqual(len(published),500)
        for guide in builder.GUIDES:
            with self.subTest(slug=guide['slug']):
                slug=guide['slug'];url='https://pdrkampus.com/konu/'+slug+'/'
                source=(ROOT/'konu'/slug/'index.html').read_text();page=Page(source)
                self.assertFalse(page.noindex)
                self.assertEqual(page.canonicals,[url]);self.assertEqual(len(page.primary_h1),1)
                self.assertEqual(page.primary_h1[0],guide['title'])
                self.assertIn(url,self.urls);self.assertIn('href="/konu/'+slug+'/"',self.listing)
                self.assertTrue(published[slug]['indexable']);self.assertEqual(published[slug]['contentStatus'],'published')
                for title,body in guide['sections']:
                    self.assertIn(html.escape(title,quote=True),source);self.assertIn(html.escape(body,quote=True),source)
                self.assertIn(html.escape(builder.EXTRA[slug]['example'],quote=True),source)
                graphs=[node for schema in page.schemas for node in schema.get('@graph',[])]
                web=[node for node in graphs if node.get('@type')=='WebPage']
                self.assertEqual([node['url'] for node in web],[url]);self.assertEqual(web[0]['name'],guide['title'])
                self.assertIn('<meta name="twitter:title" content="'+html.escape(guide['title'],quote=True)+'">',source)

    def test_drafts_remain_noindex_and_source_targets_are_preserved(self):
        for guide in builder.GUIDES:
            with self.subTest(slug=guide['slug']):
                draft=(builder.OUTPUT/(guide['slug']+'.html')).read_text()
                self.assertTrue(Page(draft).noindex)
                expected=re.findall(r'<a class="guide2-card" href="([^"]+)"',draft)
                public=(ROOT/'konu'/guide['slug']/'index.html').read_text()
                actual=re.findall(r'<a class="resource-card-cover" href="([^"]+)"',public)
                self.assertEqual(actual,expected)
                self.assertNotIn('guide2-card"',public)
                self.assertNotIn('editoryal taslağıdır',public)

    def test_shared_library_cards_and_progressive_controls(self):
        self.assertEqual(self.listing.count('data-editorial-card'),500)
        self.assertEqual(self.listing.count('EDITORIAL-500-START'),1)
        self.assertIn('library-results',self.listing)
        self.assertIn('id="guide-search"',self.listing)
        self.assertIn('id="guide-group"',self.listing)
        self.assertIn('href="konu/sosyometri/"',self.listing)
        self.assertTrue(protected(ROOT)['pass'],protected(ROOT))

    def test_transformation_removes_foreign_schema_and_escapes_metadata(self):
        guide={'slug':'test','title':'BEP < örnek','summary':'Aile & ekip'}
        source='''<html><head><title>BEP</title><meta name="description" content="Aile"><link rel="canonical" href="https://pdrkampus.com/konu/test/"><meta name="robots" content="noindex,follow"><meta name="twitter:title" content="Akran"><script type="application/ld+json">{"@type":"Article","headline":"Akran"}</script></head><body><main><h1>BEP</h1><p>Deneme içerik</p></main></body></html>'''
        page=Page(production_page(source,guide))
        self.assertEqual(len(page.schemas),1)
        self.assertFalse(page.noindex)
        self.assertEqual(page.schemas[0]['@graph'][0]['name'],'BEP < örnek')

if __name__=='__main__':unittest.main()
