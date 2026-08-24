# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B / PHYSICS PATCH ANALYSIS`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_BATCH_GENERATED / HUMAN_REVIEW_COMPLETE / PHYSICAL_PLAUSIBILITY_GATE_READY / V3_PATCH_RETEST_REVIEWED / S04_PASS / S05_PASS / S02_S06_PATCH_REQUIRED`
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

For this R3 production, the veil is primarily a Doubao generation-entry / compatibility device, not a final narrative HARD continuity gate. Final QA prioritizes visual quality, identity stability, lyric fit, physical plausibility and editability.

## Dynamic camera / physics research

- stable baseline: `R3_B_DYNAMIC_PROMPTS_v1.md`
- camera calibration: `R3_B_DYNAMIC_PROMPTS_v2_CAMERA_CALIBRATION.md`
- camera matrix: `R3_B_CAMERA_CALIBRATION_MATRIX_v1.md`
- human review: `R3_B_DYNAMIC_SOURCE_HUMAN_REVIEW_v1.md`
- physics gate: `R3_B_PHYSICAL_PLAUSIBILITY_GATE_v1.md`
- open-source control research + next patch: `R3_B_OPEN_SOURCE_CONTROL_RESEARCH_AND_PATCH_PLAN_v1.md`

## v3 patch retest result

Uploaded retest batch:
- `3S02.mp4`
- `3S4.mp4`
- `3S5.mp4`
- `3S06.mp4`

### S04
`PASS ENOUGH FOR CURRENT LOOP`
- partial foreground occlusion materially improves same-scene continuity;
- keep current source;
- full occlusion remains reserved for intentional hidden transition tests.

### S05
`PASS ENOUGH FOR CURRENT LOOP`
- dry mirror + separately located rainy background window solves the major surface-ownership problem;
- keep current source.

### S02
`FAIL / RAIN PHYSICS`
- rain is still visually over-large / tube-like / spatially ambiguous;
- do not keep adding prose around droplet merging;
- next route: first-frame preload of an already-existing thin exterior rain rivulet + one simple downward track;
- freeze camera for the physics retry and use only one slow rack focus.

### S06
`FAIL / CONCEPT + OBJECT PHYSICS`
- transparent ice object is not stably established because it was not clearly present in frame 0;
- hand / face / veil / transparent object / phase-change stack is too complex;
- full new first frame is mandatory;
- next route: ice object resting on dark saucer in foreground, already wet with one visible bead; woman soft-focus background; no hand interaction; one bead detaches and falls; locked camera + one rack focus.

## Key experimental rules from retest

### FIRST-FRAME STATE PRELOAD
Any small transparent / reflective / deforming object that carries the lyric event must be clearly present in the first frame.

### ONE PHYSICS EVENT PER SOURCE
One 5s source contains at most one difficult material interaction.

### CONTROL BUDGET
For difficult physics:
- camera complexity LOW;
- one object/material event only;
- character performance LOW.

For difficult camera motion:
- simple scene physics;
- no material phase transformation.

## Current Gate / Next execution

`SHOT_LIBRARY_LOCKED = NO`

Keep without more generation:
`S01 / S03 / S04(v3) / S05(v3) / S07 / S08`

Tomorrow patch only:
`S02 / S06`

Next:
1. prepare S02 v4 first-frame state with thin exterior rivulet;
2. prepare NEW S06 v4 first frame with ice + pre-existing bead + woman background;
3. generate only S02/S06 with simplified physics/control budgets;
4. run physical plausibility QA;
5. if pass, lock shot library and enter Picture Edit / HG04.

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
→ **`TOMORROW PATCH S02 + S06 ONLY`**
