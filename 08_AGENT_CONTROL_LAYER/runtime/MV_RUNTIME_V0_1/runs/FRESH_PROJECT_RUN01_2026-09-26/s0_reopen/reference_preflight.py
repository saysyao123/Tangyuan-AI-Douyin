"""Bounded S0 reference screening; no full-song timeline or final selection."""
import json,re,subprocess,hashlib
from pathlib import Path
import sherpa_onnx,soundfile as sf
from opencc import OpenCC
R=Path(__file__).resolve().parent
M=Path('/tmp/s1c-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17')
rec=sherpa_onnx.OfflineRecognizer.from_sense_voice(model=str(M/'model.int8.onnx'),tokens=str(M/'tokens.txt'),num_threads=4,language='zh',use_itn=False)
cc=OpenCC('t2s')
def norm(s):return re.sub(r'[^\u4e00-\u9fff]','',cc.convert(s))
for cid in ('B','C'):
 meta=json.loads((R/f'{cid}_meta_private.json').read_text())
 target=R/f'{cid}_reference_90s.wav'
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(R/f'{cid}_reference_partial.mp3'),'-t','90','-ac','1','-ar','16000',str(target)],check=True)
 a,sr=sf.read(target,dtype='float32');lyrics=norm(meta.get('lyric_text') or '')
 rows=[]
 for start in (0,30,60):
  end=min(start+30,len(a)/sr);s=rec.create_stream();s.accept_waveform(sr,a[start*sr:round(end*sr)]);rec.decode_stream(s)
  text=s.result.text;n=norm(text)
  # Longest contiguous match is supporting evidence only, never final human lock.
  from difflib import SequenceMatcher
  match=SequenceMatcher(None,n,lyrics,autojunk=False).find_longest_match()
  row={'start':start,'end':end,'text':text,'asr_char_count':len(n),'asr_sha256':hashlib.sha256(n.encode()).hexdigest(),'trusted_lyric_chars':len(lyrics),'longest_contiguous_match_chars':match.size,'trusted_text_match':bool(lyrics and match.size>=6)}
  rows.append(row);print(json.dumps({'id':cid,**row},ensure_ascii=False),flush=True)
 (R/f'{cid}_preflight_private.json').write_text(json.dumps({'meta':meta,'rows':rows,'preview_duration':len(a)/sr},ensure_ascii=False,indent=2))
