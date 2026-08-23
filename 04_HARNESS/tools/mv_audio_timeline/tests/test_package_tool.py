import csv, json, math, subprocess, sys, tempfile, wave
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / 'package_tool.py'


def run(*args, expect=0):
    p = subprocess.run([sys.executable, str(TOOL), *map(str, args)], text=True, capture_output=True)
    if p.returncode != expect:
        raise AssertionError(f'rc={p.returncode} expected={expect}\nstdout={p.stdout}\nstderr={p.stderr}')
    return p


def make_wav(path: Path, seconds=5.0, sr=8000):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        frames = []
        for i in range(int(seconds * sr)):
            v = int(6000 * math.sin(2 * math.pi * 220 * i / sr))
            frames.append(v.to_bytes(2, 'little', signed=True))
        w.writeframes(b''.join(frames))


def write_csv(path, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)


def valid_package(root: Path):
    audio = root / 'a.wav'; make_wav(audio)
    lyrics = root / 'lyrics.txt'; lyrics.write_text('第一句\n第二句\n第一句\n', encoding='utf-8')
    pkg = root / 'pkg'
    run('init', '--package', pkg, '--audio', audio, '--lyrics', lyrics, '--title', 'T', '--artist', 'A', '--version', 'V', '--source-clip-start', '10', '--source-clip-end', '15')
    raw = root / 'align.csv'
    rows = [
        {'line_id': 'L01', 'lyric': '第一句', 'clip_start_s': '0.5', 'clip_end_s': '1.5'},
        {'line_id': 'L02', 'lyric': '第二句', 'clip_start_s': '1.6', 'clip_end_s': '3.0'},
        {'line_id': 'L03', 'lyric': '第一句', 'clip_start_s': '3.1', 'clip_end_s': '4.5'},
    ]
    write_csv(raw, rows)
    run('import-alignment', '--package', pkg, '--timeline', raw, '--evidence-class', 'ASR_FORCED_ALIGNMENT', '--tool', 'fixture', '--tool-version', '1')
    run('mark-qa', '--package', pkg, '--pass-qa', '--note', 'fixture ground truth')
    return audio, pkg


def test_valid_package_passes_and_manifest_written():
    with tempfile.TemporaryDirectory() as d:
        audio, pkg = valid_package(Path(d))
        p = run('validate', '--package', pkg, '--audio', audio, '--write-manifest')
        assert json.loads(p.stdout)['pass'] is True
        assert (pkg / 'package_manifest.json').exists()
        run('export-srt', '--package', pkg)
        assert '第一句' in (pkg / 'lyrics_exact.srt').read_text(encoding='utf-8')


def test_missing_raw_evidence_fails():
    with tempfile.TemporaryDirectory() as d:
        audio, pkg = valid_package(Path(d))
        prov = json.loads((pkg / 'alignment_provenance.json').read_text())
        (pkg / prov['raw_evidence_path']).unlink()
        p = run('validate', '--package', pkg, '--audio', audio, expect=2)
        assert 'raw evidence missing' in p.stdout


def test_diagnostic_renamed_exact_still_fails():
    with tempfile.TemporaryDirectory() as d:
        audio, pkg = valid_package(Path(d))
        prov = json.loads((pkg / 'alignment_provenance.json').read_text())
        prov['evidence_class'] = 'DIAGNOSTIC_ONLY'
        (pkg / 'alignment_provenance.json').write_text(json.dumps(prov), encoding='utf-8')
        p = run('validate', '--package', pkg, '--audio', audio, expect=2)
        assert 'not strong timing truth' in p.stdout


def test_audio_sha_mismatch_fails():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d); audio, pkg = valid_package(root)
        other = root / 'other.wav'; make_wav(other, seconds=4.9)
        p = run('validate', '--package', pkg, '--audio', other, expect=2)
        assert 'locked audio SHA mismatch' in p.stdout


def test_lrc_transform_preserves_repeated_occurrence_and_offset():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d); audio = root / 'a.wav'; make_wav(audio)
        lyrics = root / 'lyrics.txt'; lyrics.write_text('甲\n乙\n甲\n', encoding='utf-8')
        pkg = root / 'pkg'
        run('init', '--package', pkg, '--audio', audio, '--lyrics', lyrics, '--title', 'T', '--artist', 'A', '--version', 'V', '--source-clip-start', '10', '--source-clip-end', '15')
        lrc = root / 'x.lrc'; lrc.write_text('[00:10.50]甲\n[00:11.50]乙\n[00:13.00]甲\n', encoding='utf-8')
        run('from-lrc', '--package', pkg, '--lrc', lrc, '--source-identity', 'fixture')
        rows = list(csv.DictReader((pkg / 'line_timeline.candidate.csv').open(encoding='utf-8')))
        assert [r['lyric'] for r in rows] == ['甲', '乙', '甲']
        assert rows[0]['clip_start_s'] == '0.500' and rows[2]['clip_start_s'] == '3.000'


def test_crosscheck_large_delta_fails():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d); audio, pkg = valid_package(root)
        other = root / 'other.csv'
        rows = list(csv.DictReader((pkg / 'line_timeline.csv').open(encoding='utf-8')))
        rows[1]['clip_start_s'] = '2.40'; write_csv(other, rows)
        p = run('validate', '--package', pkg, '--audio', audio, '--crosscheck', other, expect=2)
        assert 'crosscheck delta too large' in p.stdout


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for t in tests:
        t(); print('PASS', t.__name__)
    print(f'{len(tests)} tests passed')
