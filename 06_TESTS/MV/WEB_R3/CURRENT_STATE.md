# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-C / WEB SOURCE ROUGH-CUT GATE PASS -> SUBTITLE INTEGRATION`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_COMPLETE_FOR_CURRENT_LOOP / PHYSICAL_PLAUSIBILITY_ITERATION_COMPLETE / DOUBAO_PROMPT_REWRITE_VALIDATED / FINAL_MATERIAL_REVIEW_COMPLETE / WEB_SOURCE_ROUGH_CUT_GATE_PASS / PICTURE_EDIT_CLEAN_REGRESSION_READY / HG04_PASS / PICTURE_EDIT_LOCKED`
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

## R2 WEB Source Rough-Cut Gate restored

User identified that R3 had incorrectly deferred watermark/source rough-cut handling until after HG04. R2 already promoted this as a WEB technical Gate.

Authoritative rule:
`04_HARNESS/rules/mv_web_source_roughcut.md`

R2 validated WEB geometry restored:
`crop=576:1024:72:128 -> scale=720:1280`
= approx `1.25×` whole-source zoom.

Hard WEB behavior:
- all final edit sources get the same batch geometry;
- no per-shot local watermark hiding by default;
- derived proxy only; raw sources preserved;
- source audio physically removed;
- 720×1280 / 24fps / SAR1:1;
- left-top + right-bottom worst-case corner QA before Picture Edit;
- any visible generator mark => Gate FAIL.

Current R3 artifacts:
- `R3_C_WEB_SOURCE_ROUGH_CUT_MAP_v1.csv`
- `R3_C_WEB_SOURCE_ROUGH_CUT_QA_v1.md`

Current result:
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`

Eight clean WEB proxies were generated from the final source pool. Reviewed proxy samples show no visible top-left / bottom-right generator marks.

## Picture Edit clean regression

Canonical EDL remains:
`R3_C_PICTURE_EDIT_V1_EDL.md`

The same accepted edit points were re-rendered using only the WEB rough-cut clean proxies.

Clean regression preview:
`如果风会替我说话_R3_PictureEdit_v1_WEB_RoughCutClean.mp4`

Final edit timing intent remains unchanged:
- S01 final 0–3s from source `0.15–3.15`
- S02 final 3–6s from latest rain source `2.00–5.00`
- S03 final 6–8s from source `0.60–2.60`
- S04 final 8–12s from source `0.20–4.20`
- S05 final 12–15s from source `0.30–3.30`
- S06 final 15–18s from latest ice source `2.00–5.00`
- S07 final 18–20s from source `0.80–2.80`
- S08 final 20–24.32s from source `0.40–4.72`

Technical clean preview:
- 720×1280
- 24fps
- SAR1:1
- locked BGM only
- container/frame-quantized duration ≈ `24.333333s`
- SHA-256 `70d066ca4466e72bd5876fc83b3e3c0328ac412a9eccb9e94fe566dc8cc3089a`

## HG04

Human Gate receipt:
`R3_C_HG04_PICTURE_EDIT_LOCK_v1.md`

User accepted:
- overall picture effect;
- rhythm;
- musical hit/cut-point feeling.

R2 Gate retrofit decision:
- preserve `HG04_PASS` because edit points/timing were not changed;
- previous raw-source preview is superseded by clean-proxy regression implementation;
- only reopen HG04 if the uniform crop is later judged to materially damage composition/rhythm.

`HG04_PASS = YES`
`PICTURE_EDIT_LOCKED = YES`

## Current Gate / Next execution

Current state:
`SUBTITLE INTEGRATION / FINAL VISUAL QA`

Next:
1. use clean-proxy Picture Edit as the only picture baseline;
2. integrate subtitles from Stage 2A exact SRT / locked subtitle baseline;
3. run subtitle geometry / safe-area / readability QA;
4. verify no source-audio leakage;
5. verify watermark consistency again in final render;
6. export final candidate;
7. run HG05 final acceptance.

## State chain

`HG01 PASS`
→ `BGM LOCKED`
→ `AUDIO TIMELINE LOCKED`
→ `HG03 PASS`
→ `FIRST FRAME SET LOCKED`
→ `CAMERA / PHYSICS ITERATION COMPLETE FOR CURRENT LOOP`
→ `DOUBAO PROMPT REWRITE VALIDATED`
→ `FINAL MATERIAL REVIEW COMPLETE`
→ **`WEB SOURCE ROUGH-CUT GATE PASS`**
→ `PICTURE EDIT CLEAN REGRESSION`
→ `HG04 PASS`
→ `PICTURE EDIT LOCKED`
→ **`SUBTITLE INTEGRATION / FINAL VISUAL QA`**
