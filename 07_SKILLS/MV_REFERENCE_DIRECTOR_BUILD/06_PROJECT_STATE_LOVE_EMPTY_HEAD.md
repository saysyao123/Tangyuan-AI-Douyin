# PROJECT_STATE｜爱让人脑袋空空

> Status: `ACTIVE`
> Current Stage: `MULTI_SHOT_DIRECTOR_GATE`

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
- Director Draft: `08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v2.md`
- Director Status: `DRAFT_FOR_HUMAN_GATE`
- Current Shot Plan: A=5 principal shots; B=4 principal core shots; multi-shot, lyric/beat driven
- K0: `PENDING / NOT COUNTED AS COMPLETE`
- K0 latest requirement: first frame must visibly establish all persistent core subjects/assets needed by that generated clip, so later shots do not rely on the model inventing major new people/objects/scene systems
- Dynamic Prompt: `PENDING`
- Generation: `PENDING`
- QA: `PENDING`
- Assembly: `PENDING`
- Next Action: finish Human Director Gate with the latest camera-language refinement; then formalize K0-A/K0-B, run K0 Gate, and only then compile multi-shot Dynamic Prompts.

## Hard dependencies

If Audio Version changes:

`Timeline → Segment Plan → Director → K0 → Prompt → Generation → Assembly` all become invalid.

If only downstream visual choices change, Timeline remains locked.

If Director Gate is not passed, K0 / Prompt / Generation must remain pending.
