"""Normalize two new GPT sources into the existing original shared palette."""
from PIL import Image
from pathlib import Path
from scipy.ndimage import label,binary_dilation
import numpy as np,json,sys
book=Path(__file__).resolve().parents[2];source=Path(sys.argv[1]);out=book/'art/t15';out.mkdir(exist_ok=True)
colors=json.loads((book/'art/t14/catalog.json').read_text())['palette'];palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c])
def subject(im):
 a=np.array(im);mask=a[:,:,3]>=200;l,n=label(binary_dilation(mask,iterations=2));areas=[np.sum(mask&(l==k)) for k in range(1,n+1)];keep=1+int(np.argmax(areas));a[:,:,3]=np.where(mask&(l==keep),255,0).astype('uint8');im=Image.fromarray(a,'RGBA');return im.crop(im.getchannel('A').getbbox())
def save(im,name):
 a=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE);v=np.array(a);v[np.array(im)[:,:,3]<128]=255;a=Image.fromarray(v,'P');a.putpalette(palette.getpalette());a.save(out/name,transparency=255,optimize=True)
a=subject(Image.open(source/'rental-original.png').convert('RGBA'));a.thumbnail((208,144),Image.Resampling.NEAREST);sheet=Image.new('RGBA',(208,144));sheet.alpha_composite(a,((208-a.width)//2,144-a.height));save(sheet,'rental.png')
im=Image.open(source/'operative-original.png').convert('RGBA');sheet=Image.new('RGBA',(36*4,56))
for i in range(4):
 x=i%2*im.width//2;y=i//2*im.height//2;a=subject(im.crop((x,y,x+im.width//2,y+im.height//2)));a=a.resize((round(a.width*50/a.height),50),Image.Resampling.NEAREST);sheet.alpha_composite(a,(i*36+(36-a.width)//2,3))
save(sheet,'operative.png');catalog={'palette':colors,'sources':{'rental':{'file':'rental.png','frameWidth':208,'frameHeight':144,'frames':1},'operative':{'file':'operative.png','frameWidth':36,'frameHeight':56,'frames':4}}};(out/'catalog.json').write_text(json.dumps(catalog,indent=2)+'\n');print('T15_NEW_ART_NORMALIZED')
