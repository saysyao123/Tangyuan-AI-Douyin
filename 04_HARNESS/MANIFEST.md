# Runtime Manifest v3.2

> 用途：决定当前步骤最小加载集合。除非排错，不允许“为了保险把整个仓库都读一遍”。

## Always Load

- `04_HARNESS/SKILL.md`
- `00_CONTROL/CURRENT_STATE.md`

项目级定位只有当前任务涉及定位/边界时才加载：
- `00_CONTROL/MASTER_CONTROL.md`
- `04_HARNESS/rules/account_truth.md`

## Task Load Matrix

| 当前任务 | Workflow | Rules | Template / Data |
|---|---|---|---|
| 选题 | `workflows/topic.md` | `rules/account_truth.md` | `01_TOPIC_SYSTEM/*` 按需 |
| 口播稿 | `workflows/script.md` | `rules/account_truth.md` | `templates/script_contract.md` + 当前Source |
| 录音/ASR/时间轴 | `workflows/audio.md` | `rules/production_core.md` | 当前音频/稿件 |
| 导演表 | `workflows/director.md` | `rules/production_core.md`,`rules/visual_core.md` | `templates/director_segment.md` + 当前时间轴 |
| AI镜头 | 当前Director模块 | `rules/ai_video.md`,`rules/visual_core.md` | `templates/ai_first_frame_prompt.md` |
| MV专项：选歌 / BGM截取 / Hook / 导演 / 首帧 / 动态 / 剪辑 / 歌词 / 终审 | `workflows/mv.md` | `rules/mv_golden_runtime.md`,`rules/ai_video.md` + 当前阶段相关Rules | 当前 MV Round `CURRENT_STATE.md` + `knowledge/MV_BENCHMARK_LAYER.md`；按阶段 JIT 加载 |
| HyperFrames解释 | 当前Director/Production模块 | `rules/hyperframes.md`,`rules/visual_core.md` | `templates/hyperframes_scene_contract.md` |
| 分段制作/总装 | `workflows/production.md` | `rules/production_core.md`,`rules/visual_core.md` | 已锁Director/Assets/Audio |
| 发布/数据复盘 | `workflows/publish_review.md` | `rules/account_truth.md` | `03_DATA/*`,`05_IP_ASSETS/PUBLISH_SYSTEM.md` 按需 |
| 规则升级 | `workflows/publish_review.md` | 对应rule文件 | `knowledge/PROMOTION_POLICY.md`,`03_DATA/EXPERIMENTS.md` |

## MV Runtime Rule

MV任务默认先读：
1. `workflows/mv.md`
2. `rules/mv_golden_runtime.md`
3. 当前 MV Round `CURRENT_STATE.md`
4. 当前阶段明确需要的 Rules / Prompt / Benchmark Snapshot

`mv_golden_runtime.md` 是跨Round的 Golden 运行契约，必须默认参与 Runtime。它只继承经过验证的生产正确性 / 最低质量规则，不复制 R1 的歌曲、视觉世界、人物或镜头清单。

R1历史复盘、失败样本、旧Prompt仍只在排错或规则溯源时加载，禁止默认全读。历史文件不负责运行时继承；需要跨Round继承的关键经验必须先晋升到 `rules/mv_golden_runtime.md`、对应权威Rule或 `workflows/mv.md` 的可验收 Gate。

## MV Benchmark JIT Rule

`MV_BENCHMARK_LAYER.md` 是 External Knowledge，不是硬规则正文：
- S01 / 新 Round：刷新最近 7 天轻量快照；
- Director：只挑当前歌曲相关的 3–5 个 Focused works；
- First-frame：只挑 2–3 个 Beauty references；
- Dynamic：只挑 2–3 个 Director / Action references；
- Final QA：只挑 2–3 个完成度 / 市场 references。

禁止因为 Benchmark 作者采用某个做法，就直接升级为 Locked Rule。必须先经过本项目实验和用户验收。

## Legacy Reference Policy

以下旧文件保留用于追溯，但默认不参与 Runtime：

- `KNOWLEDGE_SCRIPT_HARNESS.md`
- `TOPIC_SELECTION_HARNESS.md`
- `AUDIO_PRODUCTION_HARNESS.md`
- `AI_VIDEO_HARNESS.md`
- `VIDEO_PRODUCTION_HARNESS.md`
- `HYPERFRAMES_EXPLANATION_HARNESS.md`
- `HYPERFRAMES_ASSET_HARNESS.md`
- `HYPERFRAMES_SEMANTIC_TEXT_ANCHOR_ADDENDUM_v1.1.md`
- `DATA_REVIEW_HARNESS.md`

只有以下情况才加载旧文件：
1. 新模块缺少必要细节；
2. 需要追溯某条规则来源；
3. 正在做迁移或回归测试。

若旧文件与 `rules/*` 冲突，以 `rules/*` 为准，并记录待清理项。

## Context Budget

默认目标：
- 启动层：≤ 4个文件
- 单模块执行：≤ 7个核心文件
- 排错/迁移：才允许扩大上下文

任何新增文件都必须回答：它属于 Workflow、Rule、Template、Knowledge、State 还是 Documentation；回答不清则不要新增。