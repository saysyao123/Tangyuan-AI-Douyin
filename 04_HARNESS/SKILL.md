# Tangyuan Douyin Runtime Skill v3.1

> 角色：薄运行入口（Router），不是完整SOP。默认只读取本文件 + `MANIFEST.md` + 当前任务所需模块。

## 目标

把「汤圆AI实战」日更生产拆成可独立修改、独立验收、按需加载的模块，避免把流程、规则、模板、经验、状态堆进一个大SKILL。

## Runtime原则

1. **JIT Context**：只加载当前步骤需要的文件。
2. **Single Source of Truth**：同一硬规则只能有一个权威来源。
3. **State Externalized**：项目进度只从 Canonical State / 当前项目 durable state 读取。
4. **Workflow != Rule != Template != Knowledge != Executor**：不同层级禁止混写。
5. **Contract First**：模块只通过明确输入/输出接口连接。
6. **Executor First**：进入当前 Stage 后，必须先从 `runtime/mv_stage_executor_registry.json` 解析已有执行路径；不得从 Rule 直接跳到新建工具/模型/Workflow。
7. **Patch, Don't Cascade**：局部问题只修改对应模块；已锁定上游不连带重写。
8. **Gate Before Next**：当前步骤未通过验收，不进入下一步。

## 启动顺序

每次新对话 / Codex 执行：

```text
1. 读取 04_HARNESS/SKILL.md
2. 读取 04_HARNESS/MANIFEST.md
3. 读取当前 Canonical / project state
4. 如果是 MV：读取 runtime/mv_stage_registry.json + runtime/mv_stage_executor_registry.json
5. 根据当前 Stage 解析 registered executor
6. 加载对应 workflow + rules + template + existing tools / prior PASS sample
7. 先做 dependency doctor/check，再执行当前模块
8. 按模块 Output Contract 验收
9. 只在需要时加载下一模块
```

不要默认全文读取：
- `04_HARNESS/*_HARNESS.md`
- `05_IP_ASSETS/VISUAL_SYSTEM.md`
- `05_IP_ASSETS/HYPERFRAMES/IP_VISUAL_SYSTEM.md`
- 历史 Day 文件

这些属于参考/历史资产，只有 MANIFEST、Executor Registry 或当前任务明确需要时才读取。

## Executor First｜HARD

对于 MV：

`Runtime tells WHAT -> Executor Registry tells HOW -> Rule tells constraints -> Tool/Capability executes`。

禁止：
- 因 Rule 提到一个外部开源实现就自动安装；
- 因当前 Stage 没有 Python 脚本就认定“流程没实现”；
- 未检查已有 canonical tool / prior PASS / workflow 就创建 helper；
- 把 slot-specific 实验脚本放进 core `tools/`；
- 把 stage-specific 实验 job 挂进 authoritative Runtime Bridge；
- 每个项目重复下载已经锁定的生产模型。

缺依赖时执行 registered dependency policy：先 doctor/cache，必要时 BLOCK；只有明确允许才做独立环境 setup。

权威细节：
- `rules/mv_executor_first.md`
- `runtime/mv_stage_executor_registry.json`

## 路由

- 选题 → `workflows/topic.md`
- 口播稿 → `workflows/script.md`
- 真人录音/ASR/时间轴 → `workflows/audio.md`
- 导演表/视觉职能/素材覆盖 → `workflows/director.md`
- 分段制作/QA/总装 → `workflows/production.md`
- 发布/数据/规则升级 → `workflows/publish_review.md`
- MV → `workflows/mv.md` + Canonical Runtime + MV Executor Registry

特殊能力：
- AI首帧/5秒图生视频 → `rules/ai_video.md`
- HyperFrames逻辑解释 → `rules/hyperframes.md`

## 冲突优先级

```text
用户当前明确指令
> Canonical Runtime / approved project change
> registered Stage Executor contract
> 04_HARNESS/rules/*
> 00_CONTROL/MASTER_CONTROL.md
> 参考资料 / 历史Harness / 旧Day经验
```

任何经验不得仅因“看起来有效”自动升级为规则。规则升级见 `knowledge/PROMOTION_POLICY.md`。

## 完成定义

一个模块只有同时满足以下条件才算完成：
- 输入来源明确
- registered executor 已解析
- 未绕过已有执行路径
- 输出符合 Contract
- 对应 Gate 通过
- 未擅自修改锁定上游
- 新经验已放入正确层级，而不是直接塞进本SKILL
