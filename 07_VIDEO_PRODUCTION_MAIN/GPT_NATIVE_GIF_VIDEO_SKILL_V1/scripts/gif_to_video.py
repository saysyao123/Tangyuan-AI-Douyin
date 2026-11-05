#!/usr/bin/env python3
"""GPT-native GIF -> honest interpolated GIF + CFR MP4, with auditable QA.

Free tools only: Pillow, NumPy, OpenCV, FFmpeg.
This is a postprocessing script; it DOES NOT generate source frames with GPT.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageOps


def sha256(path:Path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def load_gif(path:Path):
    im=Image.open(path)
    if im.format != 'GIF':raise ValueError('Input must be a genuine GIF (GIF87a/GIF89a).')
    frames=[]; durations=[]
    for i in range(im.n_frames):
        im.seek(i)
        frames.append(np.asarray(im.convert('RGB')).copy())
        durations.append(int(im.info.get('duration',100)))
    if not frames:raise ValueError('No frames found')
    if any(f.shape!=frames[0].shape for f in frames):raise ValueError('Decoded frames have unequal sizes')
    return frames,durations,im.info.get('loop')


def optical_between(a:np.ndarray,b:np.ndarray,t:float,method:str='flow'):
    if t<=0:return a.copy()
    if t>=1:return b.copy()
    if method=='blend':return cv2.addWeighted(a,1-t,b,t,0)
    ga=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY)
    gb=cv2.cvtColor(b,cv2.COLOR_RGB2GRAY)
    flow_ab=cv2.calcOpticalFlowFarneback(ga,gb,None,.5,3,13,3,5,1.2,0)
    flow_ba=cv2.calcOpticalFlowFarneback(gb,ga,None,.5,3,13,3,5,1.2,0)
    # Trim outlier motion; background should not wander because of stray flow vectors.
    flow_ab=np.clip(cv2.medianBlur(flow_ab,5),-24,24)
    flow_ba=np.clip(cv2.medianBlur(flow_ba,5),-24,24)
    hh,ww=ga.shape
    gx,gy=np.meshgrid(np.arange(ww,dtype='float32'),np.arange(hh,dtype='float32'))
    # Approximate inverse warps from each endpoint to time t.
    aw=cv2.remap(a,gx-t*flow_ab[:,:,0],gy-t*flow_ab[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101)
    bw=cv2.remap(b,gx-(1-t)*flow_ba[:,:,0],gy-(1-t)*flow_ba[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101)
    return cv2.addWeighted(aw,1-t,bw,t,0)


def render_frames(source,output_count):
    # Uniformly resample whole animation timeline; do not repeat last frame infinitely.
    count=len(source)
    if count==1:raise ValueError('Source must have >= 2 frames with actual motion')
    frames=[]
    for j in range(output_count):
        idx=j*(count-1)/(output_count-1)
        k=int(np.floor(idx)); t=idx-k
        if k>=count-1:frames.append(source[-1].copy())
        else:frames.append(optical_between(source[k],source[k+1],t))
    return frames


def visual_sheet(frames, out:Path, cols:int=4, sample:int=16):
    inds=np.linspace(0,len(frames)-1,min(sample,len(frames)),dtype=int)
    thumbs=[]
    for i in inds:
        im=Image.fromarray(frames[i]); im.thumbnail((160,290))
        card=Image.new('RGB',(176,320),'#171717')
        card.paste(im,((176-im.width)//2,16))
        draw=ImageDraw.Draw(card);draw.text((10,298),f'Frame {i+1}/{len(frames)}',fill='white')
        thumbs.append(card)
    rows=(len(thumbs)+cols-1)//cols
    bg=Image.new('RGB',(cols*176,rows*320),'#222222')
    for k,im in enumerate(thumbs):bg.paste(im,((k%cols)*176,(k//cols)*320))
    bg.save(out,quality=88)


def diagnostics(frames):
    diffs=[float(np.mean(np.abs(a.astype('int16')-b.astype('int16')))) for a,b in zip(frames,frames[1:])]
    near_static=sum(d<.15 for d in diffs)
    med=float(np.median(diffs)) if diffs else 0
    high=[int(i+1) for i,d in enumerate(diffs) if med>.2 and d>max(20.,12*med)]
    return {'adjacent_mean_abs_rgb_diff': {'min':round(min(diffs),3),'median':round(med,3),'max':round(max(diffs),3)},'near_duplicate_transitions_threshold_0_15':near_static,'extreme_change_boundaries':high, 'warning':'Numerical metrics do not prove character identity, no-jitter, no scroll, or physical plausibility; human viewing required.'}


def encode_gif(frames,out:Path, duration_seconds:float):
    # GIF stores delays in centiseconds. Exact overall duration via distributed 40/50ms delays.
    cs=int(round(duration_seconds*100))
    n=len(frames)
    if cs<n:raise ValueError('GIF cannot represent sub-10ms frame delays for this count/duration.')
    delays_cs=[int(round((i+1)*cs/n))-int(round(i*cs/n)) for i in range(n)]
    if min(delays_cs)<1: raise ValueError('GIF delay under 10ms')
    images=[Image.fromarray(f).quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE) for f in frames]
    images[0].save(out,save_all=True,append_images=images[1:],duration=[100*x//10 for x in delays_cs],disposal=2,optimize=False)
    return delays_cs


def encode_mp4(frames,out:Path,fps:int):
    if not shutil.which('ffmpeg'):raise RuntimeError('ffmpeg not installed')
    h,w=frames[0].shape[:2]
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}', '-r',str(fps),'-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p','-r',str(fps),'-movflags','+faststart',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for f in frames:proc.stdin.write(f.tobytes())
        proc.stdin.close();err=proc.stderr.read().decode('utf-8',errors='replace');rc=proc.wait()
    except Exception:
        proc.kill();proc.wait();raise
    if rc:raise RuntimeError(f'ffmpeg failed: {err[-1000:]}')


def probe_mp4(path:Path):
    p=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,nb_frames,r_frame_rate,duration','-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)['streams'][0]


def main():
    a=argparse.ArgumentParser()
    a.add_argument('--input',required=True,type=Path,help='Original native GPT-generated GIF')
    a.add_argument('--out',required=True,type=Path,help='Output directory')
    a.add_argument('--seconds',type=float,default=5)
    a.add_argument('--fps',type=int,default=24)
    a.add_argument('--scale',type=int,choices=(1,2,3),default=2,help='Upscaling is NOT actual detail restoration')
    args=a.parse_args()
    if args.seconds<=0 or args.fps<=0:raise ValueError('seconds and fps must be positive')
    if abs(args.seconds*args.fps-round(args.seconds*args.fps))>.0001:raise ValueError('seconds*fps must be integer for CFR output')
    n=int(round(args.seconds*args.fps))
    args.out.mkdir(parents=True,exist_ok=True)
    source,durations,loop=load_gif(args.input)
    h0,w0=source[0].shape[:2]
    outframes=render_frames(source,n)
    if args.scale!=1:
        outframes=[cv2.resize(f,(w0*args.scale,h0*args.scale),interpolation=cv2.INTER_CUBIC) for f in outframes]
    dest_gif=args.out/'animation_5s_120f.gif';dest_mp4=args.out/'animation_5s_24fps.mp4';qa=args.out/'qa_contact_sheet.jpg'
    timing=encode_gif(outframes,dest_gif,args.seconds)
    encode_mp4(outframes,dest_mp4,args.fps)
    visual_sheet(outframes,qa)
    verified,verified_durs,_=load_gif(dest_gif)
    mp4meta=probe_mp4(dest_mp4)
    assert len(verified)==n and sum(verified_durs)==round(args.seconds*1000), 'GIF verification failed'
    assert int(mp4meta['nb_frames'])==n and mp4meta['r_frame_rate']==f'{args.fps}/1', 'MP4 verification failed'
    report={
      'status':'FILE_TECH_QA_PASSED_VISUAL_QA_REQUIRED',
      'input':str(args.input), 'input_sha256':sha256(args.input),
      'source':{'frames':len(source),'width':w0,'height':h0,'duration_ms':sum(durations),'loop':loop},
      'method':'Optical flow Farneback bidirectional warping and blending; not native GPT generated 120 frames',
      'output':{'fps':args.fps,'frames':n,'duration_seconds':args.seconds,'size':list(outframes[0].shape[1::-1]),
                'gif':dest_gif.name,'gif_frame_count_verified':len(verified),'gif_duration_ms_verified':sum(verified_durs),
                'mp4':dest_mp4.name,'mp4_frame_count_verified':int(mp4meta['nb_frames']), 'mp4_fps_verified':mp4meta['r_frame_rate']},
      'diagnostics':diagnostics(outframes),
      'visual_qa_checklist':{'all_frames_complete':'REQUIRES_HUMAN_VIEWING','no_scroll_or_grid_slip':'REQUIRES_HUMAN_VIEWING',
                           'no_face_or_hand_warp':'REQUIRES_HUMAN_VIEWING','start_end_action':'REQUIRES_HUMAN_VIEWING',
                           'sound_and_subtitles':'NOT_APPLICABLE'},
      'provenance':{'native_source_frames':len(source),'interpolated_or_resampled_frames':n-len(source),
                    'upsampling_not_restoration':args.scale>1,'no_external_paid_api':True}
    }
    (args.out/'qa_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'gif':str(dest_gif),'mp4':str(dest_mp4),'qa_report':str(args.out/'qa_report.json')},ensure_ascii=False))

if __name__=='__main__':main()