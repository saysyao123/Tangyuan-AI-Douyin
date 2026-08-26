# D02-A｜WEB Source Rough-Cut QA v2

- Batch geometry: `crop=576:1024:72:128 -> scale=720:1280 -> SAR 1:1`
- Equivalent source zoom: ~1.25x
- Applied uniformly to: S1 / S2 / S3 / S4-A / S4 / S5 / S6
- Source audio: removed from all derived proxies
- Picture timing / EDL: unchanged from Rough Cut v1
- Locked BGM: `D02-A_HG02_B_尾部1.2s柔和淡出_26.424s.mp3`
- Output duration: `26.423991s`

## Corner-risk QA

Representative frames checked across all seven timeline sources, including:
- first source / opening frame family;
- S4-A known bottom-right generator-mark risk;
- near-face S4 / S5 frames;
- final S6 release frame family.

Result:
- `NO_VISIBLE_GENERATOR_MARK = YES`
- `watermark_left_top_pass = YES`
- `watermark_right_bottom_pass = YES`
- `batch_geometry_consistent = YES`
- `SAR_1_1 = YES`
- `composition_exception = NO`
- `source_audio_removed = YES`

Gate:
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`
