# CODEX R1｜GOLDEN TARGET

> This file is the objective comparison target for MODE A.

## Human Golden Sample

- Song: `你有没有真的爱过我`
- Artist: `阿图表妹`
- Source interval: `00:01:23.800 -> 00:02:00.600`
- Reference duration: `36.80s`
- Audio fade in: `0.25s`
- Audio fade out: `1.20s`
- Human accepted final family: `R1_MV_v4_final_polish.mp4`
- Human accepted subtitle file: `lyrics_exact_v3_1.srt`

## Segment order｜HARD

```text
S1 你的回应是一直沉默
S2 只剩下落寞
S3 我有什么错
S4 短暂柔情似流星划落
S5 你有没有真的爱过我
S6 我是你诗的哪个段落
S7 落款第几页 / 第几次临摹
S8 还是匆匆一瞥就略过
```

Do not reorder in MODE A.

## Validated production structure

- 8 approved first frames
- 8 dynamic clips
- each source dynamic clip approximately 5s
- final audio approximately 36.8s
- preserve more complete internal actions rather than equally trimming every clip
- selective short overlap / dissolve is preferred over mechanical equal timing

## Baseline timeline reproduction

For the first automated reconstruction attempt:
- treat each S1–S8 clip as up to `5.00s` usable source;
- use short adjacent overlap / dissolve of approximately `0.45s`;
- 7 overlaps reduce ~40.0s raw video to ~36.85s;
- trim / align final render to locked audio duration ~36.80s;
- if source internal cut points require small trim changes, record them explicitly in `timeline.json`.

This is a reproducible engineering baseline, not a command to alter approved directing.

## Golden subtitle text and timing

Exact accepted SRT:

```srt
1
00:00:00,200 --> 00:00:05,120
你的回应是一直沉默

2
00:00:05,200 --> 00:00:08,120
只剩下落寞

3
00:00:08,200 --> 00:00:10,120
我有什么错

4
00:00:10,200 --> 00:00:15,120
短暂柔情似流星划落

5
00:00:15,200 --> 00:00:20,120
你有没有真的爱过我

6
00:00:20,200 --> 00:00:25,120
我是你诗的哪个段落

7
00:00:25,200 --> 00:00:28,120
落款第几页

8
00:00:28,200 --> 00:00:30,120
第几次临摹

9
00:00:30,200 --> 00:00:36,450
还是匆匆一瞥就略过
```

## Subtitle style target

- Chinese light text
- dark semi-transparent rounded rectangle background
- background tightly fits subtitle
- text visually centered horizontally and vertically inside box
- lower safe zone
- maximum 2 lines
- restrained fade only
- no KTV word-by-word highlight in MODE A

Exact font is not a hard equality target if the Codex environment lacks the same font; layout and readability take priority.

## Final polish target

- do not retime approved subtitle timing after alignment passes
- approximately last `0.55s` may gently fade toward black
- preserve original BGM fade
- no additional AI source audio

## Publish-grade source target

Codex mode aims to replace manual watermarked sources with watermark-free HD equivalents.

Preferred:
- 9:16
- >= 1080×1920 when source supports it
- no visible generation / platform watermark

If only 720×1280 is available, record it rather than upscaling and pretending it is native HD.

## Comparison philosophy

MODE A is **not** pixel-identical reproduction because source videos may be replaced by higher-quality watermark-free versions.

Compare:
1. creative invariants
2. segment order
3. audio version / cut
4. timeline structure
5. subtitle text / timing
6. visual source continuity
7. publish-grade technical quality

Do not use SSIM / pixel similarity as the primary pass criterion when source replacement occurs.

## Critical dynamic prompt hard rule for future MODE B

For any character-containing image-to-video prompt, first line must be exactly:

`*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。`

The leading `***` is part of the locked text.
