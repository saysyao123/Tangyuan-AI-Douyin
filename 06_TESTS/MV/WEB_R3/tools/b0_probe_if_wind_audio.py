#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import requests

API = "https://api.bugpk.com/api/douyin"
TARGETS = [
    {
        "account": "火乐烁",
        "aweme_id": "7674213606980010597",
        "work_url": "https://www.douyin.com/video/7674213606980010597",
    },
    {
        "account": "XIANGJISHI",
        "aweme_id": "7674182530162440933",
        "work_url": "https://www.douyin.com/video/7674182530162440933",
    },
    {
        "account": "乐 ♩青春",
        "aweme_id": "7673915982527960265",
        "work_url": "https://www.douyin.com/video/7673915982527960265",
    },
]


def popcount32(x: int) -> int:
    return (x & 0xFFFFFFFF).bit_count()


def parse_fpcalc(path: Path) -> tuple[float, list[int]]:
    proc = subprocess.run(
        ["fpcalc", "-raw", "-length", "120", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    duration = 0.0
    fp: list[int] = []
    for line in proc.stdout.splitlines():
        if line.startswith("DURATION="):
            duration = float(line.split("=", 1)[1])
        elif line.startswith("FINGERPRINT="):
            raw = line.split("=", 1)[1].strip()
            fp = [int(x) for x in raw.split(",") if x]
    return duration, fp


def best_fingerprint_similarity(a: list[int], b: list[int]) -> dict[str, Any]:
    if not a or not b:
        return {"score": 0.0, "shift": None, "overlap": 0}

    best = {"score": -1.0, "shift": 0, "overlap": 0}
    min_overlap = min(24, len(a), len(b))
    if min_overlap < 8:
        min_overlap = max(4, min(len(a), len(b)))

    # shift > 0 means b begins later relative to a.
    for shift in range(-(len(b) - min_overlap), len(a) - min_overlap + 1):
        a_start = max(0, shift)
        b_start = max(0, -shift)
        overlap = min(len(a) - a_start, len(b) - b_start)
        if overlap < min_overlap:
            continue
        dist = 0
        for i in range(overlap):
            dist += popcount32(a[a_start + i] ^ b[b_start + i])
        score = 1.0 - (dist / (32.0 * overlap))
        # Prefer more overlap when scores are almost equal.
        if score > best["score"] + 1e-9 or (
            abs(score - best["score"]) <= 1e-9 and overlap > best["overlap"]
        ):
            best = {"score": round(score, 6), "shift": shift, "overlap": overlap}
    return best


def fetch_detail(session: requests.Session, url: str) -> dict[str, Any]:
    waits = [0, 3, 7, 15]
    last_exc: Exception | None = None
    for attempt, wait in enumerate(waits):
        if wait:
            time.sleep(wait)
        try:
            r = session.get(API, params={"url": url}, timeout=30)
            if r.status_code == 429:
                continue
            r.raise_for_status()
            data = r.json()
            if not isinstance(data, dict) or data.get("code") != 200:
                raise RuntimeError(f"business failure: {data}")
            return data
        except Exception as exc:
            last_exc = exc
    raise RuntimeError(f"detail request failed: {last_exc}")


def media_url_from_detail(detail: dict[str, Any]) -> str:
    data = detail.get("data") or {}
    if not isinstance(data, dict):
        return ""
    url = data.get("url") or ""
    if url:
        return str(url)
    backups = data.get("video_backup") or []
    if isinstance(backups, list) and backups:
        first = backups[0]
        if isinstance(first, dict):
            return str(first.get("url") or "")
        return str(first)
    return ""


def ffprobe(path: Path) -> dict[str, Any]:
    proc = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration:stream=codec_type,codec_name,sample_rate,channels",
            "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def main() -> int:
    out_dir = Path("06_TESTS/MV/WEB_R3/B0_IF_WIND_AUDIO_PROBE")
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
        "Referer": "https://www.douyin.com/",
    })

    reports: list[dict[str, Any]] = []
    fingerprints: dict[str, list[int]] = {}

    with tempfile.TemporaryDirectory(prefix="r3_b0_ifwind_") as tmp:
        tmpdir = Path(tmp)
        for index, target in enumerate(TARGETS, 1):
            detail = fetch_detail(session, target["work_url"])
            data = detail.get("data") or {}
            media_url = media_url_from_detail(detail)
            if not media_url:
                raise RuntimeError(f"no media url for {target['account']}")

            media_path = tmpdir / f"{target['aweme_id']}.mp4"
            with session.get(media_url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with media_path.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

            probe = ffprobe(media_path)
            fp_duration, fp = parse_fpcalc(media_path)
            fingerprints[target["aweme_id"]] = fp

            reports.append({
                **target,
                "detail_msg": detail.get("msg", ""),
                "detail_type": data.get("type") if isinstance(data, dict) else None,
                "detail_title": data.get("title") if isinstance(data, dict) else "",
                "author": data.get("author") if isinstance(data, dict) else "",
                "music": data.get("music") if isinstance(data, dict) else None,
                "bytes": media_path.stat().st_size,
                "ffprobe": probe,
                "fp_duration": fp_duration,
                "fingerprint_length": len(fp),
            })

            if index < len(TARGETS):
                time.sleep(3)

    pairs = []
    for i in range(len(TARGETS)):
        for j in range(i + 1, len(TARGETS)):
            a = TARGETS[i]
            b = TARGETS[j]
            sim = best_fingerprint_similarity(
                fingerprints[a["aweme_id"]], fingerprints[b["aweme_id"]]
            )
            pairs.append({
                "a_account": a["account"],
                "a_aweme_id": a["aweme_id"],
                "b_account": b["account"],
                "b_aweme_id": b["aweme_id"],
                **sim,
            })

    min_score = min((p["score"] for p in pairs), default=0.0)
    # Chromaprint same-recording matches are normally much higher than unrelated audio.
    same_audio_family = min_score >= 0.70
    summary = {
        "song_family": "如果风会替我说话",
        "targets": len(TARGETS),
        "all_detail_parse_pass": len(reports) == len(TARGETS),
        "pairwise_min_similarity": min_score,
        "same_audio_family": same_audio_family,
        "decision": "SAME_AUDIO_FAMILY_CONFIRMED" if same_audio_family else "AUDIO_MISMATCH_OR_REVIEW_REQUIRED",
    }
    payload = {"summary": summary, "works": reports, "pairwise": pairs}
    (out_dir / "audio_probe_report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if same_audio_family else 2


if __name__ == "__main__":
    raise SystemExit(main())
