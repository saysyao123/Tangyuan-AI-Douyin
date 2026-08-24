# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B / DYNAMIC SOURCE GENERATION`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / DATA_CENTER_V1_PASS / D01_PASS / D02_PASS / HG01_PASS / SONG_FAMILY_LOCKED / TREND_REFERENCE_AUDIO_LOCKED / HG02_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / R3_B_CHARACTER_VISUAL_BASELINE_LOCKED / FIRST_FRAME_DIRECTOR_PLAN_READY / MMP01_READY / FIRST_FRAME_EXECUTION_PLAN_READY / FIRST_FRAME_SET_QA_PASS / HG03_PASS / FIRST_FRAME_SET_LOCKED / DYNAMIC_PROMPTS_V1_READY`
- UPDATED_AT: `2026-08-24 Asia/Shanghai`

## Locked Audio

Song family: `如果风会替我说话`

Trend-native audio reference:
`DOUYIN_MUSIC_ASSET:7670880580757867270`

Locked BGM:
`如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`

Identity:
- duration: `24.320000s`
- decoded content: `24.286621s`
- sample rate: `44100 Hz`
- channels: `2`
- SHA-256: `f128163c62f16eb94e5e302d2f97f725bcaa775a457fc09ffd21b9c4f65a8553`

`BGM_LOCKED = YES`

## Audio Timeline Package

Status: `LOCKED`
Canonical directory: `06_TESTS/MV/WEB_R3/AUDIO_TIMELINE_PACKAGE/`

Canonical line coordinates:
1. `0–3` 如果风会替我说话
2. `3–6` 如果雨会替我回答
3. `6–8` 如果我还会想起他
4. `8–12` 如果还能一起回家
5. `12–15` 如果梦能模糊真假
6. `15–18` 如果痛能随之融化
7. `18–20` 如果我们还是傻瓜
8. `20–24` 如果爱不只是童话

`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`

## R3-B Visual Baseline

Character / world direction:
`R3_B_VISUAL_DIRECTION_LOCK_v1.md`

Director plan:
`R3_B_FIRST_FRAME_DIRECTOR_PLAN_v1.md`

Masked micro-performance layer:
`R3_B_MASKED_MICRO_PERFORMANCE_MMP01_v1.md`

First-frame execution plan:
`R3_B_FIRST_FRAME_EXECUTION_PLAN_v1.md`

Locked character language:
- same fictional young adult East Asian woman;
- distinctive elongated almond-eye region with defined brow-eye depth and wet catchlight;
- no real-celebrity identity reproduction;
- low-frequency clean skin with real microstructure;
- dark hair with fine loose strands;
- smoke-charcoal semi-transparent veil fully covering lower face in every human frame;
- emotion carried by eyes / brows / posture / hands / wind / rain.

## First-frame Set

The full S01–S08 set was regenerated after director review to correct near-shot compression.

Accepted shot-scale rhythm:
`EXTREME CLOSE -> CLOSE/REFLECTION -> MEDIUM -> WIDE -> MEDIUM/REFLECTION -> CLOSE -> MEDIUM -> MEDIUM-WIDE/WIDE`

Machine QA:
`R3_B_FIRST_FRAME_SET_QA_v1.md`

Human Gate receipt:
`R3_B_HG03_FIRST_FRAME_SET_LOCK_v1.md`

States:
- `FIRST_FRAME_SET_QA_PASS = YES`
- `HG03_PASS = YES`
- `FIRST_FRAME_SET_LOCKED = YES`

## Dynamic Stage

Dynamic prompt package:
`R3_B_DYNAMIC_PROMPTS_v1.md`

Target:
- Seedance 2 mini;
- 5s source per segment;
- 9:16;
- default 1–2 shots, edit-driven;
- one dominant visual event per source;
- first-frame character closure enforced;
- veil continuity enforced;
- `SOURCE_AUDIO = REMOVE`;
- no BGM / singing / dialogue / narration generated in source clips.

Generation order:
`R3_S01 -> R3_S02 -> R3_S03 -> R3_S04 -> R3_S05 -> R3_S06 -> R3_S07 -> R3_S08`

## Current Gate / Next execution

Current stage:
`DYNAMIC_SOURCES_PENDING_EXTERNAL_GENERATION`

Next actions:
1. generate eight 5s image-to-video sources from the locked first frames using `R3_B_DYNAMIC_PROMPTS_v1.md`;
2. return sources in sequence S01–S08;
3. run W07-style source QA: identity / veil / topology / event / camera / clean in-out / source audio;
4. patch only failing sources at the nearest cause;
5. when source QA passes, lock normalized shot library and enter Picture Edit / HG04.

## State chain

`D01 PASS`
→ `D02 PASS`
→ `HG01 PASS`
→ `BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ `R3_B_CHARACTER_VISUAL_BASELINE_LOCKED`
→ `FIRST_FRAME_SET_QA_PASS`
→ `HG03 PASS`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_PROMPTS_V1_READY`
→ **`DYNAMIC_SOURCES_PENDING_EXTERNAL_GENERATION`**

## Data center refresh

Keep the current 9-account data center intact and refresh approximately every 15 days by `aweme_id` incremental merge. Database refresh is independent of the current production Gate.
