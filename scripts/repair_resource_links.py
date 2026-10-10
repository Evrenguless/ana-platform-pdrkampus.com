"""Repair stale related-card targets only using the same card's real source link."""
import re
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
def exists(root,path):
 file=root/unquote(urlsplit(path).path).lstrip('/')
 return file.is_file() or (file/'index.html').is_file()
def repair(root,source):
 def card(match):
  block=match.group(0)
  # A missing preview must not be presented as a real cover image.
  def image(m):
   return m[0] if exists(root,m[1]) else '<span class="resource-format-tile">PDF<small>Belge</small></span>'
  block=re.sub(r'<img\b[^>]*src="(/assets/resource-previews/[^"]+)"[^>]*>',image,block)
  links=re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>Resmî dosyayı aç',block)
  fallback=next((u for u in links if urlsplit(u).scheme in ('http','https')),None)
  if fallback:
   def link(m):
    if exists(root,m[1]):return m[0]
    return '<a href="'+fallback+'" target="_blank" rel="noopener noreferrer">'
   block=re.sub(r'<a href="(/kaynak-detay/[^"]+/)">',link,block)
  return block
 return re.sub(r'<article\b[^>]*class="catalog-card"[^>]*>.*?</article>',card,source,flags=re.S)
def main():
 changed=[]
 for file in ROOT.rglob('*.html'):
  old=file.read_text();new=repair(ROOT,old)
  if new!=old:file.write_text(new);changed.append(file.relative_to(ROOT).as_posix())
 print('Related-card files repaired:',len(changed))
if __name__=='__main__':main()
