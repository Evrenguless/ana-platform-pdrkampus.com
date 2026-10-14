"""Regression gate for explicitly revised priority manuscripts and source cards.

This validates draft quality evidence, never clinical accuracy or publication.
"""
import collections
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_500_publication_readiness as audit
import build_first_editorial_batch as builder


class PriorityEditorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        builder.load_editorial_batches()
        cls.sources = builder.load_primary_sources()
        builder.PRIMARY_SOURCES = cls.sources
        cls.guides = {g['slug']: g for g in builder.GUIDES}

    def test_priority_manuscripts_have_substantive_chapters(self):
        for slug in self.sources['guides']:
            with self.subTest(slug=slug):
                guide = self.guides[slug]
                chapters = guide['sections']
                self.assertGreaterEqual(len(chapters), 5)
                self.assertGreaterEqual(sum(len(audit.words(t)) for _, t in chapters), 250)
                self.assertTrue(all(len(audit.words(t)) >= 15 for _, t in chapters))
                self.assertGreaterEqual(len(audit.words(builder.EXTRA[slug]['example'])), 20)

    def test_critical_and_bep_guides_have_explicit_references(self):
        critical = [s for s in self.guides if any(r in s for r in audit.RISK)]
        self.assertEqual(len(critical), 33)
        for slug in critical:
            self.assertIn(slug, self.sources['guides'])
        for slug in self.guides:
            if slug.startswith(('bep-', 'ozel-egitim-')):
                self.assertIn('meb-bep', self.sources['guides'][slug])
        for slug in ('kriz-kendine-zarar-ifadesi', 'ogrenci-intihar-ifadesinde-acil-destek'):
            self.assertIn('nice-self-harm', self.sources['guides'][slug])

    def test_priority_groups_do_not_reuse_complete_chapters(self):
        paragraphs = collections.defaultdict(set)
        for slug in self.sources['guides']:
            for _, text in self.guides[slug]['sections']:
                paragraphs[audit.normalized(text)].add(slug)
        duplicates = [sorted(slugs) for slugs in paragraphs.values() if len(slugs) > 1]
        self.assertEqual(duplicates, [])

    def test_primary_cards_survive_real_auditor_and_are_escaped(self):
        source = copy.deepcopy(self.sources)
        source['sources']['meb-bep']['title'] = '<script>alert("unsafe")</script>'
        source['sources']['meb-bep']['scope'] = 'Koşul < veri & destek'
        with patch.object(builder, 'PRIMARY_SOURCES', source):
            rendered = builder.primary_source_cards('bep-hazirlama-okul-ekibi')
        reader = audit.Reader()
        reader.feed(rendered)
        self.assertEqual(reader.materials_cards, 1)
        self.assertIn(source['sources']['meb-bep']['url'], reader.links)
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertIn('Koşul &lt; veri &amp; destek', rendered)
        self.assertIn('uzman onayı değildir', rendered)

    def test_invalid_references_fail_before_draft_generation(self):
        for mutation in ('unknown', 'insecure_url', 'approval'):
            data = copy.deepcopy(self.sources)
            if mutation == 'unknown':
                data['guides']['bep-hazirlama-okul-ekibi'] = ['invented-document']
            elif mutation == 'insecure_url':
                data['sources']['meb-bep']['url'] = 'javascript:alert(1)'
            else:
                data['publication_approved'] = True
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / 'references.json'
                path.write_text(json.dumps(data), encoding='utf-8')
                with patch.object(builder, 'PRIMARY_SOURCE_PATH', path):
                    with self.assertRaises(ValueError):
                        builder.load_primary_sources()


if __name__ == '__main__':
    unittest.main()
