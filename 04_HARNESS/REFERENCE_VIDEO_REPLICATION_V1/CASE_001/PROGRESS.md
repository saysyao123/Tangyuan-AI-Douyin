# CASE_001 — PROGRESS.md

## Current State

```text
ANALYSIS_ARCHITECTURE = PASS
HYPIT_REFERENCE_PARITY = CONDITIONAL_PASS
TIME_AXIS_COMPATIBILITY = PASS
FUNCTIONAL_ACOUSTIC_ALIGNMENT = PASS
HISTORICAL_P1_P2_PARITY = PENDING
REPLICA_DESIGN = PASS
END_TO_END_REPLICATION = PENDING
```

## 已完成

- Reference 基础规格与全片分析；
- Hook / Pause / Reveal / Chapter Interrupt / Stable Host World 拆解；
- Persistent Systems 生命周期；
- Shot 与 Performance Beat 分离；
- 主段视觉运动峰值记录；
- 参考事实 vs Director Interpretation 分离；
- Must Preserve / Optional Surface / Source-specific 分类；
- Hypit 原项目方法对照；
- 中文 P1/P2 时间轴与 `hypit.transcript@1` 兼容方案；
- 67 个视觉 Caption 状态恢复；
- 15 个连续声学块的 Hybrid Acoustic Alignment；
- 650 个中文/数字单位的真实音频参与时间轴；
- Hypit-compatible transcript shape；
- Semantic Caption boundary audit：median 0.060s / P90 0.254s / max 0.340s；
- 一个新 AI 主题的 Replica Blueprint 草案（仅作为结构验证，不代表主题已锁定）。

## Step 1 当前结论

### Functional Acoustic Alignment = PASS

本轮已经得到可以实际驱动：

- 中文逐字/逐词高亮；
- Semantic Moment / Selection；
- Gesture 与 Caption 绑定；
- dense evidence grids；
- Replica timing transfer；

的真实音频参与时间轴。

默认生产版本：`transcript.hybrid.hypit.refined.json`。

### Historical P1/P2 Parity = PENDING

当前 runtime 无 Faster-Whisper / WhisperX / Xingyu CTC 模型权重，且模型下载受网络限制，因此 Hybrid Acoustic Alignment 不得冒充历史 P1/P2 输出。

若未来有可用模型环境，再执行 Faster-Whisper Small → 冲突触发 Xingyu CTC，并与本轮 Hybrid Timeline 做逐字 delta 对比。

## 当前唯一主任务

Step 1 已达到可进入 Replica 实测的功能门槛。

下一步不再继续堆时间轴分析文档，而是由用户与 Director 一起确认 **Step 2：第一条换主题 Replica 应选择什么主题**，随后再建立 Target Brief / Script / Treatment / Seedance Takes / HyperFrames composition。
