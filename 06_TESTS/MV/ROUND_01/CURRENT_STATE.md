# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S03`
- STAGE_NAME: `Director / Visual System Planning`
- STATE: `READY_FOR_FOCUSED_BENCHMARK`
- PREVIOUS_LOCK: `R1S02_REFERENCE_BGM_CLIP_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- R1S02_LOCK: `06_TESTS/MV/ROUND_01/R1S02_LOCK.md`
- SELECTED_REFERENCE_BGM: `你有没有真的爱过我｜阿图表妹`
- APPROVED_CLIP: `你有没有真的爱过我_建议剪辑片段_v1.mp3`
- APPROVED_DURATION: `36.80s`
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
- User review: `PASS / version is good`

All later Beat timing, director design, first frames, Seedance prompts and final editing must use this exact clip. No silent version swap.

### Locked Lyric Span

1. 你的回应是一直沉默
2. 只剩下落寞
3. 我有什么错
4. 短暂柔情似流星划落
5. 你有没有真的爱过我
6. 我是你诗的哪个段落
7. 落款第几页
8. 第几次临摹
9. 还是匆匆一瞥就略过

### Reference vs Publish BGM

- `REFERENCE_BGM`: locked and approved for production.
- `PUBLISH_BGM`: exact Douyin platform asset / account availability remains a hard pre-publish Gate.

`AVAILABLE_AT_PUBLISH = TRUE` is still required before release.

## Current Benchmark / Observer System

- Song observer pool: `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- Rolling MV benchmark: `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

Benchmark is loaded JIT and never directly becomes a hard rule.

## R1S03 Next Allowed Action

Run focused Benchmark analysis for 3–5 works relevant to this song, then produce:

1. visual-world concept;
2. emotional / dynamic strength curve across the exact 36.80s clip;
3. Beat-level narrative tasks;
4. shot-language variation plan;
5. anti-homogeneity list;
6. first-frame group direction.

Do not generate first frames before the director/visual-system proposal receives user review.

## Pending / Risks

- Exact Douyin music_id pending Codex hardening test.
- Account-side publish availability pending pre-publish validation.
- Final production must continue using the approved local reference clip.
