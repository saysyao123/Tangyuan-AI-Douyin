# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1_FINAL`
- STAGE_NAME: `Round Close / Golden Sample Lock`
- STATE: `COMPLETE_LOCKED`
- PREVIOUS_LOCK: `R1S04_FIRST_FRAME_SET_LOCKED`
- FINAL_LOCK: `06_TESTS/MV/ROUND_01/R1_FINAL_LOCK.md`
- FINAL_ACCEPTANCE: `06_TESTS/MV/ROUND_01/R1_FINAL_ACCEPTANCE.md`
- RETROSPECTIVE: `06_TESTS/MV/ROUND_01/R1_RETROSPECTIVE.md`
- BRANCH: `test/mv-round-01`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Golden Sample

- Song: `你有没有真的爱过我｜阿图表妹`
- User-supplied source: `你有没有真的爱过我-阿图表妹.mp3`
- Locked source interval: `00:01:23.800 -> 00:02:00.600`
- Locked reference duration: `36.80s`
- Final accepted edit family: `R1_MV_v4_final_polish.mp4`
- Accurate lyric timing: `lyrics_exact_v3_1.srt`
- Production structure: `8 first frames + 8 × 5s dynamic clips`
- User final review: `PASS / 整体效果不错`

This is the first MV Golden Sample.

## Stable R1 Decisions

### 1. Manual song-selection path
Until Codex datasource hardening is complete:

`~5 MV/music observer sources -> recent ~30-day song scan -> direct real MV/video links -> user chooses Reference BGM`

Do not block manual production on exact `music_id` automation.

### 2. Reference BGM lock
Actual approved audio excerpt must be locked before downstream work. No silent version swap.

### 3. First frame
Every first frame is a `0-second dynamic anchor`, not a static poster.

### 4. Production segmentation
Conceptual visual units and production segments are separate decisions.

R1 validated one working example:
`6 conceptual units -> 8 first frames -> 8 × 5s raw video -> 36.8s final`

This is a reference, not a universal quota.

### 5. Character image-to-video prefix｜HARD RULE
For every character-containing image-to-video prompt, the first line must be exactly:

`*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。`

The leading `***` must remain.

Authoritative rule source:
`04_HARNESS/rules/ai_video.md`

### 6. Dynamic camera / shot structure
- single-shot remains valid;
- 2–3 shot grammar inside a 5s clip is R1-validated and useful for selected emotional / reflection / macro segments;
- do not force one structure across every segment;
- camera repetition must be reviewed across the whole set.

A larger cinematic camera library remains experimental for R2.

### 7. Dynamic retry
Diagnose root cause first.

R1 example:
- paper occlusion generated a hole;
- fix was not “stronger negative words” alone;
- change the physical mechanism to camera-driven occlusion behind a solid intact paper edge.

### 8. Editing
R1 v2 proved better than simple equal trimming:
- preserve more complete internal 5s action;
- use selective trim + short overlap / transition to fit the locked audio;
- emotional flow and action integrity before mechanical equal timing.

### 9. Subtitle timing｜HARD RULE
Subtitle / lyric timing must come from the locked audio, not visual segment boundaries.

Codex preferred automation:
`Whisper word timestamps -> known lyric constraint correction -> human spot-check`

R1 corrected same-version timing was user-reviewed as accurate.

### 10. Watermark / HD sources
Manual R1 files may contain visible generation/platform watermarks.

This does NOT block R1 acceptance.

Codex production must replace them with watermark-free HD source outputs before a publish-grade render while preserving approved edit timing / subtitles / directing.

Status: `DEFERRED_TO_CODEX_SOURCE_PIPELINE`

## Runtime Promotion

MV SOP v1:
`04_HARNESS/workflows/mv.md`

AI video hard rules:
`04_HARNESS/rules/ai_video.md`

Benchmark knowledge:
`04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

Pending experiments:
`03_DATA/EXPERIMENTS.md`

## Known limitations from R1

- precise wall-clock / active-human / model-wait time was not consistently logged; do not invent retrospective numbers;
- exact music_id / Creator Center availability remains Codex hardening work;
- watermark-free HD source replacement not run in this manual environment;
- Whisper word-level automation not run here;
- advanced lyric effects not calibrated;
- larger single-shot cinematic camera library not yet validated.

## Next Allowed Action

**Do not continue mutating R1 creative output.**

Only two valid next paths:

1. Start `ROUND_02` using R1 Golden Sample as the quality floor; or
2. Run a named Codex hardening task for datasource / Whisper / watermark-free HD source replacement / automated edit recreation, explicitly preserving the R1 Golden creative decisions.

R1 is closed.