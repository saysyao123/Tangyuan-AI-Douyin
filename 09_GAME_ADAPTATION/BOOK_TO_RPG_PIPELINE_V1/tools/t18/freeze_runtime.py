"""Freeze executable bytes to accepted CI; allow only explicitly verified private presentation."""
from pathlib import Path
import shutil,os,sys,json
base,out=map(Path,sys.argv[1:3]);presentation={'pilot/index.html','pilot/config.js','chapter/index.html','chapter/config.js','night/index.html','night/config.js'};repaired=[]
for p in base.rglob('*'):
 if not p.is_file():continue
 name=p.relative_to(base).as_posix()
 if name.startswith('downloads/')or name in {'runtime-manifest.json','download-checksums.json'}:continue
 if name in presentation or('/projects/book-pilot-'in name and name.endswith('.json')):continue
 q=out/name;q.parent.mkdir(parents=True,exist_ok=True)
 if not q.exists()or q.read_bytes()!=p.read_bytes():repaired.append(name)
 shutil.copyfile(p,q)
# File transfer checkpoints must observe fresh writes even when a CI ZIP has older timestamps.
for p in out.rglob('*'):
 if p.is_file():os.utime(p,None)
print(json.dumps({'executableRuntimeFrozenToCI':True,'repaired':repaired}))
