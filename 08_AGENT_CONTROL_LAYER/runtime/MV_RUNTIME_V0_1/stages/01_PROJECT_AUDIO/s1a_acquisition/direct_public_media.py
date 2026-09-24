#!/usr/bin/env python3
import hashlib, json, mimetypes, os, subprocess, sys, urllib.request
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: direct_public_media.py <https-url> [output_dir]", file=sys.stderr)
    raise SystemExit(2)

url=sys.argv[1]
out=Path(sys.argv[2] if len(sys.argv)>2 else "direct_out")
out.mkdir(parents=True,exist_ok=True)

if not url.startswith("https://"):
    raise SystemExit("Only HTTPS public media URLs are accepted.")

req=urllib.request.Request(url,method="HEAD",headers={"User-Agent":"Tangyuan-S1A/0.1"})
try:
    with urllib.request.urlopen(req,timeout=30) as r:
        ctype=(r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        length=r.headers.get("Content-Length")
except Exception as e:
    (out/"acquisition_report.json").write_text(json.dumps({
      "adapter":"DIRECT_PUBLIC_MEDIA_V0_1","url":url,"status":"HEAD_FAILED","error":str(e)
    },ensure_ascii=False,indent=2),encoding="utf-8")
    raise

if not (ctype.startswith("audio/") or ctype.startswith("video/") or ctype in {"application/octet-stream"}):
    report={"adapter":"DIRECT_PUBLIC_MEDIA_V0_1","url":url,"status":"REJECTED_CONTENT_TYPE","content_type":ctype}
    (out/"acquisition_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(0)

ext=mimetypes.guess_extension(ctype) or ".bin"
dest=out/("media"+ext)
req=urllib.request.Request(url,headers={"User-Agent":"Tangyuan-S1A/0.1"})
with urllib.request.urlopen(req,timeout=90) as r, open(dest,"wb") as f:
    while True:
        chunk=r.read(1024*1024)
        if not chunk: break
        f.write(chunk)

sha=hashlib.sha256(dest.read_bytes()).hexdigest()
try:
    probe=json.loads(subprocess.check_output([
      "ffprobe","-v","error",
      "-show_entries","format=duration,format_name,bit_rate:stream=codec_name,codec_type,sample_rate,channels,width,height",
      "-of","json",str(dest)
    ],text=True))
except Exception as e:
    probe={"error":str(e)}

status="MEDIA_ACQUIRED" if "error" not in probe else "MEDIA_BYTES_ACQUIRED_PROBE_FAILED"
report={
  "adapter":"DIRECT_PUBLIC_MEDIA_V0_1",
  "url":url,
  "status":status,
  "content_type":ctype,
  "content_length_header":length,
  "bytes":dest.stat().st_size,
  "sha256":sha,
  "artifact":str(dest),
  "probe":probe
}
(out/"acquisition_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
