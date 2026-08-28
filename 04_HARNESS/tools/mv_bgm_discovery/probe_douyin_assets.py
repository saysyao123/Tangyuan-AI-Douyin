#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
REPO_ROOT = Path(__file__).resolve().parents[3]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be object: {path}")
    return value


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "_", value.strip())
    return value[:64] or "source"


def asset_id_from_url(url: str) -> str | None:
    m = re.search(r"/ies-music/(\d+)\.mp3", url or "")
    return m.group(1) if m else None


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
        dist = sum(popcount32(a[a0 + i] ^ b[b0 + i]) for i in range(overlap))
        score = 1.0 - dist / (32.0 * overlap)
        candidate = {"score": round(score, 6), "shift": shift, "overlap": overlap}
        if candidate["score"] > best["score"] + 1e-9 or (
            abs(candidate["score"] - best["score"]) <= 1e-9
            and overlap > best["overlap"]
        ):
            best = candidate
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
    last: Exception | None = None
    for headers in [
        None,
        {"Referer": "https://www.douyin.com/"},
        {"Referer": "https://api.bugpk.com/"},
    ]:
        try:
            with session.get(url, headers=headers, stream=True, timeout=120) as r:
                r.raise_for_status()
                with path.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            return
        except Exception as exc:
            last = exc
            path.unlink(missing_ok=True)
    raise RuntimeError(f"download failed: {last}")


def ffprobe(path: Path) -> dict[str, Any]:
    p = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,sample_rate,channels,bit_rate",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(p.stdout)


def extract_mp3(src: Path, dst: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-vn",
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(dst),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def add_option(
    option_files: list[dict[str, Any]],
    seen_hashes: dict[str, str],
    source_path: Path,
    artifact_dir: Path,
    target: dict[str, Any],
    music: dict[str, Any],
    source_kind: str,
) -> None:
    digest = sha256(source_path)
    if digest in seen_hashes:
        return
    option_letter = chr(ord("A") + len(seen_hashes))
    suffix = "" if source_kind == "direct_douyin_music_asset" else "_video_derived"
    option_name = (
        f"HG02_option_{option_letter}_{safe_name(str(target.get('account', 'source')))}{suffix}.mp3"
    )
    option_path = artifact_dir / option_name
    option_path.write_bytes(source_path.read_bytes())
    seen_hashes[digest] = option_name
    option_files.append(
        {
            "option": option_letter,
            "file": option_name,
            "sha256": digest,
            "source_aweme_id": str(target["aweme_id"]),
            "source_account": target.get("account"),
            "music_title": music.get("title"),
            "music_author": music.get("author"),
            "duration_s": float((ffprobe(option_path).get("format") or {}).get("duration") or 0),
            "source_kind": source_kind,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generic Douyin-first MV BGM asset probe")
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    request_path = args.request if args.request.is_absolute() else REPO_ROOT / args.request
    req = load_json(request_path)

    slot_root = REPO_ROOT / str(req["slot_root"])
    report_dir = slot_root / "BGM_DISCOVERY"
    artifact_dir = slot_root / "_hg02_audio_artifact"
    report_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    targets = req.get("targets") or []
    if not targets:
        raise RuntimeError("at least one target is required")

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
            "Referer": "https://api.bugpk.com/doc-douyin.html",
            "X-Requested-With": "XMLHttpRequest",
        }
    )

    reports: list[dict[str, Any]] = []
    direct_fps: dict[str, list[int]] = {}
    video_fps: dict[str, list[int]] = {}
    option_files: list[dict[str, Any]] = []
    seen_hashes: dict[str, str] = {}

    with tempfile.TemporaryDirectory(prefix="mv_bgm_probe_") as td:
        tmp = Path(td)
        for idx, target in enumerate(targets, 1):
            aweme_id = str(target["aweme_id"])
            detail = fetch_detail(session, str(target["work_url"]))
            data = detail.get("data") or {}
            music = data.get("music") if isinstance(data, dict) else None
            music = music if isinstance(music, dict) else {}
            murl = str(music.get("url") or "")
            aid = asset_id_from_url(murl)

            direct_info: dict[str, Any] | None = None
            direct_ok = False
            direct_error: str | None = None
            video_info: dict[str, Any] | None = None
            video_error: str | None = None

            # Correct priority for BGM discovery: direct Douyin music asset first.
            # Video-derived audio is only a fallback when the music asset is absent
            # or its signed URL cannot be downloaded.
            if murl:
                direct_path = artifact_dir / (
                    f"{idx}_{safe_name(str(target.get('account', 'source')))}_direct_music_asset.mp3"
                )
                try:
                    download(session, murl, direct_path)
                    ddur, dfp = parse_fpcalc(direct_path)
                    direct_fps[aweme_id] = dfp
                    direct_info = {
                        "path": direct_path.name,
                        "sha256": sha256(direct_path),
                        "ffprobe": ffprobe(direct_path),
                        "fp_duration": ddur,
                        "fingerprint_length": len(dfp),
                    }
                    add_option(
                        option_files,
                        seen_hashes,
                        direct_path,
                        artifact_dir,
                        target,
                        music,
                        "direct_douyin_music_asset",
                    )
                    direct_ok = True
                except Exception as exc:
                    direct_error = repr(exc)
                    direct_info = {"download_error": direct_error}

            if not direct_ok:
                try:
                    vurl = media_url(detail)
                    if not vurl:
                        raise RuntimeError("no media URL in resolver response")
                    mp4 = tmp / f"{aweme_id}.mp4"
                    download(session, vurl, mp4)
                    vdur, vfp = parse_fpcalc(mp4)
                    video_fps[aweme_id] = vfp
                    video_ref = artifact_dir / (
                        f"{idx}_{safe_name(str(target.get('account', 'source')))}_video_derived.mp3"
                    )
                    extract_mp3(mp4, video_ref)
                    video_info = {
                        "path": video_ref.name,
                        "sha256": sha256(video_ref),
                        "ffprobe": ffprobe(video_ref),
                        "video_ffprobe": ffprobe(mp4),
                        "fp_duration": vdur,
                        "fingerprint_length": len(vfp),
                    }
                    add_option(
                        option_files,
                        seen_hashes,
                        video_ref,
                        artifact_dir,
                        target,
                        music,
                        "video_derived_listening_reference",
                    )
                except Exception as exc:
                    video_error = repr(exc)
            else:
                video_info = {"skipped_reason": "DIRECT_MUSIC_ASSET_AVAILABLE"}

            if not direct_ok and video_info is None:
                raise RuntimeError(
                    f"no usable audio for {target.get('account')}: direct={direct_error}; video={video_error}"
                )

            reports.append(
                {
                    **target,
                    "detail_msg": detail.get("msg", ""),
                    "detail_title": data.get("title") if isinstance(data, dict) else "",
                    "author": data.get("author") if isinstance(data, dict) else None,
                    "music": music,
                    "music_asset_id_from_url": aid,
                    "direct_music_asset": direct_info,
                    "video_fallback": video_info,
                }
            )
            if idx < len(targets):
                time.sleep(3)

    ids = [str(t["aweme_id"]) for t in targets]
    pairwise: list[dict[str, Any]] = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if ids[i] in direct_fps and ids[j] in direct_fps:
                pairwise.append(
                    {
                        "a": ids[i],
                        "b": ids[j],
                        "basis": "direct_music_asset",
                        **best_similarity(direct_fps[ids[i]], direct_fps[ids[j]]),
                    }
                )
            elif ids[i] in video_fps and ids[j] in video_fps:
                pairwise.append(
                    {
                        "a": ids[i],
                        "b": ids[j],
                        "basis": "video_audio",
                        **best_similarity(video_fps[ids[i]], video_fps[ids[j]]),
                    }
                )
            else:
                pairwise.append(
                    {
                        "a": ids[i],
                        "b": ids[j],
                        "basis": "MIXED_OR_UNAVAILABLE",
                        "score": None,
                        "shift": None,
                        "overlap": 0,
                    }
                )

    direct_hashes = [
        str((r.get("direct_music_asset") or {}).get("sha256"))
        for r in reports
        if (r.get("direct_music_asset") or {}).get("sha256")
    ]
    unique_direct_hashes = sorted(set(direct_hashes))
    if len(unique_direct_hashes) == 1 and len(direct_hashes) >= 2:
        decision = "EXACT_ASSET_CONTENT_IDENTITY_CONFIRMED"
    elif len(option_files) > 1:
        decision = "MULTIPLE_DOUYIN_AUDIO_VARIANTS_FOR_HG02"
    elif option_files:
        decision = "SINGLE_HIGH_CONFIDENCE_LISTENING_VARIANT"
    else:
        decision = "BGM_VERSION_DISCOVERY_BLOCKED"

    payload = {
        "schema_version": "1.1-generic",
        "slot_id": req["slot_id"],
        "song_family": req["song_family"],
        "discovery_priority_used": "P1_VERIFIED_DOUYIN_WORKS",
        "resolver": "BugPk /api/douyin",
        "probe_priority": "DIRECT_MUSIC_ASSET_FIRST_VIDEO_FALLBACK",
        "sampled_aweme_ids": ids,
        "works": reports,
        "pairwise_fingerprint": pairwise,
        "direct_music_asset_hashes": unique_direct_hashes,
        "listening_options": option_files,
        "decision": decision,
        "hg02_ready": bool(option_files),
    }
    (report_dir / "asset_probe_report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (artifact_dir / "manifest.json").write_text(
        json.dumps(
            {
                "slot_id": req["slot_id"],
                "song_family": req["song_family"],
                "decision": decision,
                "options": option_files,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "ok": True,
                "slot_id": req["slot_id"],
                "decision": decision,
                "options": option_files,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
