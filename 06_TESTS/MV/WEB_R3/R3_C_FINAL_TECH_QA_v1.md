# WEB R3｜Final Technical QA v1

Status: `PASS / HG05 CANDIDATE READY`
Song: `如果风会替我说话`
Date: `2026-08-25 Asia/Shanghai`

## Final candidate

File:
`如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`

SHA-256:
`b96ddb81395772395ed8946b3fc30341f124bef14124f47a203dda87a3ef9f42`

## Video technical identity

- codec: H.264
- resolution: `720×1280`
- fps: `24`
- SAR: `1:1`
- aspect: `9:16`
- video duration: `24.333333s`
- container duration: `24.333333s`
- no detected black interval >= 0.08s under blackdetect threshold used for QA

## Audio

- codec: AAC
- audio duration: `24.286009s`
- source: approved clean Picture Edit / locked production BGM only
- decoded audio correlation vs clean Picture Edit: `1.000000`
- decoded audio correlation vs locked BGM reference: `0.998553` (expected lossy AAC/MP3 encode-domain difference)
- no AI generated source-audio stream added during subtitle render

`SOURCE_AUDIO_LEAKAGE = NO`

## Watermark / WEB rough-cut regression

Authority:
`R3_C_WEB_SOURCE_ROUGH_CUT_QA_v1.md`

Final candidate derives only from WEB clean proxy Picture Edit.
Representative final frames at:
`1.5 / 4.5 / 7.0 / 10.0 / 13.5 / 16.5 / 19.0 / 22.0 / 24.15s`
were visually reviewed.

Observed:
- no visible top-left generator mark;
- no visible bottom-right generator mark;
- no mixed watermark state;
- no stretch caused by WEB crop;
- S08 final release remains compositionally readable.

`WATERMARK_HANDLING_CONSISTENCY = PASS`

## Subtitle

Authority:
`R3_C_SUBTITLE_IMPLEMENTATION_QA_v1.md`

- canonical exact SRT used unchanged;
- all 8 lines implemented;
- all event boundaries exact at 24fps whole-frame boundaries;
- font/position baseline inherited from R1/WEB R2;
- per-line box regenerated from actual rendered glyph bbox;
- L/R/T/B padding = `10/10/10/10px` on all 8 lines;
- text/box center error = `0px` in generated overlay geometry;
- no overflow / critical-face obstruction in reviewed samples;
- final subtitle ends at `24.000s`, leaving the final visual tail clean.

`SUBTITLE_IMPLEMENTATION_QA_PASS = YES`

## Picture / rhythm preservation

No Edit Map / cut-point redesign was performed after HG04.
The final candidate uses the same approved Picture Edit timing and only adds the locked subtitle layer on top of the clean WEB rough-cut regression picture.

Therefore:
`HG04_RHYTHM_EVIDENCE_PRESERVED = YES`

## Gate result

`FINAL_TECH_QA_PASS = YES`
`DELIVERABLE_RENDERED = YES`
`HG05_FINAL_ACCEPTANCE_PENDING = YES`

No upstream Gate is reopened.