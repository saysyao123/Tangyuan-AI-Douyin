# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B / FIRST-FRAME SET GENERATION`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / DATA_CENTER_V1_PASS / D01_PASS / D02_PASS / HG01_PASS / SONG_FAMILY_LOCKED / TREND_REFERENCE_AUDIO_LOCKED / HG02_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / R3_B_CHARACTER_VISUAL_BASELINE_LOCKED / FIRST_FRAME_DIRECTOR_PLAN_READY`
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

Locked SONG_FAMILY:
`如果风会替我说话`

Selection receipt:
`D02_HG01_SELECTION_RECEIPT_v1.md`

## B0｜Exact Audio Version Discovery

Trend-native audio reference:
`DOUYIN_MUSIC_ASSET:7670880580757867270`

Three independent core works expose the same asset and pairwise Chromaprint similarity is >= `0.986020`, all best alignments `shift=0`.

Decision:
`SAME_AUDIO_FAMILY_CONFIRMED`

## HG02｜BGM lock

Human Gate: `PASS`

Receipt:
`B0_HG02_BGM_LOCK_RECEIPT_v1.md`

Locked artifact:
`如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`

Identity:
- duration: `24.320000s`
- decoded content: `24.286621s`
- sample rate: `44100 Hz`
- channels: `2`
- SHA-256: `f128163c62f16eb94e5e302d2f97f725bcaa775a457fc09ffd21b9c4f65a8553`
- speed/time-stretch: `none after HG02 artifact creation`

`BGM_LOCKED = YES`

## Stage 2A｜Audio Timeline Package

Status: `LOCKED`

Canonical directory:
`06_TESTS/MV/WEB_R3/AUDIO_TIMELINE_PACKAGE/`

Primary route:
`SAME_VERSION_LRC`

Canonical 8-line excerpt:
1. `0–3` 如果风会替我说话
2. `3–6` 如果雨会替我回答
3. `6–8` 如果我还会想起他
4. `8–12` 如果还能一起回家
5. `12–15` 如果梦能模糊真假
6. `15–18` 如果痛能随之融化
7. `18–20` 如果我们还是傻瓜
8. `20–24` 如果爱不只是童话

Package includes:
- `audio_identity.json`
- `trusted_lyrics.txt`
- `raw_evidence/timed_lyrics_source.md`
- `alignment_provenance.json`
- `line_timeline.csv`
- `lyrics_exact.srt`
- `anchor_words.csv`
- `music_events.csv`
- `alignment_qa_report.md`
- `package_manifest.json`

Gate:
`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`

Word-level karaoke timing is not claimed; line-level MV production coordinates are locked.

## R3-B｜Visual Calibration / Character Baseline

User-approved direction:
`R3_B_VISUAL_DIRECTION_LOCK_v1.md`

Decision:
`R3_B_CHARACTER_VISUAL_BASELINE_LOCKED = YES`

Character language:
- fictional young adult East Asian woman;
- distinctive elongated almond-eye region; stronger brow-eye depth and wet catchlight;
- do not reproduce a real celebrity identity;
- low-frequency clean skin with real microstructure;
- dark hair with fine loose strands;
- smoke-charcoal semi-transparent veil fully covering lower face in every human frame;
- emotion carried by eyes / brows / posture / hands / wind / rain, never by exposed mouth.

Director plan:
`R3_B_FIRST_FRAME_DIRECTOR_PLAN_v1.md`

Eight lyric-driven production segments are allocated with differentiated composition:
`HOOK wind -> rain response -> memory absence -> home warmth -> dream/reflection -> pain dissolves -> imperfect us -> dawn release`.

## Current Gate / Next execution

Current stage:
`FIRST_FRAME SET GENERATION + SET-LEVEL QA`

Next actions:
1. generate S01–S08 first frames using the locked visual baseline;
2. preserve same woman / veil / world while varying shot geometry and dominant event;
3. run set-level QA: lyric hit / beauty / identity / veil integrity / repetition / dynamic executability;
4. submit the complete set to `HG03 Visual Direction / First-frame Set Gate`;
5. after HG03 PASS, enter Dynamic Prompt + external video generation.

## State chain

`D01 PASS`
→ `D02 PASS`
→ `HG01 PASS`
→ `SONG_FAMILY_LOCKED`
→ `TREND_REFERENCE_AUDIO_VERSION_LOCKED`
→ `HG02 PASS`
→ `BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ `R3_B_CHARACTER_VISUAL_BASELINE_LOCKED`
→ `FIRST_FRAME_DIRECTOR_PLAN_READY`
→ **`FIRST_FRAME_SET_GENERATING`**

## Data center refresh

Keep the current 9-account data center intact and refresh approximately every 15 days by `aweme_id` incremental merge. Database refresh is independent of the current visual production Gate.
