from pathlib import Path
import tempfile,importlib.util,json
from zipfile import ZipFile
module=Path(__file__).resolve().parents[1]/'tools/release_inventory.py'
spec=importlib.util.spec_from_file_location('inventory',module);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp);(p/'index.html').write_text('ok');expected=m.inventory(p);(p/'runtime-manifest.json').write_text(json.dumps({'files':expected}));(p/'downloads').mkdir()
 def zipfile(name,manifest,files,bad=False):
  with ZipFile(p/'downloads'/name,'w') as z:
   for key,data in files.items():z.writestr(key,data)
   z.writestr(manifest,json.dumps({'files':{key:m.digest(data if not bad else b'wrong') for key,data in files.items()}}))
 def receipts():
  data=[{'path':f.name,'bytes':f.stat().st_size,'sha256':m.digest(f.read_bytes())} for f in (p/'downloads').iterdir()];(p/'download-checksums.json').write_text(json.dumps(data))
 zipfile('lantern-inn-static.zip','runtime-manifest.json',{'index.html':b'ok','DOWNLOADS.md':b'downloads'})
 zipfile('corresponding-source.zip','SOURCE-MANIFEST.json',{'source.ts':b'code'})
 zipfile('lantern-inn-project.zip','PROJECT-MANIFEST.json',{'manifest.json':b'project'})
 receipts();m.check(p)
 for name in ['extra.js','.rsync-tmp/old.js']:
  f=p/name;f.parent.mkdir(exist_ok=True);f.write_text('old')
  try:m.check(p)
  except ValueError:pass
  else:raise AssertionError('inventory accepted '+name)
  f.unlink()
  if f.parent!=p:f.parent.rmdir()
 (p/'index.html').write_text('changed')
 try:m.check(p)
 except ValueError:pass
 else:raise AssertionError('changed file accepted')
 (p/'index.html').write_text('ok')
 zipfile('lantern-inn-static.zip','runtime-manifest.json',{'index.html':b'ok','DOWNLOADS.md':b'downloads'},True);receipts()
 try:m.check(p)
 except ValueError as error:assert 'inner inventory' in str(error)
 else:raise AssertionError('CRC-valid ZIP with refreshed outer hash concealed inner mismatch')
print('RELEASE_NEGATIVE_CONTROLS=PASS extra/temporary/changed/CRC-valid-inner-mismatch rejected')
