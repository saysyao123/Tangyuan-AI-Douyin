"""Technical export checks; audio correlation is not a lyric listening gate."""
import argparse,json,subprocess,hashlib
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('video');ap.add_argument('source_audio');ap.add_argument('--out',required=True);a=ap.parse_args()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=index,codec_name,codec_type,width,height,avg_frame_rate,nb_read_frames,duration,sample_rate,channels:format=duration','-of','json',a.video]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
def samples(f):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',f,'-vn','-ac','1','-ar','16000','-f','f32le','-'])
    return np.frombuffer(raw,dtype='<f4')
x,y=samples(a.source_audio),samples(a.video)
def rms(z):
    z=z[:len(z)//160*160].reshape(-1,160);return np.sqrt((z*z).mean(axis=1))
x,y=rms(x),rms(y);n=min(len(x),len(y));x,y=x[:n],y[:n]
scores=[]
for lag in range(-30,31):
    xx=x[max(0,lag):min(n,n+lag)];yy=y[max(0,-lag):min(n,n-lag)]
    scores.append((float(np.corrcoef(xx,yy)[0,1]),lag))
corr,lag=max(scores)
checks={'portrait_1080x1920':(v['width'],v['height'])==(1080,1920),'30fps':v['avg_frame_rate']=='30/1','641_frames':int(v['nb_read_frames'])==641,'audio_present':bool(au),'duration_within_one_frame':abs(float(v['duration'])-21.360907)<1/30,'audio_envelope_preserved':corr>.95,'audio_offset_within_10ms':abs(lag)<=1}
result={'video':Path(a.video).name,'sha256':hashlib.sha256(Path(a.video).read_bytes()).hexdigest(),'probe':probe,'checks':checks,'audio_rms_correlation':corr,'audio_rms_best_lag_seconds':lag*.01,'audio_rms_resolution_seconds':.01,'audio_subjective_listening':'not performed in this run; reuse user-confirmed source','technical_result':'PASS' if all(checks.values()) else 'REVISE'}
Path(a.out).write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({'result':result['technical_result'],'checks':checks,'correlation':corr,'lag':lag*.01}))
if not all(checks.values()):raise SystemExit(1)
