# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B / S02+S06 V4 PHYSICS RETEST`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_BATCH_GENERATED / HUMAN_REVIEW_COMPLETE / PHYSICAL_PLAUSIBILITY_GATE_READY / V3_PATCH_RETEST_REVIEWED / S04_PASS / S05_PASS / S02_S06_V4_FIRST_FRAMES_READY / S02_S06_V4_DYNAMIC_PROMPTS_READY`
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

## Keep without more generation

`S01 / S03 / S04(v3) / S05(v3) / S07 / S08`

S08 remains the current `WORLD-OPENING RELEASE` benchmark.

## Physics / control evidence

- `R3_B_PHYSICAL_PLAUSIBILITY_GATE_v1.md`
- `R3_B_OPEN_SOURCE_CONTROL_RESEARCH_AND_PATCH_PLAN_v1.md`
- `R3_B_DYNAMIC_PROMPTS_v4_S02_S06_PHYSICS_PATCH.md`

Experimental rules active for this retest:
- `FIRST-FRAME STATE PRELOAD`
- `ONE PHYSICS EVENT PER SOURCE`
- `CONTROL BUDGET`
- `STATE -> TRACK -> CAMERA -> RESIDUE`

## S02 v4

New first-frame state is ready:
- same woman at rain window;
- existing thin rain trails already visible on the exterior-facing glass surface;
- reflection already established;
- no need for droplet birth/merge.

Dynamic target:
`PRELOADED EXTERIOR RIVULET`
- locked camera;
- one existing thin rivulet moves downward only;
- no new droplets / merging / size explosion;
- local reflection distortion only;
- one slow rack focus.

## S06 v4

New first-frame state is ready:
- foreground ice cube already established on dark tray;
- ice already wet;
- one small bead already exists at lower edge;
- woman remains soft-focus background observer;
- no hand interaction.

Dynamic target:
`PRELOADED ICE + SINGLE DROP`
- locked camera;
- one pre-existing bead detaches once and falls vertically;
- ice geometry remains stable;
- one slow rack focus from ice to eyes;
- minimal character performance.

## Current Gate / Next execution

`SHOT_LIBRARY_LOCKED = NO`

Next:
1. generate S02 v4 from the new rain-window first frame;
2. generate S06 v4 from the new ice first frame;
3. run physical plausibility QA only on these two clips;
4. if both pass, lock shot library;
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
→ `V3 PATCH RETEST`
→ `S04 PASS / S05 PASS`
→ `S02+S06 V4 FIRST FRAMES READY`
→ **`S02+S06 V4 PHYSICS RETEST READY`**
