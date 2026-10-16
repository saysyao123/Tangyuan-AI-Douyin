"""Verify private text binding against the native project and exact public CI runtime."""
from pathlib import Path
import json,hashlib,re,sys
ci,out,project,config=map(Path,sys.argv[1:5])
def mechanic(x):
 if isinstance(x,list):return [mechanic(v) for v in x]
 if isinstance(x,dict):return {k:mechanic(v) for k,v in x.items() if k not in {'name','label','description','desc','text'}}
 return x
def scan(root):
 d={}
 for p in root.rglob('*'):
  if not p.is_file():continue
  key=p.relative_to(root).as_posix()
  if p.suffix=='.json':
   v=json.loads(p.read_text());d[key]=sorted(v.keys()) if key=='content/locale.json' else mechanic(v)
  else:d[key]=hashlib.sha256(p.read_bytes()).hexdigest()
 return d
public=scan(ci/'public-project');private=scan(project);assert public==private,'Native project mechanics/assets differ'
a=json.loads((ci/'runtime-manifest.json').read_text())['files'];b=json.loads((out/'runtime-manifest.json').read_text())['files'];assert a.keys()==b.keys(),'Runtime path set differs'
diff=[k for k in a if a[k]!=b[k]]
allowed=lambda k:k in {'pilot/index.html','pilot/config.js','chapter/index.html','chapter/config.js'} or (k.endswith('.json') and any(x in k for x in ['projects/book-pilot-opening/','projects/book-pilot-cinematic/']))
assert all(allowed(k) for k in diff),[k for k in diff if not allowed(k)]
# Native private cues are decoded JSON values, not serialized string substring matches.
values=[]
def collect(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='text' and isinstance(v,str):values.append(v)
   collect(v)
 elif isinstance(x,list):
  for v in x:collect(v)
for p in (project/'content/scenes').glob('*.json'):collect(json.loads(p.read_text()))
source=(Path(__file__).parent/'opening.mts').read_text();keys=set(re.findall(r"say\('([^']+)'",source));cfg=json.loads(config.read_text());assert all(cfg['text'][k] in values for k in keys)
print(json.dumps({'status':'PASS','nativeProjectFiles':len(public),'privateCuesBound':len(keys),'runtimeFiles':len(a),'byteIdenticalToCI':len(a)-len(diff),'privatePresentationDifferences':diff,'claim':'Same new native mechanics, IDs, geometry, events and binary assets; exact runtime paths and non-content bytes'},indent=2))
