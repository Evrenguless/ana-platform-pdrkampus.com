import tempfile,unittest
from pathlib import Path
from repair_resource_links import repair
class RelatedLinkTests(unittest.TestCase):
 def test_missing_targets_use_only_same_card_source(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);source='<article class="catalog-card"><img src="/assets/resource-previews/missing.jpg" alt="Cover"><h2><a href="/kaynak-detay/missing/">Kaynak</a></h2><a href="https://example.org/real.pdf">Resmî dosyayı aç</a></article>'
   result=repair(root,source)
   self.assertNotIn('/kaynak-detay/missing/',result);self.assertNotIn('<img',result)
   self.assertIn('resource-format-tile',result);self.assertIn('https://example.org/real.pdf',result)
 def test_existing_targets_unchanged_and_no_source_not_invented(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);file=root/'kaynak-detay/real/index.html';file.parent.mkdir(parents=True);file.write_text('real')
   source='<article class="catalog-card"><a href="/kaynak-detay/real/">Gerçek</a><a href="https://example.org/real.pdf">Resmî dosyayı aç</a></article>'
   self.assertEqual(source,repair(root,source))
   missing='<article class="catalog-card"><a href="/kaynak-detay/missing/">Missing</a></article>'
   self.assertEqual(missing,repair(root,missing))
if __name__=='__main__':unittest.main()
