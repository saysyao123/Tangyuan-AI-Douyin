"""Package exact clean corresponding source, canonical project and static player."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys,hashlib,json,subprocess
root,out,book=map(lambda x:Path(x).resolve(),sys.argv[1:4]);downloads=out/'downloads';downloads.mkdir(exist_ok=True)
subprocess.run([sys.executable,str(book/'tools/release_inventory.py'),'write',str(out)],check=True)
def add_tree(z,d,prefix):
 for p in sorted(d.rglob('*')):
  if not p.is_file() or any(part in ['node_modules','dist','.git','__pycache__'] for part in p.relative_to(d).parts):continue
  z.write(p,Path(prefix)/p.relative_to(d))
def seal_zip(filename,manifest):
 with ZipFile(filename,'a',ZIP_DEFLATED) as z:
  files={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if not n.endswith('/')}
  z.writestr(manifest,json.dumps({'version':1,'files':files},indent=2)+'\n')
with ZipFile(downloads/'lantern-inn-project.zip','w',ZIP_DEFLATED) as z:add_tree(z,root/'projects/book-lantern-inn','book-lantern-inn')
with ZipFile(downloads/'corresponding-source.zip','w',ZIP_DEFLATED) as z:
 for name in ['package.json','pnpm-lock.yaml','pnpm-workspace.yaml','tsconfig.json','tsconfig.base.json','LICENSE']:
  if (root/name).exists():z.write(root/name,name)
 for name in ['content','shared','reforge','editor']:add_tree(z,root/'packages'/name,'packages/'+name)
 add_tree(z,root/'patches','patches')
 z.write(root/'data/raw/unifont-cn.bdf','data/raw/unifont-cn.bdf')
 add_tree(z,root/'projects/book-lantern-inn','projects/book-lantern-inn')
 for name in ['tools','player','tests']:add_tree(z,book/name,'book-rpg/'+name)
 z.writestr('README-T1-BUILD.md','''# Lantern Inn corresponding source\n\nType PAL upstream f98d0ddd89ebdee7b04502ee35de26ee82c6d246; GPL-3.0.\nContains the exact patched engine/editor and original assets used by this distribution.\n\nBuild with Node 22.19+ and Python 3:\n\n````\npython -m pip install pillow\nnpx --yes pnpm@10.17.1 install --frozen-lockfile\nnode book-rpg/tools/type_pal_t1_build.mjs . output\npython -m http.server 8080 --directory output\n````\n\nOpen http://localhost:8080. No PAL commercial asset files or external model API required.\nOriginal UI, title and cursor replace upstream PAL-derived defaults; Unifont notices are retained.\nScripts type_pal_t1_full.mts and type_pal_t1_art.ts must run through the editor Vite SSR module graph.\n''')
seal_zip(downloads/'lantern-inn-project.zip','PROJECT-MANIFEST.json')
seal_zip(downloads/'corresponding-source.zip','SOURCE-MANIFEST.json')
# Keep source/project ZIPs alongside the static ZIP, avoiding recursively nested archives.
# The separately offered source archive supplies complete GPL corresponding source.
with ZipFile(downloads/'lantern-inn-static.zip','w',ZIP_DEFLATED) as z:
 for p in sorted(out.rglob('*')):
  if p.is_file() and p.parent!=downloads and p.name not in ['download-checksums.json','runtime-manifest.json']:
   rel=p.relative_to(out)
   if str(rel) in ['index.html','help.html']:
    html=p.read_text().replace('href="downloads/','href="https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/downloads/')
    z.writestr(str(rel),html)
   else:z.write(p,rel)
 z.writestr('DOWNLOADS.md','# Separate source and content downloads\n\nComplete corresponding GPL source is offered alongside this distribution at:\nhttps://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/downloads/corresponding-source.zip\n\nCanonical content22 project:\nhttps://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/downloads/lantern-inn-project.zip\n\nGitHub source and reproducible build scripts:\nhttps://github.com/saysyao123/Tangyuan-AI-Douyin/tree/main/09_GAME_ADAPTATION/BOOK_TO_RPG_PIPELINE_V1\n')
seal_zip(downloads/'lantern-inn-static.zip','runtime-manifest.json')
receipts=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in downloads.glob('*.zip')]
(out/'download-checksums.json').write_text(json.dumps(receipts,indent=2)+'\n');print('DOWNLOAD_PACKAGES_READY',json.dumps(receipts))
