# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B / DYNAMIC SOURCE HUMAN REVIEW + PHYSICS PATCH`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_BATCH_GENERATED / HUMAN_REVIEW_COMPLETE / PHYSICAL_PLAUSIBILITY_GATE_READY / PATCH_BATCH_REQUIRED`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

## Locked Audio

Song family: `如果风会替我说话`
Locked BGM: `如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`
Duration: `24.320000s`
`BGM_LOCKED = YES`

## Audio Timeline

`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`

1. `0–3` 如果风会替我说话
2. `3–6` 如果雨会替我回答
3. `6–8` 如果我还会想起他
4. `8–12` 如果还能一起回家
5. `12–15` 如果梦能模糊真假
6. `15–18` 如果痛能随之融化
7. `18–20` 如果我们还是傻瓜
8. `20–24` 如果爱不只是童话

## Visual / First-frame

- `R3_B_VISUAL_DIRECTION_LOCK_v1.md`
- `R3_B_FIRST_FRAME_DIRECTOR_PLAN_v1.md`
- `R3_B_FIRST_FRAME_EXECUTION_PLAN_v1.md`
- `R3_B_HG03_FIRST_FRAME_SET_LOCK_v1.md`

`FIRST_FRAME_SET_LOCKED = YES`

## Veil policy clarification

For this R3 production, the face veil is primarily a **Doubao generation-entry / compatibility device**.

Therefore:
- first frame / prompt may still use the veil to enable generation;
- final dynamic source is **not automatically failed** merely because the veil shifts or reveals more of the lower face;
- veil continuity is no longer a final narrative HARD gate for this song;
- final QA should prioritize visual quality, identity stability, lyric fit, physical plausibility and editability.

This clarification overrides earlier R3 machine-QA assumptions where veil reveal alone caused failure.

## Dynamic Camera Calibration

Prompt package:
`R3_B_DYNAMIC_PROMPTS_v2_CAMERA_CALIBRATION.md`

Camera matrix:
`R3_B_CAMERA_CALIBRATION_MATRIX_v1.md`

Generated batch:
`S01–S08 / 8 x 5s Seedance 2 mini`

Machine QA:
`R3_B_DYNAMIC_SOURCE_QA_v1.md`

Human review override:
`R3_B_DYNAMIC_SOURCE_HUMAN_REVIEW_v1.md`

Physics gate:
`R3_B_PHYSICAL_PLAUSIBILITY_GATE_v1.md`

Patch plan:
`R3_B_PATCH_PLAN_v2_PHYSICS_DIRECTOR.md`

## Human source decisions

### Keep
- `S01` — accepted visually; veil reveal is not a blocker.
- `S03` — no major issue.
- `S07` — overall works.
- `S08` — strong benchmark; camera + emotional release highly approved.

### Conditional
- `S02` — overall usable, but rain/glass physics are incorrect or ambiguous; quality-first patch preferred.

### Regenerate / redesign
- `S04` — camera move excellent, but full occlusion causes uncontrolled post-occlusion scene/pose reconstruction; current second half is narratively unclear.
- `S05` — rain/water appears on the wrong side / inside the glass volume; surface ownership failure.
- `S06` — full concept failure, not merely a mask issue; rebuild shot from first principles.

Recommended patch batch:
`S02 / S04 / S05 / S06`

## Camera-learning status

### Strong positive evidence
- `S08 SLOW CRANE / WORLD-OPENING RELEASE` — current benchmark.
- `S03 SLOW DOLLY-OUT REVEAL` — useful positive evidence.

### Valuable but needs correct use
- `FULL FOREGROUND OCCLUSION` — good as an intentional hidden transition from Scene A -> Scene B; risky for same-scene continuity.
- `PARTIAL FOREGROUND REVEAL` — preferred for same-scene continuity.

### Not yet proven as stable grammar
- lateral slider along glass;
- mini orbit around reflection;
- diagonal slider + rack focus.

## Physical Plausibility Gate

Before camera motion, every complex shot must define:
- camera side;
- character side;
- boundary plane(s);
- effect ownership (rain / reflection / condensation / light);
- gravity / flow direction;
- occlusion continuity;
- post-occlusion target state.

New QA axis:
`PHYSICAL_PLAUSIBILITY = PASS / PARTIAL / FAIL`

A beautiful shot with obvious impossible physics cannot receive final source lock.

## Current Gate / Next execution

`SHOT_LIBRARY_LOCKED = NO`

Next:
1. rewrite S02 / S04 / S05 / S06 using physics-first topology;
2. regenerate only those four sources;
3. run patch QA;
4. if pass, lock shot library;
5. enter Picture Edit / HG04.

## State chain

`HG01 PASS`
→ `BGM LOCKED`
→ `AUDIO TIMELINE LOCKED`
→ `HG03 PASS`
→ `FIRST FRAME SET LOCKED`
→ `CAMERA CALIBRATION GENERATED`
→ `HUMAN REVIEW COMPLETE`
→ `PHYSICAL PLAUSIBILITY GATE READY`
→ **`PATCH BATCH S02/S04/S05/S06`**
