#!/usr/bin/env python3
"""Final AUDIO_TIMELINE_PACKAGE lock gate.

Layer 1 (`package_tool.py validate`) proves timing evidence/provenance/audio identity.
This layer proves the complete editor-facing package is present and internally
consistent. Only this command may write a manifest with
AUDIO_TIMELINE_PACKAGE_LOCKED=true.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE = HERE / "package_tool.py"
REQUIRED = [
    "audio_identity.json", "trusted_lyrics.txt", "alignment_provenance.json",
    "line_timeline.csv", "lyrics_exact.srt", "anchor_words.csv",
    "music_events.csv", "alignment_qa_report.md",
]


def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()


def rows(path: Path):
    with path.open('r', encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))


def srt_time(x: str) -> float:
    m=re.fullmatch(r'(\d+):(\d+):(\d+)[,.](\d+)', x.strip())
    if not m: raise ValueError(f'bad SRT time {x!r}')
    h,mi,s,ms=map(int,m.groups()); return h*3600+mi*60+s+ms/(1000 if len(m.group(4))==3 else 10**len(m.group(4)))


def parse_srt(path: Path):
    out=[]
    for block in re.split(r'\n\s*\n', path.read_text(encoding='utf-8-sig').strip()):
        ls=[x.rstrip() for x in block.splitlines() if x.strip()]
        if len(ls)<3: continue
        tm=next((x for x in ls if '-->' in x), None)
        if not tm: continue
        a,b=[x.strip() for x in tm.split('-->',1)]
        ti=ls.index(tm); text='\n'.join(ls[ti+1:]).strip()
        out.append((srt_time(a),srt_time(b),text))
    return out


def core_validate(pkg: Path, audio: str|None, crosscheck: str|None):
    cmd=[sys.executable,str(CORE),'validate','--package',str(pkg)]
    if audio: cmd += ['--audio',audio]
    if crosscheck: cmd += ['--crosscheck',crosscheck]
    p=subprocess.run(cmd,text=True,capture_output=True)
    try: payload=json.loads(p.stdout)
    except Exception: payload={'pass':False,'errors':['core validator returned non-JSON'], 'raw_stdout':p.stdout, 'raw_stderr':p.stderr}
    return p.returncode,payload


def cmd_seal_qa(args):
    pkg=Path(args.package); report=pkg/'alignment_qa_report.md'; provp=pkg/'alignment_provenance.json'
    if not report.exists() or report.stat().st_size < 40: raise ValueError('alignment_qa_report.md missing/too small')
    prov=json.loads(provp.read_text(encoding='utf-8')); prov['qa_report_path']='alignment_qa_report.md'; prov['qa_report_sha256']=sha(report)
    provp.write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'success':True,'qa_report_sha256':prov['qa_report_sha256']},ensure_ascii=False)); return 0


def cmd_validate(args):
    pkg=Path(args.package); errors=[]; warnings=[]
    for n in REQUIRED:
        if not (pkg/n).exists(): errors.append(f'missing complete-package asset: {n}')
    if errors:
        print(json.dumps({'pass':False,'errors':errors,'warnings':warnings},ensure_ascii=False,indent=2)); return 2
    rc,core=core_validate(pkg,args.audio,args.crosscheck)
    if rc!=0 or not core.get('pass'):
        errors.append('timing core validation failed'); errors.extend(core.get('errors',[]))
    ident=json.loads((pkg/'audio_identity.json').read_text(encoding='utf-8')); duration=float(ident.get('timeline_duration_s',ident.get('content_duration_s')))
    prov=json.loads((pkg/'alignment_provenance.json').read_text(encoding='utf-8'))
    if prov.get('qa_report_path')!='alignment_qa_report.md': errors.append('provenance does not reference alignment_qa_report.md')
    elif prov.get('qa_report_sha256')!=sha(pkg/'alignment_qa_report.md'): errors.append('alignment QA report SHA mismatch')
    tl=rows(pkg/'line_timeline.csv'); line_map={r['line_id']:r for r in tl}
    srt=parse_srt(pkg/'lyrics_exact.srt')
    if len(srt)!=len(tl): errors.append(f'SRT/timeline line count mismatch {len(srt)} != {len(tl)}')
    else:
        for r,(a,b,text) in zip(tl,srt):
            if text.replace('\n','').strip()!=r['lyric'].replace('\n','').strip(): errors.append(f"SRT lyric mismatch {r['line_id']}")
            if abs(a-float(r['clip_start_s']))>.005 or abs(b-float(r['clip_end_s']))>.005: errors.append(f"SRT time mismatch {r['line_id']}")
    anchors=rows(pkg/'anchor_words.csv')
    need={'anchor_id','line_id','phrase','start_s','end_s','qa_status'}
    if not anchors: errors.append('anchor_words.csv is empty')
    elif not need.issubset(anchors[0]): errors.append(f'anchor_words schema missing {sorted(need-set(anchors[0]))}')
    else:
        for a in anchors:
            lr=line_map.get(a['line_id'])
            if not lr: errors.append(f"anchor references unknown line {a['line_id']}"); continue
            st,en=float(a['start_s']),float(a['end_s']); ls,le=float(lr['clip_start_s']),float(lr['clip_end_s'])
            if st<ls-.05 or en>le+.05 or en<=st: errors.append(f"anchor outside lyric window {a['anchor_id']}")
            if a['qa_status']!='PASS': errors.append(f"anchor QA not PASS {a['anchor_id']}")
    ev=rows(pkg/'music_events.csv'); need={'event_id','time_s','type','description','qa_status'}
    if not ev: errors.append('music_events.csv is empty')
    elif not need.issubset(ev[0]): errors.append(f'music_events schema missing {sorted(need-set(ev[0]))}')
    else:
        prev=-1.0
        for e in ev:
            t=float(e['time_s'])
            if t<0 or t>duration+.05: errors.append(f"music event out of bounds {e['event_id']}")
            if t<prev: errors.append(f"music events not sorted {e['event_id']}")
            if e['qa_status']!='PASS': errors.append(f"music event QA not PASS {e['event_id']}")
            prev=t
    passed=not errors
    result={'pass':passed,'errors':errors,'warnings':warnings,'core':core,'lines':len(tl),'anchors':len(anchors),'music_events':len(ev)}
    if passed and args.write_manifest:
        manifest={
            'package_version':'1.0','AUDIO_TIMELINE_PACKAGE_LOCKED':True,'audio_sha256':ident.get('audio_sha256'),
            'timeline_duration_s':duration,'evidence_class':prov.get('evidence_class'),'files':{}
        }
        for p in sorted(pkg.iterdir()):
            if p.is_file() and p.name!='package_manifest.json': manifest['files'][p.name]=sha(p)
        (pkg/'package_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        result['manifest']='package_manifest.json'
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 0 if passed else 2


def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('seal-qa'); a.add_argument('--package',required=True); a.set_defaults(func=cmd_seal_qa)
    a=sub.add_parser('validate'); a.add_argument('--package',required=True); a.add_argument('--audio'); a.add_argument('--crosscheck'); a.add_argument('--write-manifest',action='store_true'); a.set_defaults(func=cmd_validate)
    args=p.parse_args()
    try:return args.func(args)
    except Exception as e:
        print(json.dumps({'pass':False,'state':'AUDIO_TIMELINE_PACKAGE_BLOCKED','error':type(e).__name__,'message':str(e)},ensure_ascii=False),file=sys.stderr); return 3

if __name__=='__main__': raise SystemExit(main())
