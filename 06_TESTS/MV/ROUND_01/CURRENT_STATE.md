# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S05`
- STAGE_NAME: `Dynamic Video Prompt Planning`
- STATE: `READY_FOR_DYNAMIC_PROMPT_REVIEW`
- PREVIOUS_LOCK: `R1S04_FIRST_FRAME_SET_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- R1S02_LOCK: `06_TESTS/MV/ROUND_01/R1S02_LOCK.md`
- R1S04_LOCK: `06_TESTS/MV/ROUND_01/R1S04_LOCK.md`
- DYNAMIC_PROMPTS: `06_TESTS/MV/ROUND_01/R1S05_DYNAMIC_PROMPTS_v1.md`
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

User reviewed the complete eight-image group and said the current first-frame effect is satisfactory. The full set is production-approved.

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

## R1S05 Dynamic Prompt Set｜v1 READY

Full set:
`06_TESTS/MV/ROUND_01/R1S05_DYNAMIC_PROMPTS_v1.md`

### Critical keyframe mapping｜actual generation order
- `KF01 = S1` — 你的回应是一直沉默
- `KF02 = S5` — 你有没有真的爱过我
- `KF03 = S6` — 我是你诗的哪个段落
- `KF04 = S2` — 只剩下落寞
- `KF05 = S3` — 我有什么错
- `KF06 = S4` — 短暂柔情似流星划落
- `KF07 = S7` — 落款第几页 / 第几次临摹
- `KF08 = S8` — 还是匆匆一瞥就略过

Generate in keyframe order if convenient:
`KF01 -> KF02 -> KF03 -> KF04 -> KF05 -> KF06 -> KF07 -> KF08`

Final editing order remains:
`S1(KF01) -> S2(KF04) -> S3(KF05) -> S4(KF06) -> S5(KF02) -> S6(KF03) -> S7(KF07) -> S8(KF08)`

### Camera / motion differentiation
- KF01/S1: static tension + tiny lateral desk slide / ink bleed.
- KF02/S5: restrained portrait micro-performance + very small emotional push.
- KF03/S6: spatial traversal through paper layers / parallax occlusion.
- KF04/S2: lateral reveal of empty courtyard; keep heroine small.
- KF05/S3: fingertip water contact + reflection distortion + camera lowers to waterline.
- KF06/S4: meteor-driven tilt/reframe + wind/reflection event; highest environmental motion.
- KF07/S7: macro brush finish + focus shift + peel back layered traces.
- KF08/S8: mostly static camera + foreground page occlusion / cold ending.

### Shared hard rules
1. Exactly 5s each, 9:16, Seedance 2 mini.
2. Start from the corresponding approved first frame and preserve it as the 0-second state.
3. No human not visible in that first frame may appear.
4. Preserve heroine identity, veil, costume, geometry, palette, and material continuity.
5. No AI dialogue, singing, narration, or BGM; environment sound only if sound instructions are required.
6. One dominant visual event + one secondary physical after-effect per segment.
7. Avoid repeating `standing + slow push + hair/robe movement` across the set.
8. Keep all raw 5s outputs; final trim happens against the locked 36.80s audio after dynamic QA.

## Current Benchmark / Observer System
- Song observer pool: `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- Rolling MV benchmark: `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

Benchmark remains JIT reference only and never directly becomes a hard production rule.

## Current Risks / Pending
- Dynamic prompts v1 await user review / actual Seedance generation test.
- Generated dynamic videos require QA for identity consistency, veil continuity, motion quality, camera repetition and lyric hit.
- Exact Douyin music_id pending Codex hardening test.
- Account-side publish availability pending pre-publish validation.

## Next Allowed Action

Generate the eight 5-second Seedance 2 mini clips from `R1S05_DYNAMIC_PROMPTS_v1.md`, preferably in keyframe generation order, then return all eight original outputs for dynamic QA.

Do not begin final editing before the generated dynamic videos pass review.