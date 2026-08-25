#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path("06_TESTS/MV/WEB_R3/30D_60/D01-B")
OUT = ROOT / "AUDIO_TIMELINE_PACKAGE_VERIFY"
OUT.mkdir(parents=True, exist_ok=True)

ASSET_URL = "https://lf3-music-east.douyinstatic.com/obj/ies-music-hj/7673442361086610233.mp3"
LRC_PAGE = "https://www.gequbao.com/music/58674784"
EXPECTED_SOURCE_STARTS = [91.11, 94.84, 98.71, 102.60, 105.96]
SEMANTIC_IDS = [
    "L01_SELF_RESCUE_HOOK",
    "L02_SELF_LOVE_HARDSHIP",
    "L03_BLOOM_RELATIONAL_TURN",
    "L04_BLESSING_REMEMBER_ME",
    "L05_NEXT_VERSE_CONTAMINATION_CHECK",
]


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, binary: bool = False):
    r = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.content if binary else r.text


def extract_timed_lines(page: str) -> list[tuple[float, str]]:
    text = html.unescape(re.sub(r"<[^>]+>", "\n", page))
    found = []
    pat = re.compile(r"\[(\d{2}):(\d{2}(?:\.\d+)?)\]\s*([^\[\n\r]+)")
    for m in pat.finditer(text):
        sec = int(m.group(1)) * 60 + float(m.group(2))
        lyric = m.group(3).strip()
        if lyric:
            found.append((round(sec, 3), lyric))
    # de-dupe exact timestamp/text copies caused by page rendering.
    uniq = []
    seen = set()
    for item in found:
        if item not in seen:
            seen.add(item)
            uniq.append(item)
    return uniq


def select_target(lines: list[tuple[float, str]]) -> list[tuple[float, str]]:
    selected = []
    for expected in EXPECTED_SOURCE_STARTS:
        candidates = [(abs(t - expected), t, s) for t, s in lines if abs(t - expected) <= 0.08]
        if not candidates:
            raise RuntimeError(f"missing trusted LRC timestamp near {expected}")
        _, t, s = min(candidates)
        selected.append((t, s))
    return selected


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def ffprobe(path: Path) -> dict:
    p = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,sample_rate,channels,bit_rate",
        "-of", "json", str(path),
    ])
    return json.loads(p.stdout)


def main() -> int:
    asset = OUT / "locked_raw_asset.mp3"
    asset.write_bytes(fetch(ASSET_URL, binary=True))
    probe = ffprobe(asset)

    page = fetch(LRC_PAGE)
    timed = extract_timed_lines(page)
    selected = select_target(timed)
    trusted = OUT / "trusted_runtime_lyrics.txt"
    trusted.write_text("\n".join(s for _, s in selected) + "\n", encoding="utf-8")

    aligned = OUT / "lyric_align_raw.json"
    cmd = [
        "lyric-align", str(asset), str(trusted),
        "--language", "zh", "--model", "small",
        "-f", "json", "-o", str(aligned),
    ]
    proc = run(cmd)
    raw = json.loads(aligned.read_text(encoding="utf-8"))

    # Normalize likely JSON shapes without preserving copyrighted text.
    items = raw.get("lines") if isinstance(raw, dict) else raw
    if not isinstance(items, list):
        for key in ("aligned", "results", "segments"):
            if isinstance(raw, dict) and isinstance(raw.get(key), list):
                items = raw[key]
                break
    if not isinstance(items, list):
        raise RuntimeError(f"unrecognized lyric-align JSON shape: {type(raw)} keys={list(raw) if isinstance(raw, dict) else None}")

    normalized = []
    for i, (src_start, lyric) in enumerate(selected):
        item = items[i] if i < len(items) and isinstance(items[i], dict) else {}
        start = item.get("start")
        end = item.get("end")
        matched = item.get("matched")
        score = item.get("score", item.get("similarity", item.get("confidence")))
        try:
            start = float(start) if start is not None else None
        except Exception:
            start = None
        try:
            end = float(end) if end is not None else None
        except Exception:
            end = None
        expected_clip = round(src_start - EXPECTED_SOURCE_STARTS[0], 3)
        delta = round(start - expected_clip, 3) if start is not None else None
        normalized.append({
            "line_id": SEMANTIC_IDS[i],
            "lyric_sha256": sha_text(lyric),
            "source_lrc_start_s": src_start,
            "expected_clip_start_s": expected_clip,
            "secondary_align_start_s": start,
            "secondary_align_end_s": end,
            "secondary_matched": bool(matched) if matched is not None else start is not None,
            "secondary_score": score,
            "start_delta_s": delta,
        })

    deltas = [abs(x["start_delta_s"]) for x in normalized[:4] if x["start_delta_s"] is not None]
    matched4 = all(x["secondary_matched"] and x["secondary_align_start_s"] is not None for x in normalized[:4])
    median_delta = sorted(deltas)[len(deltas)//2] if deltas else None
    max_delta = max(deltas) if deltas else None
    # Hard green thresholds mirror mv_audio_timeline.md initial thresholds.
    green = bool(matched4 and median_delta is not None and median_delta <= 0.25 and max_delta is not None and max_delta <= 0.50)

    contamination = normalized[4]
    payload = {
        "song_family": "我救自己于人间水火",
        "audio_asset_id": "7673442361086610233",
        "audio_asset_url_sha256": sha_text(ASSET_URL),
        "audio_sha256": sha_file(asset),
        "audio_probe": probe,
        "primary_route": "CANDIDATE_SAME_VERSION_LRC",
        "primary_source_url": LRC_PAGE,
        "source_occurrence": "SECOND_CHORUS_CANDIDATE",
        "source_clip_offset_s": EXPECTED_SOURCE_STARTS[0],
        "secondary_route": "LYRIC_ALIGN_FASTER_WHISPER_CJK_FUZZY_ANCHOR",
        "secondary_model": "faster-whisper small / zh",
        "line_results_redacted": normalized,
        "first_four_all_matched": matched4,
        "first_four_median_abs_start_delta_s": median_delta,
        "first_four_max_abs_start_delta_s": max_delta,
        "next_verse_line_detected": bool(contamination["secondary_matched"] and contamination["secondary_align_start_s"] is not None),
        "next_verse_secondary_start_s": contamination["secondary_align_start_s"],
        "automatic_green": green,
        "decision": "ALIGNMENT_GREEN" if green else "ALIGNMENT_REVIEW_REQUIRED",
        "cli_stdout_tail": proc.stdout[-1000:],
        "copyright_note": "Plain lyric strings and raw ASR text are intentionally excluded from persisted report; only semantic IDs, hashes, timestamps and QA are saved.",
    }
    (OUT / "alignment_verification_redacted.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Remove runtime plaintext and raw text-bearing alignment before artifact upload.
    trusted.unlink(missing_ok=True)
    aligned.unlink(missing_ok=True)
    asset.unlink(missing_ok=True)

    print(json.dumps({
        "decision": payload["decision"],
        "median_delta": median_delta,
        "max_delta": max_delta,
        "next_verse_detected": payload["next_verse_line_detected"],
        "next_verse_start": payload["next_verse_secondary_start_s"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
