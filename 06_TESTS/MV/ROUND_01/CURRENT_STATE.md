# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S06`
- STAGE_NAME: `Editing / Subtitle / Final Polish`
- STATE: `V4_FINAL_POLISH_READY_FOR_USER_REVIEW`
- PREVIOUS_LOCK: `R1S04_FIRST_FRAME_SET_LOCKED`
- BRANCH: `test/mv-round-01`
- SELECTED_REFERENCE_BGM: `你有没有真的爱过我｜阿图表妹`
- APPROVED_CLIP: `你有没有真的爱过我_建议剪辑片段_v1.mp3`
- APPROVED_DURATION: `36.80s`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked / Effective Decisions

### Simplified song-selection path｜Temporarily LOCKED
For current manual production:

`5-source MV/music observer pool -> recent ~30-day repeated-song scan -> direct MV/video links -> user judges song + visual -> choose Reference BGM`

Deeper datasource hardening (`exact music_id / Creator Center probe / account-side availability / automated preview acquisition`) is deferred to Codex-capable environment.

### Reference BGM｜LOCKED
- Song: `你有没有真的爱过我`
- Artist: `阿图表妹`
- Source supplied by user: `你有没有真的爱过我-阿图表妹.mp3`
- Source interval: `00:01:23.800 -> 00:02:00.600`
- Final clip duration: `36.80s`
- Fade in: `0.25s`
- Fade out: `1.20s`
- User review: `PASS`

### Production structure｜LOCKED
- conceptual visual units: `6`
- production segments: `8`
- first frames: `8`
- dynamic videos: `8 × 5s = 40s raw material`
- final audio: `36.80s`

### First-frame set｜LOCKED
- all eight first frames approved by user.
- same fictional East Asian heroine, dark ink-green robe, muted-gold hairpin, translucent black veil.
- new-Eastern cinematic photorealism + restrained poetic surrealism.
- every first frame is a `0-second dynamic anchor`.

### Dynamic generation｜PASS for this round
All 8 Seedance clips were generated and reviewed.

User-confirmed useful learnings:
- `S1 / S2 / S4 / S6` passed directly.
- `S3 / S5 / S7` initially triggered portrait-protection before generation; re-generation succeeded after restoring the proven AI-character declaration and multi-shot prompt grammar.
- `S8` first generation hallucinated a hole in the foreground paper; revised camera-based solid-paper occlusion solved the issue sufficiently for editing.
- three-shot 5s structures worked well and should remain part of the motion-language toolkit.
- future single-shot segments should test more cinematic camera grammars rather than default slow pushes.

### Mandatory portrait-safe prompt prefix｜HARD RULE
For every dynamic prompt containing a person, preserve the leading `***` exactly:

`*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。`

The `***` is intentionally retained as part of the prompt-weighting convention used in the validated workflow.

### Editing rounds
- `v1`: first straight trim/cut assembly — user said overall direction OK.
- `v2`: improved timing by preserving more of each 5s internal motion and compressing total duration via short overlaps / transitions — user said noticeably better and more accurate.
- `v3`: first lyric subtitle pass — timing inaccurate because captions were approximated from visual segment boundaries.
- `v3.1`: subtitle timing corrected using the locked audio source time and matching song LRC; user confirmed timing is accurate and effect is good.
- `v4`: final-polish candidate based on v3.1; no change to approved cut timing or subtitle timing, only subtle final visual fade for cleaner ending.

### Subtitle timing｜LOCKED for current song
Subtitle timing must come from the locked final audio, never inferred from visual segment boundaries.

Current relative cue starts against `01:23.800` clip start:
- `00:00.200` 你的回应是一直沉默
- `00:05.200` 只剩下落寞
- `00:08.200` 我有什么错
- `00:10.200` 短暂柔情似流星划落
- `00:15.200` 你有没有真的爱过我
- `00:20.200` 我是你诗的哪个段落
- `00:25.200` 落款第几页
- `00:28.200` 第几次临摹
- `00:30.200` 还是匆匆一瞥就略过

Future Codex production should use:
`locked final audio -> Whisper word timestamps -> known lyric constrained correction -> sentence-level subtitle timing -> human spot-check`.

Hard rule:
`subtitle timing source = final locked audio alignment`, not `video segment timing`.

## Current Files / Process References
- `R1S04_FIRST_FRAME_PROMPTS_v1.md`
- `R1S04_LOCK.md`
- `R1S05_DYNAMIC_PROMPTS_v1.md`
- `R1S05_DYNAMIC_PROMPTS_v2_PORTRAIT_SAFE.md`
- `R1S06_SUBTITLE_ALIGNMENT_RULE.md`

## Benchmark / Observer System
- Song observer pool: `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- Rolling MV benchmark: `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

## Current Risks / Pending
- `v4` final-polish candidate still needs user review.
- exact Douyin `music_id` pending Codex hardening test.
- account-side publish availability pending pre-publish validation.
- cinematic camera-motion library still needs dedicated future experiments and benchmarking.

## Next Allowed Action

User review of `R1_MV_v4_final_polish.mp4`.

If PASS:
1. lock this R1 edit as the accepted Golden Sample candidate;
2. create a structured Round 01 retrospective;
3. extract reusable rules into the MV SOP / runtime knowledge layer;
4. separately plan camera-grammar experiments for later rounds.
