#!/usr/bin/env python3
"""T26: Build native Type PAL directional assets from previously approved V2 stands.
Designed to be called in a disposable CI checkout. Does not edit story, map,
collision, save schema, webpage shell or original approved PNGs.
4 directions x 3 frames, actor canvas/foot anchor unchanged.
"""
from pathlib import Path
from PIL import Image
import json,gzip,struct,hashlib,sys
book=Path(__file__).resolve().parents[2]
project=Path(sys.argv[1]).resolve()
report=Path(sys.argv[2]).resolve()
report.mkdir(parents=True,exist_ok=True)
palette_file=project/'assets/generated/colors/project-standard.json'
pal=json.loads(palette_file.read_text())['colors']
assert len(pal)==256
pal_img=Image.new('P',(1,1))
pal_img.putpalette([v for rgb in pal for v in rgb])
catalog_path=project/'assets/index.json'
catalog=json.loads(catalog_path.read_text())
manifest={'status':'UNREVIEWED_VISUAL_CANDIDATE','original_t22_gameplay':True,'frames':{},'provenance':'T19 P1 V2 user-approved four-direction standing assets, not T19 rejected gait',
'gate':{'format':'PENDING','visual_motion':'NOT_PASSED','real_engine':'PENDING'}}

def pose(stand,phase):
    if phase==0:return stand.copy()
    w,h=stand.size;cut=int(h*.68);mid=w//2
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    im.alpha_composite(stand.crop((0,0,w,cut)),(0,0))
    legs=stand.crop((0,cut,w,h))
    dx=1 if phase==1 else -1
    im.alpha_composite(legs.crop((0,0,mid,h-cut)),(dx,cut-(1 if phase==1 else 0)))
    im.alpha_composite(legs.crop((mid,0,w,h-cut)),(mid-dx,cut-(0 if phase==1 else 1)))
    return im

def frame_rle(pixels,w,h):
    out=bytearray(struct.pack('<HH',w,h));i=0
    while i<len(pixels):
        visible=pixels[i]!=255;j=i
        while j<len(pixels) and (pixels[j]!=255)==visible and j-i<127:j+=1
        out.append((j-i) if visible else (0x80+j-i))
        if visible:out.extend(pixels[i:j])
        i=j
    return out

def native_gzip(frames):
    out=bytearray(2*len(frames))
    for i,(pixels,w,h) in enumerate(frames):
        struct.pack_into('<H',out,i*2,len(out)//2)
        out.extend(frame_rle(pixels,w,h))
        if len(out)%2:out.append(0)
    return gzip.compress(out,mtime=0)

def decode(blob):
    raw=gzip.decompress(blob);n=struct.unpack_from('<H',raw,0)[0]
    result=[]
    for f in range(n):
        offset=struct.unpack_from('<H',raw,2*f)[0]*2
        w,h=struct.unpack_from('<HH',raw,offset)
        at=offset+4;pix=[]
        while len(pix)<w*h:
            run=raw[at];at+=1
            if run>=128:pix.extend([255]*(run-128))
            else:pix.extend(raw[at:at+run]);at+=run
        result.append((pix,w,h))
    return result

for role,name,w,h in [('adult','hero',36,56),('child','child',32,44)]:
    src=book/f'art/t26/{role}_4dir_approved.png'
    approved=Image.open(src).convert('RGBA')
    assert approved.size==(4*w,h),(src,approved.size)
    frames=[]
    montage=Image.new('RGBA',(3*w,4*h),(27,29,36,255))
    for direction in range(4):
        stand=approved.crop((direction*w,0,(direction+1)*w,h))
        for stride in range(3):
            frame=pose(stand,stride)
            q=frame.convert('RGB').quantize(palette=pal_img,dither=Image.Dither.NONE)
            pix=bytearray(q.tobytes())
            for index,a in enumerate(frame.getchannel('A').tobytes()):
                if a<128:pix[index]=255
                elif pix[index]==255:
                    rgb=frame.getpixel((index%w,index//w))[:3]
                    pix[index]=min(range(255),key=lambda j:sum((rgb[k]-pal[j][k])**2 for k in range(3)))
            frames.append((pix,w,h))
            montage.alpha_composite(frame,(stride*w,direction*h))
    blob=native_gzip(frames)
    assert len(frames)==12
    assert decode(blob)==[(list(p),w,h) for p,w,h in frames],role
    rel=f'assets/generated/sprites/{name}.rle'
    (project/rel).write_bytes(blob)
    key=f'sprite.{name}'
    assert key in catalog['assets'] and catalog['assets'][key]['kind']=='sprite'
    catalog['assets'][key]['bytes']=len(blob)
    catalog['assets'][key]['sha256']=hashlib.sha256(blob).hexdigest()
    montage.resize((3*w*5,4*h*5),Image.Resampling.NEAREST).save(report/f'{name}-4x3-contact.png')
    manifest['frames'][name]={'dimensions':[w,h],'directions':4,'strides':3,'gzipBytes':len(blob),
      'sha256':hashlib.sha256(blob).hexdigest(),'pixelExactRoundtrip':True,
      'originalSourceGitBlobSha':'d87af2cb906bcf3621e415a281f2fe213e4ee4e6' if role=='adult' else '04c7a4e23461361e7a479c7b89648f87d0bc0221'}
catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
manifest['gate']['format']='PASS'
(report/'T26_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('T26_APPROVED_CHARACTER_FORMAT_READY',json.dumps(manifest['frames'],ensure_ascii=False))
