#!/usr/bin/env python3
"""Second cloud environment: Ubuntu direct yt-dlp media download with EJS and Python-bundled FFmpeg.
This checks actual saved bytes and 1s decode; no cookies, DRM or media retention.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
urls = {
  "douyin": ["https://www.douyin.com/video/7699684520735660214","https://www.douyin.com/video/7682249897617247522"],
  "bilibili": ["https://www.bilibili.com/video/BV13x41117TL","https://www.bilibili.com/video/BV1AerZB6EWa/"],
  "youtube": ["https://www.youtube.com/watch?v=aqz-KE-bpKQ","https://www.youtube.com/watch?v=YE7VzlLtp-4"],
  "cc0_control": ["https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"]
}
dest=Path("linux_quick_results");dest.mkdir(exist_ok=True)
def run(args,timeout=90):
    try:
        p=subprocess.run(args,capture_output=True,text=True,errors="replace",timeout=timeout)
        return p.returncode,p.stdout,p.stderr
    except subprocess.TimeoutExpired:
        return -1,"","Timeout"
def summarize(s):
    if "Fresh cookies" in s:return "SESSION_REQUIRED"
    if "412" in s:return "HTTP_412"
    if "not a bot" in s:return "BOT_CHECK"
    if "403" in s:return "HTTP_403"
    return s.splitlines()[-1][:150] if s.splitlines() else "OTHER"
base=["yt-dlp","--ignore-config","--no-playlist","--no-warnings","--js-runtimes","node",
      "--socket-timeout","12","--retries","1"]
results={"os":"ubuntu","yt_dlp":run(["yt-dlp","--version"],15)[1].strip(),
         "node":run(["node","--version"],15)[1].strip(),"platforms":{}}
for name, items in urls.items():
  rows=[]
  for idx,url in enumerate(items):
    record={"url":url,"metadata_ok":False,"download_ok":False,"decoded":False}
    rc,stdout,err=run([*base,"--dump-single-json",url],85)
    record["probe_error"]=summarize(err) if rc else None
    if rc==0:
      try:
        js=json.loads(stdout);record["metadata_ok"]=True
        record["extractor"]=js.get("extractor_key")
        record["format_count"]=len(js.get("formats") or [])
        if js.get("has_drm") or js.get("is_live"): record["blocked"]="protected/live"
      except ValueError:record["probe_error"]="BAD_JSON"
    folder=dest/f"{name}_{idx}";folder.mkdir(exist_ok=True)
    if record["metadata_ok"] and not record.get("blocked"):
      fmt="b[height<=480]/bv*[height<=480]+ba/best"
      rc,stdout,err=run([*base,"-f",fmt,"--download-sections","*0-3",
                         "--merge-output-format","mp4","--no-progress",
                         "-o",str(folder/"test.%(ext)s"),url],100)
      files=[f for f in folder.iterdir() if f.suffix.lower() in (".mp4",".webm",".mkv")]
      record["download_error"]=summarize(err) if rc else None
      if rc==0 and files:
        f=max(files,key=lambda x:x.stat().st_size)
        chk,_,stderr=run(["ffmpeg","-v","error","-i",str(f),"-t","1","-f","null","-"],35)
        record["decoded"]=(chk==0)
        record["download_ok"]=record["decoded"] and f.stat().st_size>1000
        record["size_bytes"]=f.stat().st_size
        record["sha256"]=hashlib.sha256(f.read_bytes()).hexdigest()
    shutil.rmtree(folder,ignore_errors=True)
    print("CASE",name,idx,json.dumps(record,ensure_ascii=False),flush=True)
    rows.append(record)
    results["platforms"][name]={"verified":sum(bool(x["download_ok"]) for x in rows),"rows":rows}
    (dest/"results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
print("FINAL",json.dumps({k:v["verified"] for k,v in results["platforms"].items()}),flush=True)
