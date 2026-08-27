# Rules｜MV Audio Timeline Priority Route v1

Status: `LEAN_R1 CANDIDATE`

Goal: answer only two production questions from the exact HG02 BGM: complete sung lyrics and line start/end timing.

## Priority

### P0 — Same-version timed lyric/LRC
Use when the lyric timing source is demonstrably the same audio version/occurrence. Verify identity, map clip offset/occurrence, run one QA, then lock.

### P1 — Lightweight ASR mapping (default AI route)
Use when P0 is unavailable or ambiguous. One full-clip lightweight ASR pass with word timestamps, one trusted-lyric audit, then monotonic trusted-text mapping. If complete line coverage passes, lock and stop.

Preferred validated reference from OSS_OPT_R1: faster-whisper 1.2.1 / small / CPU int8 / zh / word timestamps.

### P2 — Heavy forced alignment fallback
Use only on a concrete P1 failure: incomplete line mapping, non-monotonic timing, unresolved repeated occurrence, difficult vocal/mix, or an explicit precision requirement. Xingyu/CTC is a fallback, not a default second opinion.

## Hard efficiency rules
- stop at the first route that passes;
- do not run P0+P1+P2 for reassurance;
- do not reinstall production models per song;
- creator captions/descriptions/hashtags are not complete lyric authority;
- one trusted-text audit is normal; repeated evidence hunting is not;
- waveform/BPM may support structure but cannot invent lyric timestamps;
- final authority remains the canonical Audio Timeline package/final gate.
