#!/usr/bin/env python3
import json, os, shutil, subprocess, sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
CFG=json.loads((BASE/"target.json").read_text(encoding="utf-8"))
OUT=Path(os.environ.get("S1A_ROUTER_OUT","router_out"))
OUT.mkdir(parents=True,exist_ok=True)

def run(script,outdir,args=None):
    env=os.environ.copy()
    env["S1A_OUT"]=str(outdir)
    cmd=[sys.executable,str(BASE/script)]
    if args: cmd += args
    p=subprocess.run(cmd,env=env,text=True,capture_output=True)
    report_path=outdir/"acquisition_report.json"
    report={}
    if report_path.exists():
        report=json.loads(report_path.read_text(encoding="utf-8"))
    else:
        report={"adapter":script,"status":"ADAPTER_ERROR","returncode":p.returncode,
                "stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]}
    return report

reports=[]
apple_dir=OUT/"apple"
deezer_dir=OUT/"deezer"
apple=run("apple_itunes_preview.py",apple_dir)
reports.append(apple)
deezer=run("deezer_preview.py",deezer_dir)
reports.append(deezer)

chosen=None
chosen_dir=None
for rep, od in [(apple,apple_dir),(deezer,deezer_dir)]:
    if rep.get("status")=="MEDIA_ACQUIRED":
        chosen=rep; chosen_dir=od; break

# Optional verified direct-media fallbacks.
if chosen is None:
    for i,item in enumerate(CFG.get("direct_media_urls",[]),1):
        if not item.get("version_verified"):
            reports.append({
              "adapter":"DIRECT_PUBLIC_MEDIA_V0_1",
              "status":"SKIPPED_UNVERIFIED_VERSION",
              "url":item.get("url"),
              "version_label":item.get("version_label")
            })
            continue
        d=OUT/f"direct_{i}"
        rep=run("direct_public_media.py",d,[item["url"],str(d)])
        rep["version_label"]=item.get("version_label")
        rep["verification_evidence"]=item.get("verification_evidence")
        reports.append(rep)
        if rep.get("status")=="MEDIA_ACQUIRED":
            chosen=rep; chosen_dir=d; break

final={
  "router":"S1A_ACQUISITION_ROUTER_V0_1",
  "target":CFG,
  "adapter_reports":reports,
  "status":"CATALOG_COVERAGE_BLOCKED",
  "selected_adapter":None
}

if chosen is not None:
    final["status"]="MEDIA_ACQUIRED"
    final["selected_adapter"]=chosen.get("adapter")
    final["selected_report"]=chosen
    src=None
    art=chosen.get("artifact")
    if art:
        p=Path(art)
        if p.exists(): src=p
    if src is None and chosen_dir:
        files=[p for p in chosen_dir.iterdir() if p.is_file() and p.name not in {"acquisition_report.json","candidates.json"}]
        if files: src=files[0]
    if src:
        dst=OUT/("final_"+src.name)
        shutil.copy2(src,dst)
        final["final_artifact"]=str(dst)
        final["final_bytes"]=dst.stat().st_size

(OUT/"final_report.json").write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(final,ensure_ascii=False,indent=2))
