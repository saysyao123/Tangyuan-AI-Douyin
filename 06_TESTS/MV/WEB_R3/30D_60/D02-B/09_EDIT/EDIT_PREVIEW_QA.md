# D02-B｜Edit Preview QA v1

Status: `PASS_FOR_HG04_REVIEW`

Preview: `D02-B_picture_preview_v1.mp4`
Preview SHA256: `127fd8dc4928401d7d28b88caa0dba8feadeacc077af45793841a89227c1d8e2`

## Technical
- 720x1280, 24fps, SAR 1:1.
- Duration ~15.39s against locked BGM target ~15.412s; frame/audio rounding only, no new lyric clock.
- Locked HG02 BGM is the only production audio.
- AI source audio removed before edit.
- No subtitles at HG04 picture-rhythm stage.

## Picture / rhythm
- External visible sequence: `S1 close approach -> S2 boundary/turn -> S3 rear-three-quarter continuation -> S4 long-axis release`.
- Visual scale opens progressively instead of alternating randomly between close and wide.
- S1 is deliberately trimmed before the generated smile dominates the performance.
- S2 mild slowdown (~0.91x) is not visually disruptive in preview and preserves the complete HOLD -> YIELD arc.
- S3 is used at native speed and carries the semantic handoff from `算了` into weather/time having passed.
- S4 remains native-speed for 5s, then last-frame hold carries the post-vocal music tail without starting a new event.
- No random internal cuts detected in chosen windows.
- Perceptible shot count remains low and readable.

## WEB safety
- Previous validated watermark-safe center-crop method used for native 9:16 sources.
- Current uploaded S2 file reports 720x960; normalized without stretch and kept compositionally usable.
- Representative clean-proxy frames show no visible generator corner mark.

## Known creative note / future improvement
- Camera design can still be strengthened in later MVs; current source set is accepted as stable and usable.
- S1 source did not fully perform `忍住`; edit patches this locally by handing restraint to S2 rather than regenerating S1.

Gate recommendation: present this preview to HG04 for picture-rhythm review.
