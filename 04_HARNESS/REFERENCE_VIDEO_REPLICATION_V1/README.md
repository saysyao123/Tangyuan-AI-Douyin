# Reference Video Replication V1

> Status: ANALYSIS_ARCHITECTURE_PASS / END_TO_END_PENDING_VALIDATION

本目录用于把一条参考视频拆成**可复刻、可换主题、可重新执行**的生产蓝图。

它不是“看视频后写一段提示词”，而是把参考片转成一套可复用的导演语法：

`Reference Video → Evidence → Semantic Analysis → Word/Character Timeline → Transferable Relationships → Target Script → Generation Takes → Deterministic Composition`

## 核心原则

1. **参考真相与目标设计分离**：Reference 只记录原视频实际发生了什么；Brief/Treatment 才定义新视频要做什么。
2. **语义关系优先于复制秒数**：原片秒数用于证据定位；新片视觉事件优先跟随 Script 的 Moment / Selection。
3. **Shot 与 Performance Beat 分离**：固定机位视频里，人物手势、前倾、头部动作可能是主要视觉节奏，不应误判为切镜。
4. **逐词/逐字时间轴是复刻核心基础设施**：文字时间必须能绑定字幕、MG、B-roll、动作和音效。
5. **Hypit 负责视频理解框架；旧 P1/P2 管中文时间真值**：二者组合，而不是互相替代。
6. **动作参考优先保存源片证据**：当动作/摄影机运动是参考片的关键价值时，保留 source excerpt 供 reference-directed generation 使用。
7. **禁止无动力链滑行/漂移**：人物位移必须有可读的抬脚、落脚、蹬地、重心转移或明确的上半身支撑逻辑。

## 文件结构

```text
REFERENCE_VIDEO_REPLICATION_V1/
├── README.md
├── REFERENCE_VIDEO_REPLICATION_HARNESS.md
├── HYPIT_PARITY_AUDIT.md
├── TIME_AXIS_ADAPTER.md
├── VALIDATION_PLAN.md
└── CASE_001/
    ├── ANALYSIS.md
    ├── TIMELINE.md
    ├── SYSTEMS_AND_PERFORMANCE.md
    └── PROGRESS.md
```

## 当前结论

本轮已经证明：

- 参考视频理解架构成立；
- 按 Hypit 的 `ANALYSIS.md + TIMELINE.md` 思路可以形成可迁移的导演模型；
- 我们旧的 Faster-Whisper Small + trusted-text mapping + Xingyu CTC P2 可以作为 Hypit `hypit.transcript@1` 的时间轴后端；
- 当前还缺两个最终验证：
  1. 在 CASE_001 上真正跑出完整逐词/逐字时间轴；
  2. 换一个新主题，完整生成至少一套 Seedance Takes + HyperFrames/Studio 合成。

完成这两项后，才把状态升级为 `REFERENCE_REPLICATION_PIPELINE_V1 = VALIDATED`。

## 不进入 GitHub 的内容

- 原参考视频本体；
- 大体积证据视频/音频；
- 模型缓存；
- 账号、API Key、Cookie 或任何凭据。

这些只在本地/项目资产目录保存，GitHub 中保留方法、结构、时间轴、分析和可复用规则。