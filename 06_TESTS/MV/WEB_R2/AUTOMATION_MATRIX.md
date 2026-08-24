# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录自动化程度，不因“渲染出文件”就高估正确性。

## Overall

- Current Stage: `W08B PROCESS LOCK / PRE-W09 SUBTITLE OPTIMIZATION`
- Overall State: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS / V3_SUPERSEDED / V3_1_DIRECTION_IMPROVED / EDITING_RUNTIME_PROMOTED`
- Human aesthetic gates passed: `4 + V3.1 direction judged better, not final subtitle lock`
- External-required stages encountered: `1`
- Timing technical rescues: `2 major edit failures`
- Audio timeline hard gate: `PASS`
- Editing-runtime retrofit: `PROMOTED`

## Stage Board

| Stage | 内容 | 实际状态 | 备注 |
|---|---|---|---|
| W00 | 能力基线 | AUTO / PASS | |
| W01 | 选歌 | HUMAN_GATE / PASSED | 用户选歌 |
| W02 | BGM截取 | LOCKED | 37.120s + SHA |
| **W02A** | **AUDIO_TIMELINE_PACKAGE** | **PASS / LOCKED** | BGM 后第一硬 Gate；后续所有时间依赖服从它 |
| W03 | 语义/Natural Beat | PASS / TIMING REBOUND | 使用 canonical Package |
| W04 | 导演 | PASSED / FUTURE PROCESS UPDATED | 以后同时规划 edit role / source portfolio |
| W05 | 首帧 | PASSED | 9/9 |
| W06 | 动态提示词 | PASS / RULE PROMOTED | 默认1–2镜；3镜任务型；密集多镜只用于少数峰值 |
| W06-X | Seedance生成 | EXTERNAL_REQUIRED / COMPLETE | 2S1–2S9 |
| W07 | 动态QA | PASS WITH TRIM / FUTURE OUTPUT UPGRADED | 以后必须产出 executable VISUAL_SOURCE_MAP |
| W08A | Editor Audio Gate | PASS | Package + locked BGM revalidated |
| **W08B** | **Picture Edit** | **V3 superseded / V3.1 long-cut direction improved / process promoted** | 17段→9段；Fragmentation Gate进入规则 |
| **W09** | **Subtitle** | **NEXT / STYLE NOT LOCKED** | timing source已锁；下一轮只优化形式/实现 |
| W10 | Final QA | NOT_STARTED | |
| W11 | Close | NOT_STARTED | |

## Process promotions from V3/V3.1

### 1. Audio timeline placement
Fixed order:
`BGM_LOCKED -> AUDIO_TIMELINE_PACKAGE_LOCKED -> Natural Beat/Director -> generation -> edit -> subtitle`.

Reason:
- earlier than BGM lock risks wasted alignment if excerpt/version changes;
- later allows guessed timing to contaminate visual production.

### 2. Dynamic source portfolio
Do not default to dense multi-shot 5s sources.

Preferred:
- 1-shot: HOLD / space / emotion / RELEASE;
- 2-shot: normal semantic source;
- 3-shot: discovery / selected peak;
- >3-shot: exceptional hook/peak only.

Default: `1–2 shots`.

### 3. Long-cut editing
- Anchor Word != mandatory external cut;
- preserve source internal action arc;
- avoid consecutive <2s fragments;
- avoid short A-B-A recycling;
- final release gets breathing room;
- run Fragmentation Gate before Edit Map lock.

### 4. WEB watermark fallback
Current web environment:
- use consistent whole-source enlargement/crop;
- derive from worst batch watermark location;
- inspect top-left + bottom-right danger frames;
- preserve 9:16 / SAR1:1;
- no watermark leakage may be delegated to user QA.

Codex/publish-grade path remains preferred when available.

### 5. Subtitle sequence
`canonical timing -> diagnostic implementation check -> style optimization -> implementation re-check`.

Do not change subtitle timestamps to fit picture cuts.

## Reusable authority split

- `04_HARNESS/workflows/mv.md` v1.4 — stage/Gates
- `04_HARNESS/rules/mv_golden_runtime.md` v1.3 — cross-round stable lessons
- `04_HARNESS/rules/mv_audio_timeline.md` v1.0 — timing truth
- `04_HARNESS/rules/mv_editing.md` v1.0 — editing/source/watermark/subtitle implementation
- `04_HARNESS/rules/ai_video.md` v1.3 — edit-driven source generation
- `06_TESTS/MV/WEB_R2/W08B_EDITING_RUNTIME_RETROFIT_v1.md` — R2 evidence/retrofit note

## Current states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `V3_1_LONG_CUT_DIRECTION = PREFERRED / USER_SAYS_BETTER`
- `EDITING_RUNTIME_PROMOTED = YES`
- `DYNAMIC_SOURCE_PORTFOLIO_RULE_PROMOTED = YES`
- `WEB_WATERMARK_FALLBACK_PROMOTED = YES`
- `SUBTITLE_TIMING_SOURCE_LOCKED = YES`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next

Proceed to subtitle form/style optimization on the V3.1 long-cut direction.
Keep W02A timing unchanged.
Any new WEB preview must use the promoted uniform whole-source watermark-safe crop before user handoff.
