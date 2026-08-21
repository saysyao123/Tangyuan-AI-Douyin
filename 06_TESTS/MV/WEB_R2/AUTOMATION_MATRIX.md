# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W01`
- Overall State: `IN_PROGRESS`
- Fully automated stages: `1`
- Human aesthetic gates passed: `0`
- External-required stages encountered: `0`
- Non-aesthetic manual interventions: `0`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub read/write 可用；Web 可用；Files/Library 可用；Image Generation 接口存在，实际生产留 W05 验证；本地 ffmpeg/ffprobe、MoviePy、pydub、OpenCV 可用；无独立 Whisper/faster-whisper；不能控制用户本机/浏览器或 Seedance 外部站点 |
| W01 | 选歌研究 | HUMAN_GATE | IN_PROGRESS | 最终选歌 | 自动刷新观察源并筛候选，用户只做最终审美选择 |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | NOT_STARTED | 可能上传音频 + 试听确认 | |
| W03 | Beat分析 | AUTO | NOT_STARTED | 无 | |
| W04 | 导演/生产分配 | HUMAN_GATE | NOT_STARTED | 审美确认 | |
| W05 | 首帧提示词+生图 | HUMAN_GATE | NOT_STARTED | 整组审美确认 | Image Generation 实际生产能力在本 Stage 验证 |
| W06 | 动态提示词 | AUTO | NOT_STARTED | 无 | |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | NOT_STARTED | 外部生成+上传 | 当前能力基线未发现可直接执行 Seedance 的工具；到 W06-X 依真实执行正式记账 |
| W07 | 动态QA/返工设计 | AUTO | NOT_STARTED | 外部失败段重生成 | |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | W00 已验证本地音视频处理工具；当前无独立 Whisper/faster-whisper，字幕对齐方法到 W08 按同版本可靠 LRC/音频证据验证 |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W00 Capability Baseline Evidence

- GitHub connector: `VERIFIED` — 已从 `test/mv-web-r2` 读取指定文件，并可向同分支写回状态文件。
- Public Web research: `AVAILABLE` — 当前对话具备网页搜索/打开页面能力；具体选歌研究在 W01 实测。
- Files / uploads / Library analysis: `AVAILABLE` — 可搜索、读取、物化会话与 Library 文件。
- Image Generation: `AVAILABLE_INTERFACE` — 当前对话暴露生图能力；是否满足本项目首帧质量线延后到 W05 实测，不在 W00 虚报通过。
- Local audio/video processing: `VERIFIED` — `ffmpeg`、`ffprobe`、MoviePy、pydub、OpenCV 可用，可进行裁剪、转码、抽帧、合成等本地处理。
- ASR / Whisper: `NOT_PRESENT_AS_DEDICATED_LOCAL_CAPABILITY` — 未检测到 `whisper` / `faster_whisper`；后续不得声称 Whisper 已运行。
- Seedance execution: `NOT_AVAILABLE_IN_CURRENT_WEB_TOOLSET` — 不假设能登录或控制外部 Seedance；正式状态在 W06-X 记录。
- User local machine/browser control: `NOT_AVAILABLE`。

## 状态枚举

- `AUTO`
- `HUMAN_GATE`
- `EXTERNAL_REQUIRED`
- `PARTIAL`
- `BLOCKED`
- `FAIL`

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|

类型只允许：
- `AESTHETIC_GATE`
- `FILE_INPUT`
- `EXTERNAL_TOOL`
- `LOGIN/CAPTCHA`
- `TECHNICAL_RESCUE`

## Final Questions

R2 结束时必须回答：
1. 网页端能否自动完成选歌研究？
2. 不靠 Codex，网页端能否自动裁剪用户上传 BGM？
3. 导演 / 首帧 / 提示词能否自动完成到只需审美 Gate？
4. Seedance 是否仍是最大人工断点？
5. 视频上传回来后，QA / 剪辑 / 字幕能否自动闭环？
6. 哪些能力应留在 Web，哪些应移交 Codex？
