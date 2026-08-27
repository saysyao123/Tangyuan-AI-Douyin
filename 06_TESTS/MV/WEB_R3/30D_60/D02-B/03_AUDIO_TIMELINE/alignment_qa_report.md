# D02-B｜Audio Timeline Alignment QA Report

Status: `PASS / P1 LIGHTWEIGHT TIMELINE LOCKED`
Route: `P1_D01B_LIGHTWEIGHT_FASTER_WHISPER`
Song: `有几次想你了`
Locked audio SHA-256: `6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4`

## Human lyric audit

- User decision: `歌词OK`
- Decision time: `2026-08-27T18:30:00+08:00`
- Trusted lyric lines: `7`
- Normalized lyric characters: `45`
- `LYRIC_TEXT_LOCKED = YES`

## Primary timing evidence

- Tool: `faster-whisper 1.2.1`
- Model: `small`
- Device/compute: `CPU / int8`
- Language: `zh`
- Word timestamps: `enabled`
- Workflow run: `33060055071`
- Durable raw evidence: `raw_evidence/faster_whisper/lightweight_mapping_report.json`
- Mapping result: `7/7 lines`
- Per-line character coverage: `100%`
- Sequence ratio: `1.0`
- Line starts strictly monotonic: `YES`
- Exact locked audio SHA verified: `YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = YES`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = YES`

## Boundary QA

| Line | Lyric | Start | End | Coverage | QA |
|---|---|---:|---:|---:|---|
| L01 | 有几次想你了 | 0.000 | 1.880 | 100% | PASS |
| L02 | 有几次忍住了 | 2.020 | 3.640 | 100% | PASS |
| L03 | 有几句想说的 | 3.780 | 5.400 | 100% | PASS |
| L04 | 都变成算了 | 5.600 | 7.180 | 100% | PASS |
| L05 | 有几场雨停了 | 7.320 | 8.940 | 100% | PASS |
| L06 | 有几阵风过了 | 9.120 | 10.700 | 100% | PASS |
| L07 | 有多舍不得也该放下了 | 10.860 | 14.260 | 100% | PASS |

Checks:
- [x] locked audio SHA reverified
- [x] first lyric boundary represented by primary word-timestamp evidence
- [x] every lyric line start mapped
- [x] every lyric line end/display handoff mapped
- [x] middle representative lines mapped
- [x] longest/final line mapped
- [x] final lyric end is inside locked audio duration
- [x] repeated occurrence ambiguity absent
- [x] no unmatched line silently interpolated
- [x] SRT text/timing matches the locked line timeline
- [x] visual edit boundaries were not used as lyric timing evidence

`ALIGNMENT_GROUND_TRUTH_QA_PASS = YES`

## Existing fallback cross-check

A previously validated Xingyu CTC fallback run exists from the same corrected seven-line audio/lyrics. It is retained only as P2 archive evidence, not as a required second-model production step.

Existing P2-vs-P1 line-start deltas are all <= `0.300s`; median absolute start delta is approximately `0.022s`, with no conflict above the `0.50s` review threshold. This supports the P1 line-level timing without changing the rule that normal production stops after P1 PASS.

## Final package state

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = YES`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = YES`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = YES`
- `LYRIC_TIMELINE_LOCKED = YES`
- `MUSIC_EVENT_MAP_VERIFIED = DEFERRED_DOWNSTREAM_NON_BLOCKING`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`

`anchor_words.csv` and `music_events.csv` are downstream Natural Beat / Director enrichment under `OSS_OPT_R1`; they do not block lyric-timeline lock.

## Route decision

`P0 SAME_VERSION_LRC -> P1 D01B_LIGHTWEIGHT_FASTER_WHISPER -> P2 XINGYU_CTC_FALLBACK`

D02-B stops at P1 because P1 passed all lyric-timeline QA. Xingyu remains preserved as fallback and is not loaded on the normal PASS path.
