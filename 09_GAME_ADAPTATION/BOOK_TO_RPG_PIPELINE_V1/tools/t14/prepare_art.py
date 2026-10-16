"""Read authored indexed PNG inputs into the official RLE encoder's plain frame contract."""
from PIL import Image
from pathlib import Path
import json,sys,base64
source=Path(sys.argv[1]);catalog=json.loads((source/'catalog.json').read_text());out={'palette':catalog['palette'],'sprites':{},'portraits':{}}
for role,spec in catalog['sources'].items():
 p=source/spec['file'];im=Image.open(p)
 if spec.get('kind')=='portrait':out['portraits'][role.removeprefix('portrait-')]=base64.b64encode(p.read_bytes()).decode();continue
 assert im.mode=='P';frames=[]
 for i in range(spec['frames']):
  a=im.crop((i*spec['frameWidth'],0,(i+1)*spec['frameWidth'],spec['frameHeight']));pixels=a.tobytes();opaque=bytes(0 if v==255 else 1 for v in pixels)
  frames.append({'width':a.width,'height':a.height,'pixels':base64.b64encode(pixels).decode(),'opaque':base64.b64encode(opaque).decode()})
 out['sprites'][role]=frames
Path(sys.argv[2]).write_text(json.dumps(out,separators=(',',':'))+'\n');print('T14_INDEXED_ART_INPUTS_READY',len(out['sprites']),'sprite sheets',len(out['portraits']),'portraits')
