# Runtime Manifest v3.4

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
| MV专项 | `workflows/mv.md` | `rules/mv_golden_runtime.md`,`rules/mv_audio_timeline.md` + 当前阶段相关Rules | 当前 MV Round `CURRENT_STATE.md`；时间轴阶段加载 `templates/mv_audio_timeline_package_contract.md` + `tools/mv_audio_timeline/*`；Benchmark 按需 |
| HyperFrames解释 | 当前Director/Production模块 | `rules/hyperframes.md`,`rules/visual_core.md` | `templates/hyperframes_scene_contract.md` |
| 分段制作/总装 | `workflows/production.md` | `rules/production_core.md`,`rules/visual_core.md` | 已锁Director/Assets/Audio |
| 发布/数据复盘 | `workflows/publish_review.md` | `rules/account_truth.md` | `03_DATA/*`,`05_IP_ASSETS/PUBLISH_SYSTEM.md` 按需 |
| 规则升级 | `workflows/publish_review.md` | 对应rule文件 | `knowledge/PROMOTION_POLICY.md`,`03_DATA/EXPERIMENTS.md` |

## MV Runtime Rule

MV任务默认先读：
1. `workflows/mv.md`
2. `rules/mv_golden_runtime.md`
3. `rules/mv_audio_timeline.md`
4. 当前 MV Round `CURRENT_STATE.md`
5. 当前阶段 JIT 需要的 Rules / Template / Benchmark。

这 4 个默认入口负责：
- 权威流程；
- 跨Round Golden正确性；
- BGM之后第一个硬节点 `AUDIO_TIMELINE_PACKAGE`；
- 当前项目状态。

R1历史复盘、失败样本、旧Prompt只在排错/规则溯源/回归测试时加载。历史文件不负责正常Runtime继承；需要跨Round保留的经验必须晋升到 Rule / Workflow / Template / Gate。

## MV Audio Timeline JIT Rule

BGM一旦 `BGM_LOCKED`，下一阶段必须加载：
- `rules/mv_audio_timeline.md`
- `templates/mv_audio_timeline_package_contract.md`
- `tools/mv_audio_timeline/package_tool.py`
- 需要强制对齐时再加载/调用 `tools/mv_audio_timeline/run_alignment.py`

时间轴模块的最终 PASS **不得由 Agent 自报**。必须运行：

`python 04_HARNESS/tools/mv_audio_timeline/package_tool.py validate ...`

并得到进程退出码 `0`，同时写出 `package_manifest.json`，才允许设置：
`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`。

任何非零退出码、缺 raw evidence、缺 provenance、音频 SHA 不一致、歌词顺序不一致、任一行 QA 非 PASS 或跨源冲突超阈值：
`AUDIO_TIMELINE_PACKAGE_BLOCKED`。

在 `AUDIO_TIMELINE_PACKAGE_LOCKED = YES` 之前：
- 不进入正式 Natural Beat timing allocation；
- 不进入 Director timing allocation；
- 不进入 Picture Edit；
- 不进入 Subtitle timing/render。

进入剪辑时只做 Package revalidation，不允许剪辑模块临时重新猜时间轴。

## MV Audio Timeline Regression Rule

时间轴工具/规则/Workflow发生修改时，必须运行：

`python 04_HARNESS/tools/mv_audio_timeline/tests/test_package_tool.py`

当前回归套件必须至少覆盖：
- raw evidence缺失 → FAIL；
- diagnostic候选改名exact → FAIL；
- BGM SHA变化 → FAIL；
- repeated lyric occurrence保持顺序；
- LRC offset转换正确；
- 双源时间差超阈值 → FAIL；
- 完整强证据Package → PASS并生成manifest/SRT。

仓库 `.github/workflows/mv-audio-timeline-gate-tests.yml` 负责在相关代码/规则变更时自动运行同一套测试。

## MV Benchmark JIT Rule

`MV_BENCHMARK_LAYER.md` 是 External Knowledge，不是硬规则正文：
- 新 Round：刷新最近7天轻量快照；
- Director：只挑当前歌曲相关3–5个Focused works；
- First-frame：只挑2–3个Beauty references；
- Dynamic：只挑2–3个Director/Action references；
- Final QA：只挑2–3个完成度/市场references。

禁止因为Benchmark作者采用某个做法就直接升级为Locked Rule；必须经过本项目实验和用户验收。

## Legacy Reference Policy

旧Harness/复盘文件默认不参与Runtime。只有：
1. 新模块缺必要细节；
2. 需要追溯规则来源；
3. 做迁移/回归测试；
才加载。

若旧文件与 `rules/*` 冲突，以当前权威 Rule/Workflow 为准，并记录待清理项。

## Context Budget

默认目标：
- 启动层：≤4个核心文件；
- 单模块执行：≤7个核心文件；
- 排错/迁移才扩大上下文。

任何新增文件必须明确属于 Workflow、Rule、Template、Knowledge、State 或 Documentation；无法归类则不要新增。
