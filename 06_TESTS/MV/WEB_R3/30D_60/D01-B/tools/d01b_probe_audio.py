#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import requests

API = "https://api.bugpk.com/api/douyin"
ROOT = Path("06_TESTS/MV/WEB_R3/30D_60/D01-B")
REPORT_DIR = ROOT / "BGM_DISCOVERY"
ARTIFACT_DIR = ROOT / "_hg02_audio_artifact"
TARGETS = [
    {
        "account": "Aura",
        "aweme_id": "7673460363010018611",
        "work_url": "https://www.douyin.com/video/7673460363010018611",
    },
    {
        "account": "XIANGJISHI",
        "aweme_id": "7673442358406957285",
        "work_url": "https://www.douyin.com/video/7673442358406957285",
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def asset_id_from_url(url: str) -> str | None:
    m = re.search(r"/ies-music/(\d+)\.mp3", url or "")
    return m.group(1) if m else None


def popcount32(x: int) -> int:
    return (x & 0xFFFFFFFF).bit_count()


def parse_fpcalc(path: Path) -> tuple[float, list[int]]:
    proc = subprocess.run(
        ["fpcalc", "-raw", "-length", "120", str(path)],
        check=True, capture_output=True, text=True,
    )
    duration = 0.0
    fp: list[int] = []
    for line in proc.stdout.splitlines():
        if line.startswith("DURATION="):
            duration = float(line.split("=", 1)[1])
        elif line.startswith("FINGERPRINT="):
            fp = [int(x) for x in line.split("=", 1)[1].split(",") if x]
    return duration, fp


def best_similarity(a: list[int], b: list[int]) -> dict[str, Any]:
    if not a or not b:
        return {"score": 0.0, "shift": None, "overlap": 0}
    min_overlap = min(24, len(a), len(b))
    if min_overlap < 8:
        min_overlap = max(4, min(len(a), len(b)))
    best = {"score": -1.0, "shift": 0, "overlap": 0}
    for shift in range(-(len(b) - min_overlap), len(a) - min_overlap + 1):
        a0 = max(0, shift)
        b0 = max(0, -shift)
        overlap = min(len(a) - a0, len(b) - b0)
        if overlap < min_overlap:
            continue
        dist = sum(popcount32(a[a0+i] ^ b[b0+i]) for i in range(overlap))
        score = 1.0 - dist / (32.0 * overlap)
        if score > best["score"] + 1e-9 or (abs(score - best["score"]) <= 1e-9 and overlap > best["overlap"]):
            best = {"score": round(score, 6), "shift": shift, "overlap": overlap}
    return best


def fetch_detail(session: requests.Session, url: str) -> dict[str, Any]:
    last: Exception | None = None
    for wait in [0, 3, 7, 15]:
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
            last = exc
    raise RuntimeError(f"detail request failed: {last}")


def media_url(detail: dict[str, Any]) -> str:
    data = detail.get("data") or {}
    if not isinstance(data, dict):
        return ""
    if data.get("url"):
        return str(data["url"])
    backups = data.get("video_backup") or []
    if backups:
        first = backups[0]
        return str(first.get("url") if isinstance(first, dict) else first)
    return ""


def download(session: requests.Session, url: str, path: Path) -> None:
    with session.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def ffprobe(path: Path) -> dict[str, Any]:
    p = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration:stream=codec_type,codec_name,sample_rate,channels,bit_rate",
        "-of", "json", str(path)
    ], check=True, capture_output=True, text=True)
    return json.loads(p.stdout)


def extract_mp3(src: Path, dst: Path) -> None:
    subprocess.run([
        "ffmpeg", "-y", "-i", str(src), "-vn",
        "-codec:a", "libmp3lame", "-q:a", "2", str(dst)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
        "Referer": "https://www.douyin.com/",
    })

    reports: list[dict[str, Any]] = []
    fps: dict[str, list[int]] = {}
    direct_assets: dict[str, Path] = {}
    video_refs: dict[str, Path] = {}

    with tempfile.TemporaryDirectory(prefix="r3_d01b_audio_") as td:
        tmp = Path(td)
        for idx, target in enumerate(TARGETS, 1):
            detail = fetch_detail(session, target["work_url"])
            data = detail.get("data") or {}
            music = data.get("music") if isinstance(data, dict) else None
            music = music if isinstance(music, dict) else {}
            murl = str(music.get("url") or "")
            aid = asset_id_from_url(murl)

            vurl = media_url(detail)
            if not vurl:
                raise RuntimeError(f"no media URL for {target['account']}")
            mp4 = tmp / f"{target['aweme_id']}.mp4"
            download(session, vurl, mp4)
            vprobe = ffprobe(mp4)
            fpdur, fp = parse_fpcalc(mp4)
            fps[target["aweme_id"]] = fp

            ref_mp3 = ARTIFACT_DIR / f"{idx}_{target['account']}_video_derived.mp3"
            extract_mp3(mp4, ref_mp3)
            video_refs[target["aweme_id"]] = ref_mp3

            direct_info: dict[str, Any] | None = None
            if murl:
                direct_path = ARTIFACT_DIR / f"{idx}_{target['account']}_direct_music_asset.mp3"
                try:
                    download(session, murl, direct_path)
                    dprobe = ffprobe(direct_path)
                    ddur, dfp = parse_fpcalc(direct_path)
                    direct_assets[target["aweme_id"]] = direct_path
                    direct_info = {
                        "path": direct_path.name,
                        "sha256": sha256(direct_path),
                        "ffprobe": dprobe,
                        "fp_duration": ddur,
                        "fingerprint_length": len(dfp),
                    }
                except Exception as exc:
                    direct_info = {"download_error": repr(exc)}

            reports.append({
                **target,
                "detail_msg": detail.get("msg", ""),
                "detail_title": data.get("title") if isinstance(data, dict) else "",
                "author": data.get("author") if isinstance(data, dict) else None,
                "music": music,
                "music_asset_id_from_url": aid,
                "video_bytes": mp4.stat().st_size,
                "video_ffprobe": vprobe,
                "video_fp_duration": fpdur,
                "video_fingerprint_length": len(fp),
                "video_reference": {
                    "path": ref_mp3.name,
                    "sha256": sha256(ref_mp3),
                    "ffprobe": ffprobe(ref_mp3),
                },
                "direct_music_asset": direct_info,
            })
            if idx < len(TARGETS):
                time.sleep(3)

    pair = best_similarity(fps[TARGETS[0]["aweme_id"]], fps[TARGETS[1]["aweme_id"]])
    asset_ids = [r.get("music_asset_id_from_url") for r in reports]
    music_urls = [str((r.get("music") or {}).get("url") or "") for r in reports]
    exact_asset_same = bool(asset_ids[0] and asset_ids[0] == asset_ids[1])
    same_recording = pair["score"] >= 0.70

    preferred = TARGETS[1]["aweme_id"]
    selected_path: Path
    selected_kind: str
    if preferred in direct_assets:
        selected_path = direct_assets[preferred]
        selected_kind = "direct_douyin_music_asset"
    else:
        selected_path = video_refs[preferred]
        selected_kind = "video_derived_listening_reference"

    final_ref = ARTIFACT_DIR / "HG02_reference_我救自己于人间水火.mp3"
    final_ref.write_bytes(selected_path.read_bytes())

    decision = (
        "EXACT_ASSET_IDENTITY_CONFIRMED" if exact_asset_same
        else "SAME_RECORDING_DIFFERENT_ASSET_IDS" if same_recording
        else "AUDIO_VERSION_CONFLICT_REVIEW_REQUIRED"
    )
    payload = {
        "song_family": "我救自己于人间水火",
        "discovery_priority_used": "P1_VERIFIED_DOUYIN_WORKS",
        "sampled_aweme_ids": [t["aweme_id"] for t in TARGETS],
        "works": reports,
        "pairwise_video_fingerprint": pair,
        "asset_ids": asset_ids,
        "music_urls_same": bool(music_urls[0] and music_urls[0] == music_urls[1]),
        "exact_asset_identity": exact_asset_same,
        "same_recording_by_fingerprint": same_recording,
        "selected_listening_source_aweme_id": preferred,
        "selected_listening_source_account": "XIANGJISHI",
        "selected_listening_source_kind": selected_kind,
        "selected_listening_file": final_ref.name,
        "selected_listening_sha256": sha256(final_ref),
        "selected_listening_ffprobe": ffprobe(final_ref),
        "decision": decision,
    }
    (REPORT_DIR / "asset_probe_report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ARTIFACT_DIR / "manifest.json").write_text(
        json.dumps({
            "song_family": payload["song_family"],
            "decision": decision,
            "selected_file": final_ref.name,
            "selected_sha256": payload["selected_listening_sha256"],
            "source_aweme_id": preferred,
            "source_kind": selected_kind,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "decision": decision,
        "pair_score": pair["score"],
        "asset_ids": asset_ids,
        "selected": final_ref.name,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
