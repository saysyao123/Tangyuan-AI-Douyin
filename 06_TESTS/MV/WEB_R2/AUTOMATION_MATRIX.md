# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因文件被渲染出来就高估自动化或正确性。

## Overall

- Current Stage: `W08A`
- Overall State: `V2_REVOKED / LYRIC_ALIGNMENT_EVIDENCE_BLOCKED`
- Fully automated successful stages: `4` (`W00`, `W03 director-level analysis`, `W06 research/prompt drafting`, `W07 batch QA`)
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Non-aesthetic manual interventions / technical rescues: `8`

## Stage Board

| Stage | 内容 | 实际状态 | 用户操作/备注 |
|---|---|---|---|
| W00 | 能力基线 | AUTO / PASS | 无 |
| W01 | 选歌 | HUMAN_GATE / PASSED | 用户选择歌曲 |
| W02 | BGM截取 | PARTIAL / LOCKED | 用户上传母版并最终确认37.120s片段 |
| W03 | 歌词文本/导演Beat | AUTO / PASS | 精确歌词文本 + Natural Beats；不等于精确时间轴 |
| W04 | 导演方向 | HUMAN_GATE / PASSED | `树影之外` |
| W05 | 首帧 | HUMAN_GATE / PASSED | 9/9通过 |
| W06 | 动态提示词 | AUTO / EXPERIMENTAL PASS | Camera/Shot selector形成 |
| W06-X | Seedance生成 | EXTERNAL_REQUIRED / COMPLETE | 用户外部生成S1–S9 |
| W07 | 动态QA | AUTO / PASS WITH TRIM | 全组可进入素材池 |
| W08A | 歌词时间轴证据 | `BLOCKED / EVIDENCE_PROVENANCE_FAIL` | v2没有独立ASR/LRC/官方timed lyric原始证据 |
| W08B | Picture Edit | `INVALIDATED / REVOKED` | v1/v2均依赖未锁时间轴，不能算成功自动化 |
| W09 | Subtitle | `INVALIDATED / REVOKED` | 样式可复用；timing correctness未通过 |
| W10 | Final QA | `INVALIDATED` | 技术封装检查通过不等于歌词同步正确 |
| W11 | Round Close | NOT_STARTED | 必须在真实时间轴+成片通过后 |

## Why v2 is revoked

V2 used line starts:
`0.470 / 5.451 / 10.954 / 13.827 / 16.788 / 19.702 / 23.470 / 28.439 / 32.618`.

These are essentially the same acoustic candidate family that the W08 blocking gate had already labelled diagnostic-only and forbidden as timing truth.

No raw ASR/forced-alignment result, reliable same-version LRC, or official timed-lyric source was introduced before the file was renamed/generated as `lyrics_exact_v2.srt`.

Classification:
`TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`.

## Circular QA lesson

The earlier internal QA verified:
`rendered subtitles follow SRT`.

It did not verify:
`SRT follows actual vocals`.

Future required separation:
- `ALIGNMENT_GROUND_TRUTH_QA_PASS`
- `SUBTITLE_IMPLEMENTATION_QA_PASS`

The second cannot validate the first.

## Audio packaging ruled out

V2 final AAC vs locked BGM:
- best global lag `0.000s`;
- waveform correlation ~`0.999`.

Therefore FFmpeg/AAC global shift is not the cause.

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 是否未来可消除 |
|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 最终歌曲偏好 | 否 |
| 2 | W02 | FILE_INPUT | 缺实际可处理母版 | 可能 |
| 3 | W02 | TECHNICAL_RESCUE | v1选段边界错误 | 是 |
| 4 | W02 | TECHNICAL_RESCUE | v2选段入口/尾部不足 | 是 |
| 5 | W04 | AESTHETIC_GATE | 导演方向 | 否 |
| 6 | W05 | TECHNICAL_RESCUE | 生图流程停顿/偏虚 | 是 |
| 7 | W06/W07 | TECHNICAL_RESCUE | per-shot运镜误扩大为per-clip单运镜；S1/S2用户纠正 | 是 |
| 8 | W07 | TECHNICAL_RESCUE | S1重复与AI自带BGM未先被系统指出 | 是 |
| 9 | W08 v1 | TECHNICAL_RESCUE | 未锁歌词时间轴即剪辑/字幕，字幕样式漂移 | 是 |
| 10 | W08 v2 | TECHNICAL_RESCUE | 把诊断候选重新包装成exact时间轴；QA循环自证；用户再次发现歌词不同步 | 是；已加入provenance + independent alignment QA硬门禁 |

> 上方 Overall 的 non-aesthetic manual interventions 计当前 R2 主要技术救援/外部输入口径，不把所有历史审美Gate重复计入；Round close时统一清算。

## Process truth fixes after v2

- `mv_golden_runtime.md` upgraded to v1.1: timing provenance mandatory;
- round Master Plan downgraded to summary authority and updated to pre-edit W08A alignment Gate;
- ZERO-CONTEXT START order now loads authoritative Workflow + Golden Runtime before round summaries;
- R1 Golden close requirement upgraded: preserve accepted timing asset/provenance, not only its filename in docs.

## Next

Only valid next path:
`W08A -> acquire real timing evidence -> provenance -> ground-truth alignment QA -> lyric timeline lock`.

No v3 render until this passes.
