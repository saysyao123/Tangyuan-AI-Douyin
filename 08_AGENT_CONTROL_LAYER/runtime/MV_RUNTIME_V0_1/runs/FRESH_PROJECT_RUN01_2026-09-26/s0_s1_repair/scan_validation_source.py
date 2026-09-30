import json,re,hashlib,subprocess,argparse
from pathlib import Path
from difflib import SequenceMatcher
import sherpa_onnx,soundfile as sf
from opencc import OpenCC
R=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--model-dir',type=Path,required=True)
M=parser.parse_args().model_dir
subprocess.run(['ffmpeg','-y','-v','error','-i',str(R/'validation_full.mp3'),'-ac','1','-ar','16000',str(R/'validation_full_16k.wav')],check=True)
a,sr=sf.read(R/'validation_full_16k.wav',dtype='float32')
rec=sherpa_onnx.OfflineRecognizer.from_sense_voice(model=str(M/'model.int8.onnx'),tokens=str(M/'tokens.txt'),num_threads=4,language='zh',use_itn=False)
cc=OpenCC('t2s')
def norm(s):return re.sub(r'[^\u4e00-\u9fff]','',cc.convert(s))
lyrics=norm((R/'trusted_lyrics_private.txt').read_text())
rows=[];private=[]
for start in range(0,int(len(a)/sr),30):
 end=min(start+30,len(a)/sr);s=rec.create_stream();s.accept_waveform(sr,a[start*sr:round(end*sr)]);rec.decode_stream(s)
 text=s.result.text;n=norm(text);match=SequenceMatcher(None,n,lyrics,autojunk=False).find_longest_match()
 row={'start_seconds':start,'end_seconds':round(end,6),'asr_chars':len(n),'transcript_sha256':hashlib.sha256(n.encode()).hexdigest(),'trusted_contiguous_match_chars':match.size,'support':'SUPPORTS' if match.size>=6 else 'INSUFFICIENT','review_status':'NOT_HUMAN_LOCKED'}
 rows.append(row);private.append({'start':start,'text':text,'tokens':s.result.tokens,'timestamps':[round(start+t,3) for t in s.result.timestamps]})
 (R/'asr_private.json').write_text(json.dumps(private,ensure_ascii=False,indent=2))
 print(json.dumps(row),flush=True)
report={'method':'BLIND_SENSEVOICE_ALL_DECODED_AUDIO_THEN_TRUSTED_TEXT_COMPARISON','source_sha256':hashlib.sha256((R/'validation_full.mp3').read_bytes()).hexdigest(),'model_name':M.name,'lyric_prompt_supplied_to_recognizer':False,'decoded_duration_seconds':len(a)/sr,'rows':rows,'supporting_window_count':sum(r['support']=='SUPPORTS' for r in rows),'human_audio_review':'PENDING','formal_s1_seal':False,'asr_alone_can_seal':False}
(R/'full_scan_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('DONE',flush=True)
