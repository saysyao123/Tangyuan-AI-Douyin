# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W04`
- Overall State: `AWAITING_DIRECTOR_AESTHETIC_GATE`
- Fully automated stages: `2`
- Human aesthetic gates encountered: `3`
- Human aesthetic gates passed: `2`
- External-required stages encountered: `0`
- Non-aesthetic manual interventions: `3`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified；无独立 Whisper/faster-whisper；不能直接执行 Seedance |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 研究与筛选 AUTO；用户选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传官方原唱；两次边界修正；最终试听确认 | v3 锁定 `139.930s–177.050s`，37.120s；one-shot clip lock 未通过，工作流已升级到 v1.1 |
| W03 | Beat分析 | AUTO | AUTO / LOCKED | 无 | 无 Whisper；同版本歌词 + locked audio + waveform/repeated-section/beat evidence 完成结构分析，未伪造字幕级时间戳 |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PLAN_READY | 审美确认 | focused benchmark、统一概念、9段生产分配、45s raw coverage 和 Camera Repetition Gate 已自动完成；只等待导演方向确认 |
| W05 | 首帧提示词+生图 | HUMAN_GATE | NOT_STARTED | 整组审美确认 | W04通过后先生成2–3张风格锚点，再补齐9张 |
| W06 | 动态提示词 | AUTO | NOT_STARTED | 无 | |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | NOT_STARTED | 外部生成+上传 | 当前能力基线未发现可直接执行 Seedance 的工具；到 W06-X 依真实执行正式记账 |
| W07 | 动态QA/返工设计 | AUTO | NOT_STARTED | 外部失败段重生成 | |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | 当前无独立 Whisper/faster-whisper；字幕对齐必须使用可验证同版本证据 |
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

## W01 Result

- Final selection: `C3 如果你也刚好抬头看树`
- Artist / reference version: `孙天宇`
- Research: `AUTO`
- Final song choice: `AESTHETIC_GATE / PASSED`

## W02 Final Evidence

- Locked excerpt: `139.930s–177.050s`, `37.120s`, `0.020s` fade-in / `0.950s` fade-out.
- v1 + v2 required two avoidable user technical corrections.
- W02 total = `PARTIAL`; Audio Boundary Gate promoted to `workflows/mv.md v1.1`.

## W03 Final Evidence

- Dedicated ASR unavailable; not claimed.
- Exact lyric sequence cross-checked; locked audio beat estimate ~`103.36 BPM`.
- Six Natural Beats established; primary motion peak = `一颗心叽叽喳喳飞过了树梢`, recognition anchors = repeated title line, final release = cloud line.
- W03 user work = none; actual state = `AUTO`.

## W04 Current Evidence

### Focused benchmark

- current same-song AIMV exists; used as homogeneity warning, not copied;
- recent summer-song AIMV packaging and Seedance2.5 motion tests show current market motion/completion bar is rising;
- real canopy / macro / dappled-light photography used only as beauty/material reference.

### Proposed director concept

`一棵树里的夏日宇宙`.

- no visible human protagonist; camera/viewer is the lyric's `你 / 我`;
- one old urban tree is the entire world;
- scale progression: ground seed → bark → leaves → hidden bird → treetop → sky → cloud;
- recurring golden winged seed becomes the non-literal metaphor for `心飞过树梢`;
- no logos / readable signs / background people;
- current character policy avoids unnecessary portrait/identity instability.

### Coverage

- conceptual Natural Beats: `6`
- first frames: `9`
- 5s raw clips: `9`
- raw duration: `45s`
- locked final BGM: `37.120s`
- headroom: `7.880s` = ~`21.2%`

### Camera Repetition Gate

`PASS`: vertical reveal / orbit / macro slider / 3-shot reveal / snap pan / chase / locked environmental reveal / aerial lateral drift / static release are distributed across the set; no all-slow-push template.

### W04 current state

Production planning is automated and complete, but final director direction is intentionally reserved for the user aesthetic gate. W05 must not start until this gate passes.

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 最终歌曲偏好属于设计保留的审美决定 | 选择 `C3 如果你也刚好抬头看树` | 否 |
| 2 | W02 | FILE_INPUT | 官方流媒体未暴露可直接进入本地处理链的完整音频文件 | 上传匹配官方 3:16 原唱母版的 320 kbps MP3 | 可能；若未来接入授权音频资产源可消除 |
| 3 | W02 | TECHNICAL_RESCUE | v1 错把前一结构带入且截断最后歌词，自动预检没有拦截 | 指出开头不属于副歌、最后一句不完整 | 是；已加入结构映射 + Audio Boundary Gate |
| 4 | W02 | TECHNICAL_RESCUE | v2 虽结构正确，但首点过紧、尾部释放不足，仍未达到 first-pass 可通过标准 | 要求前移约0.5s并增加下一整句 | 目标上是；已加入 pickup test + one-extra-release-line test |
| 5 | W02 | AESTHETIC_GATE | v3 已技术完整，只需最终听感确认 | 确认 `可以` | 否；这是设计保留的最终审美 Gate |
| 6 | W04 | AESTHETIC_GATE | 导演世界/叙事方向属于设计保留的审美决定；生产分配本身已自动完成 | `PENDING` | 否；这是设计保留的导演 Gate |

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