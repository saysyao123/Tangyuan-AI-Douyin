"""Import the generated night prop atlas using the established original palette."""
from PIL import Image
from pathlib import Path
import numpy as np,json,sys
from scipy.ndimage import label,binary_dilation
book=Path(__file__).resolve().parents[2];out=book/'art/t16';out.mkdir(exist_ok=True)
colors=json.loads((book/'art/t14/catalog.json').read_text())['palette'];pal=Image.new('P',(1,1));pal.putpalette([v for c in colors for v in c]);src=Image.open(sys.argv[1]).convert('RGBA')
def subject(im):
 a=np.array(im);mask=a[:,:,3]>=200;l,n=label(binary_dilation(mask,iterations=2));areas=[np.sum(mask&(l==k)) for k in range(1,n+1)];keep=1+int(np.argmax(areas));a[:,:,3]=np.where(mask&(l==keep),255,0).astype('uint8');im=Image.fromarray(a);return im.crop(im.getchannel('A').getbbox())
source={}
for role,box,size in [('truck',(0,0,780,625),(160,112)),('night-shop',(790,0,1536,625),(176,144)),('bed',(0,625,790,1024),(96,72)),('television',(790,625,1536,1024),(56,64))]:
 a=subject(src.crop(box));a.thumbnail(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',size);canvas.alpha_composite(a,((size[0]-a.width)//2,size[1]-a.height));p=canvas.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE);v=np.array(p);v[np.array(canvas)[:,:,3]<128]=255;p=Image.fromarray(v);p.putpalette(pal.getpalette());p.save(out/(role+'.png'),transparency=255,optimize=True);source[role]={'file':role+'.png','frameWidth':size[0],'frameHeight':size[1],'frames':1}
(out/'catalog.json').write_text(json.dumps({'palette':colors,'sources':source},indent=2)+'\n');print('T16_NIGHT_PROPS_IMPORTED',len(source))
