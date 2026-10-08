#!/usr/bin/env python3
"""P2 isolated-source-timeline rehearsal using existing Huashu renderer. Old art: NOT PRODUCTION."""
import argparse,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
REPO=P.parents[1]
ENGINE=REPO/'08_AGENT_CONTROL_LAYER/pilots/CODE_MOTION_MV_RUN01_2026-10-06/engine/render.py'
ap=argparse.ArgumentParser();ap.add_argument('--shot',required=True,choices=[f'L{i:02d}' for i in range(1,9)]);ap.add_argument('--audio',required=True);ap.add_argument('--outdir',default=str(P/'out'));args=ap.parse_args()
shot=next(s for s in json.loads((P/'shot_contract.json').read_text())['shots'] if s['id']==args.shot)
out=Path(args.outdir).resolve();out.mkdir(parents=True,exist_ok=True)
mp4=out/('REHEARSAL_'+args.shot+'.mp4')
print('REHEARSAL / LEGACY ART ONLY:',shot['id'],shot['start'],shot['end'],flush=True)
subprocess.run([sys.executable,str(ENGINE),'--film','night','--fps','30','--from',str(shot['start']),'--to',str(shot['end']),'--audio',str(Path(args.audio).resolve()),'--out',str(mp4),'--crf','18'],check=True,cwd=str(REPO))
print('WROTE',mp4,flush=True)
