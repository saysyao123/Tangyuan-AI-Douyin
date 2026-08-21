# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W03`
- Overall State: `READY_TO_START`
- Fully automated stages: `1`
- Human aesthetic gates encountered: `2`
- Human aesthetic gates passed: `2`
- External-required stages encountered: `0`
- Non-aesthetic manual interventions: `3`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified；无独立 Whisper/faster-whisper；不能直接执行 Seedance |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 研究与筛选 AUTO；用户选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传官方原唱；两次边界修正；最终试听确认 | v3 锁定 `139.930s–177.050s`，37.120s；本轮 one-shot clip lock 未通过，工作流已升级 |
| W03 | Beat分析 | AUTO | READY_TO_START | 无 | 使用已锁 v3 BGM |
| W04 | 导演/生产分配 | HUMAN_GATE | NOT_STARTED | 审美确认 | |
| W05 | 首帧提示词+生图 | HUMAN_GATE | NOT_STARTED | 整组审美确认 | Image Generation 实际生产能力在本 Stage 验证 |
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

### Version / source

- official vocal master: `孙天宇 - 如果你也刚好抬头看树`
- official streaming duration: `3:16`
- uploaded production source: `196.127347s`, MP3 / 320 kbps / 44.1 kHz / stereo
- source SHA-256: `ad30cefef4e4a5ffedab81b26b1e38a0b679bf2b32752b6ebd29f5d97f18d7ab`

### Preview history

#### v1 — REJECTED / TECHNICAL FAILURE
- range: `130.72s–163.82s`
- opening contained non-chorus preceding material;
- final lyric line was incomplete;
- this should have been blocked before user delivery.

#### v2 — REJECTED / BOUNDARY QUALITY FAILURE
- range: `140.430s–168.900s`
- correct repeated chorus isolated;
- still lacked enough musical pickup at the start and ended before the more natural one-line release;
- user had to specify `~0.5s` additional pre-roll and one extra complete line.

#### v3 — LOCKED / PASSED
- range: `139.930s–177.050s`
- duration: `37.120s`
- fade: `0.020s in / 0.950s out`
- includes exactly one complete release line after the title-line chorus close;
- preview SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- user final gate: `PASSED`

### Automation judgment

W02 is **not** counted as successful one-shot automatic clipping.

What worked automatically:
- official version verification;
- uploaded-file validation;
- waveform / repeated-section analysis;
- local trimming / fade / rendering.

What failed:
- first-pass excerpt boundary judgment;
- pre-delivery edge QA;
- correct accounting initially treated objective repair as aesthetic feedback.

Therefore W02 final state is `PARTIAL`.

### Workflow correction promoted

`04_HARNESS/workflows/mv.md` upgraded from `v1.0` to `v1.1`.

New mandatory `Audio Boundary Gate` requires before any preview is shown:
1. intended section identity;
2. no previous-lyric contamination;
3. musical pickup / opening-breath test;
4. complete final lyric;
5. one-extra-release-line test;
6. fade only after vocal / semantic resolution;
7. platform/Douyin usage cross-check when reliable evidence exists;
8. isolated first ~3s / last ~4s listen + full excerpt listen;
9. duration follows musical completeness, not a forced numeric target.

Expected future behavior: user should receive one technically valid first preview and only need an aesthetic `PASS / change direction`, not boundary repair.

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 最终歌曲偏好属于设计保留的审美决定 | 选择 `C3 如果你也刚好抬头看树` | 否 |
| 2 | W02 | FILE_INPUT | 官方流媒体未暴露可直接进入本地处理链的完整音频文件 | 上传匹配官方 3:16 原唱母版的 320 kbps MP3 | 可能；若未来接入授权音频资产源可消除 |
| 3 | W02 | TECHNICAL_RESCUE | v1 错把前一结构带入且截断最后歌词，自动预检没有拦截 | 指出开头不属于副歌、最后一句不完整 | 是；已加入结构映射 + Audio Boundary Gate |
| 4 | W02 | TECHNICAL_RESCUE | v2 虽结构正确，但首点过紧、尾部释放不足，仍未达到 first-pass 可通过标准 | 要求前移约0.5s并增加下一整句 | 目标上是；已加入 pickup test + one-extra-release-line test |
| 5 | W02 | AESTHETIC_GATE | v3 已技术完整，只需最终听感确认 | 确认 `可以` | 否；这是设计保留的最终审美 Gate |

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
