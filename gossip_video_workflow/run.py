"""Chinese-only cloud export. Editorial research/verification belongs to the agent.

Usage: .venv/bin/python run.py --episode examples/smoke.json [--stt]
Outputs are durable only after the assistant saves them or Actions uploads them.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, re, shutil, subprocess, sys, urllib.request, wave, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / 'runtime'

def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def key(obj):return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def write(p,obj):Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
def command(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-6000:] or p.stdout[-6000:])
    return p.stdout
def ff(args):return command(['ffmpeg','-v','error','-y','-threads','2','-filter_threads','2',*args])
def probe(p):return json.loads(command(['ffprobe','-v','error','-show_format','-show_streams','-of','json',p]))
def fetch(url,p):
    if not url.startswith('https://'):raise ValueError('Public asset URL must use HTTPS')
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.partial')
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'GossipVideoWorkflow/1.0'}),timeout=60) as response,tmp.open('wb') as out:shutil.copyfileobj(response,out)
        tmp.replace(p)
    finally:tmp.unlink(missing_ok=True)

def validate(e):
    if e.get('language')!='zh':raise ValueError('Only Chinese is enabled')
    if not re.fullmatch(r'[a-zA-Z0-9_-]+',e['id']):raise ValueError('Unsafe episode id')
    facts=e.get('facts',{});used=[];names=set();rows=e['rows']
    if not rows or rows[0]['type']!='cover' or rows[-1]['type']!='end':raise ValueError('First frame must be cover; last must ask a question')
    if not e.get('technical_demo') and not e.get('editorial_review_complete'):raise ValueError('Complete source and script review before exporting')
    for row in rows:
        if not re.fullmatch(r'[a-zA-Z0-9_-]+',str(row['id'])) or row['id'] in names:raise ValueError('Unique safe shot ids required')
        names.add(row['id'])
        if row['type'] not in ['cover','video','image','tweet','end']:raise ValueError('Unknown visual type')
        if not row.get('text') or len(row['text'])>88:raise ValueError('Use one short complete sentence per caption')
        if row['kind'] not in ['fact','claim','comment']:raise ValueError('Label factual, unverified or editorial wording')
        for f in row.get('fact_ids',[]):
            if f not in facts or not facts[f].get('urls'):raise ValueError('Missing source for '+f)
            if facts[f]['status']=='unverified' and row['kind']!='claim':raise ValueError('Unverified assertion needs claim label')
            if facts[f]['status'] not in ['verified','unverified']:raise ValueError('Invalid fact status')
        if row['kind'] in ['fact','claim'] and not row.get('fact_ids'):raise ValueError('Facts and claims require source ids')
        if row['type']=='tweet':
            t=row['tweet']
            if not re.fullmatch(r'https://x\.com/[^/]+/status/\d+',t['url']):raise ValueError('Original X status URL required')
            if t.get('highlight') and t['highlight'] not in t['original']:raise ValueError('Highlight must be part of original text')
            if not t.get('translation'):raise ValueError('Chinese tweet translation required')
        if row['type']=='video':
            m=row['media'];a,b=m['start'],m['end']
            if not (0<=a<b):raise ValueError('Invalid media range')
            if not m.get('crop'):raise ValueError('Explicit crop required to remove source subtitles/station bugs')
            for source,x,y in used:
                if source==m['asset'] and max(x,a)<min(y,b):raise ValueError('Repeated source footage range')
            used.append((m['asset'],a,b))
    if not rows[-1].get('question'):raise ValueError('End with a comment question')
    forbidden=e.get('excluded_names',[])
    visible={k:v for k,v in e.items() if k not in ['excluded_names','assets','facts','source_access','brief']}
    if any(n in json.dumps(visible,ensure_ascii=False) for n in forbidden):raise ValueError('Excluded name still present in visible script')
    if forbidden and not e.get('visual_redaction_review_complete'):raise ValueError('Review excluded people in every visual, including screenshots')
    return used

def create_music(path,duration):
    # Original sparse instrumental; no external copyrighted music samples.
    import numpy as np
    import soundfile as sf
    sr=24000;t=np.arange(math.ceil(duration*sr))/sr;mix=np.zeros_like(t)
    for onset in np.arange(0,duration,60/86*2):
        local=t-onset;mask=(local>=0)&(local<1.5);v=local[mask]
        for freq in [130.8128,164.8138,195.9977]:mix[mask]+=np.sin(2*np.pi*freq*v)*np.exp(-v*3.5)*.02
    sf.write(path,mix,sr)

def make_voice(e,base,cache):
    import numpy as np
    import soundfile as sf
    pipeline=None;pack=None;rows=[];whole=[];cursor=0
    model_revision=e.get('model_revision','01e7505bd6a7a2ac4975463114c3a7650a9f7218');speed=e.get('voice_speed',.92)
    for original in e['rows']:
        row=json.loads(json.dumps(original))
        source=(base/row['audio']).resolve() if row.get('audio') else None
        signature=key({'text':row['text'],'voice':e.get('voice','zf_001'),'speed':speed,'revision':model_revision,'source':digest(source) if source else None,'runtime':'v1'})
        output=cache/(signature+'.wav')
        if not output.exists():
            if source:ff(['-i',source,'-ac','1','-ar','24000',output])
            else:
                if pipeline is None:
                    import torch
                    from huggingface_hub import snapshot_download
                    from kokoro import KModel,KPipeline
                    torch.set_num_threads(min(4,os.cpu_count() or 2))
                    model_dir=Path(snapshot_download('hexgrad/Kokoro-82M-v1.1-zh',revision=model_revision,allow_patterns=['config.json','kokoro-v1_1-zh.pth',f'voices/{e.get("voice","zf_001")}.pt'],cache_dir=str(ROOT/'models')))
                    model=KModel(repo_id='hexgrad/Kokoro-82M-v1.1-zh',config=str(model_dir/'config.json'),model=str(model_dir/'kokoro-v1_1-zh.pth')).eval()
                    pipeline=KPipeline(lang_code='z',model=model,repo_id='hexgrad/Kokoro-82M-v1.1-zh',device='cpu')
                    pack=torch.load(model_dir/'voices'/f'{e.get("voice","zf_001")}.pt',weights_only=True)
                results=list(pipeline(row['text'],voice=pack,speed=speed))
                if not results or any(len(x.phonemes)>=510 for x in results):raise ValueError('Rewrite narration to avoid truncation')
                audio=np.concatenate([x.audio.numpy() for x in results]);active=np.flatnonzero(np.abs(audio)>.002)
                if not len(active):raise ValueError('Silent narration')
                audio=audio[max(0,active[0]-120):min(len(audio),active[-1]+1440)];sf.write(output,audio,24000)
        audio,sr=sf.read(output);pause=row.get('pause',.12)
        speech=len(audio)/sr
        if not rows and speech>3:raise ValueError('Rewrite hook: first spoken sentence must finish within 3 seconds')
        row.update(start=cursor,end=cursor+speech+pause,speechDuration=speech,audio=str(output),audioSha256=digest(output))
        rows.append(row);whole.extend([audio,np.zeros(round(pause*sr))]);cursor=row['end']
        print('VOICE',row['id'],round(speech,2),flush=True)
    if cursor>300:raise ValueError('Chinese movie exceeds five minutes')
    narration=cache/'narration.wav';sf.write(narration,np.concatenate(whole),24000)
    return rows,cursor,narration

def prepare_visuals(e,base,cache,rows):
    from fontTools.ttLib import TTFont
    public=RUNTIME/'public';shutil.rmtree(public,ignore_errors=True);public.mkdir()
    mapping={};access=[]
    for name,item in e.get('assets',{}).items():
        if not re.fullmatch(r'[a-zA-Z0-9_.-]+',name):raise ValueError('Unsafe asset filename')
        if item.get('derive_frame'):continue
        local=cache/name
        try:
            if item.get('file'):local=(base/item['file']).resolve()
            elif item.get('generate')=='testsrc2':
                if not e.get('technical_demo'):raise ValueError('Generated fixtures are limited to technical tests')
                if not local.exists():ff(['-f','lavfi','-i','testsrc2=size=960x540:rate=24','-t','30','-an','-c:v','libx264','-threads','2','-pix_fmt','yuv420p',local])
            else:
                fingerprint=local.with_suffix(local.suffix+'.url.json')
                if not local.exists() or not fingerprint.exists() or json.loads(fingerprint.read_text())['url']!=item['url']:
                    fetch(item['url'],local);write(fingerprint,{'url':item['url']})
            if not local.is_file():raise FileNotFoundError(name)
            if item.get('sha256') and digest(local)!=item['sha256']:raise ValueError('Asset hash changed: '+name)
            mapping[name]=local;access.append({'asset':name,'status':'已读取','sha256':digest(local)})
        except Exception as ex:
            access.append({'asset':name,'status':'没读到','reason':type(ex).__name__});write(cache/'source-access.json',access);raise
    for name,item in e.get('assets',{}).items():
        if not item.get('derive_frame'):continue
        d=item['derive_frame'];local=cache/name
        ff(['-ss',str(d['at']),'-i',mapping[d['asset']],'-frames:v','1','-vf','crop='+d['crop'],local])
        mapping[name]=local;access.append({'asset':name,'status':'已读取','derivedFrom':d,'sha256':digest(local)})
    for style in ['Light','Medium']:
        filename=f'NotoSansCJKsc-{style}.otf';local=cache/filename
        if not local.exists():fetch('https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/'+filename,local)
        shutil.copy(local,public/filename)
        cmap=TTFont(local).getBestCmap();missing=set()
        for row in rows:
            text=''.join(str(row.get(k,'')) for k in ['text','headline','chapter','factSource','screenSource','note','question'])+e['edition']+e.get('label','热议选编')+e.get('footer','有来源，再聊看法')
            text+=json.dumps(row.get('cover',[]),ensure_ascii=False)+json.dumps(row.get('items',[]),ensure_ascii=False)+json.dumps(row.get('tweet',{}),ensure_ascii=False)
            missing|={ch for ch in text if '\u4e00'<=ch<='\u9fff' and ord(ch) not in cmap}
        if missing:raise ValueError('Missing Chinese glyphs: '+''.join(sorted(missing)))
    for row in rows:
        if row['type']=='video':
            media=row['media'];p=mapping[media['asset']];duration=float(probe(p)['format']['duration'])
            if media['end']>duration+.02:raise ValueError('Source range exceeds original movie')
            folder=public/'frames'/str(row['id']);folder.mkdir(parents=True)
            ff(['-ss',str(media['start']),'-t',str(media['end']-media['start']),'-i',p,'-vf',f'crop={media["crop"]},fps=24,scale=968:-2','-an','-q:v','2',folder/'%04d.jpg'])
            row['frames']=len(list(folder.glob('*.jpg')));row['sourceSha256']=digest(p)
            if row['frames']<2:raise ValueError('No moving source frames')
        elif row['type']=='image':
            src=mapping[row['asset']];row['image']='image-'+str(row['id'])+src.suffix;shutil.copy(src,public/row['image'])
        elif row['type']=='cover':
            for i,v in enumerate(row.get('cover',[])):
                src=mapping[v['asset']];v['file']=f'cover-{i}'+src.suffix;shutil.copy(src,public/v['file'])
    # File hash manifest invalidates render cache when any font or image changes.
    return access,key([(str(p.relative_to(public)),digest(p)) for p in sorted(public.rglob('*')) if p.is_file()])

def mix(cache,narration,duration):
    music=cache/'music.wav';create_music(music,duration)
    voice=cache/'voice-normalized.wav';bed=cache/'music-normalized.wav';master=cache/'master.wav'
    ff(['-i',narration,'-af','loudnorm=I=-17:TP=-2:LRA=7','-ar','48000','-ac','2',voice])
    ff(['-i',music,'-af','loudnorm=I=-28:TP=-9:LRA=7','-ar','48000','-ac','2',bed])
    graph=f'[0:a]asplit=2[v][sc];[1:a][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=350[duck];[duck]asplit=2[dump][mixduck];[v][mixduck]amix=inputs=2:normalize=0,apad,afade=t=out:st={max(0,duration-.45)}:d=0.45,loudnorm=I=-16:TP=-1.5:LRA=7[out]'
    ff(['-i',voice,'-i',bed,'-filter_complex',graph,'-map','[out]','-t',str(duration),'-ar','48000','-ac','2',master,'-map','[dump]','-t',str(duration),'-ar','48000','-ac','2',cache/'ducked.wav']);return master

def audit(out,t,stt):
    import numpy as np
    from PIL import Image,ImageDraw
    movie=out/'final_1080p.mp4';p=probe(movie);v=next(x for x in p['streams'] if x['codec_type']=='video')
    assert (v['width'],v['height'])==(1080,1920) and v['avg_frame_rate']=='30/1'
    assert abs(float(p['format']['duration'])-t['duration'])<.15
    report={'schema':1,'language':'zh','duration':t['duration'],'encodedDuration':p['format']['duration'],'sha256':digest(movie),'sourceRangeOverlaps':0,'missingChineseGlyphs':0,'visualReview':'pending','humanListening':'pending','stt':'pending','exactDuplicatePairs':[],'frozenSourceShots':[],'ducking':'actual narration sidechain, threshold .05 / ratio 4 / attack 20ms / release 350ms'}
    # Compare final AAC to the actual mastered narration on every full sentence.
    def samples(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','1','-ar','16000','pipe:1']),dtype=np.float32)
    encoded=samples(movie);reference=samples(t['master']);correlations=[]
    meter=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    measurements=re.findall(r'\{\s*"input_i".*?\}',meter.stderr,re.S)
    report['encodedLoudness']=json.loads(measurements[-1])
    if float(report['encodedLoudness']['input_tp'])>=0:raise ValueError('Encoded audio clips')
    cache=Path(t['master']).parent;voice=samples(cache/'voice-normalized.wav');bed=samples(cache/'music-normalized.wav');duck=samples(cache/'ducked.wav')
    def rms(x):
        n=len(x)//1600;return np.sqrt(np.mean(x[:n*1600].reshape(n,1600)**2,axis=1))
    v,b,d=rms(voice),rms(bed),rms(duck);n=min(len(v),len(b),len(d));valid=(v[:n]>.05)&(b[:n]>.001)
    gains=20*np.log10((d[:n]+1e-9)/(b[:n]+1e-9));report['voicedMusicGainMedianDb']=float(np.median(gains[valid])) if valid.any() else None
    for row in t['rows']:
        a,b=round(row['start']*16000),round((row['start']+row['speechDuration'])*16000);x=reference[a:b];y=encoded[a:b]
        correlations.append(float(np.corrcoef(x,y)[0,1]) if len(x)==len(y) else 0)
    report['minEncodedAudioCorrelation']=min(correlations)
    if not np.isfinite(correlations).all() or min(correlations)<.98:raise ValueError('Encoded audio does not match approved master')
    allseen={};motion=[]
    for row in t['rows']:
        if row['type']!='video':continue
        files=sorted((RUNTIME/'public/frames'/str(row['id'])).glob('*.jpg'));chosen=[files[i] for i in sorted(set([0,len(files)//2,len(files)-1]))];shot=[]
        for file in chosen:
            h=digest(file);shot.append(h)
            if h in allseen and allseen[h]!=row['id']:report['exactDuplicatePairs'].append([allseen[h],row['id']])
            allseen[h]=row['id']
        if len(set(shot))==1:report['frozenSourceShots'].append(row['id'])
    # Source JPEG hash flags are diagnostics, not proof that the encoded video has frozen.
    # Never skip STT or encoded-frame transition sampling because of an isolated frame flag.
    report['sourceSampleReview']='review_required' if (report['exactDuplicatePairs'] or report['frozenSourceShots']) else 'passed'
    if report['sourceSampleReview']=='review_required':
        print('VISUAL_REVIEW_REQUIRED: source JPEG hash overlaps/frozen samples; inspect encoded 2fps contacts and all transitions',flush=True)
    sample_dir=out/'encoded-samples';sample_dir.mkdir(exist_ok=True)
    ff(['-i',movie,'-vf','fps=2,scale=144:256',sample_dir/'%04d.jpg'])
    pics=sorted(sample_dir.glob('*.jpg'))
    for n in range(0,len(pics),100):
        page=Image.new('RGB',(1440,2780),'#fafaf8');draw=ImageDraw.Draw(page)
        for i,file in enumerate(pics[n:n+100]):x=(i%10)*144;y=(i//10)*278;page.paste(Image.open(file),(x,y));draw.text((x+4,y+258),f'{(n+i)/2:.1f}s',fill='#111')
        page.save(out/f'contact-{n//100+1}.jpg',quality=90)
    cuts=out/'transitions';cuts.mkdir(exist_ok=True)
    for row in t['rows'][1:]:
        frames=[]
        for i in range(10):
            dest=cuts/f'{row["id"]}-{i}.jpg';ff(['-ss',str(max(0,row['start']-.4)+i/10),'-i',movie,'-frames:v','1','-vf','scale=108:192',dest]);frames.append(dest)
        strip=Image.new('RGB',(1080,192))
        for i,file in enumerate(frames):strip.paste(Image.open(file),(i*108,0));file.unlink()
        strip.save(cuts/f'{row["id"]}.jpg',quality=90)
    if stt:
        from faster_whisper import WhisperModel
        from opencc import OpenCC
        from pypinyin import lazy_pinyin
        from difflib import SequenceMatcher
        model=WhisperModel('small',device='cpu',compute_type='int8',download_root=str(ROOT/'models/whisper'),cpu_threads=min(4,os.cpu_count() or 2));cc=OpenCC('t2s');results=[]
        def phonetics(s):return ''.join(lazy_pinyin(re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]','',cc.convert(s.lower()))))
        for row in t['rows']:
            a,b=round(row['start']*16000),round((row['start']+row['speechDuration'])*16000)
            segments,_=model.transcribe(encoded[a:b],language='zh',beam_size=5,vad_filter=False,condition_on_previous_text=False)
            heard=''.join(x.text for x in segments);similarity=SequenceMatcher(None,phonetics(row['text']),phonetics(heard)).ratio();results.append({'id':row['id'],'expected':row['text'],'heard':heard,'phoneticSimilarity':similarity,'needsReview':similarity<.88})
        write(out/'stt.json',results);report['stt']='review_required' if any(x['needsReview'] for x in results) else 'passed'
    report['automaticTechnicalChecks']='passed_with_visual_warnings' if report['sourceSampleReview']=='review_required' else 'passed';write(out/'qa.json',report)
    return report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--episode',required=True);ap.add_argument('--stt',action='store_true');args=ap.parse_args()
    path=Path(args.episode).resolve();e=json.loads(path.read_text());validate(e);base=path.parent
    for tool in ['node','npm','ffmpeg','ffprobe']:
        if not shutil.which(tool):raise RuntimeError('Missing '+tool+' in cloud environment')
    command(['node',RUNTIME/'doctor.mjs'])
    run=ROOT/'runs'/e['id'];cache=run/'cache';out=run/'output';cache.mkdir(parents=True,exist_ok=True);out.mkdir(exist_ok=True)
    state=run/'state.json';globals()['RUN_STATE']=state;write(state,{'stage':'preparing','episodeHash':key(e)})
    if not e.get('direction'):raise ValueError('Write DIRECTION before creating shots')
    (run/'DIRECTION.md').write_text(e['direction'],encoding='utf8')
    rows,duration,narration=make_voice(e,base,cache);access,visual_hash=prepare_visuals(e,base,cache,rows);master=mix(cache,narration,duration)
    timeline={'language':'zh','edition':e['edition'],'label':e.get('label','热议选编'),'footer':e.get('footer','有来源，再聊看法'),'rows':rows,'duration':duration,'fps':30,'output':str(out),'cache':str(cache),'master':str(master),'visualManifestSha256':visual_hash,'episodeHash':key(e)}
    write(RUNTIME/'timeline.json',timeline);write(out/'timeline.json',timeline);write(out/'source-access.json',{'assets':access,'accounts':e.get('source_access',[])})
    (out/'narration.md').write_text('\n\n'.join(x['text'] for x in rows),encoding='utf8');(out/'brief.md').write_text(e.get('brief','技术流程检查片，不是新闻成片。'),encoding='utf8')
    (out/'sources.md').write_text('\n\n'.join(f'{fid} · {f["status"]}\n'+f['text']+'\n'+'\n'.join(f['urls']) for fid,f in e.get('facts',{}).items()),encoding='utf8')
    def stamp(sec):
        ms=round(sec*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
    (out/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(r["start"])} --> {stamp(r["end"])}\n{r["text"]}' for i,r in enumerate(rows)),encoding='utf8')
    shutil.copy(master,out/'narration_mix.wav');write(state,{'stage':'rendering','episodeHash':key(e),'masterSha256':digest(master)})
    subprocess.run(['npm','run','build'],cwd=RUNTIME,check=True);subprocess.run(['node','render.mjs'],cwd=RUNTIME,check=True)
    report=audit(out,timeline,args.stt)
    write(state,{'stage':'exported_awaiting_review','episodeHash':key(e),'videoSha256':report['sha256'],'stt':report['stt'],'visualReview':'pending','humanListening':'pending'})
    (out/'READ_ME.md').write_text('中文云端导出包。必须查看 contact-*.jpg、keyframes、transitions，并核对 STT 后才可称为交付通过。qa.json 的 pending 不能写成已通过。未对外发布。',encoding='utf8')
    with zipfile.ZipFile(run/'delivery.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob('*'):
            if p.is_file():z.write(p,p.relative_to(out))
    print('EXPORTED',run/'delivery.zip',flush=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        if globals().get('RUN_STATE'):
            previous=json.loads(RUN_STATE.read_text());write(RUN_STATE,{**previous,'stage':'failed','failedDuring':previous['stage'],'reason':str(exc)})
        raise
