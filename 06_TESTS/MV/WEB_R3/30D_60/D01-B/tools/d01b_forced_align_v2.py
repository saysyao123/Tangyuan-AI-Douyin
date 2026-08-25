#!/usr/bin/env python3
from __future__ import annotations

import difflib
import hashlib
import json
import re
import subprocess
from pathlib import Path

import requests
from faster_whisper import WhisperModel

ROOT = Path("06_TESTS/MV/WEB_R3/30D_60/D01-B")
OUT = ROOT / "_TIMELINE_PROBE_V2"
OUT.mkdir(parents=True, exist_ok=True)

RAW_URL = "https://lf3-music-east.douyinstatic.com/obj/ies-music-hj/7673442361086610233.mp3"
RAW_SHA = "ec6c178e30bf6c910ba4080bf1d3db31b708a7b7003430cb506630b21ac08b65"
LOCKED_SHA = "cc3da15b00cd554c810c590e61ccc97bedc72db058202bdf850bcefd5bba00e5"
LOCKED_DURATION = 15.986939
FADE_START = 15.1608
FADE_DURATION = 0.8

# Runtime-only trusted lyric excerpt. The probe branch is execution-only and will not be merged.
LINES = [
    "我救自己于人间水火",
    "我爱自己于苦难生活",
    "你是我花开的那一朵",
    "祝你永远会记得我",
    "我望见了那山坡",
]
LINE_IDS = [
    "L01_SELF_RESCUE",
    "L02_SELF_LOVE",
    "L03_BLOOM_RELATION",
    "L04_REMEMBER_ME",
    "L05_NEXT_LINE_CONTAMINATION_PROBE",
]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def normalize(text: str) -> str:
    return "".join(re.findall(r"[\u4e00-\u9fff]", text))


def exact_audio() -> tuple[Path, dict]:
    raw = OUT / "raw_asset.mp3"
    locked = OUT / "locked_B_exact.mp3"
    data = requests.get(RAW_URL, timeout=90, headers={"User-Agent": "Mozilla/5.0"}).content
    raw.write_bytes(data)
    if sha_bytes(data) != RAW_SHA:
        raise RuntimeError(f"raw hash mismatch: {sha_bytes(data)}")
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw),
        "-af", f"afade=t=out:st={FADE_START}:d={FADE_DURATION}",
        "-c:a", "libmp3lame", "-b:a", "192k", str(locked),
    ])
    locked_data = locked.read_bytes()
    if sha_bytes(locked_data) != LOCKED_SHA:
        raise RuntimeError(f"locked hash mismatch: {sha_bytes(locked_data)}")
    p = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size,bit_rate:stream=codec_name,sample_rate,channels,bit_rate",
        "-of", "json", str(locked),
    ])
    return locked, json.loads(p.stdout)


def words_to_chars(segments) -> tuple[str, list[dict], list[dict]]:
    chars: list[str] = []
    times: list[dict] = []
    raw_segments: list[dict] = []
    for seg in segments:
        seg_words = []
        for w in (seg.words or []):
            token = normalize(w.word or "")
            if not token:
                continue
            start = float(w.start if w.start is not None else seg.start)
            end = float(w.end if w.end is not None else seg.end)
            span = max(end - start, 0.001)
            for j, ch in enumerate(token):
                cstart = start + span * j / len(token)
                cend = start + span * (j + 1) / len(token)
                chars.append(ch)
                times.append({"char": ch, "start": round(cstart, 4), "end": round(cend, 4)})
            seg_words.append({"token": token, "start": round(start, 4), "end": round(end, 4)})
        raw_segments.append({
            "start": round(float(seg.start), 4),
            "end": round(float(seg.end), 4),
            "text": seg.text,
            "words": seg_words,
        })
    return "".join(chars), times, raw_segments


def align_target(target: str, recognized: str, char_times: list[dict]) -> dict:
    sm = difflib.SequenceMatcher(a=target, b=recognized, autojunk=False)
    mapping: dict[int, int] = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapping[i1 + k] = j1 + k

    line_results = []
    cursor = 0
    for line_id, line in zip(LINE_IDS, LINES):
        norm = normalize(line)
        idxs = [mapping[i] for i in range(cursor, cursor + len(norm)) if i in mapping]
        coverage = len(idxs) / max(len(norm), 1)
        if idxs:
            start = min(char_times[j]["start"] for j in idxs)
            end = max(char_times[j]["end"] for j in idxs)
        else:
            start = end = None
        line_results.append({
            "line_id": line_id,
            "lyric_sha256": sha_text(norm),
            "char_count": len(norm),
            "matched_chars": len(idxs),
            "coverage": round(coverage, 4),
            "start": round(start, 4) if start is not None else None,
            "end": round(end, 4) if end is not None else None,
        })
        cursor += len(norm)

    ratio = sm.ratio()
    return {"sequence_ratio": round(ratio, 4), "lines": line_results}


def transcribe(model_name: str, audio: Path) -> dict:
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    prompt = "，".join(LINES)
    segments_gen, info = model.transcribe(
        str(audio),
        language="zh",
        beam_size=5,
        temperature=0.0,
        word_timestamps=True,
        vad_filter=False,
        condition_on_previous_text=False,
        initial_prompt=prompt,
        suppress_blank=False,
    )
    segments = list(segments_gen)
    recognized, char_times, raw_segments = words_to_chars(segments)
    target = "".join(normalize(x) for x in LINES)
    alignment = align_target(target, recognized, char_times)
    return {
        "model": model_name,
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "recognized_normalized": recognized,
        "recognized_sha256": sha_text(recognized),
        "raw_segments": raw_segments,
        "alignment": alignment,
    }


def score(result: dict) -> float:
    lines = result["alignment"]["lines"][:4]
    mean_cov = sum(x["coverage"] for x in lines) / 4
    valid_starts = sum(x["start"] is not None for x in lines)
    monotonic = all(
        lines[i]["start"] is not None and lines[i+1]["start"] is not None and lines[i]["start"] < lines[i+1]["start"]
        for i in range(3)
    )
    return mean_cov + 0.1 * valid_starts + (0.2 if monotonic else 0.0)


def main() -> int:
    audio, probe = exact_audio()
    attempts = []
    for model_name in ["small", "medium"]:
        result = transcribe(model_name, audio)
        attempts.append(result)
        if score(result) >= 1.25:
            break

    best = max(attempts, key=score)
    first4 = best["alignment"]["lines"][:4]
    next_line = best["alignment"]["lines"][4]
    coverage_ok = all(x["coverage"] >= 0.55 and x["start"] is not None for x in first4)
    monotonic = all(first4[i]["start"] < first4[i+1]["start"] for i in range(3)) if coverage_ok else False
    next_detected = next_line["coverage"] >= 0.35 and next_line["start"] is not None

    raw_payload = {
        "audio": {
            "asset_id": "7673442361086610233",
            "raw_sha256": RAW_SHA,
            "locked_sha256": LOCKED_SHA,
            "locked_duration_s": LOCKED_DURATION,
            "transform": {"fade_start_s": FADE_START, "fade_duration_s": FADE_DURATION, "curve": "tri"},
            "ffprobe": probe,
        },
        "trusted_lyrics_runtime": LINES,
        "attempts": attempts,
        "selected_model": best["model"],
        "coverage_ok": coverage_ok,
        "monotonic": monotonic,
        "next_line_detected": next_detected,
    }
    (OUT / "alignment_raw_private.json").write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    redacted_attempts = []
    for attempt in attempts:
        redacted_attempts.append({
            "model": attempt["model"],
            "language": attempt["language"],
            "language_probability": attempt["language_probability"],
            "duration": attempt["duration"],
            "recognized_sha256": attempt["recognized_sha256"],
            "sequence_ratio": attempt["alignment"]["sequence_ratio"],
            "lines": attempt["alignment"]["lines"],
        })
    redacted = {
        "audio_asset_id": "7673442361086610233",
        "audio_locked_sha256": LOCKED_SHA,
        "exact_B_reproduction_pass": True,
        "evidence_route": "TRUSTED_LYRICS_PLUS_FASTER_WHISPER_CHARACTER_ALIGNMENT",
        "attempts": redacted_attempts,
        "selected_model": best["model"],
        "first_four_coverage_ok": coverage_ok,
        "first_four_monotonic": monotonic,
        "next_line_detected": next_detected,
        "automatic_decision": "ALIGNMENT_CANDIDATE_PASS" if coverage_ok and monotonic else "ALIGNMENT_REVIEW_REQUIRED",
        "copyright_note": "Persisted report excludes plaintext lyrics and ASR transcript; raw private artifact is execution evidence only.",
    }
    (OUT / "alignment_redacted.json").write_text(json.dumps(redacted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Remove audio bytes before artifact upload; identity is represented by verified hashes.
    (OUT / "raw_asset.mp3").unlink(missing_ok=True)
    (OUT / "locked_B_exact.mp3").unlink(missing_ok=True)
    print(json.dumps({
        "decision": redacted["automatic_decision"],
        "selected_model": best["model"],
        "line_results": best["alignment"]["lines"],
    }, ensure_ascii=False))
    return 0 if coverage_ok and monotonic else 2


if __name__ == "__main__":
    raise SystemExit(main())
