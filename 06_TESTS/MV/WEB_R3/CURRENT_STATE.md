# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-C / PICTURE EDIT V1`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_COMPLETE_FOR_CURRENT_LOOP / PHYSICAL_PLAUSIBILITY_ITERATION_COMPLETE / DOUBAO_PROMPT_REWRITE_VALIDATED / FINAL_MATERIAL_REVIEW_COMPLETE / PICTURE_EDIT_V1_READY / HG04_PENDING`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

## Locked Audio

Song family: `如果风会替我说话`
Locked BGM: `如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`
Duration: `24.320000s`
`BGM_LOCKED = YES`

## Canonical lyric timeline

`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`

1. `0–3` 如果风会替我说话
2. `3–6` 如果雨会替我回答
3. `6–8` 如果我还会想起他
4. `8–12` 如果还能一起回家
5. `12–15` 如果梦能模糊真假
6. `15–18` 如果痛能随之融化
7. `18–20` 如果我们还是傻瓜
8. `20–24` 如果爱不只是童话

## R3-B material / learning lock for current loop

Canonical reports:
- `R3_B_FINAL_MATERIAL_REVIEW_AND_REUSABLE_LESSONS_v1.md`
- `R3_B_DOUBAO_PROMPT_REWRITE_VALIDATION_v1.md`
- `R3_B_PHYSICAL_PLAUSIBILITY_GATE_v1.md`

Current reusable experimental guidance:
- `TRIM BEFORE REGENERATE`
- `WEAKEST SUFFICIENT MOTION`
- `FIRST-FRAME STATE PRELOAD`
- `ONE DIFFICULT PHYSICS EVENT PER SOURCE`
- `CONTROL BUDGET`
- `SURFACE OWNERSHIP`
- `PHYSICALLY BELIEVABLE > VISUALLY LOUD`
- `STATIC BASE -> ONE ALLOWED EVENT`
- `WEAK VERB FOR HIGH-RISK MATERIALS`
- `SERIALIZE PHYSICS AND FOCUS/CAMERA`
- `FREEZE NON-TARGET MATERIAL FIELD`
- partial foreground occlusion for same-scene continuity;
- full / near-full occlusion as intentional hidden transition / edit point.

Rain strategy candidate:
- default rain = atmospheric texture, wet-glass sheen, distant streaks, bokeh/reflection;
- explicit droplet birth / merge / macro-fluid motion is not production-default.

Camera positive evidence:
- S03 mild `SLOW DOLLY-OUT REVEAL`;
- S04 foreground reveal / occlusion as transition grammar;
- S08 `WORLD-OPENING CRANE / RETREAT` benchmark.

## Picture Edit v1

Canonical EDL:
`R3_C_PICTURE_EDIT_V1_EDL.md`

Picture Edit v1 uses the latest user/Doubao-rewritten S02 and S06 outputs as primary material, combined with previously accepted S01/S03/S04/S05/S07/S08 sources.

Edit principles:
- generated 5s source is a reservoir, not a mandatory final shot length;
- use selective stable windows;
- remove all generated source audio;
- locked BGM is the only production audio;
- trim around visually loud liquid artifacts;
- use S04 foreground occlusion as a motivated cut point;
- preserve S08 continuous release as much as possible;
- no subtitles / final packaging yet.

Current candidate timeline:
- S01 final 0–3s from source `0.15–3.15`
- S02 final 3–6s from latest rain source `2.00–5.00`
- S03 final 6–8s from source `0.60–2.60`
- S04 final 8–12s from source `0.20–4.20`
- S05 final 12–15s from source `0.30–3.30`
- S06 final 15–18s from latest ice source `2.00–5.00`
- S07 final 18–20s from source `0.80–2.80`
- S08 final 20–24.32s from source `0.40–4.72`

`PICTURE_EDIT_V1_READY = YES`
`HG04_PASS = NO / PENDING HUMAN REVIEW`

## HG04 review scope

Human Gate 04 reviews only:
1. picture rhythm against BGM;
2. lyric-to-visual fit;
3. continuity / shot-scale breathing;
4. S04 -> S05 occlusion cut quality;
5. whether S02/S06 remaining physical artifacts are sufficiently hidden at real playback speed;
6. whether edit points need frame-level patching.

Do NOT add subtitles or final publish polish before HG04.

## State chain

`HG01 PASS`
→ `BGM LOCKED`
→ `AUDIO TIMELINE LOCKED`
→ `HG03 PASS`
→ `FIRST FRAME SET LOCKED`
→ `CAMERA / PHYSICS ITERATION COMPLETE FOR CURRENT LOOP`
→ `DOUBAO PROMPT REWRITE VALIDATED`
→ `FINAL MATERIAL REVIEW COMPLETE`
→ **`PICTURE EDIT V1 READY / HG04 PENDING`**
