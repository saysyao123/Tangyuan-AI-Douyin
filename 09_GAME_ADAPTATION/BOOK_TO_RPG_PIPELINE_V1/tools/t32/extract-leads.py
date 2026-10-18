from PIL import Image,ImageOps
from pathlib import Path
import sys
im=Image.open(sys.argv[1]).convert('RGBA');out=Path(sys.argv[2]);frames=[]
for colid in range(6):
 col=im.crop((round(colid*im.width/6),0,round((colid+1)*im.width/6),im.height));a=col.getchannel('A');runs=[];start=None
 for y in range(im.height):
  active=sum(v>128 for v in a.crop((0,y,a.width,y+1)).getdata())>8
  if active and start is None:start=y
  if start is not None and (not active or y==im.height-1):
   end=y if not active else y+1
   if end-start>im.height/8:runs.append((start,end))
   start=None
 assert len(runs)==4,(colid,runs)
 for d,(top,bottom) in enumerate(runs):
  a=col.crop((0,max(0,top-2),col.width,min(im.height,bottom+2)));a=a.crop(a.getchannel('A').getbbox())
  # Generated first row faces opposite the native SW slot; use its exact mirror.
  if d==0:a=ImageOps.mirror(a)
  frames.append((colid,d,a))
for role,cols in [('hero',range(3)),('child',range(3,6))]:
 group=[a for c,d,a in frames if c in cols];w=max(a.width for a in group)+8;h=max(a.height for a in group)+4
 for c,d,a in frames:
  if c not in cols:continue
  canvas=Image.new('RGBA',(w,h));canvas.alpha_composite(a,((w-a.width)//2,h-a.height));canvas.save(out/f'lead-{role}-{d}-{c%3}.webp',quality=91,method=5)
 print(role,w,h)
