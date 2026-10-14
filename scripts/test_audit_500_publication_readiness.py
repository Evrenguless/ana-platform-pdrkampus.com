#!/usr/bin/env python3
"""Regression checks for 500 PDR draft HTML auditor. No production edits."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parent / "audit_500_publication_readiness.py"
spec = importlib.util.spec_from_file_location("draft_audit", MODULE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class ReaderTests(unittest.TestCase):
    def test_page_metadata_and_cards(self):
        r = audit.Reader()
        r.feed('''<!doctype html><html><head><title>Öğrenci Rehberi</title>
          <meta name="description" content="Okul desteği">
          <meta name="robots" content="noindex,follow">
          <link rel="canonical" href="https://pdrkampus.com/konu/deneme/">
          </head><body><main><h1>Öğrenci Rehberi</h1>
          <section class="topic-section" id="adim-1"><h2>Uygulama</h2>
          <p>Öğrencinin katılımını izleyin.</p></section>
          <section class="topic-section" id="ornek"><h2>Örnek</h2>
          <p>Öğrenci kendi seçtiği göreve başlar.</p></section>
          <section class="guide2"><a class="guide2-card" href="/kaynak.pdf">Kaynak</a></section>
          <details><summary>Bir</summary><p>Yanıt</p></details>
          <details><summary>İki</summary><p>Yanıt</p></details></main></body></html>''')
        self.assertEqual(r.title, "Öğrenci Rehberi")
        self.assertEqual(r.h1, ["Öğrenci Rehberi"])
        self.assertEqual(r.desc, ["Okul desteği"])
        self.assertEqual(r.canonical, ["https://pdrkampus.com/konu/deneme/"])
        self.assertIn("noindex", r.robots[0])
        self.assertEqual(r.materials_cards, 1)
        self.assertEqual(r.faq_count, 2)
        self.assertIn("kendi seçtiği göreve", r.example)

    def test_turkish_tokenizer_and_reused_phrase_detection(self):
        self.assertEqual(audit.words("Öğrenci, güvende mi?"), ["öğrenci", "güvende", "mi"])
        self.assertEqual(audit.normalized("  ÖĞRENCİ  güvenliği! "), "öğrenci güvenliği")
        self.assertEqual(len(audit.shingles("bir iki üç dört beş altı yedi sekiz dokuz")), 2)

if __name__ == "__main__":
    unittest.main()
