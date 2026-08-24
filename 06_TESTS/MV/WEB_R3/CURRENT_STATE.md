# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B / FIRST-FRAME CALIBRATION BATCH A`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / DATA_CENTER_V1_PASS / D01_PASS / D02_PASS / HG01_PASS / SONG_FAMILY_LOCKED / TREND_REFERENCE_AUDIO_LOCKED / HG02_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / R3_B_CHARACTER_VISUAL_BASELINE_LOCKED / FIRST_FRAME_DIRECTOR_PLAN_READY / MMP01_READY / FIRST_FRAME_EXECUTION_PLAN_READY / CALIBRATION_BATCH_A_READY`
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

Micro-performance test layer:
`R3_B_MASKED_MICRO_PERFORMANCE_MMP01_v1.md`

First-frame execution plan:
`R3_B_FIRST_FRAME_EXECUTION_PLAN_v1.md`

Eight lyric-driven production segments remain canonical:
`HOOK wind -> rain response -> memory absence -> home warmth -> dream/reflection -> pain dissolves -> imperfect us -> dawn release`.

## First-frame calibration strategy

Do not blindly generate all eight frames first.

### Calibration Batch A
Generate three representative frames:
1. `S01 / HOOK` — extreme eye close-up; test distinctive character quality + wind/veil physics;
2. `S06 / HEALING` — tactile eyes+hand frame; test MMP-01 feasibility + hand/veil physical interaction;
3. `S08 / RELEASE` — medium-wide dawn frame; test identity continuity in open space + healing ceiling.

Batch A must pass:
- character identity / eye-region distinctiveness;
- veil integrity;
- cinematic realism / low AI-template feeling;
- visual differentiation;
- dynamic entrance executability;
- healing atmosphere;
- no real-celebrity identity reproduction.

If Batch A PASS:
generate `S02 + S03 + S04 + S05 + S07`, then run full set-level QA and submit HG03.

## Current Gate / Next execution

Current stage:
`CALIBRATION_BATCH_A_READY_FOR_IMAGE_GENERATION`

Next actions:
1. generate S01 / S06 / S08 first-frame calibration images;
2. run director QA against `R3_B_FIRST_FRAME_EXECUTION_PLAN_v1.md`;
3. if one frame fails, patch only its nearest root cause;
4. if all three PASS, generate remaining five frames;
5. run complete set-level QA;
6. submit S01–S08 to `HG03 Visual Direction / First-frame Set Gate`;
7. only after HG03 PASS enter Dynamic Prompt + external video generation.

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
→ `MMP01_READY`
→ `FIRST_FRAME_EXECUTION_PLAN_READY`
→ **`CALIBRATION_BATCH_A_READY_FOR_IMAGE_GENERATION`**

## Data center refresh

Keep the current 9-account data center intact and refresh approximately every 15 days by `aweme_id` incremental merge. Database refresh is independent of the current visual production Gate.
