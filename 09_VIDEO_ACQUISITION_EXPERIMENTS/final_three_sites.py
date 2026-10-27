#!/usr/bin/env python3
"""Final independent, real-media acquisition test for 3 video sites.
Runs yt-dlp with EJS+Node, and verifies a real ~3s MP4 with ffprobe + ffmpeg.
Does not use cookies, account automation, bypass tools, DRM, or republish videos.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import time

SAMPLES = {
    "douyin": [
        "https://www.douyin.com/video/7699684520735660214",
        "https://www.douyin.com/video/7682249897617247522",
    ],
    "bilibili": [
        "https://www.bilibili.com/video/BV13x41117TL",
        "https://www.bilibili.com/video/BV1AerZB6EWa/",
    ],
    "youtube": [
        "https://www.youtube.com/watch?v=aqz-KE-bpKQ",
        "https://www.youtube.com/watch?v=YE7VzlLtp-4",
    ],
    "cc0_control": [
        "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    ],
}
OUT = pathlib.Path("three_sites_results")
OUT.mkdir(parents=True, exist_ok=True)
def run(cmd, limit):
    st = time.monotonic()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=limit)
        return {"rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr,
                "seconds": round(time.monotonic()-st, 2)}
    except subprocess.TimeoutExpired:
        return {"rc": -1, "stdout": "", "stderr": "PROCESS_TIMEOUT", "seconds": round(time.monotonic()-st, 2)}
    except Exception as e:
        return {"rc": -2, "stdout": "", "stderr": type(e).__name__ + ": " + str(e)[:200],
                "seconds": round(time.monotonic()-st, 2)}
def diagnostic(err):
    e = err.lower()
    if "fresh cookies" in e: return "SESSION_REQUIRED_DOUYIN"
    if "sign in to confirm" in e or "not a bot" in e: return "BOT_CHALLENGE_YOUTUBE"
    if "http error 412" in e: return "HTTP_412"
    if "http error 403" in e: return "HTTP_403"
    if "http error 429" in e: return "HTTP_429"
    if "requested format" in e: return "FORMAT_UNAVAILABLE"
    if "not available" in e or "private video" in e: return "UNAVAILABLE"
    if "unsupported url" in e: return "UNSUPPORTED_URL"
    if "timed out" in e or "PROCESS_TIMEOUT" in err: return "TIMEOUT"
    return "OTHER"
def reason(err):
    lines = [line.strip() for line in err.splitlines() if line.strip()]
    errors = [x for x in lines if "ERROR:" in x]
    # Never include full raw media URLs or cookies in logs
    item = (errors[-1] if errors else (lines[-1] if lines else ""))[:420]
    return re.sub(r"https?://[^\s]+", "[link]", item)
def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()
def media_check(p):
    probe = run(["ffprobe","-v","error","-show_entries",
                 "format=duration,size:stream=codec_type,codec_name,width,height",
                 "-of","json",str(p)],35)
    if probe["rc"] != 0:
        return {"verified":False,"reason":"ffprobe failure: "+reason(probe["stderr"])}
    data = json.loads(probe["stdout"])
    vids = [x for x in data.get("streams",[]) if x.get("codec_type")=="video"]
    if not vids: return {"verified":False,"reason":"no video track"}
    duration = float(data.get("format",{}).get("duration") or 0)
    if duration<0.5: return {"verified":False,"reason":"short or missing video duration"}
    decoded = run(["ffmpeg","-v","error","-i",str(p),"-t","1","-f","null","-"],45)
    return {"verified":decoded["rc"]==0,
            "duration":round(duration,3),"size":p.stat().st_size,
            "sha256":sha(p), "video_codec":vids[0].get("codec_name"),
            "width":vids[0].get("width"),"height":vids[0].get("height"),
            "audio_codecs":[x.get("codec_name") for x in data.get("streams",[]) if x.get("codec_type")=="audio"],
            "ffmpeg_error":reason(decoded["stderr"]) if decoded["rc"] else ""}
base = ["yt-dlp","--ignore-config","--no-playlist","--no-warnings",
        "--js-runtimes","node","--socket-timeout","12",
        "--retries","1","--fragment-retries","1"]
report = {"created_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
          "os":platform.platform(), "python":sys.version.split()[0],
          "yt_dlp_version":run(["yt-dlp","--version"],15)["stdout"].strip(),
          "node_version":run(["node","--version"],15)["stdout"].strip(),
          "yoinks_version":run(["yoinks","--version"],15)["stdout"].strip(),
          "installed_ejs":run([sys.executable,"-m","pip","show","yt-dlp-ejs"],15)["rc"]==0,
          "policy":"public no-login no-browser-cookies no-DRM noncommercial test; media deleted",
          "platforms":{}}
def checkpoint():
    (OUT/"results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
for site, urls in SAMPLES.items():
    items=[]
    for idx,url in enumerate(urls):
        item={"url":url,"metadata":False,"download_attempted":False,"file_verified":False}
        attempt_dir = OUT/f"{site}_{idx}"
        attempt_dir.mkdir(exist_ok=True)
        print("START",site,idx,url,flush=True)
        info = run([*base,"--dump-single-json","--skip-download",url],95)
        item["probe_exit_code"]=info["rc"]
        item["probe_seconds"]=info["seconds"]
        if info["rc"]==0:
            try:
                obj=json.loads(info["stdout"])
                item.update(metadata=True, extractor=obj.get("extractor_key"),
                            title=str(obj.get("title",""))[:110],
                            format_count=len(obj.get("formats") or []),
                            has_drm=obj.get("has_drm"),
                            is_live=obj.get("is_live"))
            except Exception as e:
                item.update(probe_error="PARSE_JSON",detail=str(e)[:100])
        else:
            item.update(probe_error=diagnostic(info["stderr"]),detail=reason(info["stderr"]))
        if item["metadata"] and item.get("has_drm") is not True and not item.get("is_live"):
            item["download_attempted"]=True
            # Same pipeline yt-dlp used by Yoinks: real media bytes + ffmpeg.
            cmd = [*base,"--no-progress","-f",
                   "b[height<=480]/bv*[height<=480]+ba/best",
                   "--download-sections","*0-3","--merge-output-format","mp4",
                   "-o",str(attempt_dir/"clip.%(ext)s"),url]
            dl = run(cmd,110)
            item["download_exit_code"]=dl["rc"]
            item["download_seconds"]=dl["seconds"]
            candidates = [p for p in attempt_dir.iterdir() if p.is_file()
                          and p.suffix.lower() in (".mp4",".webm",".mkv",".mov")]
            if dl["rc"]==0 and candidates:
                qa = media_check(max(candidates,key=lambda p:p.stat().st_size))
                item["file_verified"]=bool(qa["verified"])
                item["media_qa"]=qa
                if not item["file_verified"]: item["download_error"]="MEDIA_QA_FAILED"
            else:
                item["download_error"]=diagnostic(dl["stderr"])
                item["download_detail"]=reason(dl["stderr"])
        elif item.get("has_drm") or item.get("is_live"):
            item["skip_reason"]="DRM_OR_LIVE_NOT_TESTED"
        # Delete any media immediately after validation.
        shutil.rmtree(attempt_dir,ignore_errors=True)
        items.append(item)
        report["platforms"][site]={"files_verified":sum(bool(x["file_verified"]) for x in items),
                                   "samples_tested":len(items),
                                   "samples":items}
        print("RESULT",site,idx,json.dumps({k:item.get(k) for k in
              ("metadata","probe_error","download_attempted","file_verified","download_error","media_qa")},
              ensure_ascii=False),flush=True)
        checkpoint()
report["finished_at_utc"]=dt.datetime.now(dt.timezone.utc).isoformat()
report["successfully_downloaded_sites"]=[s for s in ("douyin","bilibili","youtube")
                                         if report["platforms"][s]["files_verified"]>0]
report["control_verified"]=report["platforms"]["cc0_control"]["files_verified"]>0
checkpoint()
print("FINAL",json.dumps({"control_verified":report["control_verified"],
    "site_results":{k:{"tested":v["samples_tested"],"verified":v["files_verified"]}
                    for k,v in report["platforms"].items()}},ensure_ascii=False),flush=True)
# Exit 0 if all probes ran and JSON is valid. Failure of sites is a test outcome, NOT CI green claim of success.
