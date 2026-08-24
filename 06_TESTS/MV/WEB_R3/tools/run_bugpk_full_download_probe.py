#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from pathlib import Path
from typing import Any

import requests

BASE = "https://api.bugpk.com/api/douyin"
BACKOFF = (3, 7, 15)
SAMPLES = [
    ("P01", "7674893658771970981", "https://www.douyin.com/video/7674893658771970981"),
    ("P03", "7674976213065112294", "https://www.douyin.com/video/7674976213065112294"),
    ("P09", "7674993950716867770", "https://www.douyin.com/video/7674993950716867770"),
]


def fetch_json(session: requests.Session, url: str) -> dict[str, Any]:
    last = None
    for attempt in range(len(BACKOFF) + 1):
        try:
            response = session.get(BASE, params={"url": url}, timeout=30)
            if response.status_code == 429 and attempt < len(BACKOFF):
                time.sleep(BACKOFF[attempt])
                continue
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last = exc
            if attempt < len(BACKOFF):
                time.sleep(BACKOFF[attempt])
    raise RuntimeError(str(last))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def ffprobe(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate",
        "-of", "json", str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main() -> int:
    root = Path(__file__).resolve().parents[4]
    out = root / "06_TESTS/MV/WEB_R3/_bugpk_full_download_probe"
    out.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
    })

    reports = []
    for index, (case_id, aweme_id, share_url) in enumerate(SAMPLES):
        report: dict[str, Any] = {"case_id": case_id, "aweme_id": aweme_id, "share_url": share_url}
        temp = out / f"{case_id}_{aweme_id}.mp4"
        try:
            detail = fetch_json(session, share_url)
            data = detail.get("data") or {}
            video_url = data.get("url")
            backups = data.get("video_backup")
            if not video_url and isinstance(backups, list) and backups:
                first = backups[0]
                video_url = first.get("url") if isinstance(first, dict) else str(first)
            if detail.get("code") != 200 or not video_url:
                raise RuntimeError(f"single parse failed: code={detail.get('code')} msg={detail.get('msg')}")

            with session.get(
                video_url,
                headers={"Referer": "https://www.douyin.com/"},
                stream=True,
                timeout=120,
                allow_redirects=True,
            ) as response:
                response.raise_for_status()
                with temp.open("wb") as file:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            file.write(chunk)
                report["http_status"] = response.status_code
                report["content_type"] = response.headers.get("content-type", "")
                report["final_media_url_host"] = requests.utils.urlparse(response.url).hostname or ""

            report["bytes"] = temp.stat().st_size
            report["sha256"] = sha256(temp)
            report["ffprobe"] = ffprobe(temp)
            streams = report["ffprobe"].get("streams") or []
            report["has_video_stream"] = any(stream.get("codec_type") == "video" for stream in streams)
            report["pass"] = report["bytes"] > 100000 and report["has_video_stream"]
            report["parse_msg"] = detail.get("msg", "")
            report["title"] = data.get("title", "")
        except Exception as exc:
            report["pass"] = False
            report["error"] = str(exc)[:500]
        finally:
            if temp.exists():
                temp.unlink()
        reports.append(report)
        if index < len(SAMPLES) - 1:
            time.sleep(4)

    summary = {
        "samples": len(reports),
        "passed": sum(1 for report in reports if report.get("pass")),
        "all_pass": all(report.get("pass") for report in reports),
    }
    (out / "full_download_probe.json").write_text(
        json.dumps({"summary": summary, "reports": reports}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return 0 if summary["all_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
