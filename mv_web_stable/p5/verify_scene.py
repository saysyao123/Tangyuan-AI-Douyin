#!/usr/bin/env python3
"""Independent P5 frame-count, decoder and perceptible-motion checks."""
from pathlib import Path
import argparse,subprocess,json,sys,hashlib
from PIL import Image,ImageChops,ImageStat
P=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--shot',choices=['L01','L04','L07','L08'],required=True)
p.add_argument('--file',required=True)
p.add_argument('--art-mode',choices=['production','synthetic-fixture'],required=True)
p.add_argument('--out',required=True)
args=p.parse_args()
ranges={'L01':(0,75),'L04':(240,322),'L07':(488,562),'L08':(562,641)}
start,end=ranges[args.shot]
mp4=Path(args.file);out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
def run(x):return subprocess.run(x,capture_output=True,text=True,check=True)
report={'shot':args.shot,'mode':args.art_mode,'status':'FAIL','checks':{},'errors':[]}
try:
    pr=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(mp4)]).stdout)
    v=next(x for x in pr['streams'] if x['codec_type']=='video')
    a=next(x for x in pr['streams'] if x['codec_type']=='audio')
    exp_frames=end-start
    checks={
     'video_h264':v['codec_name']=='h264',
     'audio_aac':a['codec_name']=='aac',
     'resolution':(v['width'],v['height'])==(1080,1920),
     'fps_30':v['avg_frame_rate']=='30/1',
     'frame_count_global':int(v['nb_frames'])==exp_frames,
     'duration_global':abs(float(pr['format']['duration'])-exp_frames/30)<.095,
     'full_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mp4),'-f','null','-'],capture_output=True).returncode==0
    }
    report['checks']=checks
    shotpath=out.parent
    for k,at in enumerate((.28, .67, 1.15)):
        pic=shotpath/(args.shot+'_frame_'+str(k)+'.png')
        run(['ffmpeg','-v','error','-y','-ss',str(min(at,(end-start)/30-.13)),'-i',str(mp4),'-frames:v','1',str(pic)])
    a1,a2=[Image.open(shotpath/(args.shot+'_frame_'+str(i)+'.png')).convert('RGB').resize((270,480)) for i in (0,2)]
    d=ImageChops.difference(a1,a2)
    report['frame_difference_mean']=sum(ImageStat.Stat(d).mean)/3
    report['nonstatic_scene']=report['frame_difference_mean']>.025
    report['sha256']=hashlib.sha256(mp4.read_bytes()).hexdigest()
    report['status']='TECHNICAL_PASS' if all(checks.values()) and report['nonstatic_scene'] else 'FAIL'
    if args.art_mode=='synthetic-fixture':report['art_gate']='NOT_APPLICABLE_SYNTHETIC_ONLY'
    else:report['art_gate']='VISUAL_REVIEW_PENDING'
except Exception as e:report['errors'].append(str(e))
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
if report['status']!='TECHNICAL_PASS':sys.exit(2)
