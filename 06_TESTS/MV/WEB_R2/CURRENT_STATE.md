# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。新 Chat / Agent 默认先读 Workflow v1.4 + Golden Runtime v1.3 + MV Audio Timeline Rule，再读本文件。进入导演/动态/剪辑/字幕阶段时 JIT 加载 `04_HARNESS/rules/mv_editing.md`。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08B / V3.1_LONG_CUT_PROCESS_LOCK + PRE_W09_SUBTITLE_OPTIMIZATION`
- STAGE_NAME: `long-cut picture direction accepted as improved; editing runtime promoted; subtitle style optimization next`
- STATE: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS / V3_SUPERSEDED / V3_1_DIRECTION_IMPROVED / EDITING_RUNTIME_PROMOTED / SUBTITLE_STYLE_NOT_YET_LOCKED`
- BRANCH: `test/mv-web-r2`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.4
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md` v1.3
- AUDIO_TIMELINE_RULE: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- EDITING_RUNTIME: `04_HARNESS/rules/mv_editing.md` v1.0
- AI_VIDEO_RULE: `04_HARNESS/rules/ai_video.md` v1.3
- AUDIO_PACKAGE: `06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`
- CURRENT_EDIT_MAP: `06_TESTS/MV/WEB_R2/W08B_V3_1_LONG_CUT_EDIT_MAP_v1.csv`
- CURRENT_PREVIEW_QA: `06_TESTS/MV/WEB_R2/W08B_V3_1_LONG_CUT_SUBTITLE_PREVIEW_QA.md`
- PROCESS_RETROFIT: `06_TESTS/MV/WEB_R2/W08B_EDITING_RUNTIME_RETROFIT_v1.md`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Locked upstream truth

- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `BGM_LOCKED` — source `139.930s–177.050s`, content timeline `37.120s`, SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- W02A: `AUDIO_TIMELINE_PACKAGE_LOCKED / PASS`
- W04: `DIRECTOR_PLAN_LOCKED` — `树影之外`
- W05: `FIRST_FRAME_SET_LOCKED` — 9/9 accepted
- W06/W06-X: dynamic prompt/camera experiment + 2S1–2S9 returned
- W07: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT` — visual batch pass with trim
- W08A: `EDITOR_AUDIO_GATE_PASS`

Do not reopen W02A unless audio identity/version/clip/speed/lyrics changes.
Do not reopen approved visual generation unless a real source shortage is proven.

## Revoked / superseded artifacts

### V1
`REVOKED / TECHNICAL_RESCUE`
- picture/subtitle work began before valid lyric timing;
- subtitle style drifted.

### V2
`REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`
- wrong excerpt assumption;
- diagnostic timing promoted without Strong Route provenance;
- render-vs-SRT QA was mistaken for SRT-vs-vocal ground-truth QA.

### V3
`SUPERSEDED_BY_USER_AESTHETIC_FEEDBACK`
- timing/order correction was materially better;
- 17 external fragments still felt too busy/fragmented.

## Canonical W02A lyric clock｜LOCKED

| Line | Lyric | Start | End |
|---|---|---:|---:|
| L01 | 我要学着树叶翩翩起舞 | 0.440 | 3.702 |
| L02 | 喊几声布谷布谷 | 3.702 | 6.023 |
| L03 | 或许少有人知道 | 6.023 | 8.304 |
| L04 | 有鸟儿是这样叫 | 8.304 | 10.946 |
| L05 | 好吧哎哟哎哟 | 10.946 | 13.067 |
| L06 | 一颗心叽叽喳喳飞过了树梢 | 13.067 | 19.090 |
| L07 | 如果你也刚好抬头看树 | 19.090 | 23.493 |
| L08 | 向一朵白云学习如何漂浮 | 23.493 | 28.415 |
| L09 | 在某天某个随机的清晨或是下午 | 28.415 | 32.838 |
| L10 | 坐下来别那么严肃 | 32.838 | 37.120 |

Canonical Package files remain authoritative:
- `line_timeline.csv`
- `lyrics_exact.srt`
- `anchor_words.csv`
- `music_events.csv`
- raw forced-alignment evidence + provenance + manifest.

## Audio Timeline placement｜PROMOTED PROCESS TRUTH

The timing layer position is now explicitly locked as:

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ **`AUDIO_TIMELINE_PACKAGE_LOCKED`**
→ Natural Beat / lyric semantic analysis
→ Director allocation
→ First Frames
→ Dynamic Prompt / Generation
→ W07 `VISUAL_SOURCE_MAP`
→ Picture Edit
→ Subtitle Style/Implementation
→ Final QA.

Reason:
- earlier than BGM lock wastes work if excerpt/version changes;
- later than BGM lock allows guessed timing to contaminate Director and visual production.

## V3.1 Long-Cut direction｜USER FEEDBACK INTEGRATED

V3.1 reduced external picture fragments from `17` to `9` and was judged **better / calmer** by the user.

Promoted editing truths:
- lyrical/emotional MV defaults to long-cut-first;
- Anchor Word is not automatically a picture cut;
- preserve complete internal source action arcs;
- avoid consecutive <2s external fragments;
- avoid short-distance A-B-A recycling;
- final release should breathe;
- Fragmentation Gate runs before Edit Map lock.

Current V3.1 active sequence remains the preferred picture direction:
1. S2 Arc / leaves — 0.000–3.000
2. S4 dance — 3.000–7.125
3. S6 person→bird→person — 7.125–12.125
4. S3 emotional close-up — 12.125–14.125
5. S7 clean peak — 14.125–16.833
6. S5 long breathing shot — 16.833–23.625
7. S8 sky/space — 23.625–28.417
8. S1 giant-tree/morning-light — 28.417–32.833
9. S9 final release — 32.833–37.125

## Dynamic-source production truth｜PROMOTED

Future 5s dynamic-source generation should NOT default to dense multi-shot clips.

Preferred mixed source portfolio:
- `1-shot`: HOLD / space / continuous emotion / RELEASE;
- `2-shot`: default semantic asset, setup-event or detail-emotion;
- `3-shot`: selected discovery / setup-event-aftermath / PEAK;
- `>3-shot`: exceptional hook/peak only.

Default for Seedance-like ~5s source: **1–2 shots**, 3 shots only when the lyric/director task earns it.

Editor needs editorial headroom, not raw cut density:
- clean in/out;
- complete motion arc;
- stable endpoint;
- meaningful internal cuts only;
- W07 executable clean/risk windows.

## WEB watermark handling｜PROMOTED TEMPORARY FALLBACK

User feedback: top-left and bottom-right platform marks can still leak in WEB previews.

Until Codex/publish-grade cleanup is used, WEB editing must:
- enlarge/crop the **whole source consistently**;
- derive the transform from the worst watermark position across the batch;
- apply the same geometry to the full source batch unless a real framing failure requires escalation;
- preserve 9:16 and `SAR=1:1`;
- explicitly inspect top-left and bottom-right risk frames before delivery;
- if any watermark remains, increase the uniform safe crop/zoom before user handoff.

Preferred hierarchy:
`watermark-free HD source > Codex precise cleanup > WEB uniform whole-source zoom/crop fallback`.

## Subtitle state

V3.1 diagnostic subtitle overlay used the canonical W02A lyric clock with fade disabled so timing could be judged without fade latency.

User feedback now permits the next phase:
**subtitle form/style optimization**.

Still locked:
- lyric timing cannot be changed to fit picture cuts;
- no free ASR reinterpretation;
- no manual global nudge without line-specific evidence.

Next subtitle work may optimize only:
- font / size;
- tight semi-transparent box;
- horizontal + vertical centering;
- padding;
- lower safe area;
- long-line wrapping;
- restrained fade after alignment view is accepted;
- consistency across all lines.

## Runtime states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `V3_1_LONG_CUT_DIRECTION = PREFERRED / USER_SAYS_BETTER`
- `EDITING_RUNTIME_PROMOTED = YES`
- `WEB_WATERMARK_FALLBACK_PROMOTED = YES`
- `DYNAMIC_SOURCE_PORTFOLIO_RULE_PROMOTED = YES`
- `SUBTITLE_ALIGNMENT_TIMING_SOURCE = LOCKED_W02A`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next Allowed Action

1. Keep current V3.1 long-cut picture direction.
2. For any further WEB preview/render, apply the promoted uniform whole-source watermark-safe enlargement/crop and validate both corners.
3. Enter subtitle visual optimization using canonical `lyrics_exact.srt` unchanged.
4. After subtitle style candidate is rendered, perform:
   - style QA;
   - rendered subtitle vs canonical SRT implementation QA;
   - full-watch picture + subtitle review.
5. Do not revisit audio timing or visual generation unless new evidence requires it.
