# PROJECT_STATE｜爱让人脑袋空空

> Status: `ACTIVE`
> Current Stage: `SEGMENT_PLAN`

- Project: MV Reference Director Skill / first real run
- Song Family: `爱让人脑袋空空`
- Core Account / Primary Reference Source: `乐♩青春`
- Primary Reference: user-selected and uploaded Douyin video
- Reference Duration: `15.370998s`
- Reference Video: `1920x1080 / 30fps / H.264`
- Audio Version: exact AAC audio extracted from selected Reference
- Audio: `AAC / 44.1kHz / stereo / 15.370998s`
- Timeline Version: `v1`
- Timeline Status: `LOCKED`
- Timeline Evidence: `05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
- Preferred Cut Point: `8.700s`
- Proposed Segment A: `0.000–8.700s` (`8.700s`)
- Proposed Segment B: `8.700–15.371s` (`6.671s`)
- K0: `PENDING`
- Dynamic Prompt: `PENDING`
- Generation: `PENDING`
- QA: `PENDING`
- Next Action: lock Segment / Duration Plan from the locked Timeline, then enter Reference Deconstruction.

## Hard dependency

If Audio Version changes:

`Timeline → Segment Plan → Director → K0 → Prompt → Generation` all become invalid.

If only downstream visual choices change, Timeline remains locked.