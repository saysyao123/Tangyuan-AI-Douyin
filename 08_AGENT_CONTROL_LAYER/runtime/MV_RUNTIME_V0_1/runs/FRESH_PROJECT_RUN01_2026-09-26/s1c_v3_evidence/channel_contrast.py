import json,time,subprocess
from pathlib import Path
import numpy as np,soundfile as sf,sherpa_onnx
root=Path(__file__).resolve().parent
model=Path('/tmp/s1c-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17')
subprocess.run(['ffmpeg','-y','-v','error','-i',str(root/'full.mp3'),'-ar','16000',str(root/'stereo_16k.wav')],check=True)
a,sr=sf.read(root/'stereo_16k.wav',dtype='float32')
r=sherpa_onnx.OfflineRecognizer.from_sense_voice(model=str(model/'model.int8.onnx'),tokens=str(model/'tokens.txt'),num_threads=4,language='zh',use_itn=False)
report={'correlation':float(np.corrcoef(a.T)[0,1]),'mid_rms':float(np.sqrt(np.mean(((a[:,0]+a[:,1])/2)**2))),'side_rms':float(np.sqrt(np.mean(((a[:,0]-a[:,1])/2)**2))),'rows':[]}
for name,x in [('left',a[:,0]),('right',a[:,1]),('side',(a[:,0]-a[:,1])/2)]:
 for start in range(0,int(len(x)/sr),20):
  end=min(start+30,len(x)/sr)
  s=r.create_stream();s.accept_waveform(sr,x[start*sr:round(end*sr)]);r.decode_stream(s)
  row={'channel':name,'start':start,'end':round(end,6),'text':s.result.text,'tokens':s.result.tokens,'timestamps':[round(start+t,3) for t in s.result.timestamps]}
  report['rows'].append(row)
  (root/'channel_raw_private.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
  print(json.dumps({k:v for k,v in row.items() if k not in ['tokens','timestamps']},ensure_ascii=False),flush=True)
print('DONE',flush=True)
