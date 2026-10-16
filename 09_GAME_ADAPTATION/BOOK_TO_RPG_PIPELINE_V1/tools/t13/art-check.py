"""Directional-art contract, independent of renderer state; inspect production-authored frames."""
import json,sys,hashlib
j=json.load(open(sys.argv[1]));frames=j['frames']
def at(f,x,y):return f['pixels'][y*f['width']+x] if f['opaque'][y*f['width']+x] else None
for style in ['hero','keeper','child','guard','wolf']:
 fs=[f for f in frames if f['style']==style];assert len(fs)==12
 assert len({hashlib.sha256(bytes(f['pixels'])+bytes(f['opaque'])).hexdigest() for f in fs})==12,style+' duplicate direction/step'
 left,right=fs[3],fs[9]
 for y in range(left['height']):
  for x in range(left['width']):
   # Child downscaling uses rounded pixel coordinates; compare adult and wolf exact mirrors.
   if style!='child':assert at(left,x,y)==at(right,left['width']-1-x,y),(style,'side mirror')
 if style not in ['child','wolf']:
  assert at(left,5,10)==42 and at(right,18,10)==42,style+' nose orientation'
  assert at(fs[0],10,9)==0 and at(fs[6],10,9)!=0,style+' rear has a face'
  assert at(fs[0],16,9)==0 and at(fs[6],16,9)!=0,style+' rear has a face'
 print(style+': four distinct views and three distinct poses PASS')
print('DIRECTIONAL_ART_CONTRACT=PASS')
