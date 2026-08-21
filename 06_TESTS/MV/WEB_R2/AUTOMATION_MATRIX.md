# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W07`
- Overall State: `VISUAL_BATCH_PASS_WITH_TRIM / W08_READY`
- Fully automated stages: `4` (`W00`, `W03`, `W06 research/prompt drafting`, `W07 batch QA`)
- Human aesthetic gates encountered: `4`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Non-aesthetic manual interventions: `6`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传母版+边界确认 | final 37.120s |
| W03 | Beat分析 | AUTO | AUTO / LOCKED | 无 | six Natural Beats |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PASSED | 审美确认 | `树影之外` |
| W05 | 首帧提示词+生图 | HUMAN_GATE | HUMAN_GATE / PASSED | 整组审美确认 | 9/9 first frames passed |
| W06 | 动态提示词 | AUTO | AUTO / EXPERIMENTAL | 无 | Director Selector + Camera Contract tested |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | COMPLETED FOR CURRENT BATCH | 外部生成+上传 | S1–S9 all returned |
| W07 | 动态QA/返工设计 | AUTO | AUTO / VISUAL_PASS_WITH_TRIM | 无新增外部操作 | 9/9 reviewed; no full-batch regen; S7 only regen watch |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | READY | 看片确认 | strip all AI audio, trim, watermark cleanup, locked-BGM edit |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W07 Full Batch Evidence

QA file:
`06_TESTS/MV/WEB_R2/W07_FULL_BATCH_QA_v1.md`

Batch format:
- 9 clips;
- each ~5.04s;
- 720×1280;
- 24fps.

Status:
- S1 `SOURCE_USABLE / TRIM_REQUIRED`
- S2 `PASS_FULL / POSITIVE ONE-TAKE SAMPLE`
- S3 `PASS_FULL`
- S4 `PASS_FULL / STRONG DYNAMIC SAMPLE`
- S5 `PASS_FULL / BREATHING SHOT`
- S6 `PASS_FULL / STRONG LYRIC-HIT SAMPLE`
- S7 `SOURCE_USABLE / TRIM_REQUIRED / REGEN_WATCH`
- S8 `PASS_FULL / SHORTEN IN SEQUENCE`
- S9 `PASS_FULL / FINAL RELEASE`

No full-batch regeneration is recommended.

## Director evidence after full batch

Actual shot-structure distribution now includes:
`multi-shot / one-take Arc / 2-shot / 3-shot / one-take breathing / 3-shot discovery / multi-shot peak / one-take reset / one-take release`.

This supports the experimental selector:
`lyric task → first-frame potential → shot-count decision → one Camera Contract per Shot → load budget → edit-value gate`.

Do not promote a universal shot-count recipe.

## Whole-set trim risks

- S1 middle low-angle repetition;
- S1/S5 both use giant tree + light shaft + small person;
- S8/S9 rooftop-sky visual family overlaps strongly;
- S7 ~2.8–4.0s fabric topology/visual dominance risk.

## Audio / watermark status

- 9/9 files contain AAC source audio;
- source audio must be stripped at ingest;
- W02 locked BGM remains the only timing/music truth;
- 9/9 visibly contain lower-right `豆包AI生成` mark; W08 cleanup required.

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

类型只允许：`AESTHETIC_GATE / FILE_INPUT / EXTERNAL_TOOL / LOGIN/CAPTCHA / TECHNICAL_RESCUE`

## Next

W08 should proceed automatically from the returned raw clips and locked BGM, then stop only at the designed final viewing gate.
