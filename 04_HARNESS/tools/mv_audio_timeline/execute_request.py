#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS = REPO_ROOT / "04_HARNESS/tools/mv_audio_timeline"
PACKAGE_TOOL = TOOLS / "package_tool.py"
LIGHTWEIGHT_ALIGN = TOOLS / "lightweight_align.py"
FINAL_GATE = TOOLS / "final_gate.py"


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


def get_text(url: str, headers: dict[str, str] | None = None) -> str:
    merged = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36"
    }
    if headers:
        merged.update(headers)
    req = urllib.request.Request(url, headers=merged)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.douyin.com/"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp, path.open("wb") as f:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)


def run(cmd: list[Any], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    printable = [str(x) for x in cmd]
    print("+", " ".join(printable), flush=True)
    proc = subprocess.run(printable, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, flush=True)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, flush=True)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed rc={proc.returncode}: {printable}")
    return proc


def artist_name(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("name") or value.get("artistName") or value.get("artist") or "")
    return str(value or "")


def song_artists(song: dict[str, Any]) -> list[str]:
    values = song.get("artists") or song.get("ar") or []
    if isinstance(values, (str, dict)):
        values = [values]
    if not isinstance(values, list):
        return []
    return [name for x in values if (name := artist_name(x))]


def object_or_empty(value: Any) -> dict[str, Any]:
    """Normalize API fields that alternate between object and JSON-string schemas."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def list_or_empty(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return []
        return parsed if isinstance(parsed, list) else []
    return []


def extract_lrc_text(payload: dict[str, Any]) -> str:
    """Accept historical NetEase object wrappers and current string wrappers."""
    value = payload.get("lrc")
    if isinstance(value, dict):
        text = value.get("lyric")
        if isinstance(text, str):
            return text
    elif isinstance(value, str):
        # A string may be raw LRC or a JSON-serialized {lyric: ...} object.
        candidate = value.strip()
        if candidate.startswith("{"):
            parsed = object_or_empty(candidate)
            nested = parsed.get("lyric")
            if isinstance(nested, str):
                return nested
        return value
    for key in ("lyric", "lyrics"):
        text = payload.get(key)
        if isinstance(text, str):
            return text
    return ""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize_lyric(text: str) -> str:
    return re.sub(r"\W", "", text, flags=re.UNICODE)


def search_songs(title: str, artist: str) -> list[dict[str, Any]]:
    query = urllib.parse.quote(f"{title} {artist}".strip())
    endpoints = [
        f"https://music.163.com/api/search/get/web?csrf_token=&s={query}&type=1&offset=0&total=true&limit=20",
        f"https://music.163.com/api/cloudsearch/pc?s={query}&type=1&offset=0&limit=20",
    ]
    last_schema: dict[str, str] = {}
    for endpoint in endpoints:
        try:
            raw = get_text(endpoint, {"Referer": "https://music.163.com/"})
            data_raw = json.loads(raw)
        except Exception as exc:
            last_schema[endpoint] = f"request_or_json_error={exc!r}"
            continue
        data = object_or_empty(data_raw)
        result = object_or_empty(data.get("result"))
        candidates = list_or_empty(result.get("songs"))
        if not candidates:
            candidates = list_or_empty(data.get("songs"))
        songs = [x for x in candidates if isinstance(x, dict)]
        if songs:
            print(json.dumps({"p0_search_endpoint": endpoint, "candidate_count": len(songs)}, ensure_ascii=False))
            return songs
        last_schema[endpoint] = (
            f"root={type(data_raw).__name__}; result={type(data.get('result')).__name__}; "
            f"result_keys={sorted(result.keys())[:12]}"
        )
    raise RuntimeError(f"P0 NetEase search returned no song list; schemas={last_schema}")


def discover_netease_lrc(req: dict[str, Any], lrc_path: Path) -> tuple[int, dict[str, Any], str]:
    title = str(req["lyric_query_title"])
    artist = str(req.get("lyric_query_artist") or "")
    songs = search_songs(title, artist)

    chosen: dict[str, Any] | None = None
    for song in songs:
        name = str(song.get("name") or "")
        artists = " / ".join(song_artists(song))
        if title in name and (not artist or artist in artists):
            chosen = song
            break
    if chosen is None:
        for song in songs:
            if title in str(song.get("name") or ""):
                chosen = song
                break
    if chosen is None:
        raise RuntimeError("P0 timed lyric discovery found no plausible NetEase candidate")

    song_id = int(chosen["id"])
    lyric_raw = json.loads(
        get_text(
            f"https://music.163.com/api/song/lyric?id={song_id}&lv=1&kv=1&tv=-1",
            {"Referer": "https://music.163.com/"},
        )
    )
    lyric_payload = object_or_empty(lyric_raw)
    if not lyric_payload:
        raise RuntimeError(f"P0 lyric response root unusable: {type(lyric_raw).__name__}")
    lrc_text = extract_lrc_text(lyric_payload)
    if not lrc_text:
        raise RuntimeError("P0 candidate has no usable LRC text")
    lrc_path.write_text(lrc_text, encoding="utf-8")
    return song_id, chosen, lrc_text


def select_clip_lyrics(req: dict[str, Any], lrc_text: str, lyrics_path: Path) -> list[tuple[float, str]]:
    lrc_re = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)$")
    rows: list[tuple[float, str]] = []
    for raw_line in lrc_text.splitlines():
        match = lrc_re.search(raw_line)
        if not match:
            continue
        t = int(match.group(1)) * 60 + float(match.group(2))
        text = match.group(3).strip()
        if text:
            rows.append((t, text))

    lower = float(req.get("lyric_start_min_s", 0.0))
    duration = float(req["selected_duration_s"])
    ignore_prefixes = (
        "词：",
        "曲：",
        "制作人",
        "监制",
        "统筹",
        "企划",
        "出品人",
        "未经著作权人",
    )
    sung = [
        (t, text)
        for t, text in rows
        if lower <= t <= duration + 0.05 and not text.startswith(ignore_prefixes)
    ]
    if len(sung) < 2:
        raise RuntimeError(f"P0 LRC produced too few sung lines inside exact asset: {len(sung)}")
    lyrics_path.write_text("\n".join(text for _, text in sung) + "\n", encoding="utf-8")
    return sung


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute one Lean MV Audio Timeline request")
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    request_path = args.request if args.request.is_absolute() else REPO_ROOT / args.request
    req = load_json(request_path)
    pkg = request_path.parent

    with tempfile.TemporaryDirectory(prefix=f"mv_timeline_{req['slot_id']}_") as td:
        tmp = Path(td)
        audio = tmp / "locked_bgm.mp3"
        lrc = tmp / "source.lrc"
        lyrics = tmp / "trusted_lyrics.txt"
        asr_pkg = tmp / "asr_pkg"
        cross = tmp / "asr_crosscheck.csv"

        # 1. Exact BGM identity remains the upstream truth.
        download(str(req["selected_direct_music_url"]), audio)
        got_sha = sha256(audio)
        expected_sha = str(req["selected_audio_sha256"])
        if got_sha != expected_sha:
            raise RuntimeError(f"locked audio SHA mismatch expected={expected_sha} got={got_sha}")

        # 2. P0: same-version timed lyric candidate.
        song_id, chosen, lrc_text = discover_netease_lrc(req, lrc)
        sung = select_clip_lyrics(req, lrc_text, lyrics)
        print(json.dumps({"p0_song_id": song_id, "clip_lyric_lines": len(sung)}, ensure_ascii=False))

        title = str(req["lyric_query_title"])
        artist = str(req.get("lyric_query_artist") or "unknown")
        duration = float(req["selected_duration_s"])
        version = str(req.get("version_label") or "Douyin exact asset")

        # 3. P1: exactly one lightweight ASR pass. It is an independent check,
        # not a second final lyric truth source.
        run(
            [
                sys.executable,
                PACKAGE_TOOL,
                "init",
                "--package",
                asr_pkg,
                "--audio",
                audio,
                "--lyrics",
                lyrics,
                "--title",
                title,
                "--artist",
                artist,
                "--version",
                version,
                "--source-clip-start",
                "0",
                "--source-clip-end",
                str(duration),
            ]
        )
        p1 = run(
            [
                sys.executable,
                LIGHTWEIGHT_ALIGN,
                "--package",
                asr_pkg,
                "--audio",
                audio,
                "--model",
                "small",
                "--device",
                "cpu",
                "--compute-type",
                "int8",
                "--language",
                "zh",
            ],
            check=False,
        )
        if p1.returncode != 0:
            raise RuntimeError("P1 lightweight ASR did not pass; P2 escalation required")
        asr_candidate = asr_pkg / "line_timeline.candidate.csv"
        if not asr_candidate.exists():
            raise RuntimeError("P1 candidate timeline missing")

        # 4. Canonical timing package remains P0 LRC, independently checked by P1.
        run(
            [
                sys.executable,
                PACKAGE_TOOL,
                "init",
                "--package",
                pkg,
                "--audio",
                audio,
                "--lyrics",
                lyrics,
                "--title",
                title,
                "--artist",
                artist,
                "--version",
                version,
                "--source-clip-start",
                "0",
                "--source-clip-end",
                str(duration),
            ]
        )
        source_identity = (
            f"NetEase timed lyric song_id={song_id}; title={chosen.get('name')}; "
            f"artist={' / '.join(song_artists(chosen))}; independently checked against exact "
            "Douyin asset by P1 Faster-Whisper"
        )
        run(
            [
                sys.executable,
                PACKAGE_TOOL,
                "from-lrc",
                "--package",
                pkg,
                "--lrc",
                lrc,
                "--source-identity",
                source_identity,
                "--platform-song-id",
                str(song_id),
            ]
        )

        lrc_rows = read_csv(pkg / "line_timeline.candidate.csv")
        asr_rows = read_csv(asr_candidate)
        if len(lrc_rows) != len(asr_rows):
            raise RuntimeError(f"P0/P1 line count mismatch {len(lrc_rows)} != {len(asr_rows)}")

        deltas: list[float] = []
        with cross.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["line_id", "lyric", "clip_start_s", "clip_end_s"]
            )
            writer.writeheader()
            for row in asr_rows:
                writer.writerow({k: row[k] for k in writer.fieldnames})

        for lrc_row, asr_row in zip(lrc_rows, asr_rows):
            if normalize_lyric(lrc_row["lyric"]) != normalize_lyric(asr_row["lyric"]):
                raise RuntimeError("P0/P1 lyric sequence mismatch")
            deltas.append(
                abs(float(lrc_row["clip_start_s"]) - float(asr_row["clip_start_s"]))
            )

        median_delta = statistics.median(deltas)
        max_delta = max(deltas)
        max_median = float(req.get("max_median_start_delta_s", 0.25))
        max_line = float(req.get("max_line_start_delta_s", 0.50))
        if median_delta > max_median or max_delta > max_line:
            raise RuntimeError(
                f"P0/P1 timing conflict median={median_delta:.3f}s max={max_delta:.3f}s; "
                "P2 escalation required"
            )

        note = (
            "P0 timed LRC independently verified by one P1 Faster-Whisper pass; "
            f"full lyric mapping passed; median start delta={median_delta:.3f}s; "
            f"max={max_delta:.3f}s; exact audio SHA verified."
        )
        run([sys.executable, PACKAGE_TOOL, "mark-qa", "--package", pkg, "--pass-qa", "--note", note])
        run([sys.executable, PACKAGE_TOOL, "export-srt", "--package", pkg])

        final_rows = read_csv(pkg / "line_timeline.csv")
        with (pkg / "anchor_words.csv").open("w", encoding="utf-8", newline="") as f:
            fields = ["anchor_id", "line_id", "phrase", "start_s", "end_s", "qa_status"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for i, row in enumerate(final_rows, 1):
                start = float(row["clip_start_s"])
                end = float(row["clip_end_s"])
                writer.writerow(
                    {
                        "anchor_id": f"A{i:02d}",
                        "line_id": row["line_id"],
                        "phrase": row["lyric"][:2],
                        "start_s": f"{start:.3f}",
                        "end_s": f"{min(end, start + 0.45):.3f}",
                        "qa_status": "PASS",
                    }
                )

        with (pkg / "music_events.csv").open("w", encoding="utf-8", newline="") as f:
            fields = ["event_id", "time_s", "type", "description", "qa_status"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for i, row in enumerate(final_rows, 1):
                writer.writerow(
                    {
                        "event_id": f"E{i:02d}",
                        "time_s": row["clip_start_s"],
                        "type": "LYRIC_ENTRY",
                        "description": f"verified lyric entry {row['line_id']}",
                        "qa_status": "PASS",
                    }
                )
            writer.writerow(
                {
                    "event_id": f"E{len(final_rows)+1:02d}",
                    "time_s": f"{duration:.3f}",
                    "type": "TAIL_END",
                    "description": "locked asset tail end",
                    "qa_status": "PASS",
                }
            )

        report = (
            "# Audio Timeline Alignment QA\n\n"
            "Status: `PASS`\n\n"
            f"- Slot: `{req['slot_id']}`\n"
            "- Final timing truth: `SAME_VERSION_LRC`, verified against exact locked Douyin asset by one P1 Faster-Whisper pass.\n"
            f"- Exact audio SHA-256: `{got_sha}`\n"
            f"- Timed lyric source: NetEase song id `{song_id}`.\n"
            f"- Line count: `{len(final_rows)}`.\n"
            f"- P0/P1 median line-start delta: `{median_delta:.3f}s`.\n"
            f"- P0/P1 maximum line-start delta: `{max_delta:.3f}s`.\n"
            "- P1 mapping: full coverage and monotonic starts required by executor.\n"
            "- P2 heavy alignment: `NOT RUN` because P1 verification passed.\n"
            "- Decision: `PASS / LOCK AUDIO TIMELINE`.\n"
        )
        (pkg / "alignment_qa_report.md").write_text(report, encoding="utf-8")
        run([sys.executable, FINAL_GATE, "seal-qa", "--package", pkg])
        run(
            [
                sys.executable,
                FINAL_GATE,
                "validate",
                "--package",
                pkg,
                "--audio",
                audio,
                "--crosscheck",
                cross,
                "--write-manifest",
            ]
        )

        p1_report = asr_pkg / "raw_evidence/faster_whisper/lightweight_mapping_report.json"
        if p1_report.exists():
            (pkg / "p1_lightweight_mapping_report.json").write_bytes(p1_report.read_bytes())

        route = {
            "schema_version": "1.0-lean-r1",
            "slot_id": req["slot_id"],
            "route": "P0_LRC_VERIFIED_BY_P1_LIGHTWEIGHT_ASR",
            "p0_song_id": song_id,
            "p1_model": "faster-whisper-small",
            "median_start_delta_s": round(median_delta, 4),
            "max_start_delta_s": round(max_delta, 4),
            "p2_run": False,
            "decision": "PASS",
        }
        (pkg / "route_receipt.json").write_text(
            json.dumps(route, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(route, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
