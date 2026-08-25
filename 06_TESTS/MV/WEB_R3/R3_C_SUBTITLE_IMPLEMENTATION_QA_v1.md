# WEB R3｜Subtitle Implementation QA v1

Status: `PASS`
Song: `如果风会替我说话`
Date: `2026-08-25 Asia/Shanghai`

## 1. Authority / inputs

Timing authority:
`06_TESTS/MV/WEB_R3/AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`

Picture authority:
`如果风会替我说话_R3_PictureEdit_v1_WEB_RoughCutClean.mp4`

Subtitle visual authority:
`04_HARNESS/rules/mv_subtitle.md`
R1 Golden + WEB R2 locked baseline.

No per-line timing nudge was introduced.

## 2. Canonical subtitle events

1. `0.000–3.000` 如果风会替我说话
2. `3.000–6.000` 如果雨会替我回答
3. `6.000–8.000` 如果我还会想起他
4. `8.000–12.000` 如果还能一起回家
5. `12.000–15.000` 如果梦能模糊真假
6. `15.000–18.000` 如果痛能随之融化
7. `18.000–20.000` 如果我们还是傻瓜
8. `20.000–24.000` 如果爱不只是童话

At 24fps, all event boundaries above land on exact whole-frame boundaries.
Implementation timing delta: `0 frames` for start/end event boundaries.

## 3. Visual baseline applied

Canvas: `720×1280`
Font: `Noto Sans CJK SC Bold`
Nominal size: `46px`
Text: near-white `#F8F8F8`
Stroke: approximately `1px` dark
Subtitle center: approximately `x=360 / y=1009`
Background: dark semi-transparent rounded rectangle `#383838` family
Radius: `8px`
Padding: `10px` each side
Fade in: `100ms`
Fade out: `180ms`
Karaoke: `NO`
Max lines used: `1`

Implementation method:
- render each final line using final font/size/stroke;
- measure actual rendered glyph pixel bbox;
- build a fresh rounded box from that bbox;
- add exactly 10px L/R/T/B;
- center the complete box at the locked subtitle center;
- composite as timed overlay onto the clean Picture Edit.

## 4. All-line geometry QA

| line | text | box px | L | R | T | B | center x err | center y err |
|---|---|---:|---:|---:|---:|---:|---:|---:|
|1|如果风会替我说话|388×68|10|10|10|10|0|0|
|2|如果雨会替我回答|389×68|10|10|10|10|0|0|
|3|如果我还会想起他|388×68|10|10|10|10|0|0|
|4|如果还能一起回家|388×68|10|10|10|10|0|0|
|5|如果梦能模糊真假|389×68|10|10|10|10|0|0|
|6|如果痛能随之融化|388×68|10|10|10|10|0|0|
|7|如果我们还是傻瓜|388×67|10|10|10|10|0|0|
|8|如果爱不只是童话|388×68|10|10|10|10|0|0|

`GEOMETRY_QA = PASS`

## 5. Mandatory visual samples

Reviewed representative frames at approximately:
`1.5 / 4.5 / 7.0 / 10.0 / 13.5 / 16.5 / 19.0 / 22.0s` plus post-subtitle tail `24.15s`.

Observed:
- consistent font weight / size;
- consistent background opacity;
- visually and geometrically centered text;
- no overflow;
- no eye/critical facial-performance obstruction;
- S06 ice foreground remains readable;
- S07 object pair remains readable;
- S08 world-opening release remains readable;
- no subtitle remains after canonical final end at 24.000s.

`MANDATORY_VISUAL_SAMPLE_QA = PASS`

## 6. Audio preservation

Final subtitle candidate audio vs clean Picture Edit decoded PCM correlation:
`1.000000` (numerical rounding may report slightly >1 in float32 calculation).

Therefore subtitle rendering did not alter the approved Picture Edit audio implementation.
No AI source-audio stream was introduced.

## 7. Gate

`SUBTITLE_STYLE_QA_PASS = YES` (inherited locked R1/WEB R2 baseline)
`SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
