"""Verify private text bindings against the exact CI native project/runtime; no gameplay tests."""
from pathlib import Path
import json,hashlib,sys
public,private,ciweb,web=map(Path,sys.argv[1:5])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(p):return {str(x.relative_to(p)):x for x in p.rglob('*') if x.is_file()}
def compare(a,b,at=''):
 if type(a)!=type(b):raise ValueError('Type difference '+at)
 if isinstance(a,dict):
  if a.keys()!=b.keys():raise ValueError('Key difference '+at)
  return sum((compare(a[k],b[k],at+'/'+k)for k in a),[])
 if isinstance(a,list):
  if len(a)!=len(b):raise ValueError('Length difference '+at)
  return sum((compare(x,y,at+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))),[])
 if a==b:return []
 if not isinstance(a,str):raise ValueError('Mechanical value difference '+at)
 # Text leaf whitelist, never IDs/references or script mechanics.
 leaf=at.rsplit('/',1)[-1]
 if not (leaf in {'label','name','title','text'} or '/locale.json/'in at or '/desc/'in at or ('/config.js/' in at and (leaf in {'headline','endHeadline','intro','eyebrow'} or '/quests/'in at or '/scenes/'in at))):raise ValueError('Non-presentation string difference '+at)
 return [at]
a,b=files(public),files(private);assert a.keys()==b.keys();changed=[]
for n in a:
 if sha(a[n])!=sha(b[n]):
  if not n.endswith('.json'):raise ValueError('Binary difference '+n)
  changed+=compare(json.loads(a[n].read_text()),json.loads(b[n].read_text()),'/'+n)
# Every configured private cue is bound verbatim somewhere in native content.
cfg=json.loads(Path(sys.argv[5]).read_text()) if len(sys.argv)>5 else None
if cfg:
 strings='\n'.join(p.read_text()for p in b.values()if p.suffix=='.json')
 for k,t in cfg['text'].items():assert t in strings,'Unbound private cue '+k
# Runtime filenames and bytes are copied from fresh CI; only explicit private presentation files differ.
a,b=files(ciweb),files(web);exclude={'runtime-manifest.json','download-checksums.json'}
a={n:p for n,p in a.items()if not n.startswith('downloads/')and n not in exclude};b={n:p for n,p in b.items()if not n.startswith('downloads/')and n not in exclude};assert a.keys()==b.keys(),{'extra':sorted(b.keys()-a.keys()),'missing':sorted(a.keys()-b.keys())}
differences=[]
for n in a:
 if sha(a[n])==sha(b[n]):continue
 allowed=n in {'pilot/index.html','pilot/config.js','chapter/index.html','chapter/config.js','night/index.html','night/config.js'}or ('/projects/book-pilot-'in n and n.endswith('.json'))
 assert allowed,'Untested runtime difference '+n
 if n.endswith('/config.js'):
  def parsecfg(p):
   s=p.read_text();return json.loads(s[s.index('=')+1:].strip().removesuffix(';'))
  compare(parsecfg(a[n]),parsecfg(b[n]),'/'+n)
 differences.append(n)
print(json.dumps({'status':'PASS','projectFiles':len(files(public)),'privateTextLeafDifferences':len(changed),'nativeMechanicsAndBinaryAssetsIdentical':True,'runtimeFiles':len(a),'byteIdenticalRuntimeFiles':len(a)-len(differences),'privatePresentationFiles':differences,'privateCueBinding':len(cfg['text'])if cfg else 'separately supplied'},indent=2))
