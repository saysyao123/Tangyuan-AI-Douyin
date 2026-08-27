# OSS_OPT_R1｜Xingyu Fallback Archive v1.0

Status: `ARCHIVED / VALIDATED P2 FALLBACK / NOT DEFAULT`

## Purpose

Preserve the Xingyu route because it demonstrated high-quality Chinese forced alignment, while preventing its heavy runtime from becoming the normal short-MV production path.

## Preserved implementation

Canonical repository components:
- `04_HARNESS/tools/mv_audio_timeline/run_alignment.py`
- `04_HARNESS/tools/mv_audio_timeline/alignment_runtime.lock.json`
- `04_HARNESS/tools/mv_audio_timeline/bootstrap_alignment_env.py`
- `04_HARNESS/tools/mv_audio_timeline/package_tool.py`
- `04_HARNESS/tools/mv_audio_timeline/final_gate.py`
- `.github/workflows/r3-mv-audio-alignment-environment.yml`
- `.github/workflows/r3-mv-audio-timeline-executor.yml`

Pinned experimental runtime used:
- `xingyu-lyrics-aligner 0.7.0`
- WhisperX `3.8.6`
- Chinese CTC model pinned by `alignment_runtime.lock.json`

## D02-B validation evidence

Song: `有几次想你了`
Locked audio SHA-256: `6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4`

After the incorrect four-line input was invalidated, the corrected seven-line set was run through Xingyu forced alignment.
Observed result:
- `7/7` lyric lines aligned;
- `45/45` normalized lyric characters timed;
- missing character timestamps: `0`;
- non-monotonic line count: `0`;
- raw `alignment.json` line warnings: none;
- one export warning was caused only by a Chinese punctuation token and is avoided by stripping non-sung punctuation before alignment.

Representative line bounds from that validated fallback run:
- L1 `0.300–2.061s`
- L2 `2.061–3.802s`
- L3 `3.802–5.602s`
- L4 `5.602–7.343s`
- L5 `7.343–9.124s`
- L6 `9.124–10.864s`
- L7 `10.864–13.986s`

These timings are preserved as experimental fallback evidence, not as the current default production truth.

## Why it is fallback-only

The measured shared Xingyu/WhisperX environment cache is roughly `5.8 GB`, largely because of the broader WhisperX/PyTorch dependency graph. On ephemeral GitHub runners, environment restore adds substantial latency before a 15-second song is processed.

By comparison, the D01-B Faster-Whisper small validation cache is about `547 MB`, and the model work on D02-B measured approximately `6–8 seconds` once usable.

Therefore normal production should not pay the Xingyu runtime cost unless P1 has actually failed or higher precision is explicitly required.

## P2 activation triggers

Use Xingyu only when at least one is true:
1. Faster-Whisper does not recover the complete sung lyric structure after the single text audit.
2. Trusted-text mapping has unresolved low coverage.
3. Line ordering/timestamps are non-monotonic or implausible.
4. Repeated chorus occurrence cannot be resolved reliably.
5. Difficult vocals/mix cause the lightweight route to fail.
6. The product explicitly requires character/word-level timing beyond ordinary MV line timing.

## P2 execution discipline

- verify the exact HG02 audio SHA first;
- use audited trusted lyrics, without non-sung punctuation;
- reuse the existing pinned shared environment; do not create a per-song environment;
- run the canonical `run_alignment.py` adapter;
- use explicit Xingyu `alignment.json` line start/end when present;
- run one automatic QA;
- do not add a third alignment method unless P2 itself produces a concrete failure.

## Relationship to normal production

Normal route policy:
`P0 SAME_VERSION_LRC -> P1 D01B_LIGHTWEIGHT_FASTER_WHISPER -> P2 XINGYU_CTC_FALLBACK`

Xingyu is intentionally retained as a strong recovery/high-precision tool, not removed and not promoted to the default path.
