# EXPERIMENTS

> 本文件记录尚未达到长期规则资格的假设。

## EXP-001｜统一内容定位是否提高关注转化
状态：ONGOING

## EXP-002｜固定发布时间控制变量
状态：ONGOING

## EXP-003｜Day1 114.726秒长视频

Hypothesis：
较完整的真实故事可能建立更强信任，但也可能明显降低完播。

Status：
`PERFORMANCE_PENDING`

Observe：
- 3s retention（如可见）
- Avg Watch Time
- Completion Rate
- Follows / 1000 views

## EXP-004｜AI电影Hook + 真实证据主体

Day1结构：

AI Hook
→ Real Evidence / Remotion
→ AI + Real Outro

Status：
`PERFORMANCE_PENDING`

不能因为制作效果好就复制到每天。

## EXP-005｜Day2效率模式

Day2计划：

- 45–65秒
- 5–7段
- Evidence + Remotion为主
- AI动态0–1
- ≤180分钟

目标：

验证能否在不明显降低质量的情况下回到可持续日更生产时间。

Status：
PLANNED

---

## EXP-MV-001｜Single-shot Cinematic Camera Library

Status: `PLANNED_FOR_R2`

### Hypothesis

5秒单镜动态不应该默认退化为：

`人物站立 + 慢推 + 发丝/衣摆轻动`

如果建立一组 Seedance 可执行的电影摄影机语法库，可以在不强制三镜的情况下提高导演多样性。

### Candidate camera grammars to test

按小样逐个验证，不一次全部加入正式MV：
- lateral tracking / lateral reveal；
- foreground parallax pass；
- pedestal rise / fall；
- crane-like rise / descend；
- low-angle tracking；
- arc / small orbit around object or subject；
- motivated push / pull；
- rack-focus-led reframing；
- camera lowering to surface / waterline；
- event-driven tilt / pan；
- foreground wipe / solid-edge occlusion；
- subject-relative movement where camera and subject move at different speeds。

### Measure

每种语法至少记录：
- Seedance是否正确执行；
- 首帧一致性；
- 角色稳定；
- 画面美感损失；
- 是否易出现穿模 / 背景扭曲；
- 是否适合普通Beat / 高潮Beat；
- 是否值得进入后续 Camera Library。

### Promotion Gate

不能因为某种运镜“电影里常见”或“某导演常用”就升级为规则。
必须经过实际生成 + 用户验收。

---

## EXP-MV-002｜Codex Douyin BGM Datasource Hardening

Status: `DEFERRED_TO_CODEX_COMPUTER`

Target chain:

`Creator Center / benchmark discovery -> exact music_id -> exact version -> related aweme evidence -> audio/reference preview -> build-time availability -> publish-time availability`

R1手工版暂时采用：
`~5个MV/音乐观察源 -> 近30天歌曲 -> 真实视频链接 -> 用户选歌`

The manual path remains usable until this experiment proves a better automated replacement.

---

## EXP-MV-003｜Whisper Forced Lyric Alignment in Codex

Status: `PLANNED`

R1 already proved the rule that subtitle timing must come from locked audio, not edit-segment timing.

This experiment is only for automation quality:

`Whisper word timestamps -> known-lyrics constraint / correction -> SRT/ASS -> human spot-check`

Measure:
- phrase-start error;
- phrase-end error;
- handling of sustained notes;
- repeated words;
- instrumental gaps;
- consistency with reliable same-version LRC when available.

---

## EXP-MV-004｜Watermark-free HD Source Replacement in Codex

Status: `PLANNED`

R1 manual files can contain visible generation/platform watermarks.

Goal:
- Codex obtains watermark-free HD equivalents;
- source replacement preserves approved edit timing, subtitles, transitions and crop;
- no creative re-edit should be required only to remove watermark.

This is an asset-pipeline experiment, not a director-quality experiment.

---

## EXP-MV-005｜Advanced Lyric Effects

Status: `NOT_STARTED`

Base subtitle system is already stable enough for R1.
Only test advanced effects after timing remains accurate:
- limited word emphasis;
- key-phrase motion;
- local gradient darkening;
- small position changes tied to composition.

Do not replace the stable base lyric system until a variant clearly improves readability / emotion without competing with the image.