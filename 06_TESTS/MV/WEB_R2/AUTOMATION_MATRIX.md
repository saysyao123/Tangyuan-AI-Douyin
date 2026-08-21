# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W08/W09`
- Overall State: `SECOND_CUT_REVIEW_RENDERED / INTERNAL_QA_PASS / AWAITING_VIEWING_GATE`
- Fully automated stages: `5` (`W00`, `W03 director-level analysis`, `W06 research/prompt drafting`, `W07 batch QA`, `W08 v2 rebuild/internal QA`)
- Human aesthetic/viewing gates encountered: `5`
- Human aesthetic/viewing gates passed: `4`
- External-required stages encountered: `1`
- Non-aesthetic manual interventions: `7`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub/Web/Files/local AV stack verified |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE / PASSED | 最终选歌 | 选择 `如果你也刚好抬头看树` |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | PARTIAL / LOCKED | 上传母版+边界确认 | final 37.120s |
| W03 | Beat / lyric structure | AUTO | AUTO / DIRECTOR-LEVEL LOCK | 无 | exact lyric text + six Natural Beats；不是 word-level ASR |
| W04 | 导演/生产分配 | HUMAN_GATE | HUMAN_GATE / PASSED | 审美确认 | `树影之外` |
| W05 | 首帧提示词+生图 | HUMAN_GATE | HUMAN_GATE / PASSED | 整组审美确认 | 9/9 first frames passed |
| W06 | 动态提示词 | AUTO | AUTO / EXPERIMENTAL | 无 | Director Selector + Camera Contract tested |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | COMPLETED FOR CURRENT BATCH | 外部生成+上传 | S1–S9 all returned |
| W07 | 动态QA/返工设计 | AUTO | AUTO / VISUAL_PASS_WITH_TRIM | 无新增外部操作 | 9/9 reviewed; no full-batch regen |
| W08A | 音频/歌词时间轴 | AUTO | `REBUILT / PROJECT-LEVEL LINE MAP` | 无 | v1 timing revoked；v2逐句start/end重新从locked audio建立；不宣称Whisper |
| W08B | Picture Edit v2 | AUTO after timing map | `AUTO / REBUILT` | 无 | 按逐句/Beat重新映射；不是在v1上挪字幕 |
| W09 | Subtitle render/sync | AUTO | `AUTO / GOLDEN STYLE RESTORED / INTERNAL QA PASS` | 无 | R1 Golden字幕规格恢复；逐句出现/消失抽检 |
| W10 | Final technical QA | AUTO | `INTERNAL QA PASS FOR REVIEW CUT` | 当前只需看片 | 画幅、音轨、风险片段、字幕、安全区、黑帧检查完成 |
| W11 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | v2通过后进入 |

## W08 v1 failure

`如果你也刚好抬头看树_MV_WEB_R2_第一版成片.mp4` remains a revoked failure artifact.

Classification: `TECHNICAL_RESCUE`.

Failure:
- edit/subtitle work proceeded before a durable line-level timing map;
- user identified lyric/subtitle mismatch and therefore invalid beat/visual mapping;
- subtitle visual style drifted from R1 Golden.

## W08 v2 review-cut evidence

QA file:
`06_TESTS/MV/WEB_R2/W08_V2_REBUILD_QA.md`

Output:
`如果你也刚好抬头看树_MV_WEB_R2_第二版成片.mp4`

SHA-256:
`ff1bbb67427b0067001ebe97f5e0d7bcb3e4c9c434606c2c833ba280647adc3b`

Technical verification:
- ~37.125s at 24fps frame quantization against locked 37.120s BGM;
- 720×1280;
- SAR `1:1`;
- DAR `9:16`;
- H.264 + AAC stereo 44.1kHz;
- no black-frame event detected;
- final subtitle-render audio stream is bit-identical to the v2 base-edit audio stream;
- Seedance source audio is not mapped.

## v2 line-level map

- 0.470–4.810 `如果你也刚好抬头看树`
- 5.451–10.680 `我要学着树叶翩翩起舞`
- 10.954–13.189 `喊几声布谷布谷`
- 13.827–15.850 `或许少有人知道`
- 16.788–18.800 `有鸟儿是这样叫`
- 19.702–21.980 `好吧 哎哟哎哟`
- 23.470–26.770 `一颗心叽叽喳喳飞过了树梢`
- 28.439–32.540 `如果你也刚好抬头看树`
- 32.618–35.650 `向一朵白云学习如何漂浮`

No Whisper/faster-whisper claim.

Method: exact known lyric order constrained against locked-audio phrase onsets, vocal-band energy, breath/phrase valleys, beat evidence, repeated-chorus correspondence and final vocal resolution. The resulting SRT/CSV was used first; picture edit and subtitles were then built from that asset.

This remains project-level timing evidence until direct playback review; cross-round runtime still prefers actual ASR/forced alignment or reliable same-version timed lyric evidence when available.

## v2 edit/QA corrections

- v1 edit-map timing not reused;
- lyric/music windows drive the picture map;
- S1/S2 opening rebuilt around L1;
- S3/S4 align to L2 leaf-dance phrase;
- S6 discovery is used for bird-related lines;
- S5 is used as a deliberate breathing/unknown-space beat;
- only clean early S7 peak survives;
- final self-audit removed S7 late fabric-tail material entirely;
- S8 begins during the musical gap before title reprise, then carries L8 as one continuous high-space reset;
- S9 carries L9 and final visual tail;
- R1 Golden subtitle look restored: light Chinese text, tightly fitted dark translucent rounded box, centered text, fixed lower safe area, restrained fade;
- each subtitle line sampled before/inside/after its time window;
- platform marks cropped consistently.

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
| 10 | W06/W07 | TECHNICAL_RESCUE | per-shot运镜被错误扩大成per-clip单运镜 | 用S1/S2纠正 | 是；Director Selector已建立 |
| 11 | W07 | TECHNICAL_RESCUE | S1重复与自带BGM未先被系统指出 | 补充观感 | 是；Adjacent Shot Contrast + Source Audio hard rule |
| 12 | W08 | TECHNICAL_RESCUE | 未先建立逐句歌词时间轴就进入剪辑/字幕，且字幕规格漂移 | 指出必须先深度分析BGM/时间轴，并复用R1 Golden字幕与自审流程 | 是；v1撤销，v1.2 no-skip workflow + Golden Runtime contract已建立 |
| 13 | W08/W09 | VIEWING_GATE | 第二版已完成内部技术QA，需判断真实整片歌曲-画面观感与歌词同步 | `PENDING` | 否；最终整片观看属于保留的人类验收 |

类型语义：`AESTHETIC_GATE / FILE_INPUT / EXTERNAL_TOOL / LOGIN/CAPTCHA / TECHNICAL_RESCUE`；本表中的 `VIEWING_GATE` 仅描述当前整片验收语义，最终关账时归入 HUMAN/AESTHETIC viewing decision。

## Next

User reviews the W08 v2 complete cut.
- objective lyric/timing error -> `TECHNICAL_RESCUE`, repair timing asset before polish;
- local aesthetic edit request -> W08/W09 v3;
- pass -> final polish / W11 retrospective and Round close.