#!/usr/bin/env python3
import json, os, re, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

CONFIG = Path(__file__).with_name("target.json")
OUT = Path(os.environ.get("S1A_OUT", "s1a_out"))
OUT.mkdir(parents=True, exist_ok=True)

def norm(s):
    return re.sub(r"\s+", "", (s or "")).lower()

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Tangyuan-S1A/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent":"Tangyuan-S1A/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())

def probe(path):
    cmd = ["ffprobe","-v","error","-show_entries",
           "format=duration,format_name,bit_rate:stream=codec_name,codec_type,sample_rate,channels",
           "-of","json",str(path)]
    try:
        return json.loads(subprocess.check_output(cmd, text=True))
    except Exception as e:
        return {"error": str(e)}

cfg=json.loads(CONFIG.read_text(encoding="utf-8"))
title=cfg["title"]
artist_hints=cfg.get("artist_hints",[])
countries=cfg.get("countries",["cn","hk","tw","us"])
terms=[title] + [f"{title} {a}" for a in artist_hints]

seen={}
queries=[]
for country in countries:
    for term in terms:
        params=urllib.parse.urlencode({"term":term,"entity":"song","limit":50,"country":country})
        url="https://itunes.apple.com/search?"+params
        try:
            data=fetch_json(url)
            queries.append({"country":country,"term":term,"count":data.get("resultCount",0)})
            for x in data.get("results",[]):
                key=str(x.get("trackId") or x.get("previewUrl") or (x.get("trackName"),x.get("artistName")))
                seen[key]=x
        except Exception as e:
            queries.append({"country":country,"term":term,"error":str(e)})

cands=[]
exact=[]
nt=norm(title)
for x in seen.values():
    rec={
      "trackId":x.get("trackId"),
      "trackName":x.get("trackName"),
      "artistName":x.get("artistName"),
      "collectionName":x.get("collectionName"),
      "country":x.get("country"),
      "trackViewUrl":x.get("trackViewUrl"),
      "previewUrl":x.get("previewUrl"),
      "trackTimeMillis":x.get("trackTimeMillis"),
      "releaseDate":x.get("releaseDate"),
      "primaryGenreName":x.get("primaryGenreName"),
    }
    title_match = norm(rec["trackName"]) == nt
    artist_match = any(norm(h) in norm(rec["artistName"]) for h in artist_hints) if artist_hints else True
    rec["title_match"]=title_match
    rec["artist_match"]=artist_match
    cands.append(rec)
    if title_match and artist_match and rec["previewUrl"]:
        exact.append(rec)

report={
  "adapter":"APPLE_ITUNES_PREVIEW_V0_1",
  "target":cfg,
  "queries":queries,
  "candidate_count":len(cands),
  "exact_preview_matches":exact,
  "status":"NO_EXACT_PREVIEW_MATCH"
}

if exact:
    chosen=exact[0]
    ext=".m4a"
    url=chosen["previewUrl"]
    if ".mp3" in url.lower(): ext=".mp3"
    dest=OUT/("preview"+ext)
    download(url,dest)
    report["status"]="MEDIA_ACQUIRED"
    report["chosen"]=chosen
    report["artifact"]=str(dest)
    report["bytes"]=dest.stat().st_size
    report["probe"]=probe(dest)

(OUT/"acquisition_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"candidates.json").write_text(json.dumps(cands,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
