# CHANGELOG

## v3.0 — 2026-08-20

### Thin Skill Architecture
- 新增 `04_HARNESS/SKILL.md` 作为唯一薄运行入口。
- 新增 `04_HARNESS/MANIFEST.md`，按任务执行 JIT Context 加载。
- 将运行职责拆为 `workflows/`、`rules/`、`templates/`、`knowledge/`、`tests/`。
- `LOCKED_RULES.md` 从规则正文集合改为 Rule Registry，规则正文迁入 `04_HARNESS/rules/*`。
- `MASTER_CONTROL.md` 缩为长期项目合同，不再承载详细生产流程。
- 新增 Input / Output Contract 与模块级回归测试规范。
- 新增 Knowledge → Rule Promotion Policy，单次经验不再直接写入SKILL。
- README、PROJECT_MANIFEST、CODEX入口切换至v3 Runtime。
- 原大型 `*_HARNESS.md` 暂时保留为 Legacy Reference，默认不参与运行上下文。
- 新增 `docs/ARCHITECTURE_V3.md` 与 `docs/MIGRATION_V3.md`。

## v2.0 — 2026-08-16

### Day1正式进入发布后阶段
- Day1状态改为 `PUBLISHED_METRICS_PENDING`
- 最终技术成片记录为约114.726秒
- 开始1h / 3h / 24h性能数据周期

### Production System
- VIDEO_PRODUCTION_HARNESS升级至v2.0
- 新增AUDIO_PRODUCTION_HARNESS
- 新增AI_VIDEO_HARNESS
- 建立Production / Performance双验证制度
- 建立4层QA
- 建立Artifact Verify
- 建立Segment Lock
- 建立高清Source / Motion Asset区分
- 建立Anti-Homogeneity Gate

### Visual / Publish
- VISUAL_SYSTEM升级至v1.0
- 新增PUBLISH_SYSTEM v1.0
- 固化Day1实测字幕默认系统
- 固化系列封面/标题/标签结构，但不把Day1单次表现当增长规律

### Daily Archive
- Day文件夹新增PRODUCTION/
- 完成Day1生产归档文件
- 新增Day2启动包

### Efficiency
- Day2开始执行≤3小时生产预算
- 不在每天生产中重新发明字幕、封面、标签、QA基础规则
