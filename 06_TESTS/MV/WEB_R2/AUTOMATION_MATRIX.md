# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录自动化程度，不因“渲染出文件”就高估正确性。

## Overall

- Current Stage: `W08B / V3_EDIT_MAP`
- Overall State: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Timing technical rescues: `2 major edit failures`
- Audio timeline hard gate: `PASS`

## Stage Board

| Stage | 内容 | 实际状态 | 备注 |
|---|---|---|---|
| W00 | 能力基线 | AUTO / PASS | |
| W01 | 选歌 | HUMAN_GATE / PASSED | 用户选歌 |
| W02 | BGM截取 | LOCKED | 37.120s + SHA |
| **W02A** | **AUDIO_TIMELINE_PACKAGE** | **PASS / LOCKED** | Route B trusted-lyrics CTC forced alignment；两层机器 Gate PASS |
| W03 | 语义/Natural Beat | HISTORICAL PASS / NEEDS TIMING REFERENCE UPDATE | 视觉语义仍有效；正式 V3 时间引用改用锁定 Package |
| W04 | 导演 | PASSED | `树影之外`；已生成素材不作废 |
| W05 | 首帧 | PASSED | 9/9 |
| W06 | 动态提示词 | PASS / EXPERIMENTAL | Camera selector有效 |
| W06-X | Seedance生成 | EXTERNAL_REQUIRED / COMPLETE | S1–S9 |
| W07 | 动态QA | PASS WITH TRIM | 素材池有效 |
| W08A | Editor Audio Gate | PASS | Package manifest + locked BGM SHA revalidated |
| **W08B** | **Picture Edit / V3 Edit Map** | **CURRENT / NOT_YET_LOCKED** | 下一步 |
| W09 | Subtitle | NOT_STARTED_FOR_V3 | timing 已锁；等待 Edit Preview QA 后只做样式/实现 |
| W10 | Final QA | NOT_STARTED_FOR_V3 | |
| W11 | Close | NOT_STARTED | |

## Why V1/V2 remain revoked

### V1
- 未建立真实歌词时间轴就进入 Picture Edit / Subtitle；
- 字幕样式发生 R1 Golden 漂移。

### V2
- 把早先 `DIAGNOSTIC_ONLY` 的声学候选重新包装成 `exact`；
- 当时没有 Strong Route raw evidence / provenance；
- QA 只证明视频服从 SRT，没有证明 SRT 服从真实人声。

分类：
`TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`。

AAC/FFmpeg全局偏移已排除：
- lag `0.000s`；
- correlation ~`0.999`。

## W02A resolution

Strong Route:
- exact locked v3 BGM SHA: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`;
- trusted canonical 10-line lyrics;
- Chinese CTC forced alignment;
- model: `jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn`;
- revision: `d2af85f00e501bb8b8bcedef3b5c51eabb883088`;
- 92 target tokens -> 92 aligned spans.

Ground-truth QA:
- CTC vs old diagnostic candidate median start delta: `0.125s`;
- first/second repeated chorus shift median: `81.527s`;
- max repeat-shift deviation: `0.061s`;
- repeated occurrence mapping PASS.

Machine Gates:
- Timing Core Gate: exit `0`, PASS, 10 lines, 0 errors/warnings;
- Complete Package Gate: exit `0`, PASS, 10 lines, 10 anchors, 21 music events, 0 errors/warnings;
- `package_manifest.json`: `AUDIO_TIMELINE_PACKAGE_LOCKED=true`.

Canonical sync:
- workflow run `32655263045`;
- package payload SHA `c8308512c9f1dd63fabe70dcafb27e0a75b2d0d3450f80371429f665866656be`;
- receipt: `W02A_CANONICAL_PACKAGE_SYNCED`.

## New process truth after retrofit

Authoritative runtime now requires：

`BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ semantic Beat / Director timing allocation
→ visual production
→ `EDITOR_AUDIO_GATE_PASS`
→ Picture Edit
→ Subtitle implementation
→ Final QA。

Current package path：
`06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`

Current timing evidence status：
- locked audio identity: YES
- exact lyric text/order: YES
- strong accepted raw timing evidence: YES
- provenance verified: YES
- ground-truth alignment QA: YES
- lyric timeline locked: YES
- anchor map locked: YES
- music event map verified: YES
- Package locked: YES
- Editor Audio Gate: PASS

## Manual Intervention lesson

The user should not need to catch timing failures after final render.
A future timing problem counts as `TECHNICAL_RESCUE` if:
- Package is claimed PASS without strong raw evidence/provenance；or
- ground-truth QA is replaced by render-vs-SRT implementation QA。

## Next

Only valid next path：

`W08B V3 Edit Map`

Load the locked `line_timeline.csv + anchor_words.csv + music_events.csv + VISUAL_SOURCE_MAP`, then reconcile lyric/music truth with usable visual-action windows.

No V3 render until `EDIT_MAP_LOCKED` and `EDIT_PREVIEW_QA_PASS`.
