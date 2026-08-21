# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W06-X`
- Overall State: `EXTERNAL_REQUIRED / S1_MULTISHOT_TEST_V2_READY`
- Fully automated stages: `3` (`W00`, `W03`, `W06 research/prompt drafting`)
- Human aesthetic gates encountered: `4`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Non-aesthetic manual interventions: `5`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified；无独立 Whisper/faster-whisper；不能直接执行 Seedance |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 研究与筛选 AUTO；用户选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传官方原唱；两次边界修正；最终试听确认 | v3 锁定 `139.930s–177.050s`，37.120s；one-shot clip lock 未通过，workflow v1.1 |
| W03 | Beat分析 | AUTO | AUTO / LOCKED | 无 | 无 Whisper；同版本歌词 + locked audio evidence 完成导演级结构分析 |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PASSED | 审美选择与方向修正 | 初版连续“树叙事”被否；最终锁定 `树影之外` |
| W05 | 首帧提示词+生图 | HUMAN_GATE | HUMAN_GATE / PASSED | 整组审美确认 | 9/9最终首帧通过；统一情绪系统 + 多元镜头系统 |
| W06 | 动态提示词 | AUTO | AUTO / EXPERIMENTAL | 无 | 开源运镜研究完成；v1 的“每5秒一个主运镜”解释经 S1 实测失败，已修正为“3–5镜 + 每镜一个主运镜”v2，尚未晋升核心规则 |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | EXTERNAL_REQUIRED / S1_V2_PENDING | 外部生成+上传 | S1 v1 已生成并回传；当前只需重测 S1 v2，不生成其余段 |
| W07 | 动态QA/返工设计 | AUTO | PARTIAL STARTED | 无额外本地操作 | 已自动分析 S1 v1 成片并做根因修复；待 S1 v2 回传继续 QA |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | 无独立 Whisper/faster-whisper；字幕对齐必须使用可验证同版本证据 |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W06 Camera Research / Experiment Status

### v1 — FAILED ON S1

Experiment file:
`06_TESTS/MV/WEB_R2/W06_CAMERA_PROMPT_EXPERIMENT_v1.md`

v1 hypothesis:
`one primary Camera Contract per 5s clip; diversity across the 9-clip set`.

Returned S1 evidence:
- raw clip `5.09s / 720×1280 / 24fps`;
- camera composition effectively stays fixed, producing one-take/stiff feeling;
- character/fabric carries nearly all movement;
- veil topology breaks and an independent white scarf-like strip crosses the upper frame.

This is classified as a prompt/director interpretation failure, not user aesthetic preference.

### v2 — CURRENT TEST

Experiment file:
`06_TESTS/MV/WEB_R2/W06_S1_MULTISHOT_CAMERA_TEST_v2.md`

Corrected principle:
- keep the proven `3–5 shot` MV structure when appropriate;
- **one clear Camera Contract per Shot**, not per entire 5s clip;
- use explicit hard cuts, shot-size/angle contrast and per-shot movement;
- camera/edit rhythm should carry primary dynamics, with fabric/light/leaves as secondary dynamics.

S1 v2 four-shot map:
1. extreme wide + Dolly In;
2. low-angle medium close-up + small Arc/Truck;
3. veil/eyes close-up + Rack Focus;
4. worm’s-eye/low-angle + Tilt Up into canopy/sky.

Veil topology patch explicitly forbids detached or duplicated white fabric, sky-borne scarf/ribbon and offscreen cloth generation.

Do not expand v2 to S2–S9 until S1 v2 passes generated-video QA.

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 最终歌曲偏好属于设计保留的审美决定 | 选择 `如果你也刚好抬头看树` | 否 |
| 2 | W02 | FILE_INPUT | 官方流媒体未暴露可直接进入本地处理链的完整音频文件 | 上传匹配官方3:16原唱母版的320 kbps MP3 | 可能 |
| 3 | W02 | TECHNICAL_RESCUE | v1 错把前一结构带入且截断最后歌词 | 指出开头不属于副歌、最后一句不完整 | 是；已加入 Audio Boundary Gate |
| 4 | W02 | TECHNICAL_RESCUE | v2 首点过紧、尾部释放不足 | 要求前移约0.5s并增加下一整句 | 目标上是；已加入 pickup + extra-release-line test |
| 5 | W02 | AESTHETIC_GATE | v3 技术完整，只需最终听感确认 | `可以` | 否 |
| 6 | W04 | AESTHETIC_GATE | 导演世界与MV美学属于保留的人类审美决策 | 否决连续“树叙事”，最终通过 `树影之外` | 否 |
| 7 | W05 | TECHNICAL_RESCUE | 三张风格锚点后网页端未按计划自动继续，且一张明显偏虚 | 询问是否卡住并要求继续 | 是；未来必须主动续跑并自检清晰度 |
| 8 | W05 | AESTHETIC_GATE | 首帧整组美学与镜头多样性需要人工最终判断 | 多轮比较后确认最终九张方案 | 否 |
| 9 | W06-X | EXTERNAL_TOOL | 当前网页工具没有 Seedance 2 mini 执行接口 | 已生成并回传 S1 v1；当前需外部生成 S1 v2 | 取决于未来工具能力 |
| 10 | W06/W07 | TECHNICAL_RESCUE | 助手把“one camera movement per shot”错误扩大成“one camera movement per 5s clip”，导致 S1 一镜到底感、运镜弱，并诱发独立白纱拓扑错误 | 用户指出应把运镜重新融合回原有3–5镜结构，并指出空中莫名白纱 | 是；v2 已改为“3–5镜 + 每镜单运镜 Camera Contract”，待生成验证 |

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