#!/usr/bin/env python3
import json, os, re, subprocess, urllib.parse, urllib.request
from pathlib import Path

CONFIG=Path(__file__).with_name("target.json")
OUT=Path(os.environ.get("S1A_OUT","deezer_out"))
OUT.mkdir(parents=True, exist_ok=True)

def norm(s):
    return re.sub(r"\s+","",(s or "")).lower()

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Tangyuan-S1A/0.1"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def download(url,dest):
    req=urllib.request.Request(url,headers={"User-Agent":"Tangyuan-S1A/0.1"})
    with urllib.request.urlopen(req,timeout=60) as r, open(dest,"wb") as f:
        f.write(r.read())

def probe(path):
    try:
        out=subprocess.check_output([
          "ffprobe","-v","error",
          "-show_entries","format=duration,format_name,bit_rate:stream=codec_name,codec_type,sample_rate,channels",
          "-of","json",str(path)
        ],text=True)
        return json.loads(out)
    except Exception as e:
        return {"error":str(e)}

cfg=json.loads(CONFIG.read_text(encoding="utf-8"))
title=cfg["title"]
artist_hints=cfg.get("artist_hints",[])
queries=[title]+[f'{title} {a}' for a in artist_hints]
seen={}
qlog=[]

for q in queries:
    url="https://api.deezer.com/search?"+urllib.parse.urlencode({"q":q,"limit":100})
    try:
        data=get_json(url)
        items=data.get("data",[])
        qlog.append({"term":q,"count":len(items)})
        for x in items:
            seen[str(x.get("id"))]=x
    except Exception as e:
        qlog.append({"term":q,"error":str(e)})

nt=norm(title)
cands=[]
exact=[]
for x in seen.values():
    artist=(x.get("artist") or {}).get("name")
    rec={
      "id":x.get("id"),
      "title":x.get("title"),
      "title_short":x.get("title_short"),
      "artist":artist,
      "album":(x.get("album") or {}).get("title"),
      "duration":x.get("duration"),
      "link":x.get("link"),
      "preview":x.get("preview"),
      "rank":x.get("rank")
    }
    title_match=norm(rec["title_short"] or rec["title"])==nt
    artist_match=any(norm(h) in norm(artist) for h in artist_hints) if artist_hints else True
    rec["title_match"]=title_match
    rec["artist_match"]=artist_match
    cands.append(rec)
    if title_match and artist_match and rec["preview"]:
        exact.append(rec)

report={
 "adapter":"DEEZER_PREVIEW_V0_1",
 "target":cfg,
 "queries":qlog,
 "candidate_count":len(cands),
 "exact_preview_matches":exact,
 "status":"NO_EXACT_PREVIEW_MATCH"
}

if exact:
    chosen=exact[0]
    dest=OUT/"preview.mp3"
    download(chosen["preview"],dest)
    report["status"]="MEDIA_ACQUIRED"
    report["chosen"]=chosen
    report["artifact"]=str(dest)
    report["bytes"]=dest.stat().st_size
    report["probe"]=probe(dest)

(OUT/"acquisition_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"candidates.json").write_text(json.dumps(cands,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
