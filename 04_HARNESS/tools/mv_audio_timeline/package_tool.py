#!/usr/bin/env python3
"""MV Audio Timeline Package tool.

Dependency-light correctness gate for lyric/music timing packages.
It does not invent alignment. It only transforms strong timing evidence,
exports timing assets, and independently validates package provenance.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PACKAGE_VERSION = "1.0"
STRONG_EVIDENCE = {"SAME_VERSION_LRC", "ASR_FORCED_ALIGNMENT", "OFFICIAL_TIMED_LYRIC"}
FORBIDDEN_TRUTH = {"DIAGNOSTIC_ONLY", "ACOUSTIC_CANDIDATE", "WAVEFORM_GUESS", "EDITOR_ESTIMATE"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_duration(path: Path) -> float:
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True, capture_output=True, check=True,
    )
    return float(p.stdout.strip())


def normalize_lyric(s: str) -> str:
    return "".join(ch.lower() for ch in s.strip() if ch.isalnum() or "\u3400" <= ch <= "\u9fff")


_LRC_RE = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)$")


@dataclass
class LrcLine:
    time_s: float
    text: str


def parse_lrc(path: Path) -> list[LrcLine]:
    out: list[LrcLine] = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        for m in _LRC_RE.finditer(raw):
            mins = int(m.group(1)); secs = float(m.group(2)); text = m.group(3).strip()
            if text:
                out.append(LrcLine(mins * 60 + secs, text))
    out.sort(key=lambda x: x.time_s)
    return out


def read_lyrics(path: Path) -> list[str]:
    return [ln.strip() for ln in path.read_text(encoding="utf-8-sig").splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def find_subsequence(lrc: list[LrcLine], lyrics: list[str], min_similarity: float = 0.78) -> list[int]:
    from difflib import SequenceMatcher
    norm_lrc = [normalize_lyric(x.text) for x in lrc]
    indices: list[int] = []; cursor = 0
    for lyric in lyrics:
        target = normalize_lyric(lyric); best_i, best_score = -1, -1.0
        for i in range(cursor, len(lrc)):
            score = 1.0 if norm_lrc[i] == target else SequenceMatcher(None, target, norm_lrc[i]).ratio()
            if score > best_score: best_i, best_score = i, score
            if score == 1.0: break
        if best_i < 0 or best_score < min_similarity:
            raise ValueError(f"Cannot map trusted lyric monotonically: {lyric!r}; best score={best_score:.3f}")
        indices.append(best_i); cursor = best_i + 1
    return indices


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def format_srt_time(t: float) -> str:
    ms = int(round(max(0, t) * 1000)); h, rem = divmod(ms, 3600000); m, rem = divmod(rem, 60000); s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def cmd_init(args: argparse.Namespace) -> int:
    pkg = Path(args.package); pkg.mkdir(parents=True, exist_ok=True)
    audio = Path(args.audio).resolve(); lyrics = Path(args.lyrics).resolve()
    container_duration = ffprobe_duration(audio)
    content_duration = (args.source_clip_end - args.source_clip_start) / args.speed_factor
    identity = {
        "package_version": PACKAGE_VERSION, "title": args.title, "artist": args.artist, "version": args.version,
        "audio_path": str(audio), "audio_sha256": sha256_file(audio),
        "content_duration_s": round(content_duration, 6), "container_duration_s": round(container_duration, 6),
        "timeline_duration_s": round(content_duration, 6),
        "source_clip_start_s": args.source_clip_start, "source_clip_end_s": args.source_clip_end,
        "speed_factor": args.speed_factor, "time_stretched": abs(args.speed_factor - 1.0) > 1e-9,
    }
    (pkg / "audio_identity.json").write_text(json.dumps(identity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (pkg / "trusted_lyrics.txt").write_text("\n".join(read_lyrics(lyrics)) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "package": str(pkg), "audio_sha256": identity["audio_sha256"], "content_duration_s": content_duration, "container_duration_s": container_duration}, ensure_ascii=False))
    return 0


def cmd_from_lrc(args: argparse.Namespace) -> int:
    pkg = Path(args.package)
    identity = json.loads((pkg / "audio_identity.json").read_text(encoding="utf-8")); lyrics = read_lyrics(pkg / "trusted_lyrics.txt")
    lrc_path = Path(args.lrc).resolve(); lrc = parse_lrc(lrc_path); idx = find_subsequence(lrc, lyrics, args.min_similarity)
    clip_start = float(identity.get("source_clip_start_s") if args.clip_start is None else args.clip_start)
    lead_in = args.render_lead_in; duration = float(identity.get("timeline_duration_s", identity.get("rendered_duration_s"))); rows = []
    for n, (lyric, i) in enumerate(zip(lyrics, idx), start=1):
        source_start = lrc[i].time_s; clip_t = source_start - clip_start + lead_in
        if n < len(idx):
            source_end = lrc[idx[n]].time_s; clip_end = source_end - clip_start + lead_in; end_method = "NEXT_ALIGNED_LINE_START"
        else:
            source_end = None; clip_end = duration; end_method = "CLIP_END_PROVISIONAL"
        rows.append({
            "line_id": f"L{n:02d}", "lyric": lyric, "clip_start_s": f"{clip_t:.3f}", "clip_end_s": f"{clip_end:.3f}",
            "source_start_s": f"{source_start:.3f}", "source_end_s": "" if source_end is None else f"{source_end:.3f}",
            "evidence_class": "SAME_VERSION_LRC", "end_method": end_method, "qa_status": "NEEDS_GROUND_TRUTH_QA",
        })
    raw_dir = pkg / "raw_evidence"; raw_dir.mkdir(exist_ok=True); raw_copy = raw_dir / "source.lrc"; raw_copy.write_bytes(lrc_path.read_bytes())
    write_csv(pkg / "line_timeline.candidate.csv", rows, list(rows[0].keys()))
    provenance = {
        "package_version": PACKAGE_VERSION, "evidence_class": "SAME_VERSION_LRC", "source_identity": args.source_identity,
        "platform_song_id": args.platform_song_id, "raw_evidence_path": str(raw_copy.relative_to(pkg)), "raw_evidence_sha256": sha256_file(raw_copy),
        "transform": {"formula": "clip_time = source_song_time - source_clip_start + render_lead_in", "source_clip_start_s": clip_start, "render_lead_in_s": lead_in},
        "trusted_lyrics_count": len(lyrics), "mapped_lrc_indices": idx, "ground_truth_qa": "PENDING",
    }
    (pkg / "alignment_provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"success": True, "mapped_lines": len(rows), "candidate": str(pkg / "line_timeline.candidate.csv")}, ensure_ascii=False)); return 0


def cmd_import_alignment(args: argparse.Namespace) -> int:
    pkg = Path(args.package); src = Path(args.timeline).resolve(); rows = load_csv(src)
    required = {"line_id", "lyric", "clip_start_s", "clip_end_s"}
    if not rows or not required.issubset(rows[0]): raise ValueError(f"alignment CSV missing required columns {sorted(required)}")
    lyrics = read_lyrics(pkg / "trusted_lyrics.txt")
    if [normalize_lyric(r["lyric"]) for r in rows] != [normalize_lyric(x) for x in lyrics]: raise ValueError("alignment lyric sequence does not match trusted_lyrics.txt")
    out_rows = []
    for r in rows:
        out_rows.append({
            "line_id": r["line_id"], "lyric": r["lyric"], "clip_start_s": r["clip_start_s"], "clip_end_s": r["clip_end_s"],
            "source_start_s": r.get("source_start_s", ""), "source_end_s": r.get("source_end_s", ""),
            "evidence_class": args.evidence_class, "end_method": r.get("end_method", "ALIGNER_BOUNDARY"), "qa_status": "NEEDS_GROUND_TRUTH_QA",
        })
    raw_dir = pkg / "raw_evidence"; raw_dir.mkdir(exist_ok=True); raw_copy = raw_dir / src.name; raw_copy.write_bytes(src.read_bytes())
    write_csv(pkg / "line_timeline.candidate.csv", out_rows, list(out_rows[0].keys()))
    provenance = {"package_version": PACKAGE_VERSION, "evidence_class": args.evidence_class, "tool": args.tool, "tool_version": args.tool_version, "raw_evidence_path": str(raw_copy.relative_to(pkg)), "raw_evidence_sha256": sha256_file(raw_copy), "ground_truth_qa": "PENDING"}
    (pkg / "alignment_provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); return 0


def cmd_mark_qa(args: argparse.Namespace) -> int:
    pkg = Path(args.package); rows = load_csv(pkg / "line_timeline.candidate.csv")
    prov = json.loads((pkg / "alignment_provenance.json").read_text(encoding="utf-8")); prov["qa_note"] = args.note
    if args.pass_qa:
        for r in rows: r["qa_status"] = "PASS"
        write_csv(pkg / "line_timeline.csv", rows, list(rows[0].keys())); prov["ground_truth_qa"] = "PASS"
    else: prov["ground_truth_qa"] = "FAIL"
    (pkg / "alignment_provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); return 0


def cmd_export_srt(args: argparse.Namespace) -> int:
    pkg = Path(args.package); rows = load_csv(pkg / "line_timeline.csv"); blocks = []
    for i, r in enumerate(rows, 1): blocks.append(f"{i}\n{format_srt_time(float(r['clip_start_s']))} --> {format_srt_time(float(r['clip_end_s']))}\n{r['lyric']}\n")
    out = pkg / "lyrics_exact.srt"; out.write_text("\n".join(blocks), encoding="utf-8"); print(out); return 0


def cmd_validate(args: argparse.Namespace) -> int:
    pkg = Path(args.package); errors: list[str] = []; warnings: list[str] = []
    for name in ["audio_identity.json", "trusted_lyrics.txt", "alignment_provenance.json", "line_timeline.csv"]:
        if not (pkg / name).exists(): errors.append(f"missing required asset: {name}")
    if errors:
        print(json.dumps({"pass": False, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2)); return 2
    identity = json.loads((pkg / "audio_identity.json").read_text(encoding="utf-8")); prov = json.loads((pkg / "alignment_provenance.json").read_text(encoding="utf-8"))
    rows = load_csv(pkg / "line_timeline.csv"); lyrics = read_lyrics(pkg / "trusted_lyrics.txt"); eclass = prov.get("evidence_class")
    if eclass in FORBIDDEN_TRUTH or eclass not in STRONG_EVIDENCE: errors.append(f"evidence_class is not strong timing truth: {eclass!r}")
    raw_rel = prov.get("raw_evidence_path")
    if not raw_rel or not (pkg / raw_rel).exists(): errors.append("raw evidence missing")
    elif prov.get("raw_evidence_sha256") != sha256_file(pkg / raw_rel): errors.append("raw evidence SHA mismatch")
    if prov.get("ground_truth_qa") != "PASS": errors.append("ground_truth_qa != PASS")
    audio_path = Path(args.audio) if args.audio else Path(identity.get("audio_path", ""))
    if audio_path.exists():
        if sha256_file(audio_path) != identity.get("audio_sha256"): errors.append("locked audio SHA mismatch")
        try:
            actual_dur = ffprobe_duration(audio_path); locked_container = float(identity.get("container_duration_s", identity.get("rendered_duration_s")))
            if abs(actual_dur - locked_container) > args.duration_tolerance: errors.append(f"container duration mismatch: actual {actual_dur:.6f}, locked {locked_container:.6f}")
            if "content_duration_s" in identity:
                expected_content = (float(identity["source_clip_end_s"]) - float(identity["source_clip_start_s"])) / float(identity.get("speed_factor", 1.0))
                if abs(expected_content - float(identity["content_duration_s"])) > 0.001: errors.append("content duration does not match source clip span / speed factor")
                if abs(actual_dur - float(identity["content_duration_s"])) > args.container_padding_tolerance: errors.append(f"container/content duration delta too large: {actual_dur - float(identity['content_duration_s']):.6f}s")
        except Exception as e: errors.append(f"audio duration probe failed: {e}")
    else: warnings.append("audio file not present locally; identity/hash not re-verified in this run")
    if not rows: errors.append("empty line_timeline.csv")
    else:
        if [normalize_lyric(r["lyric"]) for r in rows] != [normalize_lyric(x) for x in lyrics]: errors.append("timeline lyric order/text does not match trusted lyrics")
        prev_start = -1.0; duration = float(identity.get("timeline_duration_s", identity.get("rendered_duration_s")))
        for r in rows:
            try: start, end = float(r["clip_start_s"]), float(r["clip_end_s"])
            except Exception: errors.append(f"invalid numeric time in {r.get('line_id')}"); continue
            if start < prev_start: errors.append(f"non-monotonic line starts at {r.get('line_id')}")
            if start < 0 or end <= start or end > duration + args.duration_tolerance: errors.append(f"invalid bounds {r.get('line_id')}: {start}-{end} duration={duration}")
            if r.get("qa_status") != "PASS": errors.append(f"line QA not PASS: {r.get('line_id')}={r.get('qa_status')}")
            prev_start = start
    if args.crosscheck:
        other = load_csv(Path(args.crosscheck))
        if len(other) != len(rows): errors.append("crosscheck line count mismatch")
        else:
            deltas = []
            for a, b in zip(rows, other):
                if normalize_lyric(a["lyric"]) != normalize_lyric(b["lyric"]): errors.append(f"crosscheck lyric mismatch {a.get('line_id')}"); continue
                d = abs(float(a["clip_start_s"]) - float(b["clip_start_s"])); deltas.append(d)
                if d > args.max_line_delta: errors.append(f"crosscheck delta too large {a.get('line_id')}: {d:.3f}s")
            if deltas:
                med = sorted(deltas)[len(deltas)//2]
                if med > args.max_median_delta: errors.append(f"crosscheck median delta too large: {med:.3f}s")
    passed = not errors
    print(json.dumps({"pass": passed, "errors": errors, "warnings": warnings, "evidence_class": eclass, "lines": len(rows)}, ensure_ascii=False, indent=2))
    if passed and args.write_manifest:
        manifest = {"package_version": PACKAGE_VERSION, "AUDIO_TIMELINE_PACKAGE_LOCKED": True, "audio_sha256": identity.get("audio_sha256"), "evidence_class": eclass, "files": {}}
        for p in sorted(pkg.iterdir()):
            if p.is_file() and p.name != "package_manifest.json": manifest["files"][p.name] = sha256_file(p)
        (pkg / "package_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if passed else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("init"); a.add_argument("--package", required=True); a.add_argument("--audio", required=True); a.add_argument("--lyrics", required=True); a.add_argument("--title", required=True); a.add_argument("--artist", required=True); a.add_argument("--version", default="official"); a.add_argument("--source-clip-start", type=float, required=True); a.add_argument("--source-clip-end", type=float, required=True); a.add_argument("--speed-factor", type=float, default=1.0); a.set_defaults(func=cmd_init)
    a = sub.add_parser("from-lrc"); a.add_argument("--package", required=True); a.add_argument("--lrc", required=True); a.add_argument("--clip-start", type=float); a.add_argument("--render-lead-in", type=float, default=0.0); a.add_argument("--source-identity", required=True); a.add_argument("--platform-song-id", default=""); a.add_argument("--min-similarity", type=float, default=0.78); a.set_defaults(func=cmd_from_lrc)
    a = sub.add_parser("import-alignment"); a.add_argument("--package", required=True); a.add_argument("--timeline", required=True); a.add_argument("--evidence-class", choices=sorted(STRONG_EVIDENCE), required=True); a.add_argument("--tool", required=True); a.add_argument("--tool-version", required=True); a.set_defaults(func=cmd_import_alignment)
    a = sub.add_parser("mark-qa"); a.add_argument("--package", required=True); g = a.add_mutually_exclusive_group(required=True); g.add_argument("--pass-qa", action="store_true"); g.add_argument("--fail-qa", action="store_true"); a.add_argument("--note", required=True); a.set_defaults(func=cmd_mark_qa)
    a = sub.add_parser("export-srt"); a.add_argument("--package", required=True); a.set_defaults(func=cmd_export_srt)
    a = sub.add_parser("validate"); a.add_argument("--package", required=True); a.add_argument("--audio"); a.add_argument("--crosscheck"); a.add_argument("--max-line-delta", type=float, default=0.50); a.add_argument("--max-median-delta", type=float, default=0.25); a.add_argument("--duration-tolerance", type=float, default=0.05); a.add_argument("--container-padding-tolerance", type=float, default=0.10); a.add_argument("--write-manifest", action="store_true"); a.set_defaults(func=cmd_validate)
    return p


def main() -> int:
    p = build_parser(); args = p.parse_args()
    try: return args.func(args)
    except subprocess.CalledProcessError as e:
        print(json.dumps({"success": False, "error": "subprocess_failed", "stderr": e.stderr}, ensure_ascii=False), file=sys.stderr); return 3
    except Exception as e:
        print(json.dumps({"success": False, "error": type(e).__name__, "message": str(e)}, ensure_ascii=False), file=sys.stderr); return 3


if __name__ == "__main__":
    raise SystemExit(main())
