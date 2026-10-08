#!/usr/bin/env python3
"""Validate real exported GPT-native vertical art. Geometry is NOT artistic approval."""
import argparse, hashlib, json, sys
from pathlib import Path
from PIL import Image

SLOTS=[f'L{i:02d}' for i in range(1,9)]
ap=argparse.ArgumentParser()
ap.add_argument('assets')
ap.add_argument('--require-all',action='store_true')
ap.add_argument('--out',default='mv_web_stable/p4/asset_report.json')
args=ap.parse_args()
folder=Path(args.assets)
rows=[]
for sid in SLOTS:
    file=folder/f'{sid}_hero.png'
    item={'id':sid,'file':file.name,'status':'MISSING'}
    if file.exists():
        try:
            with Image.open(file) as im: im.verify()
            with Image.open(file) as im:
                w,h=im.size
                item.update(width=w,height=h,mode=im.mode,ratio=w/h)
            item['sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
            item['status']='GEOMETRY_PASS_VISUAL_PENDING' if w>=900 and h>=1600 and abs(w/h-9/16)<.0125 else 'REJECT_SIZE_OR_ASPECT'
        except Exception as ex:
            item.update(status='REJECT_INVALID_IMAGE',error=str(ex))
    rows.append(item)
unknown=[f.name for f in folder.glob('*.png') if f.name not in {x+'_hero.png' for x in SLOTS}]
passed=sum(x['status']=='GEOMETRY_PASS_VISUAL_PENDING' for x in rows)
valid=(passed==8 if args.require_all else passed>=1) and not unknown and not any(x['status'].startswith('REJECT') for x in rows)
result={'geometry_status':'PASS' if valid else 'FAIL','visual_gate':'PENDING_HUMAN_REVIEW','provenance_gate':'PENDING_RECORD_VALIDATION','passed':passed,'missing':[x['id'] for x in rows if x['status']=='MISSING'],'unregistered':unknown,'assets':rows}
out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':result['geometry_status'],'passed':passed,'missing':result['missing'],'unregistered':unknown},ensure_ascii=False))
sys.exit(0 if valid else 2)
