# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B0 / EXACT AUDIO VERSION -> HG02 LISTENING`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / DATA_CENTER_V1_PASS / D01_PASS / D02_PASS / HG01_PASS / SONG_FAMILY_LOCKED / TREND_REFERENCE_AUDIO_LOCKED / HG02_PENDING_USER_LISTEN`
- UPDATED_AT: `2026-08-24 Asia/Manila`

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

The full release is not yet the production BGM lock.

## HG02 listening reference

A `24.320s` listening reference has been built from the actual 火乐烁 core work using the shared trend-native audio.

Purpose:
`HG02 listening only`

Current decision options:

### Option A｜Trend-native short MV
Lock the ~24s shared Douyin version.

Advantages:
- exact audio already repeated across 3 core accounts;
- strongest trend/version fidelity;
- fits short high-completion music-promotion format;
- avoids unnecessary version drift.

### Option B｜Extended MV
Continue to obtain/validate the full `张蓓蓓、林叙` track and choose a `30–40s` excerpt containing the same hook.

Advantages:
- more lyric/visual beat space.

Cost/risk:
- another source-version alignment step;
- may drift away from the exact audio asset already validated by the database.

## Current Gate

- `D01 = PASS`
- `D02 = PASS`
- `HG01 SONG AESTHETIC GATE = PASS`
- `SONG_FAMILY_LOCKED = 如果风会替我说话`
- `TREND_REFERENCE_AUDIO_VERSION_LOCKED = YES`
- `HG02 BGM LISTENING = PENDING`
- `BGM_LOCKED = NO`

No Audio Timeline Package, director work, first frames, dynamic prompts or visual generation may begin before HG02 PASS.

## Next execution order

1. User listens to the ~24s trend-native HG02 reference.
2. User chooses:
   - `A / 24s trend-native`, or
   - `B / continue full-track discovery for a longer excerpt`.
3. If A: lock BGM and create Audio Timeline Package.
4. If B: obtain/validate the full track, create 1–2 excerpt candidates, then HG02 again.
5. Only after BGM lock continue into the R2-validated audio timeline / director / visual chain.

## Data center refresh

Keep the current 9-account data center intact and refresh approximately every 15 days by `aweme_id` incremental merge. Database refresh is independent of the current B0/HG02 production Gate.
