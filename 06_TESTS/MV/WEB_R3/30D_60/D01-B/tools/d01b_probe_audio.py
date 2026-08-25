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
OUT = ROOT / "_hg02_audio_artifact"
OUT.mkdir(parents=True, exist_ok=True)
RAW_URL = "https://lf3-music-east.douyinstatic.com/obj/ies-music-hj/7673442361086610233.mp3"
RAW_SHA = "ec6c178e30bf6c910ba4080bf1d3db31b708a7b7003430cb506630b21ac08b65"
CANONICAL_B_SHA = "cc3da15b00cd554c810c590e61ccc97bedc72db058202bdf850bcefd5bba00e5"
FADE_START = 15.1608
FADE_DURATION = 0.8

# Runtime-only trusted excerpt; the persisted redacted report stores hashes and semantic IDs only.
LINES = [
    "我救自己于人间水火",
    "我爱自己于苦难生活",
    "我会记得花开那一朵",
    "吾将上下而求索",
    "我救自己于人间水火",
]
LINE_IDS = ["L01_SELF_RESCUE", "L02_SELF_LOVE", "L03_REMEMBER_BLOOM", "L04_SEEKING", "L05_REPEAT_HOOK_PROBE"]


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


def norm(text: str) -> str:
    return "".join(re.findall(r"[\u4e00-\u9fff]", text))


def ensure_model():
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper==1.2.1"], check=True)
        from faster_whisper import WhisperModel
    return WhisperModel


def prepare_audio() -> tuple[Path, Path, dict]:
    raw = OUT / "_runtime_raw.mp3"
    pcm = OUT / "_runtime_locked_B_pcm.wav"
    enhanced = OUT / "_runtime_locked_B_vocal_enhanced.wav"
    r = requests.get(RAW_URL, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    raw.write_bytes(r.content)
    actual_raw_sha = sha_file(raw)
    if actual_raw_sha != RAW_SHA:
        raise RuntimeError(f"raw asset SHA mismatch: {actual_raw_sha}")

    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", f"afade=t=out:st={FADE_START}:d={FADE_DURATION}", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(pcm)])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(pcm), "-af", "highpass=f=100,lowpass=f=9000,dynaudnorm=f=150:g=9", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(enhanced)])
    probe = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate:stream=codec_name,sample_rate,channels,bit_rate", "-of", "json", str(pcm)]).stdout)
    return pcm, enhanced, probe


def chars_from_segments(segments) -> tuple[str, list[dict], list[dict]]:
    recognized: list[str] = []
    char_times: list[dict] = []
    raw_segments: list[dict] = []
    for seg in segments:
        words = []
        for w in seg.words or []:
            token = norm(w.word or "")
            if not token:
                continue
            start = float(w.start if w.start is not None else seg.start)
            end = float(w.end if w.end is not None else seg.end)
            span = max(end - start, 0.001)
            for i, ch in enumerate(token):
                recognized.append(ch)
                char_times.append({"char": ch, "start": start + span * i / len(token), "end": start + span * (i + 1) / len(token)})
            words.append({"token": token, "start": round(start, 4), "end": round(end, 4)})
        raw_segments.append({"start": round(float(seg.start), 4), "end": round(float(seg.end), 4), "text": seg.text, "words": words})
    return "".join(recognized), char_times, raw_segments


def align(recognized: str, char_times: list[dict]) -> dict:
    target = "".join(norm(x) for x in LINES)
    sm = difflib.SequenceMatcher(a=target, b=recognized, autojunk=False)
    mapping: dict[int, int] = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapping[i1 + k] = j1 + k
    results = []
    cursor = 0
    for line_id, text in zip(LINE_IDS, LINES):
        text = norm(text)
        idxs = [mapping[i] for i in range(cursor, cursor + len(text)) if i in mapping]
        results.append({
            "line_id": line_id,
            "lyric_sha256": sha_text(text),
            "char_count": len(text),
            "matched_chars": len(idxs),
            "coverage": round(len(idxs) / len(text), 4),
            "start": round(min((char_times[j]["start"] for j in idxs), default=0.0), 4) if idxs else None,
            "end": round(max((char_times[j]["end"] for j in idxs), default=0.0), 4) if idxs else None,
        })
        cursor += len(text)
    return {"sequence_ratio": round(sm.ratio(), 4), "lines": results}


def transcribe(model, label: str, path: Path) -> dict:
    segments_gen, info = model.transcribe(str(path), language="zh", beam_size=5, temperature=0.0, word_timestamps=True, vad_filter=False, condition_on_previous_text=False, initial_prompt="，".join(LINES), suppress_blank=False)
    recognized, times, raw_segments = chars_from_segments(list(segments_gen))
    return {"input": label, "language": info.language, "language_probability": info.language_probability, "duration": info.duration, "recognized_text": recognized, "recognized_sha256": sha_text(recognized), "segments": raw_segments, "alignment": align(recognized, times)}


def quality(attempt: dict) -> float:
    first4 = attempt["alignment"]["lines"][:4]
    starts = [x["start"] for x in first4]
    monotonic = all(starts[i] is not None and starts[i + 1] is not None and starts[i] < starts[i + 1] for i in range(3))
    return sum(x["coverage"] for x in first4) / 4 + (0.3 if monotonic else 0.0)


def main() -> int:
    WhisperModel = ensure_model()
    pcm, enhanced, probe = prepare_audio()
    model = WhisperModel("small", device="cpu", compute_type="int8")
    attempts = [transcribe(model, "locked_B_pcm", pcm), transcribe(model, "locked_B_vocal_enhanced", enhanced)]
    best = max(attempts, key=quality)
    first4 = best["alignment"]["lines"][:4]
    starts = [x["start"] for x in first4]
    coverage_ok = all(x["coverage"] >= 0.55 and x["start"] is not None for x in first4)
    monotonic = coverage_ok and all(starts[i] < starts[i + 1] for i in range(3))
    decision = "ALIGNMENT_CANDIDATE_PASS" if coverage_ok and monotonic else "ALIGNMENT_REVIEW_REQUIRED"

    private = {
        "audio_identity": {"asset_id": "7673442361086610233", "raw_sha256": RAW_SHA, "canonical_B_sha256": CANONICAL_B_SHA, "time_transform": {"fade_start_s": FADE_START, "fade_duration_s": FADE_DURATION, "curve": "tri"}, "pcm_probe": probe},
        "trusted_runtime_lyrics": LINES,
        "lyric_occurrence": "FIRST_CHORUS",
        "model": "faster-whisper small / int8 / zh",
        "attempts": attempts,
        "selected_input": best["input"],
        "automatic_decision": decision,
    }
    (OUT / "timeline_alignment_private.json").write_text(json.dumps(private, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    redacted_attempts = []
    for a in attempts:
        redacted_attempts.append({"input": a["input"], "language": a["language"], "language_probability": a["language_probability"], "duration": a["duration"], "recognized_sha256": a["recognized_sha256"], "sequence_ratio": a["alignment"]["sequence_ratio"], "lines": a["alignment"]["lines"]})
    redacted = {
        "audio_asset_id": "7673442361086610233",
        "canonical_B_sha256": CANONICAL_B_SHA,
        "raw_asset_sha_verified": True,
        "encoder_independent_pcm_transform_verified": True,
        "lyric_occurrence": "FIRST_CHORUS",
        "time_transform": {"fade_start_s": FADE_START, "fade_duration_s": FADE_DURATION, "curve": "tri"},
        "evidence_route": "TRUSTED_LYRICS_PLUS_FASTER_WHISPER_CHARACTER_ALIGNMENT",
        "model": "faster-whisper small / int8 / zh",
        "attempts": redacted_attempts,
        "selected_input": best["input"],
        "first_four_coverage_ok": coverage_ok,
        "first_four_monotonic": monotonic,
        "repeat_hook_probe": best["alignment"]["lines"][4],
        "automatic_decision": decision,
        "copyright_note": "Persistent report excludes plaintext lyrics and ASR transcript; private artifact is temporary execution evidence.",
    }
    (OUT / "timeline_alignment_redacted.json").write_text(json.dumps(redacted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps({"task": "D01-B exact-B forced alignment", "canonical_B_sha256": CANONICAL_B_SHA, "lyric_occurrence": "FIRST_CHORUS", "decision": decision, "selected_input": best["input"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for p in [OUT / "_runtime_raw.mp3", pcm, enhanced]:
        p.unlink(missing_ok=True)
    print(json.dumps({"decision": decision, "selected_input": best["input"], "first_four": first4, "repeat_hook_probe": best["alignment"]["lines"][4]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
