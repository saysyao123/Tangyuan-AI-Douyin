"""Independent STT on the already rendered final AAC, without rebuilding video."""
import json, pathlib, subprocess, re, hashlib, sys
from difflib import SequenceMatcher
import numpy as np
from faster_whisper import WhisperModel
from opencc import OpenCC
from pypinyin import lazy_pinyin
source=pathlib.Path(sys.argv[1]); dest=pathlib.Path(sys.argv[2]);dest.mkdir(parents=True,exist_ok=True)
movie=source/'final_1080p.mp4'
t=json.loads((source/'timeline.json').read_text(encoding='utf8'))
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)]))
video=next(x for x in meta['streams'] if x['codec_type']=='video')
assert(video['width'],video['height'],video['codec_name'])==(1080,1920,'h264')
def samples(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar','16000','-ac','1','-f','f32le','pipe:1']),dtype=np.float32)
encoded=samples(movie)
master=samples(source/'narration_mix.wav')
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4)
cc=OpenCC('t2s')
def normal(s):
    return ''.join(lazy_pinyin(re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]','',cc.convert(s.lower()))))
results=[]
for index,row in enumerate(t['rows']):
    a,b=round(row['start']*16000),round((row['start']+row['speechDuration'])*16000)
    x=encoded[a:b]; y=master[a:b]
    correlation=float(np.corrcoef(x,y)[0,1]) if len(x)==len(y) and len(x)>200 else 0.0
    segments,_=model.transcribe(x,language='zh',beam_size=5,vad_filter=False,condition_on_previous_text=False)
    heard=''.join(s.text for s in segments)
    similarity=SequenceMatcher(None,normal(row['text']),normal(heard)).ratio()
    rec={'id':row['id'],'expected':row['text'],'heard':heard,'phoneticSimilarity':round(similarity,5),'needsReview':similarity<0.88,'aacCorrelation':round(correlation,6)}
    results.append(rec)
    print('STT',index+1,'/',len(t['rows']),'ID',row['id'],'sim',round(similarity,3),'AAC',round(correlation,5),flush=True)
out={'video':'final_1080p.mp4','video_sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'duration':float(meta['format']['duration']),'width':video['width'],'height':video['height'],'fps':video['avg_frame_rate'],'count':len(results),'needsReview':[r['id'] for r in results if r['needsReview']],'minimumAACCorrelation':min(r['aacCorrelation'] for r in results),'status':'automatic_pass' if all(not r['needsReview'] and r['aacCorrelation']>=0.98 for r in results) else 'review_needed','humanListening':'pending'}
(dest/'independent_stt.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
(dest/'independent_qa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('RESULT',json.dumps(out,ensure_ascii=False),flush=True)
