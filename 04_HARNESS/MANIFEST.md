# Runtime Manifest v3.6

> 用途：决定当前任务的最小加载集合。除非排错、迁移或规则溯源，不允许“为了保险把整个仓库都读一遍”。

## Always Load

- `04_HARNESS/SKILL.md`
- 当前任务的 durable state / current slot state

项目级定位只有当前任务涉及定位/边界时才加载：
- `00_CONTROL/MASTER_CONTROL.md`
- `04_HARNESS/rules/account_truth.md`

## Task Load Matrix

| 当前任务 | Workflow | Rules / Runtime | Template / Data |
|---|---|---|---|
| 选题 | `workflows/topic.md` | `rules/account_truth.md` | `01_TOPIC_SYSTEM/*` 按需 |
| 口播稿 | `workflows/script.md` | `rules/account_truth.md` | `templates/script_contract.md` + 当前 Source |
| 录音/ASR/时间轴 | `workflows/audio.md` | `rules/production_core.md` | 当前音频/稿件 |
| 导演表 | `workflows/director.md` | `rules/production_core.md`,`rules/visual_core.md` | `templates/director_segment.md` + 当前时间轴 |
| AI镜头 | 当前 Director / MV 模块 | `rules/ai_video.md` JIT | 当前实际 Reference / K0 |
| MV专项 | `workflows/mv.md` | `rules/mv_golden_runtime.md` + `runtime/mv_macro_phase_registry.json` + Canonical Runtime | 当前 slot state；按当前 Macro Phase JIT |
| HyperFrames解释 | 当前 Director/Production 模块 | `rules/hyperframes.md`,`rules/visual_core.md` | `templates/hyperframes_scene_contract.md` |
| 分段制作/总装 | `workflows/production.md` | `rules/production_core.md`,`rules/visual_core.md` | 已锁 Director/Assets/Audio |
| 发布/数据复盘 | `workflows/publish_review.md` | `rules/account_truth.md` | `03_DATA/*`,`05_IP_ASSETS/PUBLISH_SYSTEM.md` 按需 |
| 规则升级 | `workflows/publish_review.md` | 当前权威 Rule | `knowledge/PROMOTION_POLICY.md`,`03_DATA/EXPERIMENTS.md` |

## MV Minimal Runtime

MV 默认启动只需要：
1. `workflows/mv.md`
2. `rules/mv_golden_runtime.md`
3. `runtime/mv_macro_phase_registry.json`
4. 当前 slot 的 Canonical `CURRENT_STATE.json`

底层合法状态与前置条件由以下机器权威负责，不需要在聊天上下文中重复背诵：
- `runtime/mv_stage_registry.json`
- `runtime/mv_transition_contract.json`
- `runtime/mv_human_gate_registry.json`
- `runtime/mv_artifact_registry.json`
- `tools/mv_runtime_*.py`

## MV Macro Phase JIT

### AUDIO
按实际任务加载：
- 版本发现：`rules/mv_bgm_discovery.md`
- BGM 锁定后时间真值：`rules/mv_audio_timeline.md`
- 时间轴实现细节、环境锁和回归：`tools/mv_audio_timeline/README.md` + 对应 tool/test

不要在 Manifest 复制具体 Python 版本、模型版本、命令和逐项 Gate 逻辑；这些由工具目录自身维护。

### DIRECT
按需要加载：
- `rules/mv_first_frame_qa.md`
- 当前实际 Reference / K0
- AI Reference / I2V 时才加载 `rules/ai_video.md`
- Benchmark 只挑当前歌曲相关少量参考

### GENERATE
按当前 source 风险加载：
- `rules/ai_video.md`
- 多镜/隐藏切镜被证明时：`rules/mv_source_normalization.md`
- WEB source cleanup 需要时：`rules/mv_web_source_roughcut.md`

### EDIT
按需要加载：
- `rules/mv_editing.md`
- 字幕阶段才加载 `rules/mv_subtitle.md`

### DELIVER
默认依赖 Canonical Runtime / artifact validators；只有具体技术异常时加载对应 Rule / Tool。

## Human Gate JIT

人类 Gate 的机器结构以 `runtime/mv_human_gate_registry.json` 为准。
只有需要准备用户判断或异常升级时才加载 `rules/mv_human_gates.md`。

## Benchmark / Knowledge JIT

`knowledge/*` 是外部知识与实验层，不是 Runtime 默认上下文。
- 新模型/新 Provider：只加载与当前假设有关的实验记录；
- Director：少量 focused references；
- First-frame / Dynamic：只加载与当前视觉风险相关的参考；
- 历史成功 Prompt 不自动成为当前 Prompt 依赖。

任何 Benchmark / Lesson 想进入长期 Rule，必须走 `knowledge/PROMOTION_POLICY.md`。

## Legacy Reference Policy

旧 Harness、Round、Prompt、QA 报告、Receipt 默认不参与正常 Runtime。
只有以下情况读取：
1. 排错；
2. 迁移；
3. 规则来源追溯；
4. 回归测试。

若旧文件与当前 Canonical Runtime / Rule 冲突，以当前权威层为准。

## Context Budget

默认目标：
- 启动：≤4 个核心文件；
- 正常单任务：优先 ≤5 个核心文件；
- 只有异常、迁移、研究时扩大上下文。

新增文件前必须能明确回答：它属于 Workflow、Rule、Template、Knowledge、State、Tool 还是 Documentation。无法归类或不能改变执行结果/保留必要证据时，优先不新增。
