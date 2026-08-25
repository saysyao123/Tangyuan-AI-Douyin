# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-C / FINAL CANDIDATE READY / HG05 PENDING`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_COMPLETE_FOR_CURRENT_LOOP / PHYSICAL_PLAUSIBILITY_ITERATION_COMPLETE / DOUBAO_PROMPT_REWRITE_VALIDATED / FINAL_MATERIAL_REVIEW_COMPLETE / WEB_SOURCE_ROUGH_CUT_GATE_PASS / HG04_PASS / PICTURE_EDIT_LOCKED / SUBTITLE_STYLE_QA_PASS / SUBTITLE_IMPLEMENTATION_QA_PASS / FINAL_TECH_QA_PASS / DELIVERABLE_RENDERED / HG05_PENDING`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

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

## R3-B material / learning lock

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

## WEB Source Rough-Cut Gate

Authoritative rule:
`04_HARNESS/rules/mv_web_source_roughcut.md`

R2 validated WEB baseline restored and applied:
`crop=576:1024:72:128 -> scale=720:1280`
= approx `1.25×` whole-source zoom.

Current artifacts:
- `R3_C_WEB_SOURCE_ROUGH_CUT_MAP_v1.csv`
- `R3_C_WEB_SOURCE_ROUGH_CUT_QA_v1.md`

Result:
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`

All final WEB edit sources:
- use one batch geometry;
- preserve raw source separately;
- source audio removed in clean proxy;
- 720×1280 / 24fps / SAR1:1;
- no visible top-left / bottom-right generator mark in reviewed risk samples.

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

## Subtitle implementation

Authority:
`04_HARNESS/rules/mv_subtitle.md`

Artifact:
`R3_C_SUBTITLE_IMPLEMENTATION_QA_v1.md`

Baseline applied:
- Noto Sans CJK SC Bold;
- nominal 46px;
- near-white text;
- dark semi-transparent rounded box;
- subtitle center approx `(360,1009)`;
- 10px padding on all four sides;
- 100ms fade-in / 180ms fade-out;
- no karaoke;
- exact Stage 2A SRT timings unchanged.

All 8 lines:
- actual glyph bbox -> fresh rounded box;
- L/R/T/B = `10/10/10/10px`;
- text/box center geometry error = `0px` in generated overlay specification;
- no timing nudge;
- no overflow / critical eye obstruction in reviewed samples.

`SUBTITLE_STYLE_QA_PASS = YES`
`SUBTITLE_IMPLEMENTATION_QA_PASS = YES`

## Final Candidate / Final Tech QA

Final candidate:
`如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`

SHA-256:
`b96ddb81395772395ed8946b3fc30341f124bef14124f47a203dda87a3ef9f42`

Technical:
- H.264 video;
- `720×1280`;
- `24fps`;
- `SAR=1:1`;
- video/container duration `24.333333s` (24fps frame-quantized tail around 24.32s target);
- AAC locked production audio;
- final audio vs clean Picture Edit decoded PCM correlation = `1.000000`;
- no AI source-audio leakage;
- no black interval >= 0.08s under QA threshold;
- final watermark regression samples PASS;
- subtitle geometry/timing QA PASS.

Artifact:
`R3_C_FINAL_TECH_QA_v1.md`

`FINAL_TECH_QA_PASS = YES`
`DELIVERABLE_RENDERED = YES`

## Current Gate / Next execution

Current Gate:
**`HG05 Final Acceptance Gate`**

User should review only the final candidate as a finished MV:
- overall emotional flow;
- subtitle feel/readability;
- final crop/composition after WEB rough-cut;
- transitions and release ending;
- whether any remaining visual artifact is still noticeable at normal playback speed.

If PASS:
→ create HG05 receipt
→ Stage 11 Close / retrospective / reusable-rule promotion audit.

If patch needed:
→ patch only the nearest implementation layer; do not cascade into BGM / Audio Timeline / accepted Director work unless the defect proves an upstream root cause.

## State chain

`HG01 PASS`
→ `BGM LOCKED`
→ `AUDIO TIMELINE LOCKED`
→ `HG03 PASS`
→ `FIRST FRAME SET LOCKED`
→ `CAMERA / PHYSICS ITERATION COMPLETE`
→ `DOUBAO PROMPT REWRITE VALIDATED`
→ `FINAL MATERIAL REVIEW COMPLETE`
→ `WEB SOURCE ROUGH-CUT GATE PASS`
→ `HG04 PASS`
→ `PICTURE EDIT LOCKED`
→ `SUBTITLE IMPLEMENTATION QA PASS`
→ `FINAL TECH QA PASS`
→ `DELIVERABLE RENDERED`
→ **`HG05 PENDING`**
