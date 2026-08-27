# D02-B｜WEB Source Rough-Cut QA v2

Status: `PASS`

- All five current sources are native 720x1280 / 9:16 / 24fps; no 3:4 exception exists in this revised batch.
- Reused the previously validated WEB watermark-safe method only: 1.25x center safety crop (scale to 900x1600, crop 720x1280 at x=90 y=160).
- No stretch / no aspect-ratio change.
- Representative frames show the generator corner mark outside the final frame.
- Subject, hands, linen, limestone boundaries and sea remain compositionally usable after crop.
- All AI source audio removed. Locked HG02 BGM remains the only production music in picture preview.
- No new watermark-removal method was introduced.

Result: `WEB_SOURCE_ROUGH_CUT_QA_PASS = YES`.
