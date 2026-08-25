# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-C CLOSED / R3-D NEXT`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / R3_A_PASS / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / R3_B_CURRENT_CALIBRATION_PASS / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_COMPLETE_FOR_CURRENT_LOOP / PHYSICAL_PLAUSIBILITY_ITERATION_COMPLETE / DOUBAO_PROMPT_REWRITE_VALIDATED / FINAL_MATERIAL_REVIEW_COMPLETE / WEB_SOURCE_ROUGH_CUT_GATE_PASS / HG04_PASS / PICTURE_EDIT_LOCKED / SUBTITLE_STYLE_QA_PASS / SUBTITLE_IMPLEMENTATION_QA_PASS / FINAL_TECH_QA_PASS / DELIVERABLE_RENDERED / HG05_PASS / R3_C_FULL_MV_INTEGRATION_PASS / RETROSPECTIVE_COMPLETE / R3_D_NOT_STARTED`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

## Program-level status

Original R3 modules:
- `R3-A Music Radar / Benchmark Calibration = PASS`
- `R3-B Healing Visual Calibration = PASS FOR CURRENT CALIBRATION`
- `R3-C Full MV Integration = PASS / HG05`
- `R3-D Publish Packaging + Live Data Feedback = NOT STARTED`

Therefore:
`R3_PROGRAM_COMPLETE = NO`

Do not mark the whole R3 program `COMPLETE_LOCKED` until R3-D is executed or explicitly cancelled by user decision.

## Locked Audio

Song family: `如果风会替我说话`
Locked BGM: `如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`
Duration target: `24.320000s`
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

Canonical timing source:
`AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`

## R3-A result

Current Data Center mode:
`PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`

Current calibrated snapshot:
- 9 core accounts;
- 134 cumulative observed works;
- 98 AUTO_HIGH works;
- 8 repeated SONG_FAMILY candidates;
- missing observations = UNKNOWN, not negative evidence.

Current production song was selected from direct multi-account Douyin evidence and then verified to exact Douyin music asset before HG02.

## R3-B reusable learning status

Canonical R3 evidence:
- `R3_B_FINAL_MATERIAL_REVIEW_AND_REUSABLE_LESSONS_v1.md`
- `R3_B_DOUBAO_PROMPT_REWRITE_VALIDATION_v1.md`
- `R3_B_PHYSICAL_PLAUSIBILITY_GATE_v1.md`

JIT reusable Knowledge created:
- `04_HARNESS/knowledge/MV_DYNAMIC_GENERATION_R3_LESSONS.md`
- `04_HARNESS/knowledge/MV_CAMERA_LIBRARY_CANDIDATES.md`

Current Knowledge candidates include:
- `TRIM BEFORE REGENERATE`
- `WEAKEST SUFFICIENT MOTION`
- `FIRST-FRAME STATE PRELOAD`
- `STATIC BASE -> ONE ALLOWED EVENT`
- `ONE DIFFICULT PHYSICS EVENT PER SOURCE`
- `CONTROL BUDGET`
- `SURFACE OWNERSHIP`
- `PHYSICALLY BELIEVABLE > VISUALLY LOUD`
- `WEAK VERB FOR HIGH-RISK MATERIALS`
- `SERIALIZE PHYSICS AND FOCUS/CAMERA`
- `FREEZE NON-TARGET MATERIAL FIELD`
- rain-as-atmosphere candidate;
- partial occlusion for continuity / near-full occlusion for motivated hidden cut.

These are `POSITIVE_EVIDENCE / KNOWLEDGE`, not universal hard rules until cross-song replication.

Camera positive evidence:
- S03 mild `SLOW DOLLY-OUT REVEAL`;
- S04 foreground partial reveal / occlusion;
- S04 near-full occlusion as motivated edit point;
- S06/S07 rack-focus semantic transfer;
- S08 `WORLD-OPENING CRANE / RETREAT` benchmark.

Specific camera recipes are not yet promoted to Golden Runtime.

## WEB Source Rough-Cut Gate

Authoritative rule:
`04_HARNESS/rules/mv_web_source_roughcut.md`

R2 validated WEB baseline restored and applied:
`crop=576:1024:72:128 -> scale=720:1280`
= approx `1.25×` whole-source zoom.

Current artifacts:
- `R3_C_WEB_SOURCE_ROUGH_CUT_MAP_v1.csv`
- `R3_C_WEB_SOURCE_ROUGH_CUT_QA_v1.md`

`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`

This Gate is now mandatory before WEB Picture Edit and may not be deferred to final polish.

## Picture Edit / HG04

Canonical EDL:
`R3_C_PICTURE_EDIT_V1_EDL.md`

Clean Picture Edit baseline:
`如果风会替我说话_R3_PictureEdit_v1_WEB_RoughCutClean.mp4`

Locked edit intent:
- S01 `0.15–3.15`
- S02 latest rain source `2.00–5.00`
- S03 `0.60–2.60`
- S04 `0.20–4.20`
- S05 `0.30–3.30`
- S06 latest ice source `2.00–5.00`
- S07 `0.80–2.80`
- S08 `0.40–4.72`

User accepted:
- overall picture effect;
- rhythm;
- musical hit/cut-point feeling.

`HG04_PASS = YES`
`PICTURE_EDIT_LOCKED = YES`

## Subtitle / Final Tech

Subtitle artifact:
`R3_C_SUBTITLE_IMPLEMENTATION_QA_v1.md`

Final technical artifact:
`R3_C_FINAL_TECH_QA_v1.md`

Subtitle result:
- exact Stage 2A SRT unchanged;
- R1/WEB R2 visual baseline reused;
- glyph bbox -> fresh rounded box;
- 10px four-side padding;
- geometry/timing QA PASS.

`SUBTITLE_STYLE_QA_PASS = YES`
`SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
`FINAL_TECH_QA_PASS = YES`

## Final Accepted MV / HG05

Final accepted candidate:
`如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`

SHA-256:
`b96ddb81395772395ed8946b3fc30341f124bef14124f47a203dda87a3ef9f42`

Technical:
- H.264;
- 720×1280;
- 24fps;
- SAR1:1;
- video/container ≈24.333333s;
- approved locked BGM only;
- no AI source-audio leakage;
- watermark consistency PASS;
- subtitle timing/geometry PASS.

HG05 receipt:
`R3_C_HG05_FINAL_ACCEPTANCE_v1.md`

User final review:
- final effect is good;
- final-stage implementation was essentially accepted in one pass;
- no upstream redesign requested.

`HG05_PASS = YES`
`R3_C_FULL_MV_INTEGRATION_PASS = YES`

## Retrospective / Promotion Audit

Canonical closeout analysis:
`R3_RETROSPECTIVE_AND_PROMOTION_AUDIT_v1.md`

Key promotion boundary:
- mature correctness / implementation discipline stays in Runtime Rules;
- single-song dynamic/physics/camera findings go to Knowledge and require cross-song validation;
- per-song visual recipes / failed prompts remain R3 evidence only;
- publish/growth conclusions remain unvalidated until R3-D real-data loop.

## Main branch status

At closeout audit:
- `test/mv-web-r3` = 434 commits ahead of `main`;
- 0 behind.

Do not blindly merge the entire test branch.
Use a curated production promotion path for Harness runtime / rules / templates / selected tools / knowledge, while keeping probe history and failed experiments in `06_TESTS`.

## Next execution

Default next stage from the original R3 charter:

### `R3-D1 Packaging Benchmark`
Produce two controlled candidates:
- `MUSIC_FIRST`
- `EMOTION_FIRST`

Then select one for actual publication.

### `R3-D2 Live Data Feedback`
After publication, record performance evidence and decide what packaging / radar / visual signals deserve further promotion.

Parallel next-song R&D goal:
- reuse selected R3 dynamic-generation Knowledge hypotheses;
- repeat camera candidate tests in a different song/world;
- only then promote cross-song stable items into active Rules.

## State chain

`R3-A PASS`
→ `HG01 PASS`
→ `BGM LOCKED`
→ `AUDIO TIMELINE LOCKED`
→ `R3-B CURRENT CALIBRATION PASS`
→ `HG03 PASS`
→ `FIRST FRAME SET LOCKED`
→ `DYNAMIC / CAMERA / PHYSICS ITERATION COMPLETE`
→ `WEB SOURCE ROUGH-CUT GATE PASS`
→ `HG04 PASS`
→ `PICTURE EDIT LOCKED`
→ `SUBTITLE IMPLEMENTATION QA PASS`
→ `FINAL TECH QA PASS`
→ `HG05 PASS`
→ **`R3-C CLOSED`**
→ **`R3-D NOT STARTED / NEXT`**
