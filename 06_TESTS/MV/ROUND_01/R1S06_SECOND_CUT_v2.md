# R1S06｜Second Cut v2

## Locked character prompt prefix

All future character-related dynamic prompts must start **verbatim** with:

```text
*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。
```

The leading `***` is mandatory and part of the prompt-weighting convention validated by the user.

## Second-cut objective

User approved first-cut direction and requested a second refinement pass.

Second cut intentionally does **not** add lyrics/subtitles yet. It focuses on preserving the generated internal camera grammar and improving continuity.

## Edit strategy

- final reference audio: `36.832653s`
- segment order: `S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 -> S8`
- each source dynamic is preserved at approximately the full `5.0s` rather than aggressively trimming the tail;
- seven short overlaps compress `40.0s` source coverage back to the locked `36.832653s` audio;
- overlap / dissolve duration: approximately `0.452478s` per boundary;
- purpose: preserve S3/S5/S7 multi-shot endings, S4 meteor after-effect, S6 paper-space motion and S8 cold-release tail while smoothing scene boundaries.

## Generated artifact

`R1_MV_second_cut_v2.mp4`

User review pending.

## Next, only if v2 direction passes

1. refine individual cut boundaries / transition lengths where needed;
2. add lyric subtitle system aligned to the locked BGM;
3. build first publishable edit candidate;
4. separately create a cinematic single-shot camera-move test library so future one-shot segments do not default to slow push-ins.
