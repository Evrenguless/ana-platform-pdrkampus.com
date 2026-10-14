"""Existing-library links must preserve identity, audience and working detail pages."""
import copy
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_500_publication_readiness as audit
import build_first_editorial_batch as builder


class LibraryLinksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if len(builder.GUIDES) == 5:
            builder.load_editorial_batches()
        cls.links = builder.load_library_links()
        builder.LIBRARY_LINKS = cls.links
        builder.PRIMARY_SOURCES = builder.load_primary_sources()

    def test_all_pinned_cards_go_to_existing_library_details(self):
        for slug, choice in self.links['guides'].items():
            with self.subTest(slug=slug):
                selected = builder.resources(slug)
                self.assertEqual([r['id'] for r in selected], choice['resource_ids'])
                reader = audit.Reader()
                rendered = builder.source_cards(slug)
                reader.feed(rendered)
                self.assertEqual(reader.library_material_cards, len(selected))
                card_targets = re.findall(r'<a class="guide2-card" href="([^"]+)"', rendered)
                self.assertEqual(card_targets[:len(selected)],
                                 [builder.detail_page(row) for row in selected])
                for row in selected:
                    target = builder.detail_page(row)
                    self.assertIn(target, reader.links)
                    self.assertTrue(builder.valid_detail_page(target))

    def test_external_references_do_not_hide_library_gaps(self):
        reader = audit.Reader()
        reader.feed('<a class="guide2-card" href="https://www.who.int/publications/">WHO</a>')
        self.assertEqual(reader.materials_cards, 1)
        self.assertEqual(reader.library_material_cards, 0)
        for slug in self.links['unmatched']:
            self.assertEqual(builder.resources(slug), [])

    def test_audience_and_topic_boundaries_are_preserved(self):
        self.assertIn('veliyle-uyku-duzeni', self.links['unmatched'])
        self.assertIn('etik-ikilem-okul-psikolojik-danisma', self.links['unmatched'])
        self.assertIn('kariyer-ogrenim-maliyetini-arastirma', self.links['unmatched'])
        self.assertEqual(self.links['guides']['sinav-sinavda-yardim-isteme']['resource_ids'],
                         ['osym-2026-yks-sinav-kilavuzu-pdf', 'meb-lgs-merkezi-sinav-basvuru-uygulama-kilavuzu-2026'])
        self.assertIn('mardin-sinir-lise-ogretmen-brosur-2026',
                      self.links['guides']['lise-sosyal-iliskilerde-riza']['resource_ids'])
        self.assertIn('orgm-bep-tum-ogretmenler-yol-haritasi',
                      self.links['guides']['bep-olculebilir-hedef']['resource_ids'])

    def test_unknown_stale_or_broken_materials_fail_closed(self):
        first_id = next(iter(self.links['resources']))
        for kind in ('unknown', 'changed_title', 'changed_audience', 'broken_detail', 'approval'):
            data = copy.deepcopy(self.links)
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                if kind == 'unknown':
                    data['guides']['bep-olculebilir-hedef']['resource_ids'] = ['invented-source']
                elif kind == 'changed_title':
                    data['resources'][first_id]['title'] = 'Unrelated document'
                elif kind == 'changed_audience':
                    data['resources'][first_id]['level'] = 'Wrong school stage'
                elif kind == 'approval':
                    data['publication_approved'] = True
                path = Path(temp) / 'links.json'
                path.write_text(json.dumps(data), encoding='utf-8')
                with patch.object(builder, 'LIBRARY_LINK_PATH', path):
                    if kind == 'broken_detail':
                        with patch.object(builder, 'detail_page', return_value=None):
                            with self.assertRaises(ValueError): builder.load_library_links()
                    else:
                        with self.assertRaises(ValueError): builder.load_library_links()


if __name__ == '__main__':
    unittest.main()
