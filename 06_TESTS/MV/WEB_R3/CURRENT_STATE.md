# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B0 / STAGE 2A AUDIO TIMELINE PACKAGE`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / DATA_CENTER_V1_PASS / D01_PASS / D02_PASS / HG01_PASS / SONG_FAMILY_LOCKED / TREND_REFERENCE_AUDIO_LOCKED / HG02_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_BUILDING`
- UPDATED_AT: `2026-08-24 Asia/Tokyo`

## Locked upstream nodes

### D01｜Database Evidence Node
`PASS`

Canonical data center:
`06_TESTS/MV/WEB_R3/database/data_center/`

Mode:
`PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`

Database prototype:
`STABLE / QUERY_INTERFACE_V1_PASS / HEALTH_GATE_PASS`

### D02｜HG01 Candidate Evidence
`PASS`

Selection receipt:
`D02_HG01_SELECTION_RECEIPT_v1.md`

Locked SONG_FAMILY:
`如果风会替我说话`

Other D02 songs remain candidates for future rounds.

## B0｜Exact Audio Version Discovery

Core audio probe:
`B0_IF_WIND_AUDIO_PROBE/audio_probe_report.json`

Three direct core-account works were fully parsed/downloaded and compared:
- 火乐烁 — aweme `7674213606980010597` — `24.286621s`
- XIANGJISHI — aweme `7674182530162440933` — `11.900667s`
- 乐 ♩青春 — aweme `7673915982527960265` — `12.073991s`

All three use the exact same Douyin music asset:
- asset id: `7670880580757867270`
- display: `@林叙（错位秋天已上线）创作的原声`

Pairwise Chromaprint similarity:
- 火乐烁 / XIANGJISHI: `0.994583`
- 火乐烁 / 乐 ♩青春: `0.986020`
- XIANGJISHI / 乐 ♩青春: `0.986250`

All best alignments use `shift=0`.

Decision:
`SAME_AUDIO_FAMILY_CONFIRMED`

Trend-native audio reference:
`DOUYIN_MUSIC_ASSET:7670880580757867270`

Public full-track discovery currently identifies a likely full release as:
`如果风会替我说话 — 张蓓蓓、林叙`

The full release is not the production BGM for this R3 test.

## HG02｜BGM lock

Human Gate:
`PASS`

Receipt:
`B0_HG02_BGM_LOCK_RECEIPT_v1.md`

Locked artifact:
`如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`

Locked identity:
- duration: `24.320000s`
- sample rate: `44100 Hz`
- channels: `2`
- SHA-256: `f128163c62f16eb94e5e302d2f97f725bcaa775a457fc09ffd21b9c4f65a8553`
- speed/time-stretch: `none after HG02 artifact creation`

States:
- `HG02_BGM_LISTENING_PASS = YES`
- `BGM_LOCKED = YES`

## Stage 2A｜Audio Timeline Package

Status:
`BUILDING`

Authority:
`04_HARNESS/rules/mv_audio_timeline.md`

Required before downstream timing work:
- exact audio identity
- trusted lyrics
- raw strong timing evidence
- provenance
- line timeline
- exact SRT
- anchor words
- music events
- alignment QA
- package manifest

Current Gate:
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`

No formal Director timing allocation, First Frames, Dynamic prompts, Picture Edit, or Subtitle production may begin before Stage 2A PASS.

## Current state chain

`D01 PASS`
→ `D02 PASS`
→ `HG01 PASS`
→ `SONG_FAMILY_LOCKED`
→ `TREND_REFERENCE_AUDIO_VERSION_LOCKED`
→ `HG02 PASS`
→ `BGM_LOCKED`
→ **`AUDIO_TIMELINE_PACKAGE_BUILDING`**

## Next execution order

1. Obtain/lock trusted lyric text for the exact 24.32s clip.
2. Build a Strong Route alignment against the locked BGM.
3. Independently cross-check first/middle/final lines and repeated occurrences if any.
4. Build `line_timeline.csv + lyrics_exact.srt + anchor_words.csv + music_events.csv`.
5. Run ground-truth QA and package manifest/hash checks.
6. If all hard states PASS: `AUDIO_TIMELINE_PACKAGE_LOCKED = YES` and only then enter Natural Beat / R3-B visual calibration.

## Data center refresh

Keep the current 9-account data center intact and refresh approximately every 15 days by `aweme_id` incremental merge. Database refresh is independent of the current Stage 2A production Gate.
