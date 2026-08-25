# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-B / FINAL MATERIAL REVIEW + PROMPT REWRITE VALIDATION COMPLETE`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_BATCH_GENERATED / HUMAN_REVIEW_COMPLETE / PHYSICAL_PLAUSIBILITY_GATE_READY / V3_PATCH_RETEST_REVIEWED / S04_PASS / S05_PASS / S02_S06_V4_RETEST_GENERATED / FINAL_MATERIAL_REVIEW_COMPLETE / DOUBAO_PROMPT_REWRITE_VALIDATED / EDIT_CANDIDATE_READY`
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

## Final source pool mapping

Use content mapping for edit:
- S01 = `3S1.mp4`
- S02 = `3S6.mp4` (rain window)
- S03 = `3S3.mp4`
- S04 = `3S4(1).mp4`
- S05 = `3S5(1).mp4`
- S06 = `3S2.mp4` (ice foreground)
- S07 = `3S7.mp4`
- S08 = `3S8.mp4`

Important: uploaded filenames `3S2` and `3S6` are opposite to lyric segment content; editor must follow the mapping above.

All 8 sources: 720x1280 / 24fps / 121 frames / container ≈5.088s / AAC source audio present.
`SOURCE_AUDIO = REMOVE`.

## Material review

Canonical report:
`R3_B_FINAL_MATERIAL_REVIEW_AND_REUSABLE_LESSONS_v1.md`

Decision:
- no further generation required before first picture-edit test;
- use selective clean windows rather than full 5s clips;
- S04 foreground occlusion should be used as a motivated transition/cut point rather than demanding same-scene recovery;
- S08 remains current world-opening release benchmark.

`MATERIAL_REVIEW_COMPLETE = YES`
`EDIT_CANDIDATE_READY = YES`
`FINAL_SHOT_LIBRARY_GOLDEN = NO`

## Doubao prompt rewrite validation

Canonical report:
`R3_B_DOUBAO_PROMPT_REWRITE_VALIDATION_v1.md`

User rewrote S02/S06 prompts directly in Doubao and regenerated two 5s tests.

Observed result:
- overall outputs are materially more usable;
- liquid behavior is still not perfectly controlled: rain can still thicken into a tube-like vertical trace, and ice-water separation can still elongate unnaturally;
- improvement comes mainly from **containing and de-emphasizing** the fluid event rather than solving exact fluid simulation.

Validated R3 prompt-structure candidates:
- front-load only the highest-value hard constraints;
- `STATIC BASE -> ONE ALLOWED EVENT`;
- freeze all non-target liquid/material elements;
- use weak / low-amplitude action language for high-risk materials;
- quantify direction / distance / local area;
- serialize tasks: `PHYSICS EVENT -> END -> RACK FOCUS/CAMERA -> CHARACTER RESIDUE`;
- avoid concurrent liquid physics + camera/focus changes;
- `QUANTIFIED LOCAL CHANGE > VAGUE MATERIAL LANGUAGE`.

Important epistemic boundary:
- treat front-loaded constraints as an empirical Doubao/Seedance heuristic from this R3 test;
- do not claim as universal architecture fact that prompt order numerically controls model weight or that all negative prompts are inherently lower priority.

## Reusable experimental lessons

Active R3 evidence candidates:
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
- same-scene continuity -> partial foreground occlusion;
- full/near-full occlusion -> intentional hidden transition / edit point.

Rain strategy candidate:
- default rain = atmospheric texture, wet-glass sheen, distant streaks, bokeh/reflection;
- pre-existing single surface-bound track only when narratively necessary;
- droplet birth/merge/macro fluid transformation is R&D-only by default.

## Camera-language evidence

Positive evidence:
- S03: mild `SLOW DOLLY-OUT REVEAL`
- S04: foreground reveal / occlusion as transition grammar
- S08: `WORLD-OPENING CRANE / RETREAT` benchmark

Useful but not yet validated precisely:
- S01 close-face dolly-in (tends to over-amplify)
- S07 rack focus + mild reframe
- small slider/orbit grammars from earlier rounds

Future camera testing should be controlled series tests, one camera variable at a time, without difficult physics in the same source.

## Current Gate / Next execution

Current state:
`AWAITING HUMAN ACCEPTANCE -> PICTURE EDIT / HG04`

After approval:
1. build first Picture Edit candidate from locked BGM + lyric timeline;
2. use report-recommended source windows as starting ranges, not rigid final cuts;
3. remove all source audio;
4. exploit S04 occlusion as motivated edit if rhythm supports it;
5. preserve S08 continuous release as much as possible;
6. trim around any remaining visually loud liquid-artifact frames rather than forcing liquid physics to read;
7. run HG04 on picture rhythm / lyric fit / flow;
8. only after HG04 proceed to subtitle/final polish.

## State chain

`HG01 PASS`
→ `BGM LOCKED`
→ `AUDIO TIMELINE LOCKED`
→ `HG03 PASS`
→ `FIRST FRAME SET LOCKED`
→ `CAMERA CALIBRATION GENERATED`
→ `PHYSICAL PLAUSIBILITY ITERATION`
→ `S04/S05 PATCH PASS`
→ `S02/S06 V4 RETEST`
→ `FINAL MATERIAL REVIEW COMPLETE`
→ `DOUBAO PROMPT REWRITE VALIDATED`
→ **`AWAIT HUMAN ACCEPTANCE -> PICTURE EDIT / HG04`**
