# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W06-X / W07`
- Overall State: `S1_V2_SOURCE_USABLE / S2_ONE_TAKE_PASS / DIRECTOR_SELECTOR_V1_RECORDED`
- Fully automated stages: `3` (`W00`, `W03`, `W06 research/prompt drafting`)
- Human aesthetic gates encountered: `4`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Non-aesthetic manual interventions: `6`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified；无独立 Whisper/faster-whisper；不能直接执行 Seedance |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 用户选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传官方原唱；两次边界修正；最终试听确认 | v3 锁定37.120s；workflow v1.1 |
| W03 | Beat分析 | AUTO | AUTO / LOCKED | 无 | 同版本歌词 + locked audio evidence 完成导演级结构分析 |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PASSED | 审美选择与方向修正 | 最终锁定 `树影之外` |
| W05 | 首帧提示词+生图 | HUMAN_GATE | HUMAN_GATE / PASSED | 整组审美确认 | 9/9 首帧通过 |
| W06 | 动态提示词 | AUTO | AUTO / EXPERIMENTAL | 无 | Camera Contract + Director Selector 仍在实验层；Source Audio hard rule 已加强 |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | ACTIVE | 外部生成+上传 | S1 v1 / S1 v2 / S2 已回传 |
| W07 | 动态QA/返工设计 | AUTO | PARTIAL STARTED | 用户补充观感 | S1 v2=可用素材但需剪重复；S2=单镜正向样本；声音规则升级 |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | AI源音轨默认强制删除；字幕来自锁定音频证据 |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## Generated-video Evidence

### S1 v1 — FAIL
- fixed one-take visual progression too weak;
- detached scarf-like artifact;
- failure proves weak one-take is bad, not that all one-takes are bad.

### S1 v2 — PASS_AS_SOURCE / TRIM_REQUIRED
- 5.088s / 720×1280 / 24fps;
- multi-shot camera energy substantially improved;
- approximate visual discontinuities: `2.04 / 2.42 / 3.13 / 3.88s`;
- `2.04–3.12s` contains two similar low-angle character beats; trim one rather than regenerate the whole source;
- principle learned: generated raw clip may be `SOURCE_USABLE / TRIM_REQUIRED`, not binary whole-clip pass/fail.

### S1 v2 Audio — SOURCE_AUDIO_POLICY_FAIL
- returned soundtrack contains clearly music-like harmonic content despite soft `不要BGM` wording;
- visual source remains usable because final locked song replaces all source audio;
- `04_HARNESS/rules/ai_video.md` upgraded to v1.2: explicitly forbid BGM / music / melody / beat / chords / singing / humming / narration / dialogue / voices;
- default `SOURCE_AUDIO = REMOVE`; if music still appears, mark failure and strip it in W08 rather than discard good visuals.

### S2 v1 — PASS
- 5.04s continuous small Arc/orbit-like one-take;
- strong foreground/midground/background parallax;
- simple subject action + clear camera path + more flattering endpoint;
- retained as positive one-take sample.

## Director Shot-Structure Selector v1

Experimental file:
`06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`

Decision model:
`lyric task → first-frame potential → shot-count decision → one Camera Contract per Shot → load budget → beauty/comfort gate`.

No universal default:
- 1 Shot when continuity/camera progression is the beauty;
- 2–3 Shots for setup/event/aftermath or attention shift;
- 3–5 Shots for dense lyric / motion peak / Hook when added contrast is earned.

### Adjacent Shot Contrast Gate — EXPERIMENTAL

Consecutive shots should differ in at least 2 of:
`shot size / angle / subject scale / camera direction / focal plane / dominant action / dominant visual subject`.
Otherwise merge or remove one before generation.

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 最终歌曲偏好 | 选择歌曲 | 否 |
| 2 | W02 | FILE_INPUT | 缺官方可处理音频文件 | 上传3:16母版 | 可能 |
| 3 | W02 | TECHNICAL_RESCUE | v1区间错误 | 指出副歌起点/尾句错误 | 是 |
| 4 | W02 | TECHNICAL_RESCUE | v2边界听感不足 | 要求前移0.5s并多保留一句 | 目标上是 |
| 5 | W02 | AESTHETIC_GATE | v3最终听感 | `可以` | 否 |
| 6 | W04 | AESTHETIC_GATE | 导演世界与MV美学 | 否决连续树叙事、通过树影之外 | 否 |
| 7 | W05 | TECHNICAL_RESCUE | 生图流程停顿/一张偏虚 | 用户提醒继续 | 是 |
| 8 | W05 | AESTHETIC_GATE | 首帧整组美学 | 确认九张 | 否 |
| 9 | W06-X | EXTERNAL_TOOL | 无 Seedance 执行接口 | 外部生成并回传 raw clips | 取决于工具能力 |
| 10 | W06/W07 | TECHNICAL_RESCUE | 错误把 per-shot 运镜理解成 per-clip 单运镜，后又差点统一多镜修复 | 用户用 S1/S2 对照纠正 | 是；Director Selector 已建立 |
| 11 | W07 | TECHNICAL_RESCUE | S1 v2 虽可用，但中段重复镜头与模型自带BGM未在交付前由系统先指出 | 用户指出可通过剪辑处理重复，并要求深化声音硬规则 | 是；新增 Adjacent Shot Contrast Gate，Source Audio hard rule 升级 v1.2 |

类型只允许：`AESTHETIC_GATE / FILE_INPUT / EXTERNAL_TOOL / LOGIN/CAPTCHA / TECHNICAL_RESCUE`

## Final Questions

R2 结束时必须回答：
1. 网页端能否自动完成选歌研究？
2. 不靠 Codex，网页端能否自动裁剪用户上传 BGM？
3. 导演 / 首帧 / 提示词能否自动完成到只需审美 Gate？
4. Seedance 是否仍是最大人工断点？
5. 视频上传回来后，QA / 剪辑 / 字幕能否自动闭环？
6. 哪些能力应留在 Web，哪些应移交 Codex？