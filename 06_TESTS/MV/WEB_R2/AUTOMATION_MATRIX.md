# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W02`
- Overall State: `AWAITING_AUDIO_AESTHETIC_GATE_V2`
- Fully automated stages: `1`
- Human aesthetic gates encountered: `2`
- Human aesthetic gates passed: `1`
- External-required stages encountered: `0`
- Non-aesthetic manual interventions: `1`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub read/write 可用；Web 可用；Files/Library 可用；Image Generation 接口存在，实际生产留 W05 验证；本地 ffmpeg/ffprobe、MoviePy、pydub、OpenCV 可用；无独立 Whisper/faster-whisper；不能控制用户本机/浏览器或 Seedance 外部站点 |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE | 最终选歌 | 研究与筛选自动完成；用户选择 `如果你也刚好抬头看树`，Gate 已通过 |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / GATE_PENDING_V2 | 已上传官方原唱实际音频；试听 v2 待确认 | v1 边界错误被用户 Gate 拒绝；网页端完成根因分析并仅修正 W02，不改上游；v2 按重复副歌结构重切为 `140.43s–168.90s` |
| W03 | Beat分析 | AUTO | NOT_STARTED | 无 | |
| W04 | 导演/生产分配 | HUMAN_GATE | NOT_STARTED | 审美确认 | |
| W05 | 首帧提示词+生图 | HUMAN_GATE | NOT_STARTED | 整组审美确认 | Image Generation 实际生产能力在本 Stage 验证 |
| W06 | 动态提示词 | AUTO | NOT_STARTED | 无 | |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | NOT_STARTED | 外部生成+上传 | 当前能力基线未发现可直接执行 Seedance 的工具；到 W06-X 依真实执行正式记账 |
| W07 | 动态QA/返工设计 | AUTO | NOT_STARTED | 外部失败段重生成 | |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | W00 已验证本地音视频处理工具；当前无独立 Whisper/faster-whisper，字幕对齐方法到 W08 按同版本可靠 LRC/音频证据验证 |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W00 Capability Baseline Evidence

- GitHub connector: `VERIFIED`
- Public Web research: `AVAILABLE`
- Files / uploads / Library analysis: `AVAILABLE`
- Image Generation: `AVAILABLE_INTERFACE`
- Local audio/video processing: `VERIFIED`
- ASR / Whisper: `NOT_PRESENT_AS_DEDICATED_LOCAL_CAPABILITY`
- Seedance execution: `NOT_AVAILABLE_IN_CURRENT_WEB_TOOLSET`
- User local machine/browser control: `NOT_AVAILABLE`

## W01 Discovery Evidence

- Final selection: `C3 如果你也刚好抬头看树`
- Artist / reference version: `孙天宇`
- User aesthetic gate: `PASSED`

## W02 Evidence

### Version / source

- official vocal master: `孙天宇 - 如果你也刚好抬头看树`
- official streaming duration: `3:16`
- uploaded production source: `196.127347s`, MP3 / 320 kbps / 44.1 kHz / stereo
- embedded title / artist / album match
- source SHA-256: `ad30cefef4e4a5ffedab81b26b1e38a0b679bf2b32752b6ebd29f5d97f18d7ab`

### Preview v1 — REJECTED

- range: `130.72s–163.82s`
- failure: opening contains non-chorus preceding material; final chorus line is cut before completion.
- user gate result: `重新选段`
- root cause: loose excerpt localization; insufficient repeated-section structural alignment.

### Preview v2 — CURRENT

- repeated chorus alignment: first chorus approx `58.86s`, second chorus approx `140.43s`, offset approx `81.55s`.
- chorus close correspondence: first approx `87.03s`, second approx `168.58s`.
- corrected range: `140.43s–168.90s`
- duration: `28.470s`
- fade: `0.025s in / 0.420s out`
- preview SHA-256: `b957a9e31bf7bc48a993cfdac51515cfb4f0978822abd72d7b5433c7fae8546d`
- status: `AWAITING_AESTHETIC_GATE`

### Automation lesson

W02 demonstrates that automated audio processing is available, but excerpt selection still needs a quality Gate. The user correction did not require a new tool or manual editing action from the user; after feedback, Web completed root-cause analysis and re-render automatically. This remains the designed `AESTHETIC_GATE`, not an additional `TECHNICAL_RESCUE` intervention.

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
| 1 | W01 | AESTHETIC_GATE | 3个候选均满足自动研究门槛，最终选择涉及用户对歌曲本身的审美偏好 | 选择 `C3 如果你也刚好抬头看树` | 否 |
| 2 | W02 | FILE_INPUT | 官方流媒体未暴露可直接进入本地处理链的完整音频文件 | 上传匹配官方 3:16 原唱母版的 320 kbps MP3；验证通过 | 可能；未来若接入有授权音频资产源可消除 |
| 3 | W02 | AESTHETIC_GATE | 最终短 MV 音频区间需要听感确认 | v1 反馈：开头不是完整副歌起点、尾句被截断；系统据此自动重切 v2，当前等待再次试听 | 否；这是设计保留的音频审美/质量 Gate |

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
