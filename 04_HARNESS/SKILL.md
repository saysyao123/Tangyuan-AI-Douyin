# Tangyuan Douyin Runtime Skill v3.1

> 角色：薄运行入口（Router），不是完整 SOP。默认只读取本文件 + `MANIFEST.md` + 当前任务需要的最小上下文。

## 目标

把生产系统拆成可独立修改、独立验收、按需加载的模块；让复杂性留在 Harness 内部，而不是长期堆进 Agent 上下文。

## Runtime 原则

1. **JIT Context**：只加载当前任务真正需要的文件。
2. **Single Source of Truth**：同一硬事实只能有一个权威来源。
3. **State Externalized**：MV 进度以 Canonical Runtime state/transition 为准；其他项目使用其明确的 durable state，不以聊天记忆代替。
4. **Workflow != Rule != Template != Knowledge != State**：不同职责禁止混写。
5. **Contract First**：模块只通过明确输入/输出接口连接。
6. **Patch, Don't Cascade**：局部问题只修最近根因；已锁定上游不无故重开。
7. **Outcome over paperwork**：文档、Gate、QA 只在会改变下一动作或保留必要证据时存在。
8. **Evidence before rule**：单次成功/失败先进入 Knowledge/Experiment，不直接升级长期 Rule。

## 启动顺序

```text
1. 读取 04_HARNESS/SKILL.md
2. 读取 04_HARNESS/MANIFEST.md
3. 定位当前任务 durable state
4. 根据 MANIFEST 加载当前 workflow / rule / template / tool
5. 执行当前合法动作
6. 由对应 Validator / Runtime 验证结果
7. 只在需要时加载下一模块
```

不要默认全文读取：
- `04_HARNESS/*_HARNESS.md`
- 历史 Round / Day / Retrospective
- 历史 Prompt 版本
- 大型 Visual / Benchmark / Knowledge 文件

它们只在排错、迁移、规则溯源或当前任务明确需要时加载。

## MV 特例：Macro Phase 只负责认知压缩

MV 的 Canonical Runtime 仍由：
- `runtime/mv_stage_registry.json`
- `runtime/mv_transition_contract.json`
- `runtime/mv_human_gate_registry.json`
及对应 Runtime tools 强制执行。

Agent / 用户默认只需要理解：
`AUDIO -> DIRECT -> GENERATE -> EDIT -> DELIVER`。

映射见：`runtime/mv_macro_phase_registry.json`。

Macro Phase 不能绕过、合并或伪造底层 Stage / Human Gate；它只是从 Canonical stage 派生出的轻量视图。

## 常规路由

- 选题 → `workflows/topic.md`
- 口播稿 → `workflows/script.md`
- 真人录音/ASR/时间轴 → `workflows/audio.md`
- 导演表/视觉职能/素材覆盖 → `workflows/director.md`
- 分段制作/QA/总装 → `workflows/production.md`
- MV → `workflows/mv.md`
- 发布/数据/规则升级 → `workflows/publish_review.md`

特殊能力按 MANIFEST JIT 加载，不在本文件复制实现细节。

## 冲突优先级

```text
用户当前明确指令
> Canonical Runtime / 当前项目已批准 durable state
> 当前权威 Workflow / Rule / Contract
> 项目控制文件
> Knowledge / Retrospective / 历史 Harness
```

任何经验不得仅因“看起来有效”自动升级为规则。规则生命周期见 `knowledge/PROMOTION_POLICY.md`。

## 完成定义

一个模块完成至少要求：
- 输入来源明确；
- 输出满足当前 Contract；
- 必要 Validator / Runtime PASS；
- 未擅自修改锁定上游；
- 新经验进入正确层级，而不是继续膨胀 SKILL。
