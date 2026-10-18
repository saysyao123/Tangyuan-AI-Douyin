"""Seal the exact tested runtime and matching downloads; no gameplay modifications."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,sys
root=Path(sys.argv[1]);sha=lambda b:hashlib.sha256(b).hexdigest()
source=root/'downloads/corresponding-source.zip'
with ZipFile(source) as z: files={n:z.read(n) for n in z.namelist() if not n.endswith('/') and n!='SOURCE-MANIFEST.json'}
with ZipFile(source,'w',ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in files.items():z.writestr(n,b)
 z.writestr('SOURCE-MANIFEST.json',json.dumps({'files':{n:sha(b)for n,b in files.items()}},indent=2))
excluded={'runtime-manifest.json','download-checksums.json','.openai/hosting.json'}
files={p.relative_to(root).as_posix():p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file() and p.relative_to(root).parts[0]!='downloads' and p.relative_to(root).as_posix() not in excluded}
manifest={'version':1,'files':{n:sha(b)for n,b in files.items()}}
(root/'runtime-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
with ZipFile(root/'downloads/lantern-inn-static.zip','w',ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in files.items():z.writestr(n,b)
 downloads=b'# Downloads\nThis is the exact T32 first-act website. Corresponding source and the unchanged native project are available at the online downloads path.\n'
 z.writestr('DOWNLOADS.md',downloads)
 z.writestr('runtime-manifest.json',json.dumps({'files':{**manifest['files'],'DOWNLOADS.md':sha(downloads)}},indent=2))
receipts=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted((root/'downloads').iterdir()) if p.is_file()]
(root/'download-checksums.json').write_text(json.dumps(receipts,indent=2)+'\n')
print('T32_RUNTIME_AND_SOURCE_DOWNLOADS_SEALED',len(files),[(r['path'],r['bytes'])for r in receipts])
