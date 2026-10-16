"""Prove private text substitution changes no native mechanics/assets in the fixed pilot."""
from pathlib import Path
import json,sys,hashlib
left,right=map(Path,sys.argv[1:3])
# Only presentational fields. Stable actor/item/scene IDs, conditions, events, values, geometry remain.
def mechanics(value):
 if isinstance(value,list):return [mechanics(v) for v in value]
 if isinstance(value,dict):return {k:mechanics(v) for k,v in value.items() if k not in {'name','label','description','desc','text'}}
 return value
def scan(root):
 result={}
 for p in root.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(root).as_posix()
  if p.suffix=='.json':
   v=json.loads(p.read_text())
   if rel=='content/locale.json':v=sorted(v.keys())
   result[rel]=mechanics(v)
  else:result[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
 return result
a,b=scan(left),scan(right);different=sorted(k for k in a.keys()|b.keys() if a.get(k)!=b.get(k));assert not different,different
print(json.dumps({'status':'PASS','files':len(a),'claim':'Same native mechanics, actor IDs, geometry, flags, events and binary assets; only presentation fields differ'}))
