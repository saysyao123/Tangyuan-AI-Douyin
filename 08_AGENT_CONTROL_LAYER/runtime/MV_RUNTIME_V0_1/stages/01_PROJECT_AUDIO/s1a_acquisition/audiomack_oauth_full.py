#!/usr/bin/env python3
"""
Authorized Audiomack full-source adapter.

Requires:
  AUDIOMACK_CONSUMER_KEY
  AUDIOMACK_CONSUMER_SECRET

This adapter intentionally does not attempt anonymous/private endpoint bypass.
"""
import json, os, sys, urllib.parse
from pathlib import Path

try:
    import requests
    from requests_oauthlib import OAuth1
except ImportError:
    raise SystemExit("Install requests and requests-oauthlib")

OUT=Path(os.environ.get("S1A_OUT","audiomack_oauth_out"))
OUT.mkdir(parents=True,exist_ok=True)

key=os.environ.get("AUDIOMACK_CONSUMER_KEY")
secret=os.environ.get("AUDIOMACK_CONSUMER_SECRET")
if not key or not secret:
    report={"adapter":"AUDIOMACK_OAUTH_FULL_V0_1","status":"CREDENTIALS_REQUIRED"}
    (OUT/"acquisition_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    raise SystemExit(0)

slug=os.environ.get("AUDIOMACK_TRACK_PATH","song/yu-yi-8/ruo-ai-you-jin-tou")
base="https://api.audiomack.com/v1"
auth=OAuth1(key,secret)

info_url=f"{base}/music/{slug}"
r=requests.get(info_url,auth=auth,timeout=30)
info_text=r.text
try: info=r.json()
except Exception: info={"raw":info_text[:4000]}

stream=None
if r.ok:
    stream=info.get("streaming_url")

# Official Play Track endpoint can return a fresh streaming source.
play_url=f"{base}/music/{slug}/play"
pr=requests.post(play_url,auth=auth,timeout=30)
if pr.ok:
    try:
        x=pr.json()
        if isinstance(x,str): stream=x
        elif isinstance(x,dict): stream=x.get("streaming_url") or x.get("url") or stream
    except Exception:
        raw=pr.text.strip().strip('"')
        if raw.startswith("http"): stream=raw

report={
  "adapter":"AUDIOMACK_OAUTH_FULL_V0_1",
  "track_path":slug,
  "info_status":r.status_code,
  "play_status":pr.status_code,
  "status":"NO_STREAM_URL",
  "stream_url_present":bool(stream)
}

if stream:
    dest=OUT/"full_source.mp3"
    rr=requests.get(stream,timeout=120)
    rr.raise_for_status()
    dest.write_bytes(rr.content)
    report["status"]="MEDIA_BYTES_ACQUIRED"
    report["artifact"]=str(dest)
    report["bytes"]=dest.stat().st_size

(OUT/"acquisition_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
