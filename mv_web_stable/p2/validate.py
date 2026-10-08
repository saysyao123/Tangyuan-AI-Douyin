#!/usr/bin/env python3
import argparse,json,sys,hashlib,struct
from pathlib import Path
P=Path(__file__).resolve().parent
A=argparse.ArgumentParser();A.add_argument('--out',default=str(P/'out/score.json'));A.add_argument('--require-assets',action='store_true');args=A.parse_args()
timeline=json.loads((P.parent/'lyric_timeline.json').read_text())
score=json.loads((P/'shot_contract.json').read_text())
manifest=json.loads((P/'assets_manifest.json').read_text())
lines=timeline['lyrics'];shots=score['shots'];problems=[];frames=[];last=0
if len(lines)!=8 or len(shots)!=8:problems.append('8 shots required')
for i,(line,s) in enumerate(zip(lines,shots),1):
    id=f'L{i:02d}'
    if line['id']!=id or s['id']!=id or line['text']!=s['lyric']:problems.append(id+' identity')
    a,b=s['start'],s['end']
    if a!=line['start'] or b!=line['end'] or abs(a-last)>1e-7:problems.append(id+' timing mismatch')
    st,en=round(a*30),round(b*30)
    if en<=st:problems.append(id+' empty frame span')
    peak=s['peak_cue']['local_s']
    if peak<0 or peak>=b-a:problems.append(id+' cue outside shot')
    frames.append(dict(id=id,start_frame=st,end_frame=en,frames=en-st,start=a,end=b,peak_hint=peak))
    last=b
if abs(last-timeline['audio_duration_seconds'])>1e-6:problems.append('end mismatch')
if sum(s['frames'] for s in frames)!=round(last*30):problems.append('frame coverage mismatch')
if args.require_assets:
    if manifest['source']!='GPT_NATIVE_IMAGE_GENERATION_ONLY':problems.append('image policy mismatch')
    for s in shots:
        for slot in s['asset_slots']:
            record=manifest.get('shots',{}).get(s['id'],{}).get(slot)
            if not record or record.get('state')!='READY' or record.get('source')!='GPT_NATIVE' or record.get('visual_gate')!='PASS':
                problems.append(s['id']+'/'+slot+' not approved');continue
            f=(P/record['path']).resolve()
            if not f.is_relative_to((P/'assets').resolve()) or not f.is_file():problems.append(str(f)+' absent');continue
            raw=f.read_bytes()
            if len(raw)<33 or not raw.startswith(b'\x89PNG\r\n\x1a\n'):problems.append(str(f)+' not PNG');continue
            w,h=struct.unpack('>II',raw[16:24])
            if w<768 or h<1152:problems.append(str(f)+' low res')
            if hashlib.sha256(raw).hexdigest()!=record.get('sha256'):problems.append(str(f)+' hash mismatch')
out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
r={'status':'PASS' if not problems else 'FAIL','type':'production_assets' if args.require_assets else 'structural','fps':30,'total_frames':sum(x['frames'] for x in frames),'shots':frames,'problems':problems}
out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':r['status'],'total_frames':r['total_frames'],'shot_frame_counts':[x['frames'] for x in frames],'problems':problems},ensure_ascii=False))
if problems:sys.exit(1)
