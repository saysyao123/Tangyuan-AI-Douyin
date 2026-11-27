#!/usr/bin/env python3
"""Local Skill Factory controller. Only execute reviewed, trusted local code."""
import argparse, hashlib, json, os, platform, re, shutil, subprocess, sys, time, zipfile, uuid
from pathlib import Path

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,x):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def die(msg): raise ValueError(msg)
def child(base,rel):
    if not isinstance(rel,str) or Path(rel).is_absolute(): die('relative path required')
    p=(base/rel).resolve()
    if not p.is_relative_to(base.resolve()): die('path escapes project: '+rel)
    return p
def manifest(p):
    s=read(p)
    for k in ('slug','description','task','buyer','input','output','acceptance','source','entrypoint','dependencies','limits'):
        if not s.get(k) and k!='dependencies': die('missing manifest field '+k)
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',s['slug']) or len(s['slug'])>64: die('invalid slug')
    if not isinstance(s['description'],str) or len(s['description'])>1024 or '\n' in s['description']: die('invalid description')
    for k in ('url','revision','license','review_status','evidence'):
        if not s['source'].get(k): die('missing source field '+k)
    return s

def init(spec,root):
    s=manifest(spec); root.mkdir(parents=True,exist_ok=False); product=root/'skill'/s['slug']; product.mkdir(parents=True)
    for d in ('scripts','references'): (product/d).mkdir()
    for d in ('evals','evidence','listing'): (root/d).mkdir()
    write(root/'manifest.json',s)
    (product/'SKILL.md').write_text(f'''---\nname: {s['slug']}\ndescription: {json.dumps(s['description'],ensure_ascii=False)}\n---\n# {s['slug']}\n\n## 任务\n{s['task']}\n\n## 输入\n{s['input']}\n\n## 输出\n{s['output']}\n\n## 执行\n1. 核对输入、权限和运行依赖；缺失则说明并停止，不虚构产物。\n2. 按 `references/runbook.md` 调用已审查的本地入口 `{s['entrypoint']}`。\n3. 回读产物并核验：{s['acceptance']}。\n4. 不合格先定位原因，最多两轮修复；仍失败交付事实与边界。\n\n## 限制\n{s['limits']}\n''',encoding='utf-8')
    (product/'references'/'runbook.md').write_text('待完善：输入契约、实际命令、依赖预检、失败分支、验收。\n',encoding='utf-8')
    write(root/'evals'/'cases.json',{'cases':[]})
    write(root/'evidence'/'status.json',{'stage':'draft','commercial_release':False})
    print(product)

def inspect(root):
    s=manifest(root/'manifest.json'); p=root/'skill'/s['slug']; errors=[]
    f=p/'SKILL.md'
    if not f.is_file(): errors.append('SKILL.md missing')
    else:
        text=f.read_text(encoding='utf-8'); parts=text.split('---\n',2)
        if len(parts)!=3 or parts[0]!='' or not re.search(r'^name: '+re.escape(s['slug'])+r'\s*$',parts[1],re.M): errors.append('frontmatter/name')
        if len(parts)!=3 or not re.search(r'^description: .+\S',parts[1],re.M): errors.append('description')
        if '待完善' in text: errors.append('unfinished SKILL')
    if not child(p,s['entrypoint']).is_file(): errors.append('entrypoint missing')
    for x in p.rglob('*'):
        if x.is_symlink(): errors.append('symlink: '+str(x.relative_to(p)))
        if x.is_file() and (x.name in ('.env','id_rsa','id_ed25519') or x.suffix in ('.pem','.key')): errors.append('possible credential: '+str(x.relative_to(p)))
        if x.is_file() and x.suffix=='.md' and '待完善' in x.read_text(encoding='utf-8'): errors.append('unfinished '+str(x.relative_to(p)))
    if s['source']['review_status']!='reviewed-local-candidate': errors.append('source review incomplete')
    if not (p/'THIRD_PARTY.md').is_file(): errors.append('third party declaration missing')
    files={str(x.relative_to(p)):digest(x) for x in sorted(p.rglob('*')) if x.is_file() and not x.is_symlink() and '__pycache__' not in x.parts}
    return s,p,errors,files

def evaluation_inputs(root):
    # Local consistency only: all regular files in evals, manifest, optional input_assets.
    files={'manifest.json':digest(root/'manifest.json')}
    for folder in ('evals','input_assets'):
        d=root/folder
        if d.is_symlink(): die('symlink input directory')
        if d.exists():
            for x in sorted(d.rglob('*')):
                if x.is_symlink(): die('symlink in evaluation inputs')
                if x.is_file() and '__pycache__' not in x.parts:
                    files[str(x.relative_to(root))]=digest(x)
    return files

def evaluate(root,repeat,trust):
    if not trust: die('requires --trusted-local after reviewing source, adapter and oracle; not a sandbox')
    s,p,errors,files=inspect(root)
    if errors: die('; '.join(errors))
    tests=root/'evals'/'cases.json'; oracle=root/'evals'/'oracle.py'; cases=read(tests)['cases']; inputs=evaluation_inputs(root)
    if not cases or len({c['id'] for c in cases})!=len(cases): die('empty or duplicate cases')
    reportdir=root/'evidence'/'runs'; reportdir.mkdir(parents=True,exist_ok=True)
    run=reportdir/(time.strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8])
    run.mkdir(exist_ok=False)
    rows=[]
    for case in cases:
        if not re.fullmatch(r'[a-z0-9-]+',case['id']): die('invalid case id')
        for i in range(repeat):
            w=run/f"{case['id']}-{i+1}"; w.mkdir(); inp=w/'request.json'; out=w/'result.json'; write(inp,case['request'])
            start=time.perf_counter(); error=''; actual=None; verdict=None
            try:
                proc=subprocess.run([sys.executable,str(child(p,s['entrypoint'])),str(inp),str(out),str(w)],cwd=root,capture_output=True,text=True,timeout=45)
                (w/'stdout.txt').write_text(proc.stdout[-10000:],encoding='utf-8'); (w/'stderr.txt').write_text(proc.stderr[-10000:],encoding='utf-8')
                actual=proc.returncode
                if actual!=case['exit_code']: die(f'exit {actual} != {case["exit_code"]}')
                result=read(out)
                for k,v in case['expect'].items():
                    if result.get(k)!=v: die(f'{k}: {result.get(k)!r} != {v!r}')
                if case.get('oracle'):
                    o=subprocess.run([sys.executable,str(oracle),str(inp),str(out),str(w),json.dumps(case['oracle'])],cwd=root,capture_output=True,text=True,timeout=45)
                    (w/'oracle.txt').write_text(o.stdout+'\n'+o.stderr,encoding='utf-8'); verdict=o.returncode
                    if verdict!=0: die('oracle failed')
            except Exception as e: error=str(e)
            rows.append({'id':case['id'],'repeat':i+1,'passed':not error,'critical':case.get('critical',True),'error':error,'exit_code':actual,'oracle_exit':verdict,'seconds':round(time.perf_counter()-start,4),'artifacts':{str(x.relative_to(w)):digest(x) for x in sorted(w.rglob('*')) if x.is_file() and not x.is_symlink()}})
    n=len(rows); passed=sum(r['passed'] for r in rows)
    if inputs!=evaluation_inputs(root) or files!=inspect(root)[3]: die('inputs or product changed during evaluation; retest')
    report={'type':'local-code-execution-self-test','level':'E1','product':s['slug'],'python':platform.python_version(),'platform':platform.platform(),'repeat':repeat,'distinct_cases':len(cases),'passed':passed,'total':n,'pass_rate':passed/n,'critical_failures':sum(not r['passed'] and r['critical'] for r in rows),'cases_sha256':digest(tests),'oracle_sha256':digest(oracle) if oracle.exists() else None,'product_files':files,'evaluation_inputs':inputs,'rows':rows,'limitations':['not model A/B','not independent blind evaluation','not host compatibility or payment validation','oracle authored by factory builder'],'commercial_release':False}
    write(run/'report.json',report); write(root/'evidence'/'latest.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('rows','product_files')},ensure_ascii=False,indent=2)); return 0 if passed==n else 2

def package(root,out):
    s,p,errors,files=inspect(root)
    if errors: die('; '.join(errors))
    r=read(root/'evidence'/'latest.json')
    if r['product_files']!=files or r.get('evaluation_inputs')!=evaluation_inputs(root): die('evidence stale or legacy; retest')
    if r.get('type')!='local-code-execution-self-test' or r.get('product')!=s['slug'] or r['pass_rate']<.9 or r['critical_failures'] or r['distinct_cases']<3: die('candidate gate failed')
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists(): die('output already exists')
    with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED) as z:
        for f in files:z.write(p/f,f'{s["slug"]}/{f}')
    print('LOCAL CANDIDATE ONLY:',out)

def compare(a,b):
    a,b=read(a),read(b)
    for k in ('type','product','cases_sha256','oracle_sha256','repeat','python','platform'):
        if a[k]!=b[k]: die('incomparable: '+k)
    if not a.get('evaluation_inputs') or not b.get('evaluation_inputs'): die('legacy evidence; retest both versions')
    if {k:v for k,v in a['evaluation_inputs'].items() if k!='manifest.json'}!={k:v for k,v in b['evaluation_inputs'].items() if k!='manifest.json'}: die('incomparable evaluation inputs')
    delta=b['pass_rate']-a['pass_rate']; regression=sorted({(x['id'],x['repeat']) for x in a['rows'] if x['passed']}-{(x['id'],x['repeat']) for x in b['rows'] if x['passed']})
    print(json.dumps({'pass_rate_delta':delta,'regressions':regression,'decision':'keep-candidate' if delta>0 and not regression and not b['critical_failures'] else 'do-not-promote','scope':'local execution regression only; not model A/B'},ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    i=sub.add_parser('init'); i.add_argument('spec',type=Path); i.add_argument('root',type=Path)
    for name in ('check','evaluate','package'):
        q=sub.add_parser(name); q.add_argument('root',type=Path)
        if name=='evaluate': q.add_argument('--repeat',type=int,default=1,choices=range(1,4)); q.add_argument('--trusted-local',action='store_true')
        if name=='package': q.add_argument('out',type=Path)
    q=sub.add_parser('compare'); q.add_argument('old',type=Path); q.add_argument('new',type=Path)
    a=ap.parse_args()
    try:
        if a.cmd=='init':init(a.spec.resolve(),a.root.resolve())
        elif a.cmd=='check':
            _,_,err,files=inspect(a.root.resolve()); print(json.dumps({'errors':err,'files':files,'level':'E0','commercial_release':False},ensure_ascii=False,indent=2)); return 2 if err else 0
        elif a.cmd=='evaluate':return evaluate(a.root.resolve(),a.repeat,a.trusted_local)
        elif a.cmd=='package':package(a.root.resolve(),a.out.resolve())
        else:compare(a.old,a.new)
    except Exception as e: print('BLOCKED:',e,file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
