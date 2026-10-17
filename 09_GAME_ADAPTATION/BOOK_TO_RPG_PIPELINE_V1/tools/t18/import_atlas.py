"""Mechanical atlas extraction and indexed conversion for the native asset encoder."""
from pathlib import Path
from PIL import Image
import json,base64,sys
book=Path(sys.argv[1]);project=Path(sys.argv[2]);out=Path(sys.argv[3])
palette=json.loads((project/'assets/generated/colors/project-standard.json').read_text())['colors']
image=Image.open(book/'art/t18/environment-atlas.png').convert('RGBA')
swatch=Image.new('P',(1,1));swatch.putpalette(sum(palette,[]))
specs=[('cupboard',(0,0,448,632),48),('moon-window',(448,0,885,632),64),('coat-rack',(885,0,1280,632),36),('winter-tree',(0,632,448,1280),72),('snow-wood',(448,632,885,1280),52),('stone-lantern',(885,632,1280,1280),36)]
pack={}
for name,box,width in specs:
 a=image.crop(box);a=a.crop(a.getchannel('A').getbbox());a=a.resize((width,round(a.height*width/a.width)),Image.Resampling.NEAREST)
 indexed=a.convert('RGB').quantize(palette=swatch,dither=Image.Dither.NONE);pixels=bytearray(indexed.tobytes());alpha=a.getchannel('A').tobytes()
 for i,v in enumerate(alpha):
  if v<128:pixels[i]=255
  elif pixels[i]==255:
   rgb=a.getpixel((i%a.width,i//a.width))[:3];pixels[i]=min(range(255),key=lambda n:sum((palette[n][j]-rgb[j])**2 for j in range(3)))
 indexed.frombytes(bytes(pixels));indexed.info['transparency']=255
 indexed.save(book/f'art/t18/{name}.png')
 pack[name]={'width':a.width,'height':a.height,'pixels':base64.b64encode(pixels).decode(),'opaque':base64.b64encode(bytes(v!=255 for v in pixels)).decode()}
out.write_text(json.dumps(pack,separators=(',',':')))
print('T18_ORIGINAL_ENVIRONMENT_ASSETS_READY',len(pack))
