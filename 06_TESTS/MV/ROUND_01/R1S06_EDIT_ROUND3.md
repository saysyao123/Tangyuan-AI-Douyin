# R1S06｜Edit Round 3｜Lyrics System

## Base
- locked base edit: `R1_MV_second_cut_v2.mp4`
- duration: `36.833s`
- do not change Round-2 picture timing in this round.

## Hard rule｜portrait-safe prompt prefix

For **every dynamic-video prompt that contains a human / human-like character reference image**, the following line must appear at the very beginning **exactly with the leading `***` preserved**:

`*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。`

The leading `***` is part of the production prompt and must not be removed during rewriting, formatting, normalization, prompt compression, or Codex transfer.

## Round-3 goal
Keep the approved Round-2 picture rhythm intact and add only:
1. lyric timing;
2. a restrained lyric visual system;
3. minimal finishing polish.

## Lyric visual system v1
- 9:16 / 720×1280 current source.
- single lyric phrase at a time.
- centered horizontally.
- lower safe area around y≈1010.
- bold clean Simplified-Chinese sans serif.
- near-white text.
- dark semi-transparent rounded rectangle sized to text only.
- all text centered vertically and horizontally in its box.
- short ~0.1s fade-in / ~0.15–0.2s fade-out.
- no karaoke word-by-word highlighting in this first lyric pass.
- no decorative English, no extra small text, no lyric duplication.

## Working lyric timing v1
- 00:00.35–00:04.15 `你的回应是一直沉默`
- 00:04.75–00:08.55 `只剩下落寞`
- 00:09.20–00:13.25 `我有什么错`
- 00:13.85–00:18.00 `短暂柔情似流星划落`
- 00:18.35–00:22.45 `你有没有真的爱过我`
- 00:22.95–00:27.05 `我是你诗的哪个段落`
- 00:27.45–00:29.65 `落款第几页`
- 00:29.70–00:31.65 `第几次临摹`
- 00:31.95–00:36.10 `还是匆匆一瞥就略过`

## QA
- no text overflow;
- no lyric box covering principal eye/action anchors in sampled frames;
- Round-2 picture edit remains unchanged;
- lyric box remains visually subordinate to the cinematography;
- this is review v1, not yet Golden Sample lock.

## Next
Human review of Round-3 lyric edit. If passed, proceed to final timing/polish rather than redesigning the entire subtitle system.
