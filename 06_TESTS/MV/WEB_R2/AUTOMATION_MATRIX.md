# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W08`
- Overall State: `FIRST_CUT_RENDERED / AWAITING_AESTHETIC_GATE`
- Fully automated stages: `5` (`W00`, `W03`, `W06 research/prompt drafting`, `W07 batch QA`, `W08 first-cut render/pre-delivery QA`)
- Human aesthetic gates encountered: `5`
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
| W07 | 动态QA/返工设计 | AUTO | AUTO / VISUAL_PASS_WITH_TRIM | 无新增外部操作 | 9/9 reviewed; no full-batch regen |
| W08 | 剪辑/字幕/Final v1 | AUTO if inputs ready | AUTO / FIRST_CUT_RENDERED | 当前只需看片确认 | 37.12s edit rendered, AI audio stripped, risky fragments trimmed, marks cropped out, basic lyric layer burned in, pre-delivery technical QA complete |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | W08通过后进入 |

## W08 Evidence

QA file:
`06_TESTS/MV/WEB_R2/W08_EDIT_V1_QA.md`

Output:
`如果你也刚好抬头看树_MV_WEB_R2_第一版成片.mp4`

Technical verification:
- audio `37.120s`;
- video `37.125s` (24fps frame quantization);
- 720×1280;
- SAR `1:1`;
- DAR `9:16`;
- H.264 + AAC stereo 44.1kHz;
- SHA-256 `e7f4855b862c2df8bca303028a826f474775f5fd153760c4b047e213a9148f9f`.

Edit QA actions completed automatically:
- stripped all Seedance source audio by mapping only locked W02 BGM;
- removed S1 repeated middle low-angle material;
- excluded S7 ambiguous large-fabric loop material;
- shortened S8 relative to S9;
- slowed/extended S9 for cloud release;
- used a ratio-safe crop for visible generator marks;
- checked final sampled frames for subtitle safe zone and retained-frame composition;
- caught an intermediate non-square pixel-aspect issue before handoff and rebuilt at SAR1:1 without user intervention.

Subtitle v1:
- exact known same-version lyrics;
- locked-audio waveform / phrase valleys + W03 structure evidence;
- no Whisper/faster-whisper claim;
- line-level first-cut timing only, subject to aesthetic viewing adjustment rather than falsely claiming word-level ASR precision.

## W07 Director Evidence Carried Forward

Mixed structure remains validated at current evidence level:
`multi-shot / one-take Arc / 2-shot / 3-shot / one-take breathing / 3-shot discovery / multi-shot peak / one-take reset / one-take release`.

Do not promote a universal shot-count recipe.

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
| 12 | W08 | AESTHETIC_GATE | 第一版完整成片的节奏/歌词/整体观感属于设计保留的最终观看判断 | `PENDING` | 否 |

类型只允许：`AESTHETIC_GATE / FILE_INPUT / EXTERNAL_TOOL / LOGIN/CAPTCHA / TECHNICAL_RESCUE`

## Next

User reviews W08 first cut.
- local edit/subtitle changes -> W08 v2;
- pass -> W09 retrospective / rule promotion / round close.
