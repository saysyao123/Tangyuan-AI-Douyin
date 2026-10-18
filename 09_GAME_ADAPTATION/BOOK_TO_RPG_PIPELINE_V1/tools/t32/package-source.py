from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys
root,out,book=map(Path,sys.argv[1:])
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for name in ['package.json','pnpm-lock.yaml','pnpm-workspace.yaml','tsconfig.base.json','LICENSE','biome.json']:
  z.write(root/name,name)
 for folder in ['packages','patches']:
  for p in (root/folder).rglob('*'):
   if p.is_file() and not any(x in ['node_modules','dist','.git'] for x in p.relative_to(root).parts):z.write(p,p.relative_to(root))
 for p in (book/'tools/t32').rglob('*'):
  if p.is_file():z.write(p,'t32-tools/'+p.name)
 for p in (book/'art/t32').glob('*.webp'):z.write(p,'t32-art/'+p.name)
print('T32_CORRESPONDING_DISPLAY_SOURCE_PACKAGED')
