# CASE_001 — STEP 1 Alignment Report — 2026-09-16

## Result

```text
FUNCTIONAL_ACOUSTIC_ALIGNMENT = PASS
HYPIT_TRANSCRIPT_SHAPE = PASS
HISTORICAL_P1_P2_PARITY = PENDING
```

本轮已把参考视频从“视觉 Caption 时间轴”升级为**真实音频参与的中文逐字/逐词时间轴**，并输出 Hypit 可读取的 `hypit.transcript@1` 结构。

但当前运行环境没有 Faster-Whisper / WhisperX / Xingyu CTC 模型权重，且外部模型下载受网络限制，因此本轮结果明确标记为 `Tangyuan Hybrid Acoustic Fallback v2`，**不得冒充 P1 Faster-Whisper 或 P2 Xingyu CTC 的正式输出**。

## Source

- reference video: `下载 (4).mp4`
- duration: `108.500s`
- analysis audio: `16 kHz / mono / PCM`
- recovered visual Caption states: `67`（opening 2 + main 65）

## Trusted text preparation

Caption 视觉文字作为 trusted text 候选，但显示文本与口语投影分开：

- 去除 Caption handoff 造成的边界重复，例如 `驻` / `进`；
- 两个明显同音显示错误在 spoken projection 中归一：`10弹 → 实弹`、`通天带 → 通天代`；
- 原始显示证据保留，不覆盖 Reference Truth。

## Acoustic alignment method

67 个 Caption 状态不被硬当作 67 个声学句子，而是合并为 `15` 个连续声学块。

每块执行：

1. 从原视频 16 kHz 音轨取得真实语音；
2. 生成普通话参考发音；
3. 提取 MFCC + delta；
4. 执行 monotonic global DTW；
5. 将中文字符 / 数字 lexical unit 投影到真实音频时钟；
6. 保留 Raw transcript；
7. 另输出 minimum 40 ms 的 monotonic refined transcript，供生产使用。

## Scale

- alignment blocks: `15`
- aligned spoken units: `650`
- median unit duration: `0.150s`
- P05–P95: `0.070–0.250s`
- Raw pathological short units: `6`
- Refined minimum unit duration: `0.040s`
- Refined maximum unit duration: `0.460s`

## Semantic Caption boundary audit

不是比较“附近任意一个字边界”，而是按每个 Caption 实际贡献的文字，找到该语义序列的最后一个声学单位，再与原视频 Caption handoff 比较。

结果：

- median absolute delta: `0.060s`
- P90 absolute delta: `0.254s`
- max absolute delta: `0.340s`
- within ±0.10s: `70.1%`
- within ±0.20s: `85.1%`

该结果说明 Hybrid Acoustic Timeline 已足以支持：中文逐字高亮、语义 Moment/Selection、Gesture 与 Caption 绑定、参考视频 dense evidence grids，以及下一阶段 Replica Blueprint 的真实时间驱动。

## Production decision

后续测试默认使用：

`transcript.hybrid.hypit.refined.json`

Raw 声学结果只作为证据保留。

## Remaining methodological gap

若要求与历史 Tangyuan P1/P2 完全同方法复现，仍需：

1. 在可用模型环境运行 Faster-Whisper Small + trusted-text mapping；
2. 对冲突段运行 Xingyu CTC；
3. 将结果与 Hybrid v2 做逐字 delta 对比；
4. 只有通过后，才能标记 `P1_PASS / P2_PASS`。

这不阻止当前 Reference Replica 项目进入下一阶段，但在方法论审计中应继续保留 `HISTORICAL_P1_P2_PARITY = PENDING`。
