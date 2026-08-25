# WEB R3｜WEB Source Rough-Cut Gate QA v1

Status: `PASS / R2 METHOD RESTORED`
Song: `如果风会替我说话`
Date: `2026-08-25 Asia/Shanghai`

## 0. Why this retrofit was required

R3 Picture Edit v1 was rhythmically accepted, but it incorrectly entered Picture Edit using raw/unclean WEB source geometry. This skipped a WEB R2 validated technical Gate.

R2 authoritative evidence restored:
- batch-uniform whole-source crop/zoom;
- no local per-shot hiding;
- source audio removed before edit;
- left-top / right-bottom corner-risk QA;
- 9:16 / SAR1:1 preserved.

R2 exact validated geometry:
`crop=576:1024:72:128 -> scale=720:1280`
Equivalent visual zoom: `1.25×`.

## 1. Current R3 batch processed

Eight final edit-source candidates were processed into non-destructive WEB clean proxies.
Original sources remain unchanged.

Content mapping:
- S01 = `3S1.mp4`
- S02 = latest Doubao rewrite `AI动画人物雨夜窗边视频生成(1).mp4`
- S03 = `3S3.mp4`
- S04 = `3S4(1).mp4`
- S05 = `3S5(1).mp4`
- S06 = latest Doubao rewrite `AI动画人物雨夜窗边视频生成 (2)(1).mp4`
- S07 = `3S7.mp4`
- S08 = `3S8.mp4`

## 2. Processing profile

Applied identically to all eight sources:
- input nominal: `720×1280`
- crop: `576×1024 @ x=72,y=128`
- output scale: `720×1280`
- visual zoom: `1.25×`
- fps: `24`
- SAR: `1:1`
- source audio: `REMOVED`
- output codec: H.264 WEB proxy

No per-shot repositioning or local watermark patching was used.

## 3. QA sampling

Batch source-proxy sampling:
- every source checked at approximately `0.5s` and `4.5s`;
- representative sheet therefore covered opening/ending states across all eight clips.

Picture Edit regression sampling:
- approximately `0.5 / 3.5 / 6.5 / 9.5 / 13 / 16 / 19 / 22.5s`.

Observed:
- no visible top-left generator mark in reviewed samples;
- no visible bottom-right generator mark in reviewed samples;
- no mixed watermark state;
- no stretch;
- all proxies remain 9:16 / 720×1280 / SAR1:1;
- all proxies contain zero AI source-audio streams.

`NO_VISIBLE_GENERATOR_MARK = YES` in reviewed batch samples.

## 4. Composition impact

The 1.25× WEB crop changes framing but does not alter timing.
Current review:
- S01 becomes a tighter portrait but remains usable as Hook;
- S02 rain-window composition remains readable;
- S03 room/absence still reads;
- S04 corridor depth and foreground reveal remain intact enough;
- S05 mirror geometry remains readable;
- S06 ice + background woman remain readable;
- S07 both paper objects remain visible;
- S08 world-opening release remains readable.

No current source triggered `ROUGH_CUT_GEOMETRY_EXCEPTION`.

## 5. Picture Edit regression

Re-rendered the previously accepted EDL using only WEB clean proxies.
No edit-point redesign was introduced.

Same timeline intent:
- S01 `0.15–3.15`
- S02 `2.00–5.00`
- S03 `0.60–2.60`
- S04 `0.20–4.20`
- S05 `0.30–3.30`
- S06 `2.00–5.00`
- S07 `0.80–2.80`
- S08 `0.40–4.72`

Clean regression preview:
`如果风会替我说话_R3_PictureEdit_v1_WEB_RoughCutClean.mp4`

Technical:
- video: `720×1280 / 24fps / SAR1:1`
- BGM: locked production BGM
- duration: `24.333333s` container/frame-quantized versus target 24.32s
- SHA-256: `70d066ca4466e72bd5876fc83b3e3c0328ac412a9eccb9e94fe566dc8cc3089a`

The edit timing/rhythm structure is unchanged; only source geometry is normalized before the same EDL is applied.

## 6. Gate result

`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`

Required map:
`R3_C_WEB_SOURCE_ROUGH_CUT_MAP_v1.csv`

This Gate is now restored as a mandatory WEB technical Gate before formal Picture Edit.

## 7. Process correction

Correct WEB chain from now on:

`Dynamic Source QA`
→ `Atom/Arc normalization when needed`
→ **`WEB SOURCE ROUGH-CUT GATE`**
→ `Editor Audio Gate`
→ `Picture Edit`
→ `HG04`

Watermark handling is no longer allowed to remain as `FINAL POLISH TODO`.

## 8. Patch, Don't Cascade decision

Because the user already approved Picture Edit rhythm and this retrofit did not change edit points:
- preserve `HG04 rhythm PASS` as prior human evidence;
- replace the raw-source Picture Edit implementation with the clean-proxy regression render;
- do not reopen BGM / Audio Timeline / Director / generation;
- only reopen HG04 if user sees a material composition/rhythm regression caused by the uniform crop.
