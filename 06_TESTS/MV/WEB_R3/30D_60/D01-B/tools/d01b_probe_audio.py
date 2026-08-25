#!/usr/bin/env python3
from __future__ import annotations

import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path("06_TESTS/MV/WEB_R3/30D_60/D01-B")
ARTIFACT_DIR = ROOT / "_hg02_audio_artifact"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
RAW_URL = "https://lf3-music-east.douyinstatic.com/obj/ies-music-hj/7673442361086610233.mp3"
RAW_SHA = "ec6c178e30bf6c910ba4080bf1d3db31b708a7b7003430cb506630b21ac08b65"
LOCKED_SHA = "cc3da15b00cd554c810c590e61ccc97bedc72db058202bdf850bcefd5bba00e5"
FADE_START = 15.1608
FADE_DURATION = 0.8

# Runtime-only trusted excerpt. This temporary probe implementation is restored after execution.
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


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize(text: str) -> str:
    return "".join(re.findall(r"[\u4e00-\u9fff]", text))


def ensure_whisper():
    try:
        from faster_whisper import WhisperModel
        return WhisperModel
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper==1.2.1"], check=True)
        from faster_whisper import WhisperModel
        return WhisperModel


def prepare_audio() -> tuple[Path, Path, dict]:
    raw = ARTIFACT_DIR / "_runtime_raw.mp3"
    locked = ARTIFACT_DIR / "_runtime_locked_B.mp3"
    enhanced = ARTIFACT_DIR / "_runtime_vocal_enhanced.wav"
    r = requests.get(RAW_URL, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    raw.write_bytes(r.content)
    if sha_file(raw) != RAW_SHA:
        raise RuntimeError(f"raw SHA mismatch: {sha_file(raw)}")
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(raw),
        "-af", f"afade=t=out:st={FADE_START}:d={FADE_DURATION}",
        "-c:a", "libmp3lame", "-b:a", "192k", str(locked),
    ])
    if sha_file(locked) != LOCKED_SHA:
        raise RuntimeError(f"locked SHA mismatch: {sha_file(locked)}")
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(locked),
        "-af", "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=100,lowpass=f=9000,dynaudnorm=f=150:g=9",
        "-ar", "16000", "-c:a", "pcm_s16le", str(enhanced),
    ])
    p = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size,bit_rate:stream=codec_name,sample_rate,channels,bit_rate",
        "-of", "json", str(locked),
    ])
    return locked, enhanced, json.loads(p.stdout)


def words_to_chars(segments) -> tuple[str, list[dict], list[dict]]:
    chars: list[str] = []
    times: list[dict] = []
    raw_segments: list[dict] = []
    for seg in segments:
        seg_words = []
        for word in (seg.words or []):
            token = normalize(word.word or "")
            if not token:
                continue
            start = float(word.start if word.start is not None else seg.start)
            end = float(word.end if word.end is not None else seg.end)
            span = max(end - start, 0.001)
            for idx, ch in enumerate(token):
                cstart = start + span * idx / len(token)
                cend = start + span * (idx + 1) / len(token)
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


def align(recognized: str, char_times: list[dict]) -> dict:
    target = "".join(normalize(line) for line in LINES)
    matcher = difflib.SequenceMatcher(a=target, b=recognized, autojunk=False)
    mapping: dict[int, int] = {}
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for offset in range(i2 - i1):
                mapping[i1 + offset] = j1 + offset
    results = []
    cursor = 0
    for line_id, line in zip(LINE_IDS, LINES):
        norm = normalize(line)
        mapped = [mapping[i] for i in range(cursor, cursor + len(norm)) if i in mapping]
        coverage = len(mapped) / len(norm)
        start = min((char_times[i]["start"] for i in mapped), default=None)
        end = max((char_times[i]["end"] for i in mapped), default=None)
        results.append({
            "line_id": line_id,
            "lyric_sha256": sha_text(norm),
            "char_count": len(norm),
            "matched_chars": len(mapped),
            "coverage": round(coverage, 4),
            "start": round(start, 4) if start is not None else None,
            "end": round(end, 4) if end is not None else None,
        })
        cursor += len(norm)
    return {"sequence_ratio": round(matcher.ratio(), 4), "lines": results}


def transcribe(WhisperModel, model, label: str, path: Path) -> dict:
    prompt = "，".join(LINES)
    segments_gen, info = model.transcribe(
        str(path), language="zh", beam_size=5, temperature=0.0,
        word_timestamps=True, vad_filter=False, condition_on_previous_text=False,
        initial_prompt=prompt, suppress_blank=False,
    )
    segments = list(segments_gen)
    recognized, char_times, raw_segments = words_to_chars(segments)
    return {
        "input": label,
        "language": info.language,
        "language_probability": info.language_probability,
        "duration": info.duration,
        "recognized_normalized": recognized,
        "recognized_sha256": sha_text(recognized),
        "segments": raw_segments,
        "alignment": align(recognized, char_times),
    }


def quality(attempt: dict) -> float:
    lines = attempt["alignment"]["lines"][:4]
    coverage = sum(x["coverage"] for x in lines) / 4
    starts = [x["start"] for x in lines]
    monotonic = all(starts[i] is not None and starts[i+1] is not None and starts[i] < starts[i+1] for i in range(3))
    return coverage + (0.3 if monotonic else 0.0)


def main() -> int:
    WhisperModel = ensure_whisper()
    locked, enhanced, probe = prepare_audio()
    model = WhisperModel("small", device="cpu", compute_type="int8")
    attempts = [
        transcribe(WhisperModel, model, "locked_B_mix", locked),
        transcribe(WhisperModel, model, "locked_B_vocal_enhanced", enhanced),
    ]
    best = max(attempts, key=quality)
    first4 = best["alignment"]["lines"][:4]
    starts = [x["start"] for x in first4]
    coverage_ok = all(x["coverage"] >= 0.55 and x["start"] is not None for x in first4)
    monotonic = coverage_ok and all(starts[i] < starts[i+1] for i in range(3))
    next_line = best["alignment"]["lines"][4]

    private = {
        "audio_identity": {
            "asset_id": "7673442361086610233",
            "raw_sha256": RAW_SHA,
            "locked_sha256": LOCKED_SHA,
            "transform": {"fade_start_s": FADE_START, "fade_duration_s": FADE_DURATION, "curve": "tri"},
            "ffprobe": probe,
        },
        "trusted_runtime_lyrics": LINES,
        "model": "faster-whisper small / int8 / zh",
        "attempts": attempts,
        "selected_input": best["input"],
        "automatic_decision": "ALIGNMENT_CANDIDATE_PASS" if coverage_ok and monotonic else "ALIGNMENT_REVIEW_REQUIRED",
    }
    (ARTIFACT_DIR / "timeline_alignment_private.json").write_text(json.dumps(private, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    redacted_attempts = []
    for attempt in attempts:
        redacted_attempts.append({
            "input": attempt["input"],
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
        "model": "faster-whisper small / int8 / zh",
        "attempts": redacted_attempts,
        "selected_input": best["input"],
        "first_four_coverage_ok": coverage_ok,
        "first_four_monotonic": monotonic,
        "next_line_probe": next_line,
        "automatic_decision": private["automatic_decision"],
        "copyright_note": "Persistent report excludes plaintext lyrics and ASR transcript; private artifact is temporary execution evidence.",
    }
    (ARTIFACT_DIR / "timeline_alignment_redacted.json").write_text(json.dumps(redacted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ARTIFACT_DIR / "manifest.json").write_text(json.dumps({
        "task": "D01-B exact-B forced alignment",
        "locked_sha256": LOCKED_SHA,
        "decision": redacted["automatic_decision"],
        "selected_input": best["input"],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for path in [ARTIFACT_DIR / "_runtime_raw.mp3", locked, enhanced]:
        path.unlink(missing_ok=True)
    print(json.dumps({"decision": redacted["automatic_decision"], "lines": first4, "next": next_line}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
