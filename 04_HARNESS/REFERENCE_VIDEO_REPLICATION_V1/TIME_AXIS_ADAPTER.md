# TIME_AXIS_ADAPTER.md — Hypit + 中文 P0/P1/P2 时间轴

## 为什么组合，而不是替换

Hypit 需要真实的 word boundaries，才能把 Caption、MG、B-roll、Effect 和语义 Selection 绑定到实际讲话。

我们此前的中文链路解决的是另一件事：当脚本/歌词已经可信时，不让 ASR 自己决定“正确文字”，而把 ASR/CTC 用来测量**可信文字在音频中的真实位置**。

因此：

- Hypit 负责 Reference Understanding + Semantic Timing；
- P1/P2 负责中文逐词/逐字时间真值。

---

## 历史已验证基线

此前项目中：

- P1：Faster-Whisper Small，`zh`，CPU int8，word timestamps；出现过 median line-start delta ~0.240s、max ~0.740s，因此触发 P2。
- P2：Xingyu CTC trusted-text forced alignment；已有记录达到约 median ~0.047s / max ~0.183s，另一轮锁定记录约 ~0.036s / ~0.082s。

这些是旧项目的历史基线，不代表新视频的实际测量。

---

## 决策树

### Case A — 文字未知

```text
Reference Video
↓
WhisperX / ASR
↓
Recovered Transcript + Word Time
↓
人工/视觉校正名称和明显识别错误
↓
Reference Timeline
```

若后续得到可信全文，且需要更精确中文时间，可再进入 P2。

### Case B — 有可信字幕 / 脚本

```text
Trusted Text
+
Exact Audio
↓
P1 Faster-Whisper Small
  language=zh
  compute_type=int8
  word_timestamps=True
↓
NFKC / punctuation / whitespace normalization
↓
Monotonic trusted-text mapping
↓
Quality Gate
↓
冲突是否超阈值？
  NO → lock
  YES → P2 Xingyu CTC forced alignment
↓
Word / Character Timeline Truth
```

历史上可使用 0.50s 作为 cue/line 级 hard conflict 触发参考值，但新项目应允许按任务调整。

---

## 推荐中间格式

```json
{
  "language": "zh",
  "audio_seconds": 108.5,
  "words": [
    {
      "text": "为",
      "start": 0.52,
      "end": 0.68,
      "score": 0.95
    }
  ]
}
```

中文可保留逐汉字 timing unit；Caption 层再按语义短语组合，不必把一个字做成一个 Caption Cue。

---

## Hypit 输出兼容格式

```json
{
  "format": "hypit.transcript@1",
  "source": "references/reference-001/source.mp4",
  "language": "zh",
  "audio_seconds": 108.5,
  "passages": [{
    "text": "...",
    "start_seconds": 0.52,
    "end_seconds": 108.2,
    "words": [
      {
        "text": "为",
        "start_seconds": 0.52,
        "end_seconds": 0.68,
        "score": 0.95
      }
    ]
  }]
}
```

Hypit 后续只需要消费这一统一时间轴，因此 alignment backend 可以替换，而不会破坏后面的证据网格和语义分析。

---

## Quality Gate

锁定 transcript 前至少检查：

- start/end 单调；
- 不允许 end < start；
- trusted text coverage 足够高；
- 连续讲话内没有无法解释的长空白；
- 已知 silence 区基本无错误词；
- 视觉字幕切换与附近 aligned phrase 基本一致；
- 识别词与可信文字冲突时，不得悄悄改写可信文字；
- 大局部漂移必须触发 P2 或人工检查。

---

## Reference 与 Target 的不同

### Reference

如果没有可信全文：先 ASR 恢复文字，再建立时间轴。

### Target

目标片 Script 本身就是唯一可信 verbal authority，因此生成 Take 后直接：

```text
Target Script
+
Generated Take Audio
↓
P1
↓
必要时 P2
↓
真实逐词/逐字位置
↓
Caption / MG / B-roll / Effect 自动跟随
```

这通常比 Reference 对齐更稳定，也是本 Harness 最重要的生产价值之一。