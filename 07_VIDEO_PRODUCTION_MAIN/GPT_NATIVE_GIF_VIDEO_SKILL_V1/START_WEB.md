# 网页端 / Work 零上下文启动入口

请读取本目录 `SKILL.md`、`references/PROMPTS.md`、`references/QA.md`、`references/EXPERIMENT.md` 和 `scripts/gif_to_video.py`。这是仓库 `07_VIDEO_PRODUCTION_MAIN` 下的 GPT 原生 GIF 视频专项 Skill，不替换 Work-Fisher 的主导演流程。

## 可直接粘贴的启动语句
> 请按 `GPT_NATIVE_GIF_VIDEO_SKILL_V1/SKILL.md` 直接制作视频。使用 GPT 原生 GIF 生成连续画面，先做逐帧完整性检查，优先人物一致性和固定镜头；再将合格源 GIF 通过脚本补间为 5 秒、120 帧、24 FPS 的 MP4，同时提供 GIF、MP4、16帧预览图与 QA 报告。禁止滚动拼图、截断帧、假造原生120帧、未经核对就宣称成功。尽可能自行完成，无需让我参与剪辑；若环境无 FFmpeg，给出实测限制和当前实际交付，不能拿文案冒充视频。

## 用户可补充
- 原创视频内容、参考人物/图、风格、时长、画幅（默认为 5 秒、9:16）、所需声音、结尾是否需要循环。
- 若用户只说「做一个 GIF 小视频」，采用固定机位 + 1 个主动作 + 轻环境微动的可执行默认值。

## 常用指令
- “用 GPT GIF Skill 做一条 5 秒情绪短片，画面是雨夜窗前、人物轻抬手。”
- “把这段 GPT 原生 GIF 转成稳定的 5 秒 24FPS MP4，做完 QA 再交付。”
- “沿用已有角色资产和 Work-Fisher 剧情设定，调用 GIF Skill 完成一个低幅动作镜头。”

## 文件交付
目标交付：`native_source.gif`（原生源动画）、`animation_5s_120f.gif`、`animation_5s_24fps.mp4`、`qa_contact_sheet.jpg`、`qa_report.json`。
如果用户提出了真正 1080×1920 高画质、复杂真人运动、口型同步等更高要求，先披露本专项 Skill 的能力边界，不把机械放大等同真实高清；可切换另一个已批准的视频工作流。