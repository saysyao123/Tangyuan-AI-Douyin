# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W07`
- STAGE_NAME: `Full dynamic QA / trim planning`
- STATE: `VISUAL_BATCH_PASS_WITH_TRIM / W08_READY`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- FULL_BATCH_QA: `06_TESTS/MV/WEB_R2/W07_FULL_BATCH_QA_v1.md`
- DIRECTOR_SELECTOR: `06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked Results

- W00: `AUTO / LOCKED`
- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `PARTIAL / LOCKED` — BGM `139.930s–177.050s`, rendered `37.120s`
- W03: `AUTO / LOCKED` — six Natural Beats
- W04: `HUMAN_GATE / PASSED` — `树影之外`
- W05: `HUMAN_GATE / PASSED` — first frames `9/9`
- W06: `AUTO / EXPERIMENTAL` — dynamic prompt set / Director Selector tested
- W06-X: `EXTERNAL_REQUIRED / COMPLETED FOR CURRENT BATCH` — all 9 raw Seedance clips returned

## W07 Full Batch Result

All nine returned clips are ~`5.04s / 720×1280 / 24fps`.

Batch verdict:
`VISUAL_BATCH_PASS_WITH_TRIM / NO FULL-BATCH REGEN REQUIRED`.

Actual directing mix:
- S1 multi-shot
- S2 one-take Arc
- S3 2-shot
- S4 3-shot
- S5 one-take breathing shot
- S6 3-shot discovery
- S7 multi-shot motion peak
- S8 one-take rooftop reset
- S9 one-take cloud release

This confirms the correct direction is **mixed shot structures chosen per lyric task**, not a universal one-take or 3–5-shot template.

## Per-clip status

- `S1 = SOURCE_USABLE / TRIM_REQUIRED`
  - strong wide → low-angle → eye → canopy progression;
  - two similar middle low-angle fragments should not both survive final edit.
- `S2 = PASS_FULL / POSITIVE ONE-TAKE SAMPLE`
  - orbit/parallax remains a benchmark success.
- `S3 = PASS_FULL`
  - useful emotional close-up → medium contrast.
- `S4 = PASS_FULL / STRONG DYNAMIC SAMPLE`
  - strong multi-shot body/fabric movement with clear adjacent-shot contrast.
- `S5 = PASS_FULL / BREATHING SHOT`
  - strong scale reset; shorten if S1 opening already runs long.
- `S6 = PASS_FULL / STRONG LYRIC-HIT SAMPLE`
  - person → bird → person reads clearly; bird hold may be slightly shortened.
- `S7 = SOURCE_USABLE / TRIM_REQUIRED / REGEN_WATCH`
  - early motion peak is strong;
  - ~2.8–4.0s pale fabric becomes topology-ambiguous / visually over-dominant;
  - first try trim, regenerate only if final edit lacks enough clean peak duration.
- `S8 = PASS_FULL / SHORTEN IN SEQUENCE`
  - useful rooftop reset but visually overlaps S9.
- `S9 = PASS_FULL / FINAL RELEASE`
  - prioritize as the longer final hold.

## Whole-set repetition risks

1. S1 middle: adjacent low-angle character fragments repeat.
2. S1 vs S5: both use giant tree + light shaft + small person; do not give both long screen time.
3. S8 vs S9: strongest whole-set repetition; shorten S8 and reserve longer release for S9.

## Audio HARD status

All 9 returned MP4s contain AAC source audio.

Therefore all are `SOURCE_AUDIO_PRESENT` regardless of visual pass.

Workflow consequence:
- strip/detach all Seedance source audio at ingest;
- W02 locked song master is the only music truth;
- AI source audio never drives beat or subtitle timing;
- prompt-level Source Audio hard rule remains active, but visual material is not rejected solely because Seedance ignored the audio request.

## Watermark status

All returned clips visibly include a lower-right `豆包AI生成` platform mark.

W08 must remove/cover/inpaint it consistently across all retained fragments before final delivery.

## Next Allowed Action

Enter W08 automatically:
1. strip all source audio;
2. map clean usable windows from S1–S9;
3. build the 37.120s edit against the locked BGM;
4. trim repeated / topology-risk frames;
5. remove platform marks;
6. generate subtitles from verified locked-audio evidence only;
7. only if the cut exposes insufficient peak coverage, regenerate S7 surgically.
