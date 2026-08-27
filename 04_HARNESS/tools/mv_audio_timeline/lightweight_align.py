#!/usr/bin/env python3
"""Reusable P1 lightweight lyric aligner for MV Audio Timeline.

This tool never installs a model or dependency. The execution environment must
already provide faster-whisper. It consumes the exact locked HG02 audio and the
package's audited trusted_lyrics.txt, performs one Faster-Whisper pass with word
timestamps, maps trusted Chinese lyric characters monotonically to recognized
characters, and imports a candidate line timeline into the existing canonical
package toolchain.

P1 is allowed to PASS only with complete line coverage and monotonic line starts.
Otherwise it returns REVIEW_REQUIRED/BLOCKED so the route may escalate to P2.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import package_tool as pt


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: str) -> str:
    return "".join(re.findall(r"[\u4e00-\u9fff]", text or ""))


def expected_audio_sha(identity: dict) -> str | None:
    for key in (
        "locked_rendered_sha256",
        "audio_sha256",
        "rendered_sha256",
        "source_sha256",
    ):
        value = identity.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def write_timeline(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["line_id", "lyric", "clip_start_s", "clip_end_s"]
        )
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--compute-type", default="int8")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--require-full-coverage", action="store_true", default=True)
    args = ap.parse_args()

    pkg = Path(args.package).resolve()
    audio = Path(args.audio).resolve()
    lyrics_path = pkg / "trusted_lyrics.txt"
    identity_path = pkg / "audio_identity.json"
    out_dir = pkg / "raw_evidence" / "faster_whisper"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from faster_whisper import WhisperModel
    except Exception as exc:
        print(
            json.dumps(
                {
                    "success": False,
                    "state": "AUDIO_ALIGNMENT_RUNTIME_BLOCKED",
                    "route": "P1_LIGHTWEIGHT_FASTER_WHISPER",
                    "error": type(exc).__name__,
                    "message": "faster-whisper is not available in the prepared environment; do not install per slot",
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 3

    try:
        if not audio.is_file() or not lyrics_path.is_file() or not identity_path.is_file():
            raise FileNotFoundError("audio_identity.json, trusted_lyrics.txt and locked audio are required")
        identity = json.loads(identity_path.read_text(encoding="utf-8"))
        got_sha = sha256_file(audio)
        wanted_sha = expected_audio_sha(identity)
        if wanted_sha and got_sha != wanted_sha:
            raise ValueError(f"locked audio SHA mismatch expected={wanted_sha} got={got_sha}")

        trusted = pt.read_lyrics(lyrics_path)
        if not trusted:
            raise ValueError("trusted lyrics are empty")

        t0 = time.monotonic()
        model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
        t1 = time.monotonic()
        segments_gen, info = model.transcribe(
            str(audio),
            language=args.language,
            beam_size=5,
            temperature=0.0,
            word_timestamps=True,
            vad_filter=False,
            condition_on_previous_text=False,
            initial_prompt="，".join(trusted),
            suppress_blank=False,
        )
        segments = list(segments_gen)
        t2 = time.monotonic()

        chars: list[dict[str, object]] = []
        recognized: list[str] = []
        out_segments = []
        for seg in segments:
            words = []
            for word in seg.words or []:
                token = norm(word.word)
                if not token:
                    continue
                start = float(word.start if word.start is not None else seg.start)
                end = float(word.end if word.end is not None else seg.end)
                span = max(end - start, 0.001)
                for i, ch in enumerate(token):
                    cstart = start + span * i / len(token)
                    cend = start + span * (i + 1) / len(token)
                    chars.append({"char": ch, "start": cstart, "end": cend})
                    recognized.append(ch)
                words.append({"token": token, "start": start, "end": end})
            out_segments.append(
                {
                    "start": float(seg.start),
                    "end": float(seg.end),
                    "text": (seg.text or "").strip(),
                    "normalized": norm(seg.text),
                    "words": words,
                }
            )

        recognized_text = "".join(recognized)
        target = "".join(norm(x) for x in trusted)
        matcher = difflib.SequenceMatcher(a=target, b=recognized_text, autojunk=False)
        mapping: dict[int, int] = {}
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1):
                    mapping[i1 + k] = j1 + k

        cursor = 0
        rows = []
        line_results = []
        for idx, line in enumerate(trusted, 1):
            text = norm(line)
            mapped = [mapping[i] for i in range(cursor, cursor + len(text)) if i in mapping]
            coverage = len(mapped) / len(text) if text else 0.0
            start = min((float(chars[j]["start"]) for j in mapped), default=None)
            end = max((float(chars[j]["end"]) for j in mapped), default=None)
            line_results.append(
                {
                    "line_no": idx,
                    "text": line,
                    "char_count": len(text),
                    "matched_chars": len(mapped),
                    "coverage": round(coverage, 4),
                    "start": None if start is None else round(start, 4),
                    "end": None if end is None else round(end, 4),
                }
            )
            if start is not None and end is not None:
                rows.append(
                    {
                        "line_id": f"L{idx:02d}",
                        "lyric": line,
                        "clip_start_s": f"{start:.3f}",
                        "clip_end_s": f"{end:.3f}",
                    }
                )
            cursor += len(text)

        starts = [x["start"] for x in line_results]
        monotonic = bool(starts) and all(
            starts[i] is not None
            and starts[i + 1] is not None
            and float(starts[i]) < float(starts[i + 1])
            for i in range(len(starts) - 1)
        )
        full_coverage = bool(line_results) and all(x["coverage"] == 1.0 for x in line_results)
        decision = (
            "LIGHTWEIGHT_ALIGNMENT_PASS"
            if full_coverage and monotonic and len(rows) == len(trusted)
            else "LIGHTWEIGHT_ALIGNMENT_REVIEW_REQUIRED"
        )

        report = {
            "schema_version": "1.0-lean-r1",
            "route": "P1_LIGHTWEIGHT_FASTER_WHISPER",
            "audio_sha256": got_sha,
            "tool": {
                "name": "faster-whisper",
                "model": args.model,
                "device": args.device,
                "compute_type": args.compute_type,
            },
            "language": getattr(info, "language", None),
            "language_probability": getattr(info, "language_probability", None),
            "model_init_seconds": round(t1 - t0, 3),
            "transcribe_seconds": round(t2 - t1, 3),
            "sequence_ratio": round(matcher.ratio(), 4),
            "recognized_normalized": recognized_text,
            "line_results": line_results,
            "all_lines_full_coverage": full_coverage,
            "line_starts_monotonic": monotonic,
            "decision": decision,
            "segments": out_segments,
        }
        report_path = out_dir / "lightweight_mapping_report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if decision != "LIGHTWEIGHT_ALIGNMENT_PASS":
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 4

        timeline = out_dir / "normalized_timeline.csv"
        write_timeline(timeline, rows)
        ns = argparse.Namespace(
            package=str(pkg),
            timeline=str(timeline),
            evidence_class="ASR_TRUSTED_TEXT_MAPPING",
            tool="faster-whisper-small",
            tool_version="1.2.1-candidate",
        )
        pt.cmd_import_alignment(ns)
        print(
            json.dumps(
                {
                    "success": True,
                    "decision": decision,
                    "timeline": str(timeline),
                    "report": str(report_path),
                    "next": "canonical ground-truth QA then final_gate; do not run P2",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "success": False,
                    "state": "AUDIO_TIMELINE_PACKAGE_BLOCKED",
                    "route": "P1_LIGHTWEIGHT_FASTER_WHISPER",
                    "error": type(exc).__name__,
                    "message": str(exc),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
