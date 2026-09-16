# CASE_001 — PROGRESS.md

## Current State

```text
ANALYSIS_ARCHITECTURE = PASS
HYPIT_REFERENCE_PARITY = PASS_EXCEPT_REAL_ALIGNMENT
TIME_AXIS_COMPATIBILITY = PASS
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
- 一个新 AI 主题的 Replica Blueprint。

## 当前硬缺口

### 1. Reference 真实逐词/逐字时间轴尚未实际跑完

当前执行环境缺少已缓存的 Faster-Whisper / Xingyu runtime，并且无法稳定联网下载模型，因此没有伪造 word timestamps。

### 2. 还没有完成新主题 End-to-End 生成

仍需：

- Character / World Anchor；
- 一组 Seedance Takes；
- Target Script P1/P2 alignment；
- HyperFrames/Studio composition；
- final MP4；
- Reference vs Target relationship audit。

## Next Action

优先级：

1. 在已有 Faster-Whisper Small 的环境运行 P1；
2. 质量门失败则运行 P2 Xingyu CTC；
3. 转成 `hypit.transcript@1`；
4. 用逐词标签重做关键 evidence grids；
5. 更新 CASE_001 Timeline，使 Performance Beat 绑定 exact phrase；
6. 再开始新主题生成验证。

## 不应继续做的事情

在真实 word time 未跑出来之前，不继续堆更多描述文档；下一阶段应以实测 alignment 和 generation proof 为主。