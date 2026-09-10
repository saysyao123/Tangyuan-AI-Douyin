# PROJECT_STATE｜爱让人脑袋空空

> Status: `ACTIVE`
> Current Stage: `GENERATION_QA_ROUND01`

- Project: MV Reference Director Skill / first real run
- Song Family: `爱让人脑袋空空`
- Core Account / Primary Reference Source: `乐♩青春`
- Primary Reference: user-selected and uploaded Douyin video
- Reference Duration: `15.370998s`
- Audio Version: exact AAC audio extracted from selected Reference
- Timeline Version: `v1`
- Timeline Status: `LOCKED`
- Timeline Evidence: `05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
- Final Segment A: `0.000–8.700s` (`8.700s`)
- Final Segment B: `8.700–15.370998s` (`6.670998s`)
- Final Transition: `Hard Cut @ 8.700s`
- Generated Material Plan: A=`12s`; B=`10s`; optional 5–15s coverage only if a concrete edit/scene need appears
- Segment Plan: `06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v2.md`
- Reference Deconstruction: `07_LOVE_EMPTY_HEAD_REFERENCE_DECONSTRUCTION_v1.md`
- Director: `08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v3_LOCKED.md`
- K0 Spec: `09_LOVE_EMPTY_HEAD_K0_SPEC_v1.md`
- K0 Gate: `10_LOVE_EMPTY_HEAD_K0_GATE_v1.md`
- Dynamic Prompt v1: `10_LOVE_EMPTY_HEAD_MULTI_SHOT_PROMPTS_v1.md`
- Generation Round 01: `COMPLETED / REAL EVIDENCE`
- Generation A actual: `12.096009s / HEVC / 720x1280 / 24fps / AAC stereo`
- Generation B actual: `10.080000s / HEVC / 720x1280 / 24fps / AAC stereo`
- Generation QA Evidence: `11_LOVE_EMPTY_HEAD_GENERATION_QA_ROUND01.md`
- Visual Director/Prompt: `PASS CANDIDATE`
- Timing behavior: `SOFT CHOREOGRAPHY / NOT FRAME-ACCURATE`
- Anti-sliding locomotion: `PASS CANDIDATE`
- Character consistency: `GOOD / MINOR CLOSE-UP DRIFT`
- Watermark: `BLOCKER_FOR_FINAL_DELIVERY` (dynamic/moving Dola AI watermark, sometimes overlaps face/hand/detail regions)
- Audio: `FAIL_CURRENT_CONTRACT` (generated continuous musical/BGM bed; next prompt must explicitly allow scene SFX only and disallow music/voice)
- Final QA: `NOT PASS YET`
- Assembly: `PENDING`
- Next Action: keep successful visual Director/Prompt structure; make one controlled prompt change for Audio Contract only, while separately resolving the upstream clean/no-watermark delivery path. Do not Promote until real clean/audio-compliant output passes QA.

## Hard dependencies

If Audio Version changes:

`Timeline → Segment Plan → Director → K0 → Prompt → Generation → Assembly` all become invalid.

If only downstream visual choices change, Timeline remains locked.

## Audio Contract for next iteration

Allowed only: wind / grass and cloth rustle / footsteps / distant lake-water ambience / subtle wind-spirit whoosh.

Disallow: BGM / music / score / melody / singing / humming / dialogue / voice / vocalization / rhythmic percussion or beat track.

If forbidden music or voice remains, strip the entire generated audio track during final editing and rebuild from locked BGM + controlled scene SFX.
