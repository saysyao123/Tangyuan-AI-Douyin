#!/usr/bin/env python3
"""Verify P2 rendered lyric clip, duration, audio, global frame slice and mid-frame preview."""
import argparse,json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--shot',choices=[f'L{i:02d}' for i in range(1,9)],required=True);args=ap.parse_args()
o=P/'out';f=o/('REHEARSAL_'+args.shot+'.mp4')
s=next(q for q in json.loads((P/'shot_contract.json').read_text())['shots'] if q['id']==args.shot)
st,en=round(s['start']*30),round(s['end']*30)
checks={};err=None
try:
    info=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)],capture_output=True,text=True,check=True).stdout)
    v=next(q for q in info['streams'] if q['codec_type']=='video')
    a=next(q for q in info['streams'] if q['codec_type']=='audio')
    checks={'resolution':(v['width'],v['height'])==(1080,1920),'video_codec':v['codec_name']=='h264','audio_codec':a['codec_name']=='aac','fps':v['avg_frame_rate']=='30/1','frame_slice':int(v.get('nb_frames',0))==en-st,'duration':abs(float(info['format']['duration'])-(en-st)/30)<0.1}
    checks['decode']=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(f),'-f','null','-'],capture_output=True).returncode==0
    thumb=o/(args.shot+'_middle.png')
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str((en-st)/60),'-i',str(f),'-frames:v','1',str(thumb)],check=True)
    checks['preview']=thumb.exists() and thumb.stat().st_size>1000
except Exception as ex:err=str(ex)
result={'stage':'P2_CLIP_ISOLATION','mode':'REHEARSAL_LEGACY_ART','shot':args.shot,'global_start_frame':st,'global_end_frame':en,'status':'PASS' if checks and all(checks.values()) else 'FAIL','checks':checks,'error':err}
(o/(args.shot+'_verification.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
if result['status']!='PASS':sys.exit(1)
