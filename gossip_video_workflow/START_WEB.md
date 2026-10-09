# 新对话启动入口

直接复制下面这段到网页端新对话：

> 请读取 GitHub 仓库 saysyao123/Tangyuan-AI-Douyin 的 main 分支，目录 gossip_video_workflow，先读 START_WEB.md、WORKFLOW.md、prompts/DOUYIN_NARRATION.md、QA.md 和 BASELINE.md。沿用已验收的纸白、安全橙、真实视频为主的画面；只做中文，9:16，五分钟以内。旁白像朋友把事情讲明白，有反差、有观点，但所有事实先核实并进入简报。先执行云端环境检查，检查通过后直接完成采集、口语稿、逐句免费配音、实际测时、React/GSAP逐帧渲染、音乐自动压低和成片验收。最后交付中文成片、720p预览、封面、简报全文、旁白稿、3–4张关键帧和一个交付ZIP。没读到的来源单独说明，不编造X收藏、账号或评论。保留进度检查点，不替我发消息或帖子。

如果没有选题，助手搜最近适合的三条主线，先核实再组合，不能自称官方“热榜第一”。默认用户时区 Asia/Shanghai；“昨天”须用当地完整一天转成 UTC 查询。“今日热议选编”可以含近几天持续热议，但必须说清新进展日和原事件日。

## 助手必须实际完成的启动检查

1. 将本目录的代码读到云端工作区，使用仓库已测试提交/锁文件。读取工程，不需要用户电脑开机。
2. 验证 Python 3.12、Node 22+、FFmpeg/ffprobe、可写目录及至少数 GiB 可用空间。
3. 缺依赖时，在**云端**运行 `bash gossip_video_workflow/bootstrap.sh`。若网络策略或工具能力阻止安装，如实列出失败步骤，改用下方 GitHub 网页导出；不要要求用户安装本地大模型。
4. 在 `runtime/` 运行 `node doctor.mjs`，必须真的成功启动 headless Chromium 并输出 `ready`。这不是登录浏览器或接管用户设备。
5. 首次新环境运行：`.venv/bin/python run.py --episode examples/smoke.json --stt`（命令工作目录为本目录）。实际拿到 MP4 和检查文件后才标“出片环境可用”。技术片的视觉和旁白是自检，不代表真实新闻已经采集。
6. 用制作助手的实际文件能力保存交付与检查点。GitHub 持久化代码；原始影片、逐句音频、成片保存为用户可下载文件。新对话不得依赖旧 `/tmp` 路径。

只有终端、网页检索和 MP4 文件交付都可用时，才走“对话内全流程”。ChatGPT 网页中可运行的云端环境需要相应账户入口和网络权限；官方说明见 [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)。本仓库不能自行创建或发布用户账户的 Codex Cloud 环境；可将本目录 bootstrap 作为环境安装步骤，并用实际自检验收后保存该环境。

## GitHub 网页直接导出

1. 制作助手按 WORKFLOW 先完成来源核实和 episode JSON。使用公开素材 HTTPS 地址；配音默认免费 Kokoro 中文女声，模型在云端运行。
2. 打开 [Chinese Gossip Video - Web Export](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/workflows/gossip_video_web.yml)。登录有仓库运行权限的 GitHub 账号，点击 **Run workflow**，选择 **main**。
3. 将助手给出的完整 JSON 粘入 `episode_json`，点击运行。留空是技术自检。无需本地命令行；JSON通过事件文件读取，不作为 shell 命令执行。
4. 打开完成的运行页，下载 `chinese-video-delivery-运行ID`。里面有 `delivery.zip` 和输出/QA文件。失败时看具体步骤，保留已上传的部分结果，不能称已交付。
5. 把下载的 ZIP 交给同一网页对话，助手完成 STT 标记、联系表、转场和人物检查，发成片链接。没有执行环境的纯文字对话无法自己查看完整视频和导出；这时用具备文件处理能力的云端任务收尾。

GitHub 导出是手动入口，没有设置每天定时制作或自动发布。首次源码提交会触发一次技术自检；该运行结果必须在 evidence 回执中记录，不预先声称成功。Artifacts 有保留期限，完成后下载保存。
