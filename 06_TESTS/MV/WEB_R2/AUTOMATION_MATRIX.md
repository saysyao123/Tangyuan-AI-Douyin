# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W06-X / W07`
- Overall State: `S2_ONE_TAKE_PASS / DIRECTOR_SELECTOR_V1_RECORDED`
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
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传官方原唱；两次边界修正；最终试听确认 | v3 锁定 `139.930s–177.050s`，37.120s；workflow v1.1 |
| W03 | Beat分析 | AUTO | AUTO / LOCKED | 无 | 同版本歌词 + locked audio evidence 完成导演级结构分析 |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PASSED | 审美选择与方向修正 | 最终锁定 `树影之外` |
| W05 | 首帧提示词+生图 | HUMAN_GATE | HUMAN_GATE / PASSED | 整组审美确认 | 9/9 首帧通过；统一情绪系统 + 多元镜头系统 |
| W06 | 动态提示词 | AUTO | AUTO / EXPERIMENTAL | 无 | 开源运镜研究完成；Camera Contract 进入实验层；Shot count 改为逐段导演判断 |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | ACTIVE | 外部生成+上传 | S1、S2 已回传；S2 单镜 Arc 成为正向样本 |
| W07 | 动态QA/返工设计 | AUTO | PARTIAL STARTED | 无额外本地操作 | S1 failure + S2 pass 已分析；形成 Director Shot-Structure Selector v1 |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | 无独立 Whisper/faster-whisper；字幕对齐必须使用可验证同版本证据 |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W06/W07 Camera Evidence

### S1 v1 — FAIL

- 5.09s / 720×1280 / 24fps;
- fixed one-take composition barely evolves;
- visual progression too weak;
- fabric carries too much motion;
- detached white scarf-like artifact = veil topology failure.

Conclusion: failure is `weak one-take / weak visual progression`, not proof that one-take is invalid.

### S2 v1 — PASS

- 5.04s / 720×1280 / 24fps;
- continuous Arc / orbit-like one-take;
- tree trunk / character / curved wall create readable parallax;
- character-space relationship changes throughout the clip;
- endpoint reaches a more flattering three-quarter angle;
- subject action remains simple enough for stable generation;
- user explicitly judged the orbit feeling as good.

Positive hypothesis:
`strong depth + simple action + parallax + clear camera path + better endpoint = successful one-take.`

## Director Shot-Structure Selector v1

Experimental file:
`06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`

New decision model:

`lyric task → first-frame performance potential → shot-count decision → one Camera Contract per Shot → motion-load budget → beauty/comfort gate`.

Shot-count policy:
- `1 Shot`: continuous emotion / gesture / spatial reveal / release where camera movement itself provides sustained progression;
- `2–3 Shots`: setup → event → aftermath, detail shift or one semantic turn;
- `3–5 Shots`: dense lyric / motion peak / strong Hook where scale-angle contrast is actually needed.

Neither one-take nor 3–5-shot is the default. Every structure must earn its use.

Per-shot motion budget:
- 1 primary camera move;
- 1 primary subject action;
- 1 secondary physical motion.

S2 is retained as positive evidence and must not be rewritten merely to increase cut count.

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 最终歌曲偏好属于设计保留的审美决定 | 选择 `如果你也刚好抬头看树` | 否 |
| 2 | W02 | FILE_INPUT | 官方流媒体未暴露可直接进入本地处理链的完整音频文件 | 上传匹配官方3:16原唱母版的320 kbps MP3 | 可能 |
| 3 | W02 | TECHNICAL_RESCUE | v1 错把前一结构带入且截断最后歌词 | 指出开头不属于副歌、最后一句不完整 | 是 |
| 4 | W02 | TECHNICAL_RESCUE | v2 首点过紧、尾部释放不足 | 要求前移约0.5s并增加下一整句 | 目标上是 |
| 5 | W02 | AESTHETIC_GATE | v3 技术完整，只需最终听感确认 | `可以` | 否 |
| 6 | W04 | AESTHETIC_GATE | 导演世界与MV美学属于保留的人类审美决策 | 否决连续“树叙事”，最终通过 `树影之外` | 否 |
| 7 | W05 | TECHNICAL_RESCUE | 三张风格锚点后网页端未按计划自动继续，且一张明显偏虚 | 询问是否卡住并要求继续 | 是 |
| 8 | W05 | AESTHETIC_GATE | 首帧整组美学与镜头多样性需要人工最终判断 | 多轮比较后确认最终九张方案 | 否 |
| 9 | W06-X | EXTERNAL_TOOL | 当前网页工具没有 Seedance 2 mini 执行接口 | 已生成并回传 S1、S2 raw MP4 | 取决于未来工具能力 |
| 10 | W06/W07 | TECHNICAL_RESCUE | 助手把“one camera movement per shot”错误扩大成“one camera movement per 5s clip”，且曾进一步把 3–5镜当成统一修复方向 | 用户指出 S1 僵硬、白纱异常，并补充 S2 单镜环绕实际上成立，要求提升逐段导演判断能力 | 是；已建立 Director Shot-Structure Selector v1，待更多实测验证 |

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