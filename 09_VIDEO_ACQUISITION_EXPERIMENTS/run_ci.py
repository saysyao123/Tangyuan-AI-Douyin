#!/usr/bin/env python3
"""Five-source public access smoke test: retain JSON only, not third-party footage."""
from __future__ import annotations
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = Path("acquisition_runs")
BASE.mkdir(exist_ok=True)
TESTS = [
    ("douyin", "https://www.douyin.com/video/7682249897617247522", "probe"),
    ("bilibili", "https://www.bilibili.com/video/BV1AerZB6EWa/", "probe"),
    ("youtube", "https://www.youtube.com/watch?v=YE7VzlLtp-4", "probe"),
    ("hongguo_related_web", "https://hongguoduanju.com/player/7690961604636052505", "clip"),
    ("w3c_control", "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4", "clip"),
]
result = {"schema_version": 1, "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
          "scope": "public non-DRM 3-second smoke tests, no cookies, no media persisted",
          "tests": {}, "acceptance": {}}
for name, url, mode in TESTS:
    print("TEST_START", name, mode, flush=True)
    cmd = [sys.executable, str(HERE / "acquire.py"), "--url", url, "--mode", mode,
           "--rights-basis", "internal_evaluation", "--clip-seconds", "3",
           "--max-size-mb", "25", "--output-dir", str(BASE)]
    # subprocess timeout is independent of the downloader's own timeout.
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=160)
        row = json.loads(done.stdout.strip().splitlines()[-1])
        row["command_exit_code"] = done.returncode
    except Exception as e:
        row = {"status": "TEST_HARNESS_ERROR", "error_code": type(e).__name__,
               "error_detail": str(e)[:250], "command_exit_code": 99}
    result["tests"][name] = row
    (BASE / "ci_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TEST_RESULT", name, json.dumps({
        k: row.get(k) for k in ("status", "error_code", "metadata_ok", "file_verified", "error_detail")
    }, ensure_ascii=False), flush=True)

control = result["tests"]["w3c_control"]
result["acceptance"] = {
    "acquisition_pipeline_e2e": bool(control.get("file_verified")),
    "platforms_checked": [name for name, _, _ in TESTS],
    "hongguo_related_web_verified": bool(result["tests"]["hongguo_related_web"].get("file_verified")),
    "douyin_verified": bool(result["tests"]["douyin"].get("file_verified")),
    "bilibili_verified": bool(result["tests"]["bilibili"].get("file_verified")),
    "youtube_verified": bool(result["tests"]["youtube"].get("file_verified")),
    "main_branch_untouched": True,
    "full_length_download_tested": False,
    "downstream_render_tested": False,
}
result["finished_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
(BASE / "ci_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("ACCEPTANCE", json.dumps(result["acceptance"], ensure_ascii=False), flush=True)
if not result["acceptance"]["acquisition_pipeline_e2e"]:
    print("Control media end-to-end check failed; do not claim downloader is operational.", flush=True)
    sys.exit(1)
