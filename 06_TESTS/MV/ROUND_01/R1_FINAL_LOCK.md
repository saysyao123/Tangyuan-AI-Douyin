# Round 01｜FINAL LOCK

> Status: `LOCKED`
> Locked at: `2026-08-21`
> Human decision: final R1 result accepted; proceed to Round close.

## Final Golden Sample

- Song: `你有没有真的爱过我｜阿图表妹`
- Reference audio interval: `01:23.800 -> 02:00.600`
- Reference duration: `36.80s`
- Final accepted edit family: `R1_MV_v4_final_polish.mp4`
- Accurate lyric timing asset: `lyrics_exact_v3_1.srt`
- First frames: `8`
- Dynamic source clips: `8 × 5s`

## Locked outcomes

1. R1 Golden Sample accepted.
2. `04_HARNESS/workflows/mv.md` is MV SOP v1 runtime workflow.
3. Character image-to-video prompts must use the exact `***` fictional-AI-character prefix in `rules/ai_video.md`.
4. First frames are treated as `0-second dynamic anchors`.
5. 2–3 shot grammar inside a 5s clip is a validated option, not a universal requirement.
6. Subtitle timing is derived from locked audio alignment, never visual-segment boundaries.
7. Editing should preserve useful internal motion arcs and use selective trim / overlap rather than mechanically equal clip lengths.
8. Watermark-free HD source replacement is deferred to Codex and does not invalidate the R1 creative acceptance.

## Deferred / experimental

- exact Douyin music_id / Creator Center datasource automation;
- larger single-shot cinematic camera library;
- Whisper forced lyric alignment automation;
- watermark-free HD source replacement automation;
- advanced lyric effects.

Track these in `03_DATA/EXPERIMENTS.md`.

## No further mutation rule

Do not silently modify the R1 Golden Sample rules, timing, or accepted creative decisions inside this Round.

Any further creative calibration must begin as:
- `ROUND_02`, or
- a named Codex hardening task that explicitly preserves the R1 Golden creative reference.
