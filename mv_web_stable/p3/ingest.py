#!/usr/bin/env python3
"""Ingest four exported GPT-native PNGs from the ChatGPT P3 delivery ZIP into this Git repo.
Run from any directory: python mv_web_stable/p3/ingest.py /path/to/extracted/assets
This script NEVER claims that a baked hero still is an independent moving character layer.
"""
import hashlib,json,shutil,struct,sys
from pathlib import Path
P=Path(__file__).resolve().parent
manifest=json.loads((P/'four_anchor_manifest.json').read_text(encoding='utf-8'))
src=Path(sys.argv[1]).resolve()
dest=P/'assets'
dest.mkdir(parents=True,exist_ok=True)
results=[]
for x in manifest['images']:
    name=x['id']+'_GPT_NATIVE_HERO.png'
    f=src/name
    if not f.is_file():raise SystemExit('MISSING '+str(f))
    blob=f.read_bytes()
    if not blob.startswith(b'\x89PNG\r\n\x1a\n'):raise SystemExit('NOT_PNG '+str(f))
    w,h=struct.unpack('>II',blob[16:24])
    sha=hashlib.sha256(blob).hexdigest()
    if (w,h)!=(x['width'],x['height']) or sha!=x['sha256']:
        raise SystemExit('IMAGE_IDENTITY_MISMATCH '+name)
    d=dest/name;shutil.copyfile(f,d)
    results.append({'shot':x['id'],'path':str(d.relative_to(P)),'status':'IMPORTED_HERO_ONLY','sha256':sha})
out=P/'import_receipt.json'
out.write_text(json.dumps({'status':'ALL_FOUR_HEROS_IMPORTED_NOT_LAYER_READY','images':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(out.read_text(encoding='utf-8'))
