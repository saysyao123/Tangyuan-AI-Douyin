#!/usr/bin/env python3
"""MV Audio Timeline Package builder / validator.

Purpose
-------
Turn strong timing evidence (same-version LRC or forced-alignment output) into a
reproducible AUDIO_TIMELINE_PACKAGE and refuse to mark it LOCKED when required
provenance or QA evidence is missing.

This tool does NOT discover lyrics and does NOT guess timestamps from waveform,
BPM, edit cuts, or character counts.

Supported flows
---------------
1) Same-version LRC fast path:
   python mv_audio_timeline_package.py from-lrc \
     --config audio_identity.json \
     --lyrics trusted_lyrics.txt \
     --lrc alignment_raw.lrc \
     --out-dir AUDIO_TIMELINE_PACKAGE

2) Validate an already assembled package:
   python mv_audio_timeline_package.py validate \
     --package-dir AUDIO_TIMELINE_PACKAGE

Exit code is non-zero when the package cannot be trusted.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

VERSION = "1.0.0"
LRC_TIME_RE = re.compile(r"\[(\d{1,3}):(\d{2})(?:[.:](\d{1,3}))?\]")
LRC_META_RE = re.compile(r"^\[(ar|ti|al|by|offset|re|ve|length):", re.I)
PUNCT_RE = re.compile(r"[\s\u3000，。！？、；：,.!?;:'\"“”‘’（）()【】\[\]《》<>·…—_-]+")


@dataclass(frozen=True)
class LrcLine:
    source_time: float
    text: str
    raw: str


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_text(s: str) -> str:
    return PUNCT_RE.sub("", s).lower()


def read_lyrics(path: Path) -> List[str]:
    lines = [x.strip() for x in path.read_text(encoding="utf-8-sig").splitlines()]
    lines = [x for x in lines if x and not x.startswith("#")]
    if not lines:
        die(f"trusted lyrics are empty: {path}")
    return lines


def parse_lrc(path: Path) -> List[LrcLine]:
    out: List[LrcLine] = []
    for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if not raw.strip() or LRC_META_RE.match(raw.strip()):
            continue
        stamps = list(LRC_TIME_RE.finditer(raw))
        if not stamps:
            continue
        text = LRC_TIME_RE.sub("", raw).strip()
        if not text:
            continue
        for m in stamps:
            minute = int(m.group(1))
            sec = int(m.group(2))
            frac_s = m.group(3) or "0"
            frac = int(frac_s) / (10 ** len(frac_s))
            out.append(LrcLine(minute * 60 + sec + frac, text, raw))
    out.sort(key=lambda x: x.source_time)
    if not out:
        die(f"no timed lyric lines found in LRC: {path}")
    return out


def monotonic_match(trusted: Sequence[str], candidates: Sequence[LrcLine]) -> List[Tuple[str, LrcLine]]:
    """Exact normalized monotonic matching; repeated lines consume later occurrences.

    Intentionally conservative: no fuzzy matching here. A public LRC that changes
    lyric wording/version should fail instead of being silently coerced.
    """
    result: List[Tuple[str, LrcLine]] = []
    cursor = 0
    for lyric in trusted:
        target = norm_text(lyric)
        hit: Optional[int] = None
        for i in range(cursor, len(candidates)):
            if norm_text(candidates[i].text) == target:
                hit = i
                break
        if hit is None:
            die(f"LRC cannot monotonically match trusted lyric: {lyric!r}")
        result.append((lyric, candidates[hit]))
        cursor = hit + 1
    return result


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"invalid JSON {path}: {e}")


def required(d: dict, key: str):
    if key not in d or d[key] in (None, ""):
        die(f"missing required field: {key}")
    return d[key]


def sec_to_srt(t: float) -> str:
    t = max(0.0, t)
    ms = int(round(t * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_csv(path: Path, rows: Iterable[dict], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fields))
        w.writeheader()
        for row in rows:
            w.writerow(row)


def build_from_lrc(args: argparse.Namespace) -> None:
    config_path = Path(args.config)
    lyrics_path = Path(args.lyrics)
    lrc_path = Path(args.lrc)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    cfg = load_json(config_path)
    title = required(cfg, "title")
    artist = required(cfg, "artist")
    exact_version = required(cfg, "exact_version")
    clip_start = float(required(cfg, "source_clip_start_sec"))
    duration = float(required(cfg, "rendered_duration_sec"))
    locked_bgm_sha = required(cfg, "locked_bgm_sha256")
    speed = float(cfg.get("speed", 1.0))
    if abs(speed - 1.0) > 1e-9:
        die("speed/time-stretch != 1.0; simple LRC offset transform is forbidden")

    trusted = read_lyrics(lyrics_path)
    lrc = parse_lrc(lrc_path)
    matched = monotonic_match(trusted, lrc)

    transformed = []
    for idx, (lyric, ll) in enumerate(matched, start=1):
        clip_time = ll.source_time - clip_start
        transformed.append({
            "line_id": f"L{idx:02d}",
            "lyric": lyric,
            "source_start_sec": round(ll.source_time, 3),
            "start_sec": round(clip_time, 3),
            "evidence": "SAME_VERSION_LRC_CANDIDATE",
            "confidence": "UNVERIFIED",
            "qa_status": "PENDING_GROUND_TRUTH_QA",
        })

    # Structural rejection: first/last mapped occurrences must plausibly overlap clip.
    pre_tol = float(args.pre_roll_tolerance)
    post_tol = float(args.post_roll_tolerance)
    starts = [r["start_sec"] for r in transformed]
    if starts != sorted(starts):
        die("transformed lyric starts are not monotonic")
    if starts[0] < -pre_tol:
        die(
            f"first matched lyric starts {starts[0]:.3f}s before clip; "
            "candidate LRC/version or trusted excerpt ordering is inconsistent"
        )
    if starts[-1] > duration + post_tol:
        die(
            f"last matched lyric starts {starts[-1]:.3f}s after clip duration; "
            "candidate LRC/version or trusted excerpt ordering is inconsistent"
        )

    # Display end is next lyric start; this is NOT claimed as vocal phoneme end.
    for i, row in enumerate(transformed):
        if i + 1 < len(transformed):
            row["end_sec"] = transformed[i + 1]["start_sec"]
            row["end_basis"] = "NEXT_LINE_HANDOFF"
        else:
            row["end_sec"] = round(duration, 3)
            row["end_basis"] = "CLIP_END_PENDING_FINAL_LINE_QA"

    # Copy canonical input assets.
    (out / "audio_identity.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (out / "trusted_lyrics.txt").write_text("\n".join(trusted) + "\n", encoding="utf-8")
    (out / "alignment_raw.lrc").write_bytes(lrc_path.read_bytes())

    provenance = {
        "package_schema": "mv-audio-timeline/v1",
        "builder_version": VERSION,
        "evidence_class": "SAME_VERSION_LRC",
        "source_platform": args.source_platform,
        "source_reference": args.source_reference,
        "source_song_id": args.source_song_id,
        "raw_evidence_sha256": sha256(out / "alignment_raw.lrc"),
        "timestamp_basis": "FULL_SONG",
        "transformation": "clip_time = source_song_time - source_clip_start_sec",
        "source_clip_start_sec": clip_start,
        "speed": speed,
        "locked_bgm_sha256": locked_bgm_sha,
        "verification_state": "CANDIDATE_PENDING_GROUND_TRUTH_QA",
        "warning": "LRC line starts are not LOCKED until audio/version ground-truth QA passes.",
    }
    (out / "alignment_provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    write_csv(
        out / "line_timeline.csv",
        transformed,
        [
            "line_id", "lyric", "source_start_sec", "start_sec", "end_sec",
            "end_basis", "evidence", "confidence", "qa_status",
        ],
    )

    # SRT is deliberately marked candidate; validator refuses LOCK while QA pending.
    srt = []
    for i, row in enumerate(transformed, start=1):
        start = max(0.0, float(row["start_sec"]))
        end = min(duration, float(row["end_sec"]))
        if end <= start:
            die(f"invalid subtitle interval for {row['line_id']}: {start} -> {end}")
        srt.extend([
            str(i),
            f"{sec_to_srt(start)} --> {sec_to_srt(end)}",
            row["lyric"],
            "",
        ])
    (out / "lyrics_candidate.srt").write_text("\n".join(srt), encoding="utf-8")

    # Empty-but-schema-valid downstream evidence tables; they must be populated before LOCK.
    write_csv(out / "anchor_words.csv", [], ["anchor_id", "line_id", "phrase", "start_sec", "end_sec", "evidence", "qa_status"])
    write_csv(out / "music_events.csv", [], ["event_id", "time_sec", "type", "description", "evidence", "qa_status"])

    qa = """# Alignment QA Report\n\n"
    qa += "- Ground-truth audio boundary review: PENDING\n"
    qa += "- Independent cross-check: PENDING\n"
    qa += "- Repeated occurrence audit: PENDING\n"
    qa += "- Public/platform LRC version identity: PENDING\n\n"
    qa += "`ALIGNMENT_GROUND_TRUTH_QA_PASS = NO`\n"
    (out / "alignment_qa_report.md").write_text(qa, encoding="utf-8")

    manifest = make_manifest(out, locked=False, reason="GROUND_TRUTH_QA_PENDING")
    (out / "package_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"success": True, "state": "CANDIDATE_PACKAGE_BUILT", "out_dir": str(out)}, ensure_ascii=False))


def make_manifest(pkg: Path, locked: bool, reason: str = "") -> dict:
    files = {}
    for p in sorted(pkg.iterdir()):
        if p.is_file() and p.name != "package_manifest.json":
            files[p.name] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    return {
        "package_schema": "mv-audio-timeline/v1",
        "builder_version": VERSION,
        "AUDIO_TIMELINE_PACKAGE_LOCKED": bool(locked),
        "state": "LOCKED" if locked else "BLOCKED",
        "reason": reason,
        "files": files,
    }


def read_line_timeline(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def validate_package(args: argparse.Namespace) -> None:
    pkg = Path(args.package_dir)
    if not pkg.is_dir():
        die(f"package directory does not exist: {pkg}")

    mandatory = [
        "audio_identity.json",
        "trusted_lyrics.txt",
        "alignment_provenance.json",
        "line_timeline.csv",
        "anchor_words.csv",
        "music_events.csv",
        "alignment_qa_report.md",
    ]
    missing = [x for x in mandatory if not (pkg / x).exists()]
    raw = list(pkg.glob("alignment_raw.*"))
    if not raw:
        missing.append("alignment_raw.*")
    if missing:
        die("missing mandatory package assets: " + ", ".join(missing))

    cfg = load_json(pkg / "audio_identity.json")
    prov = load_json(pkg / "alignment_provenance.json")
    trusted = read_lyrics(pkg / "trusted_lyrics.txt")
    rows = read_line_timeline(pkg / "line_timeline.csv")

    if len(rows) != len(trusted):
        die(f"line count mismatch: timeline={len(rows)} trusted_lyrics={len(trusted)}")
    for i, (row, lyric) in enumerate(zip(rows, trusted), start=1):
        if row.get("line_id") != f"L{i:02d}":
            die(f"unexpected line_id at row {i}: {row.get('line_id')}")
        if norm_text(row.get("lyric", "")) != norm_text(lyric):
            die(f"timeline lyric differs from trusted lyric at {row['line_id']}")

    starts = [float(r["start_sec"]) for r in rows]
    if starts != sorted(starts) or len(set(starts)) != len(starts):
        die("line starts must be strictly increasing")

    duration = float(required(cfg, "rendered_duration_sec"))
    if starts[0] < -0.8 or starts[-1] > duration + 0.8:
        die("timeline lies outside plausible locked-clip range")

    locked_bgm_sha = required(cfg, "locked_bgm_sha256")
    if prov.get("locked_bgm_sha256") != locked_bgm_sha:
        die("provenance locked_bgm_sha256 does not match audio identity")

    raw_sha = sha256(raw[0])
    if prov.get("raw_evidence_sha256") != raw_sha:
        die("raw evidence SHA does not match provenance")

    qa_text = (pkg / "alignment_qa_report.md").read_text(encoding="utf-8")
    qa_pass = "ALIGNMENT_GROUND_TRUTH_QA_PASS = YES" in qa_text
    all_line_qa = all(r.get("qa_status") == "PASS" for r in rows)
    provenance_verified = prov.get("verification_state") == "VERIFIED"

    # Exact output name is deliberately forbidden until the evidence chain passes.
    candidate_locked = qa_pass and all_line_qa and provenance_verified
    if candidate_locked:
        # Generate locked SRT from validated timeline.
        srt = []
        for i, row in enumerate(rows, start=1):
            start = max(0.0, float(row["start_sec"]))
            end = min(duration, float(row["end_sec"]))
            if end <= start:
                die(f"invalid interval {row['line_id']}")
            srt.extend([str(i), f"{sec_to_srt(start)} --> {sec_to_srt(end)}", row["lyric"], ""])
        (pkg / "lyrics_exact.srt").write_text("\n".join(srt), encoding="utf-8")
        manifest = make_manifest(pkg, True)
        (pkg / "package_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"success": True, "AUDIO_TIMELINE_PACKAGE_LOCKED": True}, ensure_ascii=False))
        return

    manifest = make_manifest(pkg, False, reason="PROVENANCE_OR_GROUND_TRUTH_QA_NOT_PASS")
    (pkg / "package_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    die(
        "package remains BLOCKED: require provenance verification, every line qa_status=PASS, "
        "and ALIGNMENT_GROUND_TRUTH_QA_PASS = YES",
        code=3,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("from-lrc", help="build a candidate package from a verified-version LRC candidate")
    a.add_argument("--config", required=True, help="audio_identity.json input")
    a.add_argument("--lyrics", required=True, help="trusted lyrics, one line per line")
    a.add_argument("--lrc", required=True, help="raw full-song LRC")
    a.add_argument("--out-dir", required=True)
    a.add_argument("--source-platform", default="UNKNOWN")
    a.add_argument("--source-reference", default="")
    a.add_argument("--source-song-id", default="")
    a.add_argument("--pre-roll-tolerance", type=float, default=0.8)
    a.add_argument("--post-roll-tolerance", type=float, default=0.8)
    a.set_defaults(func=build_from_lrc)

    v = sub.add_parser("validate", help="validate and lock an assembled package only if evidence chain passes")
    v.add_argument("--package-dir", required=True)
    v.set_defaults(func=validate_package)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
