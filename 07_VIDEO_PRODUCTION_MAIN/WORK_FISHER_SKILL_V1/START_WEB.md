# START_WEB — Work-Fisher 当前主视频流程

请使用 GitHub 仓库 `saysyao123/Tangyuan-AI-Douyin` 的 `main` 分支，进入目录 `07_VIDEO_PRODUCTION_MAIN/WORK_FISHER_SKILL_V1`。

## 必须按顺序读取
1. `README.md` 与 `WORKFLOW.md`
2. `original/korean-thriller-asset-to-video/SKILL.md`
3. `original/korean-thriller-asset-to-video/references/video-contract.md`
4. `original/korean-thriller-asset-to-video/references/image-assets.md`、`asset-continuity.md`、`worked-example.md`、`flashback-example.md`
5. `SOURCE_MANIFEST.md`：核实原版参考文档是否齐全；当前缺完整50情绪原版时，加载 `derived/EMOTION_QUICK_INDEX_50.md` 作为明确标注的速查替代
6. `QA.md` 与 `state/PROJECT_STATE_TEMPLATE.json`

**优先规则**：这套 Work-Fisher Skill 是当前新视频生成项目的默认主方案。保持原版三阶段的导演逻辑、确认要求、资产编号、角色和场景一致性、A/B机位规则、Speaker声线、固定五字段；不得提前重构、把示例当成真实产物，或跳过应检视的图像。

## 执行方式
- 用户上传小说/剧本时，先实际阅读并提取原文能支持的关键剧情、角色与冲突；针对用户要求选择可影视化的片段。长书优先制作小范围真实样片，不冒称已改编全书。
- 第一轮只输出**角色中文生图提示词**，等待整批角色确认。用户批准后执行场景及关键道具；再按确认要求使用真实生成图片。
- 若平台具有 GPT 原生生图能力，能直接生成图时实际调用并检查；否则交付当前阶段的可用提示词，并明确未生图。
- 图片已真实获得后，依据原版 `video-contract.md` 输出15秒3–4个镜头的视频提示词；一条台词只出现一次，机位仅为清晰表达剧情时新增。
- 视频生成与后期属外围执行层：可用且获授权的模型/工具实际执行、实际检查输出；工具或版权限制则明确报告，不用文本代替影片。
- 每一个新作品都使用独立状态，沿用用户已确认决定，局部反馈只修指定部分。
- 生产结果保存为项目素材 + 质量记录；优化候选单独保存，未经对照实验不能晋升原版核心。

**启动任务**：读取用户在当前对话上传的小说/剧本，按以上规则启动第一轮角色阶段。若原参考文件目前缺失，要明确报告并依照已可核实部分运行，不得假装已读到缺失文件。
