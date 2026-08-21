# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W08A`
- Overall State: `TECHNICAL_RESCUE / FIRST_CUT_REVOKED / LYRIC_TIMELINE_BLOCKED`
- Fully automated stages: `4` (`W00`, `W03 director-level analysis`, `W06 research/prompt drafting`, `W07 batch QA`)
- Human aesthetic gates encountered: `4`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Non-aesthetic manual interventions: `7`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传母版+边界确认 | final 37.120s |
| W03 | Beat / lyric structure | AUTO | AUTO / DIRECTOR-LEVEL LOCK | 无 | exact lyric text + six Natural Beats；不是 subtitle-level timing lock |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PASSED | 审美确认 | `树影之外` |
| W05 | 首帧提示词+生图 | HUMAN_GATE | HUMAN_GATE / PASSED | 整组审美确认 | 9/9 first frames passed |
| W06 | 动态提示词 | AUTO | AUTO / EXPERIMENTAL | 无 | Director Selector + Camera Contract tested |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | COMPLETED FOR CURRENT BATCH | 外部生成+上传 | S1–S9 all returned |
| W07 | 动态QA/返工设计 | AUTO | AUTO / VISUAL_PASS_WITH_TRIM | 无新增外部操作 | 9/9 reviewed; no full-batch regen |
| W08A | 音频/歌词时间轴锁定 | AUTO if timing evidence available | `BLOCKED / IN REPAIR` | 无 | 必须先锁逐句时间轴；当前强 timing source 尚未锁定，禁止继续剪辑 |
| W08B | Picture Edit | AUTO after W08A | `INVALIDATED / NOT_STARTED V2` | 无 | v1 edit revoked because it was built before lyric timeline lock |
| W09 | Subtitle render/sync | AUTO after W08B | NOT_STARTED | 无 | 先加载 R1 Golden subtitle spec，再做 style/sync QA |
| W10 | Final polish/QA | AUTO after subtitle gates | NOT_STARTED | 看片确认 | 只有所有自审 Gate PASS 后才允许交付 |
| W11 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W08 first-cut failure record

Historical file:
`如果你也刚好抬头看树_MV_WEB_R2_第一版成片.mp4`

Technical MP4 checks passed, but the creative/timing workflow did not.

### What was skipped

The assistant did not create and audit a durable `LYRIC_TIMELINE_LOCKED` asset before:
- mapping picture cuts;
- deciding lyric-hit points;
- burning subtitles.

Instead it relied on exact lyric text + waveform/valley estimates + director-level structure, which is insufficient for exact line timing.

### User-detected consequence

The user correctly identified:
- lyric subtitles do not match sung timing;
- beat/cut/video mapping based on that timeline is therefore wrong/unreliable;
- subtitle visual form also drifted from the previous Golden edit requirement;
- existing workflow/self-audit was not actually enforced.

Classification:
`TECHNICAL_RESCUE`.

The previous pending W08 `AESTHETIC_GATE` entry is removed. The first cut was not valid enough to reach the aesthetic gate.

## Workflow repair

`04_HARNESS/workflows/mv.md` upgraded from v1.1 to v1.2.

Mandatory state chain now includes a blocking pre-edit timing stage:

`BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_SYNC_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`.

No downstream render is valid if an earlier state is missing.

Project-specific gate:
`06_TESTS/MV/WEB_R2/W08_AUDIO_LYRIC_TIMELINE_GATE_v2.md`.

## R1 Golden subtitle reference restored

R1 user-accepted evidence explicitly says:
- visual-segment-derived subtitle timing was wrong;
- subtitle timing must come from locked audio alignment;
- corrected same-version timing was user-reviewed as accurate;
- accepted base visual system = light Chinese text + dark semi-transparent rounded box tightly fitted to text + text centered horizontally/vertically + comfortable fixed lower safe area + restrained fade + max 2 lines + no base karaoke effect.

Future W09 must load this reference before rendering, not reconstruct style from memory.

## Current W08A status

- `BGM_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_TIMELINE_LOCKED = NO`
- `BEAT_MAP_VERIFIED = NO` for edit-level use
- `EDIT_MAP_LOCKED = NO`
- `DELIVERABLE_RENDERED = NO`

Acoustic candidate starts / breath valleys remain diagnostic only. They cannot independently promote the timeline.

Strong timing evidence must be obtained from actual ASR/forced alignment, reliable same-version LRC, or another directly verifiable timed same-version source, then corrected against the known lyrics and boundary-audited.

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 最终歌曲偏好 | 选择歌曲 | 否 |
| 2 | W02 | FILE_INPUT | 缺官方可处理母版 | 上传音频 | 可能 |
| 3 | W02 | TECHNICAL_RESCUE | v1区间错误 | 指出错误 | 是 |
| 4 | W02 | TECHNICAL_RESCUE | v2边界不足 | 要求调整 | 目标上是 |
| 5 | W02 | AESTHETIC_GATE | v3最终听感 | 通过 | 否 |
| 6 | W04 | AESTHETIC_GATE | 导演世界/MV美学 | 修正并通过 | 否 |
| 7 | W05 | TECHNICAL_RESCUE | 生图流程停顿/偏虚 | 提醒继续 | 是 |
| 8 | W05 | AESTHETIC_GATE | 首帧整组美学 | 确认九张 | 否 |
| 9 | W06-X | EXTERNAL_TOOL | 无 Seedance 执行接口 | 外部生成 S1–S9 | 取决于工具能力 |
| 10 | W06/W07 | TECHNICAL_RESCUE | 错误把 per-shot 运镜理解为 per-clip 单运镜并差点统一多镜修复 | 用户用 S1/S2 纠正 | 是；Director Selector 已建立 |
| 11 | W07 | TECHNICAL_RESCUE | S1 v2 重复与自带BGM未先被系统指出 | 用户补充观感 | 是；已加入 Adjacent Shot Contrast + Source Audio hard rule |
| 12 | W08 | TECHNICAL_RESCUE | 未先锁逐句歌词时间轴就进入剪辑/字幕，违反 R1 已有 Golden 规则；卡点、字幕、镜头映射因此失真 | 用户指出必须先深度分析BGM并确认歌词时间轴，同时指出字幕规格与 Golden 不一致、流程存在跳步 | 是；v1作废，workflow v1.2加入不可跳过的 W08A Gate |

类型只允许：`AESTHETIC_GATE / FILE_INPUT / EXTERNAL_TOOL / LOGIN/CAPTCHA / TECHNICAL_RESCUE`

## Next

Continue W08A automatically. Do not ask the user to manually timestamp lyrics unless automated/evidence-based alignment routes are genuinely exhausted.

Only after `LYRIC_TIMELINE_LOCKED + BEAT_MAP_VERIFIED` may W08B rebuild the picture edit from scratch.
