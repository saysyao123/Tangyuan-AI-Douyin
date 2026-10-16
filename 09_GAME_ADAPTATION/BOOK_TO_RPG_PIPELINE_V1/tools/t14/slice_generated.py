from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
import numpy as np,json,re,sys
from scipy import ndimage
root=Path(__file__).resolve().parents[2];out=root/'art/t14';out.mkdir(parents=True,exist_ok=True);source=Path(sys.argv[1]);images={};sources={}
# Import authoritative standing images only; animation is authored in native sprite code.
for role,name,height,canvas in [('hero','boy-original.png',50,(36,56)),('child','girl-original.png',38,(32,44))]:
 im=Image.open(source/name);cuts=[]
 mask=np.array(im.getchannel('A'))>=200;labels,n=ndimage.label(ndimage.binary_dilation(mask,iterations=2));regions=[]
 for label,sl in enumerate(ndimage.find_objects(labels),1):
  if sl is None:continue
  y,x=sl;area=int(np.count_nonzero(labels[sl]==label))
  if area>5000 and (x.start+x.stop)/2<im.width/3:regions.append((y.start,y.stop,x.start,x.stop,area))
 regions.sort();assert len(regions)==4,(role,regions)
 for y0,y1,x0,x1,_ in regions:
  a=im.crop((x0,y0,x1,y1)).convert('RGBA');alpha=a.getchannel('A').point(lambda a:255 if a>=200 else 0);a.putalpha(alpha);bbox=alpha.getbbox();print(role,len(cuts),bbox);cuts.append(a.crop(bbox))
 if role=='hero':cuts[1]=ImageOps.mirror(cuts[2]) # audited back-left from valid back-right source; never swap metadata silently.
 scale=height/max(a.height for a in cuts)
 sheet=Image.new('RGBA',(canvas[0]*4,canvas[1]))
 for row,a in enumerate(cuts):
  a=a.resize((round(a.width*scale),round(a.height*scale)),Image.Resampling.NEAREST);sheet.alpha_composite(a,(row*canvas[0]+(canvas[0]-a.width)//2,canvas[1]-3-a.height))
 bust=cuts[0].crop((0,0,cuts[0].width,round(cuts[0].height*.49)));bust.thumbnail((60,72),Image.Resampling.NEAREST);portrait=Image.new('RGBA',(64,72));portrait.alpha_composite(bust,((64-bust.width)//2,72-bust.height));images['portrait-'+role]=portrait;sources['portrait-'+role]={'file':'portrait-'+role+'.png','frameWidth':64,'frameHeight':72,'frames':1,'kind':'portrait'}
 images[role]=sheet;sources[role]={'file':role+'.png','frameWidth':canvas[0],'frameHeight':canvas[1],'frames':4,'logicalHeight':height,'directions':['SW','NW','NE','SE']}
im=Image.open(source/'environment-original.png').convert('RGBA')
for role,box,size in [('stall',(0,70,455,510),(80,72)),('stage',(455,0,1000,520),(128,100)),('house',(995,0,1536,540),(128,112)),('gate',(0,510,555,1024),(96,96)),('pot',(590,630,930,1024),(36,40)),('tree',(990,500,1536,1024),(72,88))]:
 a=im.crop(box);alpha=a.getchannel('A').point(lambda x:255 if x>=200 else 0);a.putalpha(alpha);a=a.crop(alpha.getbbox());a.thumbnail(size,Image.Resampling.NEAREST);sheet=Image.new('RGBA',size);sheet.alpha_composite(a,((size[0]-a.width)//2,size[1]-a.height));images[role]=sheet;sources[role]={'file':role+'.png','frameWidth':size[0],'frameHeight':size[1],'frames':1}
# Six independently generated NPC designs, no reuse of the hero's face.
im=Image.open(source/'npc-original.png').convert('RGBA')
for i,role in enumerate(['merchant','officer','stranger','neighbor','performer','visitor']):
 col=i%3;row=i//3;a=im.crop((col*im.width//3,row*im.height//2,(col+1)*im.width//3,(row+1)*im.height//2));alpha=a.getchannel('A').point(lambda x:255 if x>=200 else 0);a.putalpha(alpha);a=a.crop(alpha.getbbox());scale=50/a.height;b=a.resize((round(a.width*scale),50),Image.Resampling.NEAREST);sheet=Image.new('RGBA',(36,56));sheet.alpha_composite(b,((36-b.width)//2,3));images[role]=sheet;sources[role]={'file':role+'.png','frameWidth':36,'frameHeight':56,'frames':1}
 bust=a.crop((0,0,a.width,round(a.height*.49)));bust.thumbnail((60,72),Image.Resampling.NEAREST);portrait=Image.new('RGBA',(64,72));portrait.alpha_composite(bust,((64-bust.width)//2,72-bust.height));images['portrait-'+role]=portrait;sources['portrait-'+role]={'file':'portrait-'+role+'.png','frameWidth':64,'frameHeight':72,'frames':1,'kind':'portrait'}
# Keep original authored palette slots; allocate remaining191 to the GPT set.
s=(root/'tools/type_pal_t1_art.ts').read_text();old=re.search(r"export const colors = \[(.*?)\]\.map",s,re.S).group(1);old=[tuple(bytes.fromhex(x)) for x in re.findall(r"'([0-9a-f]{6})'",old)]
ground=[(178,166,143),(154,147,132),(131,130,118),(108,112,107),(84,94,94),(71,80,83),(213,219,212),(235,235,217),(98,86,71),(123,108,85),(102,114,92),(76,91,77),(179,130,81),(214,165,103),(68,57,53),(142,85,65)]
cloud=[]
for im in images.values():
 arr=np.array(im);cloud.extend(arr[arr[:,:,3]>200,:3].tolist())
flat=Image.new('RGB',(len(cloud),1));flat.putdata([tuple(x) for x in cloud]);q=flat.quantize(colors=191,method=Image.Quantize.MEDIANCUT);new=[tuple(q.getpalette()[i:i+3]) for i in range(0,573,3)];colors=old+ground+new+[(255,0,255)];assert len(colors)==256
palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c]);catalog={'version':1,'palette':colors,'sources':sources,'generation':'Built-in GPT image generation; transparent source atlases privately retained; no PAL source images used as generation inputs.','animation':'Four audited standing views plus explicit native three-pose leg/arm rig; fixed frame foot anchors.'}
contact=Image.new('RGB',(1000,800),'#273432');d=ImageDraw.Draw(contact)
for i,(role,im) in enumerate(images.items()):
 ix=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE);a=np.array(ix);a[np.array(im)[:,:,3]<128]=255;ix=Image.fromarray(a.astype('uint8'),'P');ix.putpalette(palette.getpalette());ix.info['transparency']=255
 if role in ['tree','stage','gate','house','stall','pot']:
  mask=a!=255;parts,n=ndimage.label(ndimage.binary_dilation(mask,iterations=2));keep=1+int(np.argmax([np.sum(mask&(parts==k)) for k in range(1,n+1)]));a[mask&(parts!=keep)]=255;ix=Image.fromarray(a.astype('uint8'),'P');ix.putpalette(palette.getpalette());ix.info['transparency']=255
 ix.save(out/(role+'.png'),optimize=True)
 v=ix.convert('RGBA');v.thumbnail((240,112),Image.Resampling.NEAREST);x=(i%4)*250;y=(i//4)*130;contact.paste(v,(x,y+12),v);d.text((x+2,y),role,fill='white')
(out/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n');contact.save(out/'contact.png')
print('Normalized public original GPT assets',[(p.name,p.stat().st_size) for p in out.iterdir()])
