# PROJECT_STATE｜爱让人脑袋空空

> Status: `ACTIVE`
> Current Stage: `MULTI_SHOT_DYNAMIC_PROMPT`

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
- Segment Plan: `06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v2.md` (`LOCKED / NOT YET GENERATION-VALIDATED`)
- Reference Deconstruction: `07_LOVE_EMPTY_HEAD_REFERENCE_DECONSTRUCTION_v1.md`
- Director: `08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v3_LOCKED.md`
- Director Status: `LOCKED_FOR_CURRENT_PROJECT / NOT YET GENERATION-VALIDATED`
- Current Shot Plan: A=5 principal core shots + A0 establishing; B=4 principal core shots + B0 establishing; lyric/beat-driven multi-shot
- Camera Language: follow / tracking / push / pull / side-move / light orbit / rise + medium / close / face detail / hand detail / foot detail / wide / extreme-wide
- K0 Spec: `09_LOVE_EMPTY_HEAD_K0_SPEC_v1.md`
- K0 Gate: `10_LOVE_EMPTY_HEAD_K0_GATE_v1.md`
- K0 Status: `PASSED_FOR_CURRENT_PROJECT / NOT YET GENERATION-VALIDATED`
- K0 Contract: first frame = first-shot dynamic anchor + persistent asset contract; visibly establish the main character, core clothing silhouette, wind-spirit, main environment, traversable ground/direction, light/weather/wind needed downstream
- Dynamic Prompt: `ACTIVE / TO COMPILE`
- Generation: `PENDING`
- QA: `PENDING`
- Assembly: `PENDING`
- Next Action: compile Segment A 12s and Segment B 10s multi-shot Dynamic Prompts from locked Timeline + Director v3 + passed K0; then enter Seedance 2.5 generation.

## Hard dependencies

If Audio Version changes:

`Timeline → Segment Plan → Director → K0 → Prompt → Generation → Assembly` all become invalid.

If only downstream visual choices change, Timeline remains locked.

Dynamic Prompt must not introduce new persistent asset systems that were not declared by K0 unless a deliberate coverage redesign is approved.