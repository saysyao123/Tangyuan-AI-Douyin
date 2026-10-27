#!/usr/bin/env python3
"""Public-URL video extraction smoke test. No cookies, DRM bypass, or media uploads."""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import time
import traceback

ROOT = pathlib.Path("yoinks_probe")
ROOT.mkdir(exist_ok=True)
SAMPLES = {
    "douyin": "https://www.douyin.com/video/7682249897617247522",
    "bilibili": "https://www.bilibili.com/video/BV1AerZB6EWa/",
    "youtube": "https://www.youtube.com/watch?v=YE7VzlLtp-4",
    "hongguo": "https://hongguoduanju.com/player/7690961604636052505",
}

def call(cmd: list[str], timeout: int) -> dict:
    before = time.monotonic()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout)
        return {"returncode": p.returncode, "stdout": p.stdout[-6000:], "stderr": p.stderr[-4000:],
                "seconds": round(time.monotonic() - before, 1)}
    except subprocess.TimeoutExpired as e:
        return {"returncode": None, "stdout": "", "stderr": f"Timed out ({timeout}s): {str(e)[:120]}",
                "seconds": round(time.monotonic() - before, 1)}
    except Exception as e:
        return {"returncode": None, "stdout": "", "stderr": f"{type(e).__name__}: {e}",
                "seconds": round(time.monotonic() - before, 1)}

results = {
    "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "yt_dlp_version": call(["yt-dlp", "--version"], 15)["stdout"].strip(),
    "ffmpeg_version": call(["ffmpeg", "-version"], 15)["stdout"].splitlines()[0],
    "mode": "public no-login no-cookies no-DRM probe and up-to-3-second temporary download, original media never uploaded",
    "platforms": {},
}
for name, url in SAMPLES.items():
    print("START", name, url, flush=True)
    folder = ROOT / name
    folder.mkdir(exist_ok=True)
    probe_file = folder / "info.json"
    probe = call(["yt-dlp", "--ignore-config", "--no-playlist", "--no-warnings",
                  "--socket-timeout", "12", "--retries", "1",
                  "--dump-single-json", url], 75)
    data = {"url": url, "probe_exit_code": probe["returncode"], "probe_seconds": probe["seconds"],
            "probe_error_tail": probe["stderr"][-1600:], "metadata_ok": False,
            "download_attempted": False, "media_downloaded": False, "decoded": False}
    if probe["returncode"] == 0:
        try:
            meta = json.loads(probe["stdout"])
            data.update({"metadata_ok": True, "title": str(meta.get("title", ""))[:150],
                         "extractor": meta.get("extractor_key"), "duration": meta.get("duration"),
                         "format_count": len(meta.get("formats") or []),
                         "is_live": meta.get("is_live"),
                         "availability": meta.get("availability"),
                         "has_drm": meta.get("has_drm")})
        except Exception as exc:
            data["metadata_parse_error"] = str(exc)
    # Intentionally do not attempt downloads of DRM-protected or live sources.
    if data["metadata_ok"] and data.get("has_drm") in (None, False) and not data.get("is_live"):
        data["download_attempted"] = True
        args = ["yt-dlp", "--ignore-config", "--no-playlist", "--no-warnings",
                "--socket-timeout", "12", "--retries", "1", "--fragment-retries", "1",
                "--no-progress", "--no-overwrites", "--max-filesize", "25M",
                "-f", "best[height<=480]/bestvideo[height<=480]+bestaudio/best",
                "--download-sections", "*0-3", "--merge-output-format", "mp4",
                "-o", str(folder / "video.%(ext)s"), url]
        dl = call(args, 100)
        data.update({"download_exit_code": dl["returncode"],
                     "download_seconds": dl["seconds"],
                     "download_error_tail": (dl["stderr"] + "\n" + dl["stdout"])[-1600:]})
        video_files = [p for p in folder.iterdir() if p.is_file() and p.name.startswith("video.")
                       and not p.name.endswith((".part", ".ytdl", ".json"))]
        if video_files:
            f = sorted(video_files, key=lambda p: p.stat().st_size, reverse=True)[0]
            data["file_extension"] = f.suffix
            data["file_bytes"] = f.stat().st_size
            fp = call(["ffprobe", "-v", "error", "-show_entries",
                       "format=duration:stream=codec_type,codec_name,width,height",
                       "-of", "json", str(f)], 25)
            try:
                obj = json.loads(fp["stdout"])
                streams = obj.get("streams") or []
                data["video_streams"] = [x for x in streams if x.get("codec_type") == "video"]
                data["audio_streams"] = [x for x in streams if x.get("codec_type") == "audio"]
                data["media_duration"] = obj.get("format", {}).get("duration")
                data["media_downloaded"] = bool(data["video_streams"]) and f.stat().st_size > 0
                if data["media_downloaded"]:
                    decode = call(["ffmpeg", "-v", "error", "-i", str(f), "-t", "1",
                                   "-f", "null", "-"], 25)
                    data["decoded"] = decode["returncode"] == 0
                    data["decode_error"] = decode["stderr"][-600:]
            except Exception as exc:
                data["ffprobe_error"] = str(exc)
    for p in folder.iterdir():
        if p.is_file():
            p.unlink()
    results["platforms"][name] = data
    print("RESULT", name, json.dumps(data, ensure_ascii=False), flush=True)
    (ROOT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

results["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
(ROOT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print("FINAL", json.dumps(results, ensure_ascii=False), flush=True)
