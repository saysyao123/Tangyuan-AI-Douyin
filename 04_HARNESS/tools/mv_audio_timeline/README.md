# MV Audio Timeline Tool v1.0

This directory turns `AUDIO_TIMELINE_PACKAGE` from a prose rule into an executable correctness gate.

## Core idea

The tool **does not invent timestamps**. It only:
1. locks audio identity (SHA + duration + clip offset);
2. normalizes strong timing evidence;
3. independently validates provenance and timeline correctness before editing can continue.

A file named `exact.srt` is not trusted by name. `validate` must PASS.

## Typical flow

```bash
python package_tool.py init \
  --package /project/AUDIO_TIMELINE_PACKAGE \
  --audio /audio/locked_bgm.mp3 \
  --lyrics /project/trusted_lyrics.txt \
  --title "Song" --artist "Artist" --version "official" \
  --source-clip-start 139.930 --source-clip-end 177.050
```

### Route A — verified same-version LRC

```bash
python package_tool.py from-lrc \
  --package /project/AUDIO_TIMELINE_PACKAGE \
  --lrc /evidence/source.lrc \
  --source-identity "Platform + song-id + exact version"
```

This creates a **candidate**, never an automatic lock. Standard LRC usually carries line starts only, so actual audio QA is still required.

### Route B — trusted lyrics + forced alignment

If the engine and its model are already installed/preheated:

```bash
python run_alignment.py \
  --engine xingyu \
  --package /project/AUDIO_TIMELINE_PACKAGE \
  --audio /audio/locked_bgm.mp3
```

or:

```bash
python run_alignment.py \
  --engine lyric-align \
  --package /project/AUDIO_TIMELINE_PACKAGE \
  --audio /audio/locked_bgm.mp3 \
  --separate
```

The adapter never installs models automatically and never falls back to waveform guesses. Missing engine/model => `AUDIO_TIMELINE_PACKAGE_BLOCKED`.

## Ground-truth QA

After real vocal-boundary review / independent evidence check:

```bash
python package_tool.py mark-qa \
  --package /project/AUDIO_TIMELINE_PACKAGE \
  --pass-qa \
  --note "line-by-line vocal boundary audit passed"
```

Then:

```bash
python package_tool.py export-srt --package /project/AUDIO_TIMELINE_PACKAGE
python package_tool.py validate \
  --package /project/AUDIO_TIMELINE_PACKAGE \
  --audio /audio/locked_bgm.mp3 \
  --write-manifest
```

Optional independent cross-check:

```bash
python package_tool.py validate \
  --package /project/AUDIO_TIMELINE_PACKAGE \
  --audio /audio/locked_bgm.mp3 \
  --crosscheck /evidence/second_timeline.csv \
  --write-manifest
```

Default cross-source thresholds:
- median line-start delta <= `0.25s`;
- each line-start delta <= `0.50s`;
- any larger conflict blocks until reviewed/explained.

## Gate rejects

- missing raw evidence;
- `DIAGNOSTIC_ONLY`, waveform or editor-estimate evidence;
- changed locked-audio SHA or duration;
- lyric order drift;
- repeated-chorus occurrence mismatch;
- non-monotonic/out-of-range timestamps;
- any line without explicit QA PASS;
- cross-source disagreement above threshold.

## Regression test

```bash
python tests/test_package_tool.py
```

The suite includes the exact WEB R2 failure class: a diagnostic timeline renamed as “exact” still fails.
