# LOCKED_RULES｜Rule Registry v3.0

> 本文件从“规则正文集合”改为**规则注册表**。规则正文只存在于 `04_HARNESS/rules/*`，避免同一规则复制多份。

## Active Rule Sources

### Account / Truth / Content Boundary
权威文件：`04_HARNESS/rules/account_truth.md`

覆盖：账号、第一季、真实性、内容边界、发布实验纪律、提问规则。

### Production Core
权威文件：`04_HARNESS/rules/production_core.md`

状态：`PRODUCTION_VALIDATED`

覆盖：真实音频先于时间轴、独立ASR、唯一Master Narration、高清Source、镜头运动、Segment Lock、四层QA、准确数字、Artifact Verify、Material Coverage、Evidence Integrity。

### Visual Core
权威文件：`04_HARNESS/rules/visual_core.md`

状态：`PRODUCTION_VALIDATED`

覆盖：9:16、视觉职能路由、字幕与容器居中、手机可读、小字删除、镜头运动、Evidence、Anti-Homogeneity。

### AI Video
权威文件：`04_HARNESS/rules/ai_video.md`

覆盖：AI使用Gate、首帧、5秒稳定图生视频、QA与音轨处理。

### HyperFrames
权威文件：`04_HARNESS/rules/hyperframes.md`

覆盖：Logic Motion适用范围、Teaching Truth、Anchor/Variable/Consequence、Signature Move、Anti-PPT、竖屏与Hierarchy。

## Validation Levels

- `PRODUCTION_VALIDATED`：制作稳定性规则，可由重复生产/技术验证升级。
- `PERFORMANCE_VALIDATED`：增长/平台表现规律，必须重复真实发布数据验证。

单条结果默认进入 `03_DATA/EXPERIMENTS.md`，不得直接升级长期规则。

升级/废止流程：`04_HARNESS/knowledge/PROMOTION_POLICY.md`。
