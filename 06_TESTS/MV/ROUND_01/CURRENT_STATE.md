# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S05`
- STAGE_NAME: `Dynamic Video Prompt Planning`
- STATE: `READY_FOR_DYNAMIC_PROMPTS`
- PREVIOUS_LOCK: `R1S04_FIRST_FRAME_SET_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- R1S02_LOCK: `06_TESTS/MV/ROUND_01/R1S02_LOCK.md`
- R1S04_LOCK: `06_TESTS/MV/ROUND_01/R1S04_LOCK.md`
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
- User review: `PASS`

All later Beat timing, director design, first frames, dynamic prompts and final editing must use this exact clip. No silent version swap.

### Production Structure｜LOCKED
- conceptual visual units: `6`
- production segments: `8`
- first frames: `8`
- dynamic videos: `8 × 5s = 40s raw material`
- final reference audio: `36.80s`
- edit headroom: approximately `3.20s`

### 8 Production Segments
- S1: `你的回应是一直沉默` — opening hook / no response.
- S2: `只剩下落寞` — empty-space loneliness.
- S3: `我有什么错` — self-question / reflection.
- S4: `短暂柔情似流星划落` — first large visual event.
- S5: `你有没有真的爱过我` — emotional core.
- S6: `我是你诗的哪个段落` — poetic spatial metaphor.
- S7: `落款第几页 / 第几次临摹` — trace / repetition / detail.
- S8: `还是匆匆一瞥就略过` — cold ending / negative space.

### First-frame Set｜LOCKED
Full prompt source:
`06_TESTS/MV/ROUND_01/R1S04_FIRST_FRAME_PROMPTS_v1.md`

Approval record:
`06_TESTS/MV/ROUND_01/R1S04_LOCK.md`

User reviewed the complete eight-image group and said the current first-frame effect is satisfactory. The full set is now treated as production-approved.

Identity / world lock:
- same original fictional East Asian woman across all character frames;
- straight black hair tied low;
- one old muted-gold hairpin;
- dark ink-green long robe with restrained dull-gold details;
- translucent black veil always covers nose, mouth and lower face;
- new-Eastern cinematic photorealism + restrained poetic surrealism;
- cool ink-black / blue-gray / dark-green palette, old-paper ivory and tiny muted-gold highlights;
- no readable text / subtitles / logo / watermark;
- no second human in this R1 set.

Every approved first frame is a `0-second dynamic anchor` and its visible pending action must be continued rather than replaced.

## R1S05 Dynamic Design Requirements

Create exactly `8` independent `5-second` Seedance 2 mini prompts, one for each approved first frame.

Hard requirements:
1. Each dynamic segment begins from its corresponding approved first frame.
2. Do not introduce any human character not already visible in that first frame.
3. Preserve heroine identity, veil, costume, world, lighting logic and scene geometry.
4. No AI dialogue, singing voice, narration or BGM generation; visuals only / environment sound if model requires sound instructions.
5. Avoid the repeated pattern `character stands still + slow camera push + hair/robe moves` across the set.
6. Each segment must have one dominant visual event and one secondary physical after-effect.
7. Vary camera grammar across the eight segments: static tension, lateral reveal, reflection distortion, event-led reframing, restrained portrait micro-movement, spatial traversal, macro action, occlusion/exit.
8. Dynamic strength follows the song: restrained opening -> first rise at S4 -> emotional center S5 -> poetic rise S6 -> detail contraction S7 -> cold release S8.
9. The eight 5s source clips provide 40s raw material; editing should later trim them to the locked 36.80s audio rather than forcing all clips to play in full.
10. Seedance prompt wording must be explicit enough for the model to understand timing/action priority; do not rely on undeclared M/S/L shorthand.

## Current Benchmark / Observer System
- Song observer pool: `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- Rolling MV benchmark: `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

Benchmark remains JIT reference only and never directly becomes a hard production rule.

## Current Risks / Pending
- Dynamic prompts not written yet.
- Generated dynamic videos still require user QA for identity consistency, motion quality, camera repetition and lyric hit.
- Exact Douyin music_id pending Codex hardening test.
- Account-side publish availability pending pre-publish validation.

## Next Allowed Action

Write the full `S1-S8` dynamic prompt set for Seedance 2 mini, preserving the locked first frames and varying director/camera grammar across all eight 5-second clips.

Do not begin final editing before the generated dynamic videos themselves pass review.
