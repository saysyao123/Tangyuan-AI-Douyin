# 中文热议集锦｜网页云端工作流

把已经交付并获用户肯定的 2026-10-08 中文竖版视频，整理为独立、可恢复的生产流程。默认只做中文，9:16、1080×1920、30fps，成片不超过五分钟。延续纸白、安全橙和真实视频为主的画面；下一轮主要优化旁白口吻。

**开始使用：[START_WEB.md](START_WEB.md)。** 网页操作，运算在云端，无需用户电脑安装模型或剪辑软件。新对话须先验证终端、依赖和文件导出能力；普通网页文字对话是否能执行这些步骤，不能仅靠一段提示词保证。

|入口|如何操作|结果|
|---|---|---|
|ChatGPT Work / 有执行环境的网页任务|读取 START_WEB，完成启动检查，再研究、写稿和运行本目录|对话内交付 MP4、预览、封面、简报和旁白稿|
|GitHub 网页云端导出|打开 [Actions](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/workflows/gossip_video_web.yml)，Run workflow，粘贴已核实的中文 episode JSON|云端配音、渲染、STT；下载 Artifacts 中的 delivery.zip|

留空 JSON 会运行 **技术自检片**，画面是程序测试视频，不是吃瓜新闻成片。Actions 负责导出；选题、真假判断、画面语义和最后听感仍由制作助手完成。当前 GitHub 连接没有“首次启动 workflow”的工具，助手不可谎称已替用户点击 Run workflow；可用已支持的运行查询和文件下载工具接收结果。

常用文件：

- [WORKFLOW.md](WORKFLOW.md)：选题到交付的完整流程及失败恢复。
- [prompts/DOUYIN_NARRATION.md](prompts/DOUYIN_NARRATION.md)：更适合抖音的口语规范和实际修改示例。
- [prompts/DOUYIN_SAMPLE_2026_10_08.md](prompts/DOUYIN_SAMPLE_2026_10_08.md)：旧一期更口语的完整候选稿，事实范围不变，待试听。
- [QA.md](QA.md)：STT、抽帧、转场、重复镜头和听感复核。
- [BASELINE.md](BASELINE.md)：已完成一期的事实、验收和待改进项。
- `runtime/`：React + GSAP + Playwright + FFmpeg 导出程序。
- `run.py`：中文逐句免费配音、实测时间线、源素材裁切、混音、双分辨率和检查图。
- `examples/smoke.json`：可以直接跑的无版权素材技术样片。
- `examples/baseline-2026-10-08.json`：旧一期的中文场景/来源迁移配置，日期固定，不能冒充今天新闻。
- `evidence/`：原一期检查摘要、新运行回执和上游版本。

本目录为独立新闻集锦流程。用户本次明确选择免费合成旁白和只做中文；该选择适用于这里。MV、个人实验账号的真人声线和原有 Human Gates 继续由其各自流程管理。

技术代码已验证的程度见 [evidence/WEB_TEST.md](evidence/WEB_TEST.md)。新场景类型或新声线在通过实际样片前不标“生产稳定”。用户满意画面不等于已经验证抖音完播率或涨粉效果。

代码许可和上游来源见 [NOTICE.md](NOTICE.md)。第三方影片、模型和字体不提交 Git；模型、音频和输出使用各自许可。成片和工程备份由对话交付，不把临时下载链接写进公开仓库。
