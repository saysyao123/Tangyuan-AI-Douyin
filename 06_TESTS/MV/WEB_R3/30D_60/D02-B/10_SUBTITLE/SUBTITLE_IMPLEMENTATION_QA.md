# D02-B｜Subtitle Implementation QA v1

Status: `PASS`

## Authority
- Stage entry: `S12_HG04_PICTURE_EDIT_PASS` / `EDIT_PREVIEW_QA_PASS`.
- Timing authority: `03_AUDIO_TIMELINE/lyrics_exact.srt`.
- Visual baseline: `LOCKED_BASELINE_R1_WEB_R2` from `04_HARNESS/rules/mv_subtitle.md`.
- Source picture preview: `D02-B_picture_preview_v2_dense_lyric.mp4`.
- Source preview SHA-256: `99cdff6fa8f8af17e0e935e8a9714cc33076bdce2ea4d96037afc4989297eee5`.
- Rendered subtitle candidate: `D02-B_有几次想你了_最终候选_字幕版_v1.mp4`.

## Implementation
- Canvas: `720x1280`, `24fps`, `9:16`.
- Font: `Noto Sans CJK SC Bold`, nominal `46px`.
- Text: near-white `#F8F8F8`, `1px` dark stroke.
- Subtitle center: `x=360 / y=1009`.
- Background: `#383838`, opacity `0.666667`, radius `8px`.
- Padding: `10px` on top / bottom / left / right.
- Fade: `100ms` in / `180ms` out.
- Karaoke: disabled.
- Renderer: actual glyph bbox -> fresh RGBA rounded plate per event -> ffmpeg overlay. No text-width estimation, old-path scaling, manual per-line offset, ASR re-run or lyric-clock nudge.

## Timing implementation QA
Canonical line times were preserved exactly as event authority. At the 24fps raster boundary:

| # | lyric | start delta | end delta | result |
|---:|---|---:|---:|---|
| 1 | 有几次想你了 | 0.000s | -0.005s | PASS |
| 2 | 有几次忍住了 | +0.0217s | -0.0150s | PASS |
| 3 | 有几句想说的 | +0.0117s | -0.0250s | PASS |
| 4 | 都变成算了 | +0.0250s | -0.0133s | PASS |
| 5 | 有几场雨停了 | +0.0133s | -0.0233s | PASS |
| 6 | 有几阵风过了 | +0.0050s | -0.0333s | PASS |
| 7 | 有多舍不得也该放下了 | +0.0150s | -0.0100s | PASS |

24fps frame duration is `0.041667s`; maximum absolute start delta is `0.0250s`, maximum absolute end delta is `0.0333s`. Both are below one frame. No systematic global lag detected.

## Geometry QA｜all 7 lines
Every event was rendered from the actual final glyph bbox, then rebuilt with a fresh rounded rectangle.

- left padding: `10px` for 7/7 lines — PASS
- right padding: `10px` for 7/7 lines — PASS
- top padding: `10px` for 7/7 lines — PASS
- bottom padding: `10px` for 7/7 lines — PASS
- text bbox center vs box center X error: `0px` for 7/7 — PASS
- text bbox center vs box center Y error: `0px` for 7/7 — PASS
- box remains inside canvas and below the primary face/action zone — PASS
- no line requires semantic wrapping; longest line box width is `482px`, safely inside the 720px canvas — PASS

Risk samples checked:
- first line: `有几次想你了` — PASS
- shortest line: `都变成算了` — PASS
- longest/final line: `有多舍不得也该放下了` — PASS
- two-line case: not applicable for this lyric set.

## Visual sample QA
Mid-event frames for all seven lines plus the post-vocal tail were inspected from the rendered candidate.

- font weight/size consistent — PASS
- rounded box opacity consistent — PASS
- text visually and geometrically centered — PASS
- no subtitle clipping or safe-area overflow — PASS
- face, eyes, hand detail and world-opening action remain readable — PASS
- tail after lyric 7 is subtitle-free — PASS
- no new generator corner mark introduced by subtitle render — PASS

`SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
