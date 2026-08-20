# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S04`
- STAGE_NAME: `First-frame Prompt Planning`
- STATE: `READY_FOR_FIRST_FRAME_PROMPT_REVIEW`
- PREVIOUS_LOCK: `R1S02_REFERENCE_BGM_CLIP_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- R1S02_LOCK: `06_TESTS/MV/ROUND_01/R1S02_LOCK.md`
- SELECTED_REFERENCE_BGM: `你有没有真的爱过我｜阿图表妹`
- APPROVED_CLIP: `你有没有真的爱过我_建议剪辑片段_v1.mp3`
- APPROVED_DURATION: `36.80s`
- FIRST_FRAME_PROMPTS: `06_TESTS/MV/ROUND_01/R1S04_FIRST_FRAME_PROMPTS_v1.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked / Effective Decisions

### Simplified song-selection path｜Temporarily LOCKED
For current manual production:

`5-source MV/music observer pool -> recent ~30-day repeated-song scan -> direct MV/video links -> user judges song + visual -> choose Reference BGM`

The deeper datasource path (`exact music_id / Creator Center probe / account-side availability / automated preview acquisition`) is deferred to the Codex-capable computer for later hardening.

### Locked Reference BGM
- Song: `你有没有真的爱过我`
- Artist: `阿图表妹`
- Source supplied by user: `你有没有真的爱过我-阿图表妹.mp3`
- Exact source interval: `00:01:23.800 -> 00:02:00.600`
- Final clip duration: `36.80s`
- Fade in: `0.25s`
- Fade out: `1.20s`
- User review: `PASS`

All later Beat timing, director design, first frames, Seedance prompts and final editing must use this exact clip. No silent version swap.

### Production Structure｜Approved
- conceptual visual units: `6`
- production segments: `8`
- first frames: `8`
- dynamic videos: `8 × 5s = 40s raw material`
- final reference audio: `36.80s`
- edit headroom: approximately `3.20s`

This is sufficient for complete coverage while preserving trim / transition / lyric-sync headroom.

### 8 Production Segments
- S1: `你的回应是一直沉默` — opening hook / no response.
- S2: `只剩下落寞` — empty-space loneliness.
- S3: `我有什么错` — self-question / reflection.
- S4: `短暂柔情似流星划落` — first large visual event.
- S5: `你有没有真的爱过我` — emotional core.
- S6: `我是你诗的哪个段落` — poetic spatial metaphor.
- S7: `落款第几页 / 第几次临摹` — trace / repetition / detail.
- S8: `还是匆匆一瞥就略过` — cold ending / negative space.

### First-frame System v1
Full prompts are stored in:
`06_TESTS/MV/ROUND_01/R1S04_FIRST_FRAME_PROMPTS_v1.md`

Global identity / world lock:
- same original fictional East Asian woman across all character frames;
- straight black hair in a low loose knot;
- one old muted-gold hairpin;
- dark ink-green long robe with restrained dull-gold details;
- translucent black veil always covers nose, mouth and lower face;
- new-Eastern cinematic photorealism + restrained poetic surrealism;
- cool ink-black / blue-gray / dark-green palette, old-paper ivory and tiny muted-gold highlights;
- no readable text / subtitles / logo / watermark;
- no second human in this R1 set;
- every first frame must function as a `0-second dynamic anchor`, with the next physical action already visible.

Primary style anchors for first review:
- `S1`: paper / ink / silence Hook;
- `S5`: character emotional close-up;
- `S6`: poetic paper-space metaphor.

## Current Benchmark / Observer System
- Song observer pool: `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- Rolling MV benchmark: `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

Benchmark remains JIT reference only and never directly becomes a hard production rule.

## Current Risks / Pending
- First-frame prompts are not user-locked yet.
- Need user review before image generation is treated as production evidence.
- Exact Douyin music_id pending Codex hardening test.
- Account-side publish availability pending pre-publish validation.

## Next Allowed Action

Human review of all 8 first-frame prompts.

If approved:
1. create a separate R1S04 prompt LOCK commit;
2. generate first-frame images (recommended validation anchors S1 / S5 / S6 first, or all 8 if user requests);
3. review beauty, identity consistency, visual differentiation and dynamic executability before dynamic-video prompts.

Do not begin Seedance dynamic generation before first-frame images themselves pass review.
