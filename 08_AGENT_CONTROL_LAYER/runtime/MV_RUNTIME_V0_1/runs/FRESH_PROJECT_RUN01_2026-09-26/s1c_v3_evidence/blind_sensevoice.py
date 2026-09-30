import json, time, hashlib, re, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
import sherpa_onnx

ROOT = Path(__file__).resolve().parent
MODEL = Path('/tmp/s1c-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17')
subprocess.run(['ffmpeg','-y','-v','error','-i',str(ROOT/'full.mp3'),'-ar','16000','-ac','1',str(ROOT/'full_16k.wav')],check=True)
audio, sr = sf.read(ROOT/'full_16k.wav',dtype='float32')
recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(model=str(MODEL/'model.int8.onnx'),tokens=str(MODEL/'tokens.txt'),num_threads=4,language='zh',use_itn=False)
rows=[]
for start in range(0,int(len(audio)/sr),20):
    end=min(start+30,len(audio)/sr)
    stream=recognizer.create_stream()
    stream.accept_waveform(sr,audio[start*sr:round(end*sr)])
    t=time.monotonic()
    recognizer.decode_stream(stream)
    row={'start':start,'end':round(end,6),'text':stream.result.text,'tokens':stream.result.tokens,'timestamps':[round(start+x,3) for x in stream.result.timestamps],'elapsed':round(time.monotonic()-t,2)}
    rows.append(row)
    (ROOT/'sensevoice_raw_private.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in row.items() if k not in ['tokens','timestamps']},ensure_ascii=False),flush=True)
print('DONE',flush=True)
