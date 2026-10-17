"""Compile checked-in indexed original sprites into plain frames for the native encoder."""
from pathlib import Path
from PIL import Image
import json,base64,sys
book=Path(sys.argv[1]);project=Path(sys.argv[2]);out=Path(sys.argv[3]);pack={}
for name in ['cupboard','moon-window','coat-rack','winter-tree','snow-wood','stone-lantern']:
 im=Image.open(book/f'art/t18/{name}.png');assert im.mode=='P';pixels=im.tobytes()
 pack[name]={'width':im.width,'height':im.height,'pixels':base64.b64encode(pixels).decode(),'opaque':base64.b64encode(bytes(v!=255 for v in pixels)).decode()}
out.write_text(json.dumps(pack,separators=(',',':')))
print('T18_ORIGINAL_ENVIRONMENT_ASSETS_READY',len(pack))
