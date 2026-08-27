# D02-A｜Audio Timeline Alignment QA Report

Status: `PASS / AUDIO_TIMELINE_PACKAGE_LOCKABLE`

## Primary evidence

- Route: `Strong Route B`
- Exact Douyin master SHA256: `b5c951cfd1a5d1ab8cf67c093ca0ab1242e9a9be116785588074d768eba9621d`
- Trusted lyric text was locked **before** timing.
- Forced aligner: `xingyu-lyrics-aligner 0.7.0`
- Engine/model: `WhisperX CTC / jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn`
- Result: `4/4 lines aligned`
- Timing characters: `47/47`
- Missing timing characters: `0`
- Skipped lines: `0`
- Non-monotonic lines: `0`
- Warnings: `0`
- Coverage: `1.0`

Primary evidence therefore passes the R3 trusted-lyrics forced-alignment requirement.

## Independent ASR cross-check

`faster-whisper large-v3` preserves the same four-line order and the same occurrence. Its free-ASR segment starts are earlier than the CTC line starts:

| Line | large-v3 free-ASR start | CTC start | CTC - ASR |
|---|---:|---:|---:|
| L01 | 1.780 | 2.622 | +0.842 |
| L02 | 7.060 | 8.027 | +0.967 |
| L03 | 12.840 | 14.113 | +1.273 |
| L04 | 18.600 | 19.518 | +0.918 |

Mean delta: `+1.000s`; median: `+0.9425s`.

This **does not satisfy** the automatic two-source green threshold. Machine review classifies it as `EXPLAINED_SECONDARY_DRIFT`, not an unresolved occurrence conflict: the offsets are systematic, lyric order/text agree, and free-ASR segment boundaries are not the authoritative clock in Strong Route B. The CTC route is complete, monotonic, and warning-free.

Decision: `CHG-A NOT TRIGGERED`.

## HG02-B fade interaction

- Approved fade start: `25.223991s`
- Forced-alignment final vocal end: `25.704s`
- Fade overlaps the final vocal by approximately `0.480s`.

The user explicitly preferred this B version at HG02. The fade is amplitude-only and does not change the lyric clock. No audio rollback is required.

## Locked line clock

- L01: `2.622–8.027`
- L02: `8.027–14.113`
- L03: `14.113–19.518`
- L04: `19.518–25.704`
- Intro: `0.000–2.622`
- Musical tail truth: `25.704–26.423991`

## Final QA decision

`AUDIO_TIMELINE_PACKAGE = PASS`

Timing-dependent downstream work may use this package as the single time truth.
