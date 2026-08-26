# D02-A Final Render Ready Receipt v1

Status: `FINAL_RENDER_READY / HG05_PENDING_USER_ACCEPTANCE`

## Locked picture
- Picture structure unchanged from accepted watermark-safe rough cut v2.
- WEB watermark-safe baseline preserved across the batch: `crop=576:1024:72:128 -> scale=720:1280`, equivalent ~1.25x uniform zoom before final 1080x1920 render.
- No additional shot regeneration or timeline redesign in final polish.

## Subtitle
- Canonical timing source: `AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`.
- Style inherits locked R1 / WEB_R2 subtitle baseline, proportionally scaled to 1080x1920.
- 69px bold CJK sans-serif, near-white text, dark semi-transparent rounded box, 15px equal padding, center x=540/y=1514.
- Long lines use semantic two-line wrapping only where needed.
- Fade in 100ms / fade out 180ms.
- Geometry QA: all-line padding 15/15/15/15px; text/box center error 0px; safe-region PASS.

## Final render technical QA
- file: `D02-A_做她的大地别做她的天_26.424s_最终发布版_v1.mp4`
- SHA256: `9d295d95e4fcecc9bc59b616c7c8efe61ce4c68253e8302cbfef9bf090a5564d`
- size: 54,916,983 bytes
- duration: 26.423991s
- video: H.264 / 1080x1920 / 24fps / yuv420p
- audio: AAC / 44.1kHz / stereo
- audio mean volume: -14.3 dB
- audio max peak: -0.7 dB
- final BGM structure/fade unchanged from HG02-B lock.

## Visual QA samples
Representative frames checked across hook, first lyric, weather bridge, relationship hit, moonlight face-performance section, and final world-opening release.

PASS:
- subtitle readability and safe placement;
- no subtitle coverage of key eyes/actions;
- watermark-safe crop remains clean in sampled corners;
- no new visible edit discontinuity introduced by final polish;
- final release keeps clean tail.

## Gate
`HG04 Picture Rhythm = PASS` based on user acceptance of the watermark-safe rough cut.

Current next gate:
`HG05 Final Acceptance` — user watches the final render and explicitly accepts or requests a local patch.

## Face input rule captured from this round
For subsequent first-frame production in this project:
- generate the cinematic K0 at maximum useful clarity and according to director needs;
- do not reduce overall face/image quality for platform compatibility;
- use the validated face-region black grid as the input-adapter layer when needed;
- video stage owns face completion / performance.

Current evidence level: `REAL-MV POSITIVE EVIDENCE`; promote beyond this project only after repeated cross-song validation.
