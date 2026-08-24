# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录自动化程度，不因“渲染出文件”就高估正确性。

## Overall

- Current Stage: `W08B / V3.1_LONG_CUT_SUBTITLE_VIEWING_GATE`
- Overall State: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS / V3_SUPERSEDED / V3_1_CANDIDATE_RENDERED / TECH_QA_PASS / HUMAN_VIEW_PENDING`
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
| **W02A** | **AUDIO_TIMELINE_PACKAGE** | **PASS / LOCKED** | trusted-lyrics Chinese CTC forced alignment；两层机器 Gate PASS |
| W03 | 语义/Natural Beat | HISTORICAL PASS / TIMING REBOUND | V3/V3.1 都服从 canonical Package |
| W04 | 导演 | PASSED | `树影之外` |
| W05 | 首帧 | PASSED | 9/9 |
| W06 | 动态提示词 | PASS / EXPERIMENTAL | mixed shot structure有效 |
| W06-X | Seedance生成 | EXTERNAL_REQUIRED / COMPLETE | 2S1–2S9 |
| W07 | 动态QA | PASS WITH TRIM | 素材池继续有效 |
| W08A | Editor Audio Gate | PASS | Package + locked BGM revalidated |
| **W08B** | **Picture Edit** | **V3 SUPERSEDED / V3.1 CANDIDATE RENDERED / TECH PASS / HUMAN VIEW PENDING** | 17段降到9段 |
| W09 | Subtitle | NOT_LOCKED | 本次字幕只是诊断overlay；等待用户确认对齐后再做正式样式QA |
| W10 | Final QA | NOT_STARTED | |
| W11 | Close | NOT_STARTED | |

## V3 -> V3.1 reason

User feedback on V3:
- timing/order materially improved;
- picture edit still felt too fragmented / visually busy.

V3.1 correction:
- external fragments reduced `17 -> 9`;
- no external fragment shorter than `2.0s`;
- Anchor Word no longer automatically triggers an external cut;
- S6 generated internal person→bird→person structure carries the `鸟儿` hit inside one source segment;
- S5 becomes a ~`6.792s` breathing shot across the title line;
- final S9 remains an uninterrupted ~`4.292s` release.

Active map:
`W08B_V3_1_LONG_CUT_EDIT_MAP_v1.csv`

QA note:
`W08B_V3_1_LONG_CUT_SUBTITLE_PREVIEW_QA.md`

## Subtitle diagnostic overlay

Requested by user specifically to judge vocal/lyric alignment.

- canonical source: `AUDIO_TIMELINE_PACKAGE/line_timeline.csv`
- no free ASR / no manual timing nudge
- fade disabled for this preview
- exact timestamps rendered subject only to 24fps display quantization (`<41.667ms`; max observed start quantization ~`37ms`)
- W09 final subtitle style is still `NOT_LOCKED`

## V3.1 technical state

- preview SHA-256: `9088dc30c06bc65cacf50dd0b28bbd2042de95ea9a7dcf5a461aef9e903d3c0e`
- `720×1280`, 24fps, SAR 1:1
- video `891 frames / 37.125s`
- locked audio `37.120s`
- preview-vs-locked-BGM best lag `0.000000s`
- audio correlation `0.999043`
- all Seedance source audio discarded
- lower-right platform mark removed by consistent safe crop in reviewed frames

## Current states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = NO` — V3 lock superseded; V3.1 waits for user approval
- `V3_1_PREVIEW_RENDERED = YES`
- `V3_1_TECH_QA_PASS = YES`
- `EDIT_PREVIEW_QA_PASS = NO / HUMAN_VIEW_PENDING`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next

Only valid next action:
**user views V3.1 long-cut + exact subtitle diagnostic preview.**

If picture rhythm + subtitle alignment are both accepted:
`lock V3.1 Edit Map -> EDIT_PREVIEW_QA_PASS -> W09 formal subtitle style/implementation QA`.

If picture alone needs adjustment, modify W08B only.
If a specific subtitle line looks early/late, inspect that line against W02A ground-truth assets first; do not globally nudge subtitles.
