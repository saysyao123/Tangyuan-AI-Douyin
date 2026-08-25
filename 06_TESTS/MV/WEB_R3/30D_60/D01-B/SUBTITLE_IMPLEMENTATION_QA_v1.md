# D01-B｜Subtitle Implementation QA v1

Status: `PASS`

## Timing source

Canonical source remains the locked `AUDIO_TIMELINE_PACKAGE`:
- L01: `0.000–4.540`
- L02: `4.540–8.420`
- L03: `8.420–12.360`
- L04: `12.360–15.987`

No subtitle timing was derived from Picture Edit and no per-line nudge was applied.

## Copyright-safe text injection

Exact lyric plaintext was loaded only from the project's private temporary forced-alignment artifact and verified against the persistent SHA-256 values. Plaintext is not persisted back into the repository.

Verified hashes:
- L01: `17c60d2820eb34f421224f41230d66224c6a0e5164eae944433ad171a49520f8`
- L02: `c624f95bad7b6ca6e5cb9deb69122d21c6e0d9fea33502138c6be3b08cc871a9`
- L03: `0617a73d8d14a999d33807793a62f482a40e4f5c9473b0bfd110accbe192948e`
- L04: `25e21bc2eefc59b88d5eae1c0d476618783e1830088c303fc6d532950f7c70a1`

## Locked visual baseline

720×1280 implementation:
- font: `Noto Sans CJK SC Bold`
- nominal size: `46px`
- text: near-white
- subtle dark 1px stroke
- subtitle center: `x=360 / y=1009`
- box: dark semi-transparent rounded rectangle
- radius: `8px`
- padding: `10px` all sides
- fade in: `100ms`
- fade out: `180ms`
- no karaoke / decorative English / secondary text

## Geometry QA｜ALL LINES

| Line | Chars | L/R/T/B padding | text-box center error X/Y | Result |
|---|---:|---|---|---|
| L01 | 9 | 10/10/10/10 px | 0/0 px | PASS |
| L02 | 9 | 10/10/10/10 px | 0/0 px | PASS |
| L03 | 9 | 10/10/10/10 px | 0/0 px | PASS |
| L04 | 7 | 10/10/10/10 px | 0/0 px | PASS |

The shortest line L04 was included as the mandatory narrow-box risk sample.

## Timing implementation QA｜24fps

Frame quantization deltas remain within one frame (`41.667ms`):
- L01 start `0ms`; end approx `+1.7ms`
- L02 start approx `+1.7ms`; end approx `-3.3ms`
- L03 start approx `-3.3ms`; end approx `+15ms`
- L04 start approx `+15ms`; end approx `+13ms`

No systematic global lag detected.

## Visual sample QA

Mandatory samples checked across S01/S02/S03/S04:
- no subtitle overlaps eyes/face;
- S03 flower remains readable;
- S04 ascent remains readable;
- subtitle safe area is stable;
- font size/weight/box opacity consistent.

`SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
`SUBTITLE_STYLE_QA_PASS = INHERITED_LOCKED_BASELINE`
