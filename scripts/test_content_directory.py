"""Every sitemap URL must be discoverable without executing JavaScript."""
import collections,sys
from pathlib import Path
from urllib.parse import urljoin
from sitemap_tools import read_urlset
from seo_engine import Page
root=Path(__file__).resolve().parents[1];base='https://pdrkampus.com/'
urls={n.text for n in read_urlset(root).getroot().iter() if n.tag.endswith('loc')};links={}
for u in urls:
 path=u.removeprefix(base);file=root/(path+'index.html' if not path or path.endswith('/') else path);p=Page(file.read_text())
 assert not p.noindex and p.canonicals==[u],u
 links[u]={urljoin(u,x).split('#')[0] for x in p.links}
seen=set();queue=collections.deque([base])
while queue:
 u=queue.popleft()
 if u in seen:continue
 seen.add(u);queue.extend(v for v in links.get(u,[]) if v in urls and v not in seen)
assert seen==urls,sorted(urls-seen)[:20]
print(f'{len(urls)} canonical pages reachable from homepage using HTML links.')
