#!/usr/bin/env python3
"""Portable, offline, stdlib-only controller smoke test; not an agent behavior eval."""
import json, subprocess, sys, tempfile, zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
rows=[]
def check(name,ok,detail=''):
    rows.append({'test':name,'passed':bool(ok),'detail':detail})
def run(*args):
    return subprocess.run([sys.executable,str(HERE/'factory.py'),*map(str,args)],capture_output=True,text=True,timeout=20)
def put(p,x): p.write_text(json.dumps(x,ensure_ascii=False),encoding='utf-8')
with tempfile.TemporaryDirectory(prefix='factory-selftest-') as tmp:
    base=Path(tmp); root=base/'project'; spec=base/'spec.json'
    s=json.loads((HERE.parent/'references/manifest.example.json').read_text())
    s.update(slug='local-smoke',description='Synthetic text uppercase smoke test.',task='Uppercase test text',input='text',output='uppercase text',acceptance='exact string',source={'url':'local synthetic fixture','revision':'1','license':'original synthetic test','review_status':'reviewed-local-candidate','evidence':'inline test only'})
    put(spec,s)
    r=run('init',spec,root);check('init fresh',r.returncode==0,r.stderr)
    r=run('init',spec,root);check('reject overwrite',r.returncode!=0,r.stderr)
    r=run('check',root);check('reject unfinished',r.returncode!=0)
    p=root/'skill/local-smoke'; (p/'references/runbook.md').write_text('Synthetic local test only.'); (p/'THIRD_PARTY.md').write_text('No third party code.')
    (p/'scripts/run.py').write_text('import json,sys\nfrom pathlib import Path\na,b,w=map(Path,sys.argv[1:]); t=json.loads(a.read_text())["text"]; (w/"out.txt").write_text(t.upper()); b.write_text(json.dumps({"ok":True}))\n')
    (root/'evals/oracle.py').write_text('import json,sys\nfrom pathlib import Path\nassert (Path(sys.argv[3])/"out.txt").read_text()==json.loads(sys.argv[4])["expected"]\n')
    put(root/'evals/cases.json',{'cases':[{'id':str(i),'request':{'text':t},'exit_code':0,'expect':{'ok':True},'oracle':{'expected':e}} for i,(t,e) in enumerate([('abc','ABC'),('Hello!','HELLO!'),('','')])]})
    (root/'evals/fixture.txt').write_text('baseline')
    r=run('check',root); check('complete structure',r.returncode==0,r.stderr)
    r=run('evaluate',root);check('reject untrusted execution',r.returncode!=0)
    r=run('evaluate',root,'--trusted-local'); check('execute 3 synthetic cases with oracle',r.returncode==0,r.stderr)
    report=root/'evidence/latest.json'; old=base/'old.json';old.write_bytes(report.read_bytes())
    r=run('compare',old,report);check('identical report not promoted',r.returncode==0 and 'do-not-promote' in r.stdout,r.stderr)
    out=base/'candidate.zip'; r=run('package',root,out);check('package candidate',r.returncode==0 and out.is_file(),r.stderr)
    if out.is_file():
        with zipfile.ZipFile(out) as z: check('exclude eval and evidence files',all(n.startswith('local-smoke/') and '/evals/' not in n and '/evidence/' not in n for n in z.namelist()))
    (root/'evals/fixture.txt').write_text('changed');r=run('package',root,base/'stale.zip');check('reject stale fixture evidence',r.returncode!=0 and 'stale' in r.stderr,r.stderr)
    (root/'evals/fixture.txt').write_text('baseline');s['buyer']='changed';put(root/'manifest.json',s);r=run('package',root,base/'stale2.zip');check('reject stale manifest evidence',r.returncode!=0 and 'stale' in r.stderr,r.stderr)
    # Same task set, optional independent oracle absent: local field check only.
    cases=json.loads((root/'evals/cases.json').read_text());[c.pop('oracle') for c in cases['cases']];put(root/'evals/cases.json',cases);(root/'evals/oracle.py').unlink()
    r=run('evaluate',root,'--trusted-local');r2=run('package',root,base/'no-oracle.zip');check('optional oracle local package',r.returncode==0 and r2.returncode==0,r.stderr+r2.stderr)
result={'passed':sum(r['passed'] for r in rows),'total':len(rows),'tests':rows,'scope':'offline synthetic controller self-test only; no independent agent, no host install, no commercial release'}
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['passed']==result['total'] else 1)
