"""Ensure faster content comparison preserves the independent Jaccard definition."""
import random,unittest
from ecosystem_engine import compare_grams
class SimilarityTests(unittest.TestCase):
 def test_exact_results_for_boundary_and_diverse_sizes(self):
  rand=random.Random(20261011);texts={'tiny':set(range(20)), 'base':set(range(100)), 'boundary':set(range(90)), 'below':set(range(89)), 'copy':set(range(100)), 'large':set(range(300))}
  for i in range(15):texts['random-'+str(i)]=set(rand.sample(range(200),rand.randrange(45,150)))
  expected=[];keys=list(texts)
  for i,a in enumerate(keys):
   if len(texts[a])<50:continue
   for b in keys[i+1:]:
    if not texts[b]:continue
    ratio=len(texts[a]&texts[b])/len(texts[a]|texts[b])
    if ratio>=.9:expected.append({'first':a,'second':b,'similarity':round(ratio,3),'action':'editorial_review_only'})
  self.assertEqual(compare_grams(texts),expected)
if __name__=='__main__':unittest.main()
