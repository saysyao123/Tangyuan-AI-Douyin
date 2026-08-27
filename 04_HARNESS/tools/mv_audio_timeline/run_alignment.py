#!/usr/bin/env python3
"""Adapters for external known-lyrics alignment engines.

Never installs models and never silently falls back to guesses. If an engine is
unavailable it exits non-zero with AUDIO_TIMELINE_PACKAGE_BLOCKED.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import package_tool as pt


def run_logged(cmd: list[str], cwd: Path, log_prefix: Path) -> subprocess.CompletedProcess:
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    log_prefix.parent.mkdir(parents=True, exist_ok=True)
    log_prefix.with_suffix('.stdout.txt').write_text(p.stdout or '', encoding='utf-8')
    log_prefix.with_suffix('.stderr.txt').write_text(p.stderr or '', encoding='utf-8')
    if p.returncode != 0:
        raise RuntimeError(f"engine command failed rc={p.returncode}; inspect {log_prefix}.stderr.txt")
    return p


def parse_srt(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding='utf-8-sig')
    time_re = re.compile(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)')
    rows = []
    for block in re.split(r'\n\s*\n', text.strip()):
        lines = [x.strip() for x in block.splitlines() if x.strip()]
        ti = next((i for i, x in enumerate(lines) if '-->' in x), None)
        if ti is None:
            continue
        m = time_re.search(lines[ti])
        if not m:
            continue
        v = list(map(int, m.groups()))
        s = v[0]*3600 + v[1]*60 + v[2] + v[3]/1000
        e = v[4]*3600 + v[5]*60 + v[6] + v[7]/1000
        rows.append({'line_id': f'L{len(rows)+1:02d}', 'lyric': ''.join(lines[ti+1:]), 'clip_start_s': f'{s:.3f}', 'clip_end_s': f'{e:.3f}'})
    return rows


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['line_id', 'lyric', 'clip_start_s', 'clip_end_s']); w.writeheader(); w.writerows(rows)


def timeline_duration(identity: dict) -> float:
    """Resolve the canonical content timeline duration across schema generations.

    Current package_tool writes timeline_duration_s/content_duration_s. Older
    packages may still carry rendered_duration_s. Container duration is the
    final compatibility fallback because encoded padding must not become the
    preferred lyric clock when a content duration exists.
    """
    for key in ('timeline_duration_s', 'content_duration_s', 'rendered_duration_s', 'container_duration_s'):
        value = identity.get(key)
        if value is not None:
            return float(value)
    raise KeyError('audio identity contains no usable timeline duration field')


def xingyu_rows_from_alignment(path: Path, trusted: list[str]) -> list[dict[str, str]]:
    """Normalize Xingyu JSON without discarding explicit line-end evidence.

    Xingyu is run in trusted-lyrics forced-alignment mode, so output line text
    must preserve the supplied lyric sequence. The JSON contains authoritative
    per-line starts *and ends*; using only LRC starts would incorrectly stretch
    the final lyric to the full audio duration.
    """
    payload = json.loads(path.read_text(encoding='utf-8'))
    lines = payload.get('lines')
    if not isinstance(lines, list) or len(lines) != len(trusted):
        raise ValueError(f'Xingyu alignment line count mismatch: {0 if not isinstance(lines, list) else len(lines)} != {len(trusted)}')
    rows = []
    prev_start = -1.0
    for n, (lyric, line) in enumerate(zip(trusted, lines), 1):
        if not isinstance(line, dict):
            raise ValueError(f'Xingyu alignment line {n} is not an object')
        returned = str(line.get('text', ''))
        if pt.normalize_lyric(returned) != pt.normalize_lyric(lyric):
            raise ValueError(f'Xingyu changed/mismatched trusted lyric at line {n}: {returned!r} != {lyric!r}')
        try:
            start = float(line['start']); end = float(line['end'])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'Xingyu missing/invalid line boundary at line {n}') from exc
        if start < 0 or end <= start or start < prev_start:
            raise ValueError(f'Xingyu invalid/non-monotonic boundary at line {n}: {start}-{end}')
        rows.append({'line_id': f'L{n:02d}', 'lyric': lyric, 'clip_start_s': f'{start:.3f}', 'clip_end_s': f'{end:.3f}'})
        prev_start = start
    return rows


def engine_xingyu(args, pkg: Path, audio: Path, lyrics: Path) -> Path:
    exe = shutil.which('xingyu-align')
    if not exe:
        raise FileNotFoundError('xingyu-align not installed; install and preheat the Chinese alignment model explicitly')
    out = pkg / 'raw_evidence' / 'xingyu'; out.mkdir(parents=True, exist_ok=True)
    cmd = [exe, 'align', '--audio', str(audio), '--lyrics', str(lyrics), '--output-dir', str(out), '--language', args.language, '--device', args.device, '--json-result']
    run_logged(cmd, pkg, out / 'engine')
    alignment = out / 'alignment.json'
    if not alignment.exists():
        raise FileNotFoundError('xingyu did not produce alignment.json')
    trusted = pt.read_lyrics(lyrics)
    rows = xingyu_rows_from_alignment(alignment, trusted)
    norm = out / 'normalized_timeline.csv'; write_rows(norm, rows); return norm


def engine_lyric_align(args, pkg: Path, audio: Path, lyrics: Path) -> Path:
    exe = shutil.which('lyric-align')
    if not exe:
        raise FileNotFoundError('lyric-align not installed; install lyric-align[asr] explicitly')
    out = pkg / 'raw_evidence' / 'lyric-align'; out.mkdir(parents=True, exist_ok=True); srt = out / 'lyrics.srt'
    cmd = [exe, str(audio), str(lyrics), '--language', args.language, '-f', 'srt', '-o', str(srt)]
    if args.separate: cmd.append('--separate')
    if args.no_vad: cmd.append('--no-vad')
    run_logged(cmd, pkg, out / 'engine')
    if not srt.exists():
        raise FileNotFoundError('lyric-align did not produce SRT')
    rows = parse_srt(srt); trusted = pt.read_lyrics(lyrics)
    if [pt.normalize_lyric(r['lyric']) for r in rows] != [pt.normalize_lyric(x) for x in trusted]:
        raise ValueError('lyric-align output has unmatched/missing/changed lines; keep BLOCKED and inspect raw output')
    norm = out / 'raw_evidence' / 'lyric-align' / 'normalized_timeline.csv'; write_rows(norm, rows); return norm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--package', required=True); ap.add_argument('--audio', required=True); ap.add_argument('--engine', choices=['xingyu', 'lyric-align'], required=True)
    ap.add_argument('--language', default='zh'); ap.add_argument('--device', default='cpu'); ap.add_argument('--min-similarity', type=float, default=.78)
    ap.add_argument('--separate', action='store_true'); ap.add_argument('--no-vad', action='store_true')
    args = ap.parse_args(); pkg = Path(args.package).resolve(); audio = Path(args.audio).resolve(); lyrics = pkg / 'trusted_lyrics.txt'
    try:
        if not (pkg / 'audio_identity.json').exists() or not lyrics.exists():
            raise FileNotFoundError('package must be initialized before alignment')
        if args.engine == 'xingyu': norm = engine_xingyu(args, pkg, audio, lyrics); tool = 'xingyu-lyrics-aligner'; exe_name = 'xingyu-align'
        else: norm = engine_lyric_align(args, pkg, audio, lyrics); tool = 'lyric-align'; exe_name = 'lyric-align'
        exe = shutil.which(exe_name); vp = subprocess.run([exe, '--version'], text=True, capture_output=True) if exe else None
        version = (vp.stdout or vp.stderr).strip() if vp else 'unknown'
        ns = argparse.Namespace(package=str(pkg), timeline=str(norm), evidence_class='ASR_FORCED_ALIGNMENT', tool=tool, tool_version=version)
        pt.cmd_import_alignment(ns)
        print(json.dumps({'success': True, 'engine': args.engine, 'normalized_timeline': str(norm), 'next': 'ground-truth QA, then mark-qa --pass-qa'}, ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({'success': False, 'state': 'AUDIO_TIMELINE_PACKAGE_BLOCKED', 'engine': args.engine, 'error': type(e).__name__, 'message': str(e)}, ensure_ascii=False), file=sys.stderr); return 4


if __name__ == '__main__':
    raise SystemExit(main())
