# WEB R2｜ZERO-CONTEXT START PROMPT

把下面整段直接发给新的 ChatGPT 网页端对话：

```text
你现在要执行本仓库的 WEB R2 AI MV 网页端自动化测试。

这不是继续上一轮聊天，而是一次零上下文的新 Round。目标是测试：在不依赖 Codex 的情况下，网页端 ChatGPT 从选歌到成片到底哪些阶段可以完全自动、哪些只需要我做审美确认、哪些必须我去外部平台操作。

请使用已连接的 GitHub，并以分支：
test/mv-web-r2
作为本轮唯一写入分支。

开始前严格按顺序读取：
1. 06_TESTS/MV/WEB_R2/CURRENT_STATE.md
2. 06_TESTS/MV/WEB_R2/README.md
3. 06_TESTS/MV/WEB_R2/WEB_R2_MASTER_PLAN.md
4. 06_TESTS/MV/WEB_R2/AUTOMATION_MATRIX.md
5. 04_HARNESS/workflows/mv.md
6. 只有当前 Stage 需要时，再按 JIT 原则读取对应 rules / benchmark / Golden R1 文件。

不要扫描整个仓库，不要让我重新解释 R1，不要默认从记忆继续。

执行原则：
- 从 CURRENT_STATE 指定 Stage 开始；当前是 W00；
- 能自己搜索、读取、分析、生成、裁剪、检查、编辑的工作，都直接自己完成；
- 不要把“让我自己去搜索/整理/运行命令”当作正常流程；
- 只有审美选择、外部平台登录/验证码、外部 Seedance 生成、确实缺失的原始文件才允许请求我操作；
- 每次需要我操作时，明确标记这是 `AESTHETIC_GATE / FILE_INPUT / EXTERNAL_TOOL / LOGIN/CAPTCHA / TECHNICAL_RESCUE` 中的哪一种；
- 每完成一个 Stage，更新 `WEB_R2/AUTOMATION_MATRIX.md` 和 `CURRENT_STATE.md`；
- 不得覆盖 `06_TESTS/MV/ROUND_01/`；R1 只作为 Golden Quality Floor；
- 不得为了自动化而降低质量门槛；
- 任何人物相关 Seedance 图生视频提示词第一行必须原样为：
*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。
前面的 *** 不能删除；
- 动态镜头不能默认全部慢推或一镜到底。单镜、2–3镜都可用，但必须做整组 Camera Repetition Gate，并在本轮继续测试更丰富的电影常用运镜；
- 字幕时间必须来自最终锁定音频，不允许按画面段落边界推算；
- 如果当前网页端没有 Whisper，明确记录，并选择可验证的同版本 LRC/音频对齐方案，不要伪装成 Whisper 已运行；
- 如果网页端无法直接执行 Seedance，明确标记 W06-X = EXTERNAL_REQUIRED，我只负责外部生成并把原始视频发回来；其他部分你继续自动完成；
- 每一轮交付文件优先 ZIP，避免下载问题。

本轮不是复刻《你有没有真的爱过我》的纸墨视觉。请从新的候选歌开始，但 R1 的美感、歌词命中、导演层次、动态质量、剪辑和字幕准确度是最低质量线。

现在执行 W00。完成能力基线后，如果没有真正阻塞项，直接进入 W01：自动刷新约5个MV/音乐观察源最近约30天的歌曲，筛出3–5个强候选并给我真实视频链接。不要先问我想听什么歌。
```