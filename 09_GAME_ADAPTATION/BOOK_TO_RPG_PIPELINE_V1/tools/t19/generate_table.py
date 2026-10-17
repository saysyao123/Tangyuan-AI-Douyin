#!/usr/bin/env python3
"""T19 P2 isolated indexed 80x48 meal-table candidate; original art, no story changes."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, gzip, struct, sys
BOOK=Path(__file__).resolve().parents[2]
PALETTE=json.loads((BOOK/'art/t14/catalog.json').read_text())['palette']
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else BOOK/'art/t19/preview'
OUT.mkdir(parents=True,exist_ok=True)
im=Image.new('RGBA',(80,48));d=ImageDraw.Draw(im)
D='#38291e';SIDE='#65452d';TOP='#9d7550';LIT='#b58a59';GRAIN='#785237';RIM='#453025'
for x in (13,62):
 d.polygon([(x,23),(x+6,25),(x+6,45),(x+2,46)],fill=D)
 d.line((x+1,26,x+1,44),fill=SIDE)
d.polygon([(39,9),(77,20),(41,34),(3,21)],fill=RIM)
d.polygon([(39,11),(74,20),(40,31),(6,21)],fill=TOP)
for k in range(27):
 x=10+(k*13)%60;y=16+(k*7)%14
 if 7<=x<=72 and y<27:d.point((x,y),fill=GRAIN if k%3 else LIT)
d.polygon([(4,21),(40,34),(40,38),(5,25)],fill='#533625')
d.polygon([(40,34),(77,20),(77,25),(40,38)],fill=SIDE)
d.line((7,23,39,35),fill=LIT);d.line((41,35,74,23),fill=GRAIN)
d.line((18,36,63,37),fill=RIM,width=2)
for cx,cy in [(24,16),(52,19)]:
 d.ellipse((cx-8,cy-3,cx+8,cy+4),fill='#3d4043')
 d.ellipse((cx-7,cy-4,cx+7,cy+1),fill='#d4c2a1')
 d.ellipse((cx-6,cy-3,cx+6,cy),fill='#ae6e38')
 for ox,oy in [(-3,-1),(0,-2),(3,-1)]:d.point((cx+ox,cy+oy),fill='#e8c182')
 d.point((cx+1,cy-1),fill='#547455')
 d.line((cx-6,cy+2,cx+5,cy+2),fill='#8e9590')
d.line((48,24,58,21),fill='#453222');d.line((49,26,59,23),fill='#cda16a')
pal=Image.new('P',(1,1));pal.putpalette(sum(PALETTE,[]))
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE)
pixels=bytearray(q.tobytes());alpha=im.getchannel('A').tobytes()
for i,v in enumerate(alpha):
 if v<128:pixels[i]=255
 elif pixels[i]==255:
  rgb=im.getpixel((i%80,i//80))[:3]
  pixels[i]=min(range(255),key=lambda j:sum((PALETTE[j][k]-rgb[k])**2 for k in range(3)))
q=Image.frombytes('P',(80,48),bytes(pixels));q.putpalette(sum(PALETTE,[]))
q.save(OUT/'noodle-table-preview.png',transparency=255)
# Pinned Type PAL GPL-3.0 sprite RLE, a single frame: u16 word-offset(1), u16 width/height, <=127 RLE runs.
frame=bytearray(struct.pack('<HH',80,48));i=0
while i<len(pixels):
 on=pixels[i]!=255;j=i
 while j<len(pixels) and j-i<127 and (pixels[j]!=255)==on:j+=1
 n=j-i;frame.append(n if on else 128+n)
 if on:frame.extend(pixels[i:j])
 i=j
raw=bytearray(struct.pack('<H',1));raw.extend(frame)
if len(raw)&1:raw.append(0)
data=gzip.compress(raw,mtime=0)
(OUT/'noodle-table-preview.rle').write_bytes(data)
meta={'size':[80,48],'frames':1,'opaque':sum(v!=255 for v in pixels),
 'sha256':hashlib.sha256(data).hexdigest(),'source':'original hand-authored 80x48 pixel design',
 'gate':'isolated P2 preview only; not approved production asset'}
(OUT/'MANIFEST.json').write_text(json.dumps(meta,indent=2)+'\n')
print('T19_TABLE_GENERATED',json.dumps(meta))
