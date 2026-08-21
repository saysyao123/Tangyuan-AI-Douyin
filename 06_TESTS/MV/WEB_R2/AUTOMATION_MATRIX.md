# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W06-X`
- Overall State: `EXTERNAL_REQUIRED / CAMERA_TEST_V1_READY`
- Fully automated stages: `3` (`W00`, `W03`, `W06`)
- Human aesthetic gates encountered: `4`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Non-aesthetic manual interventions: `4`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified；无独立 Whisper/faster-whisper；不能直接执行 Seedance |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 研究与筛选 AUTO；用户选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传官方原唱；两次边界修正；最终试听确认 | v3 锁定 `139.930s–177.050s`，37.120s；one-shot clip lock 未通过，workflow v1.1 |
| W03 | Beat分析 | AUTO | AUTO / LOCKED | 无 | 无 Whisper；同版本歌词 + locked audio evidence 完成导演级结构分析 |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PASSED | 审美选择与方向修正 | 初版“树的连续空间叙事”被否；最终锁定 `树影之外`：人物情绪 + 巨尺度 + 非线性MV碎片结构 |
| W05 | 首帧提示词+生图 | HUMAN_GATE | HUMAN_GATE / PASSED | 整组审美确认 | 9/9最终首帧通过；形成“统一情绪系统 + 多元镜头系统，不是统一空间叙事系统” |
| W06 | 动态提示词 | AUTO | AUTO / TEST_V1_READY | 无 | 开源运镜研究 + 9条实验提示词完成；尚未晋升核心规则 |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | EXTERNAL_REQUIRED / READY | 外部生成+上传 | 当前网页工具不能直接执行 Seedance 2 mini；建议先测 S1/S3/S7 |
| W07 | 动态QA/返工设计 | AUTO | NOT_STARTED | 外部失败段重生成 | raw clips 回传后自动进入 |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | 无独立 Whisper/faster-whisper；字幕对齐必须使用可验证同版本证据 |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W04 Final Evidence

Final concept: `树影之外`.

- one fictional East Asian female protagonist;
- functional light sand/grey veil integrated with wardrobe, lower face always covered;
- ancient tree + restrained grey-white curved concrete architecture + large sky negative space;
- low saturation + hard motivated natural backlight + real material texture;
- MV is built from lyrical visual fragments and viewpoint contrast, not a continuous location walkthrough.

## W05 Final Evidence

- accepted first frames: `9 / 9`;
- visual coverage includes monumental extreme wide, medium reach, veil/eye close-up, full-body fabric motion, bird relationship, worm’s-eye motion peak and rooftop sky release;
- one avoidable execution rescue: the assistant stopped after three style anchors instead of continuing automatically, and one output was visibly soft; user had to ask whether generation had stalled;
- final set passed after whole-set angle/repetition correction.

## W06 Camera Research / Prompt Experiment

Experiment file:
`06_TESTS/MV/WEB_R2/W06_CAMERA_PROMPT_EXPERIMENT_v1.md`

Research sources include:
- `songguoxs/seedance-prompt-skill`
- `Emily2040/seedance-2.0`
- `yinxiaowai/awesome-ai-video-camera-movement-prompts`
- `fal-ai-community/skills`
- `maciejdzierzek/seedance-prompt-generator`
- supporting camera-vocabulary repositories

Test principle:
`one primary camera contract per 5s clip; diversity across the 9-clip set`.

Camera distribution:
`Locked / Arc / Rack Focus / Truck / Tilt / Dolly Pull-back / Pedestal Up / Pan / small optical Zoom Out`.

No promotion to core rules until W07 generated-video evidence.

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
| 9 | W06-X | EXTERNAL_TOOL | 当前网页工具没有 Seedance 2 mini 执行接口 | `PENDING`：外部生成并回传 raw MP4 | 取决于未来工具能力 |

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