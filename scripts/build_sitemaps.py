"""Build or verify canonical sitemaps from the existing public URL inventory."""
import argparse,json
from pathlib import Path
from sitemap_tools import read_urlset,eligible_outputs
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 outputs,excluded=eligible_outputs(ROOT,read_urlset(ROOT).getroot())
 for name,content in outputs.items():
  file=ROOT/name
  if args.check:
   if not file.exists() or file.read_text()!=content:raise SystemExit('Regenerate sitemap: '+name)
  else:file.parent.mkdir(parents=True,exist_ok=True);file.write_text(content)
 print(json.dumps({'sitemap_files':len(outputs)-1,'excluded':excluded},ensure_ascii=False))
if __name__=='__main__':main()
