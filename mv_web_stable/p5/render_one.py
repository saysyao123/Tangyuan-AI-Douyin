#!/usr/bin/env python3
"""Invoke original Huashu render.py for 1 real GPT-art shot.
Available art: L01 L04 L07 L08. Never supplies or assumes other four.
"""
import argparse,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
ENGINE=ROOT/'08_AGENT_CONTROL_LAYER/pilots/CODE_MOTION_MV_RUN01_2026-10-06/engine/render.py'
D={'L01':(0,2.5),'L04':(8,10.75),'L07':(16.25,18.75),'L08':(18.75,21.360907)}
parser=argparse.ArgumentParser()
parser.add_argument('--shot',choices=D,required=True)
parser.add_argument('--audio',required=True)
parser.add_argument('--out',required=True)
parser.add_argument('--fps',type=int,default=30)
parser.add_argument('--art-mode',choices=['production','synthetic-fixture'],default='production')
a=parser.parse_args()
st,en=D[a.shot]
start_frame,end_frame=round(st*a.fps),round(en*a.fps)
source_in=start_frame/a.fps
clip_duration=(end_frame-start_frame)/a.fps
out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
silent=out.with_name(out.stem+'.noaudio.mp4')
if a.art_mode=='production':
    subprocess.run([sys.executable,str(P/'stage_assets.py')],check=True)
else:
    fixture=ENGINE.parent/'assets/gpt/.SYNTHETIC_FIXTURE_ONLY'
    if not fixture.is_file():raise SystemExit('FAIL_CLOSED_NO_FIXTURE_MARKER: '+str(fixture))
    print('WARNING_SYNTHETIC_ASSETS_NOT_GPT_PRODUCTION',flush=True)
subprocess.run([sys.executable,str(ENGINE),'--film','gpt','--solo',a.shot.lower(),'--no-counter','--from','0','--to',str(clip_duration),'--fps',str(a.fps),'--out',str(silent),'--crf','18'],check=True,cwd=str(ROOT))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-ss',str(source_in),'-t',str(clip_duration),'-i',str(Path(a.audio).resolve()),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(out)],check=True)
print('HUASHU_IMAGE_SCENE_RENDERED_ART_MODE_'+a.art_mode.upper(),a.shot,'source_frames',start_frame,end_frame,'count',end_frame-start_frame,out)
