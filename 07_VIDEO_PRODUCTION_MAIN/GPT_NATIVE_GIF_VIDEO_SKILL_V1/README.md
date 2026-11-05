# GPT Native GIF-to-Video Skill v1.0

**用途**：使用 GPT 原生 GIF 生成 5 秒低幅度动画镜头，以免费光流补间 + FFmpeg 合成 120 帧 / 24 FPS MP4 与 GIF，并强制逐帧 QA。

**入口**：`SKILL.md`（Agent Skills 格式）；`START_WEB.md`（ChatGPT 网页端与 Work 零上下文）；`scripts/gif_to_video.py`（实际产线）。

**与项目关系**：这是 `07_VIDEO_PRODUCTION_MAIN` 的专项子技能，与 `WORK_FISHER_SKILL_V1` 并列，不更改既定视频总路由；适用于情绪微电影、MV 中的低幅动作镜头。无需额外付费订阅。

**测试**：`python scripts/gif_to_video.py --input /path/to/native_source_30frames.gif --out result --seconds 5 --fps 24 --scale 2`。

**生产红线**：GIF 文件规格正确 ≠ 视觉动作完全合格；禁止滚动图和拆帧错位，必须查看输出的 MP4；禁止把补间帧说成原生帧。

**样本素材**：历史 30 帧原生 GIF 在本轮交付的完整 ZIP 内，未提交进 GitHub（避免把较大的示例二进制文件作为源码）。

## Work 深度审核 / 升级入口

[WORK_AUDIT_START.md](WORK_AUDIT_START.md) 是 Work 模式的零下载、零上下文审核指令。要求实际检查、测试、修复代码并将通过验收的更改同步到 GitHub `main`；网页端通过 `START_WEB.md` 再读取最新提交。GitHub 不等于 ChatGPT 内置 Skill 的自动热更新。
