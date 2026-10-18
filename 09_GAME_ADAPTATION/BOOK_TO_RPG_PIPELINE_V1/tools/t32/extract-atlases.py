"""Mechanical sprite-cell extraction only: preserve original alpha, no painting/rig warping."""
from PIL import Image
from pathlib import Path
import sys
src=Path(sys.argv[1]);out=Path(sys.argv[2]);im=Image.open(src).convert('RGBA')
roles=['merchant','neighbor','stranger','visitor','operative','performer']
for i,role in enumerate(roles):
 x0=round(i*im.width/6);x1=round((i+1)*im.width/6);col=im.crop((x0,0,x1,im.height));a=col.getchannel('A');runs=[];start=None
 for y in range(im.height):
  active=sum(v>128 for v in a.crop((0,y,a.width,y+1)).getdata())>10
  if active and start is None:start=y
  if start is not None and (not active or y==im.height-1):
   end=y if not active else y+1
   if end-start>im.height/8:runs.append((start,end))
   start=None
 assert len(runs)==4,(role,runs)
 for d,(top,bottom) in enumerate(runs):
  frame=col.crop((0,max(0,top-2),col.width,min(im.height,bottom+2)));box=frame.getchannel('A').getbbox();frame=frame.crop(box)
  frame.save(out/f'npc-{role}-{d}.webp',quality=90,method=6)
 print(role,runs)
