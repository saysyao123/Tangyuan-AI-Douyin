#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import requests

API = "https://api.bugpk.com/api/douyin"
WORK_URL = "https://www.douyin.com/video/7674213606980010597"
OUT_DIR = Path("06_TESTS/MV/WEB_R3/_hg02_audio_artifact")


def fetch_detail(session: requests.Session) -> dict:
    for wait in (0, 3, 7, 15):
        if wait:
            time.sleep(wait)
        r = session.get(API, params={"url": WORK_URL}, timeout=30)
        if r.status_code == 429:
            continue
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and data.get("code") == 200:
            return data
    raise RuntimeError("BugPk single-work parse failed")


def media_url(detail: dict) -> str:
    data = detail.get("data") or {}
    url = data.get("url") or ""
    if url:
        return str(url)
    backup = data.get("video_backup") or []
    if isinstance(backup, list) and backup:
        first = backup[0]
        return str(first.get("url") if isinstance(first, dict) else first)
    return ""


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
        "Referer": "https://www.douyin.com/",
    })
    detail = fetch_detail(session)
    url = media_url(detail)
    if not url:
        raise RuntimeError("No resolved video media URL")

    mp4 = OUT_DIR / "source.mp4"
    with session.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with mp4.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    mp3 = OUT_DIR / "如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(mp4),
        "-vn", "-c:a", "libmp3lame", "-b:a", "192k", str(mp3)
    ], check=True)

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration,size",
        "-of", "json", str(mp3)
    ], check=True, capture_output=True, text=True)
    info = json.loads(probe.stdout)
    receipt = {
        "song_family": "如果风会替我说话",
        "source_account": "火乐烁",
        "source_aweme_id": "7674213606980010597",
        "douyin_music_asset_id": "7670880580757867270",
        "purpose": "HG02 listening reference only",
        "audio_probe": info,
    }
    (OUT_DIR / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp4.unlink(missing_ok=True)
    print(json.dumps(receipt, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
