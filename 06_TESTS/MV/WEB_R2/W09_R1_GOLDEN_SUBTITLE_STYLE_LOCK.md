# WEB R2｜W09 R1 Golden Subtitle Style Lock

> Status: `STYLE_TARGET_LOCKED / IMPLEMENTATION_QA_NEXT`
> User decision: `按照R1之前做的字幕标准就行，位置，大小和效果，R1那版都还可以`

## Authority

R1 Golden references:
- `06_TESTS/MV/ROUND_01/R1S06_EDIT_ROUND3.md`
- `06_TESTS/MV/ROUND_01/R1_FINAL_ACCEPTANCE.md`
- `06_TESTS/MV/CODEX_R1/GOLDEN_TARGET.md`

The R1 record preserves the layout/effect standard but does not preserve one exact numeric font-size as a hard equality target. CODEX R1 explicitly prioritizes layout/readability when exact font identity is unavailable.

## Locked style target

For current 720×1280 WEB R2 implementation:
- Chinese lyric only;
- bold clean Simplified-Chinese sans serif;
- near-white text;
- dark semi-transparent tight background box;
- text visually centered horizontally + vertically inside the box;
- subtitle visual center around `y≈1010`;
- single lyric phrase at a time;
- maximum 2 lines;
- restrained fade: approximately `100ms in / 180ms out`;
- no karaoke / word-by-word highlight;
- no decorative English / small helper text / lyric duplication.

Current WEB implementation proxy:
- font: `Noto Sans CJK SC Bold` (environment-equivalent clean CJK sans);
- size: `34` at 720×1280, chosen to reproduce the R1 recorded scale/position rather than create a new style;
- center position: `x=360, y=1010`;
- long L09 wraps to two centered lines;
- timing source remains canonical W02A `lyrics_exact.srt` / `line_timeline.csv` unchanged.

## QA sampled

Sampled current render:
- ordinary short line;
- middle long line;
- title line;
- longest L09 two-line wrap;
- final line.

Checks:
- no overflow;
- box stays subordinate to cinematography;
- centered layout remains stable;
- no change to locked picture edit;
- no change to canonical lyric clock.

## State

`SUBTITLE_STYLE_TARGET_LOCKED = R1_GOLDEN`

Next:
1. verify burned subtitle start/end follows canonical timing asset;
2. run `SUBTITLE_IMPLEMENTATION_QA`;
3. then W10 final technical/full-watch QA.
