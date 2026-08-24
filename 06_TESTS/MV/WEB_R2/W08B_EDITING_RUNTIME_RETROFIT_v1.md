# WEB R2｜Editing Runtime Retrofit v1

> Date: 2026-08-24
> Status: `PROCESS_PROMOTION / USER_FEEDBACK_INTEGRATED`
> Purpose: preserve the editing/timing/source-production lessons from V1 → V3.1 so a new Chat/Agent does not repeat the same failures.

## 1. User-validated direction

V3 corrected the timing/order problem but still felt too fragmented.
V3.1 reduced external fragments from 17 to 9 and was judged materially better.

Current user feedback to promote:
- WEB editing should temporarily use **whole-source enlargement / uniform crop** to guarantee both top-left and bottom-right generator marks are outside the visible frame;
- do not rely on partial/local hiding that can leak on some clips;
- Codex can later use the better publish-grade path; this WEB rule is a temporary environment-specific fallback;
- subtitle visual style should be optimized only after timing and picture rhythm are stable;
- the complete editing logic must become reusable so the user does not need to repeatedly correct fragmentation, watermark handling, or timing workflow placement.

## 2. Root cause hierarchy

### Timing failures V1/V2
Root cause: exact audio/lyric timing was not a durable hard Gate before downstream production.

Promotion:
`BGM_LOCKED -> AUDIO_TIMELINE_PACKAGE_LOCKED -> Natural Beat/Director -> generation -> edit -> subtitle`.

### V3 fragmentation
Root cause: semantic Anchor hits were overtranslated into external picture cuts; many source clips already contained internal multi-shot structure.

Promotion:
- Anchor Word != Cut Point;
- long-cut first for lyrical/emotional MV;
- preserve complete internal action arcs;
- Fragmentation Gate before Edit Map lock.

### WEB watermark leakage
Root cause: crop/hiding was not globally derived from worst-case watermark position across all sources.

Promotion:
- WEB preview uses one consistent whole-source zoom/crop transform;
- validate top-left and bottom-right risk frames across the batch before handoff;
- no mixed watermark state.

## 3. Best source-generation interface for the current editor

Do **not** solve the long-cut request by generating denser multi-shot clips everywhere.

Preferred portfolio for ~5s Seedance sources:
- 1-shot one-take: HOLD / spatial progression / emotion / RELEASE;
- 2-shot: common semantic source, setup-event or detail-emotion;
- 3-shot: discovery / setup-event-aftermath / selected PEAK;
- >3-shot: exceptional hook/peak only.

Default preference: `1–2 shots`.

Why:
If final picture edit uses ~8–12 external source segments and every source already contains 3–5 internal cuts, the real viewed shot count becomes dense again even though the Edit Map looks simple.

What the editor needs is not “more cuts”, but **more editorial headroom**:
- clear action arc;
- clean in/out;
- stable endpoint;
- meaningful internal cut only when narrative function changes;
- risk windows already mapped by W07.

## 4. Audio Timeline correct position

Final decision:

`Song/version choice`
→ `actual excerpt selection + human BGM lock`
→ **`AUDIO_TIMELINE_PACKAGE`**
→ `Natural Beat / semantic map`
→ `Director allocation`
→ `First frames / dynamic prompt design`
→ `generation`
→ `VISUAL_SOURCE_MAP`
→ `Picture Edit`
→ `subtitle style/implementation`
→ `final QA`.

Why not earlier:
Before excerpt lock, clip start/end/version can change, wasting alignment work.

Why not later:
Any time-dependent visual production based on guessed lyric positions can require visual reordering, not merely subtitle repair.

Therefore Stage 2A remains the correct and mandatory first post-BGM hard node.

## 5. Reusable editing architecture

Authority split after retrofit:
- `04_HARNESS/workflows/mv.md` v1.4: stage sequence + Gates;
- `04_HARNESS/rules/mv_golden_runtime.md` v1.3: cross-round stable lessons;
- `04_HARNESS/rules/mv_audio_timeline.md`: timing truth;
- `04_HARNESS/rules/mv_editing.md` v1.0: edit/source/subtitle implementation details;
- `04_HARNESS/rules/ai_video.md` v1.3: edit-driven dynamic source generation.

This separation is intentional: future editing improvements should usually change `mv_editing.md`, not turn the main workflow into a monolithic SOP.

## 6. Next R2 step

Keep W02A locked.
Keep V3.1 long-cut direction as the preferred picture candidate.
Before subtitle style optimization:
1. incorporate WEB whole-source watermark-safe enlargement/crop as the default preview transform;
2. perform one batch corner-risk validation;
3. lock picture direction if no new rhythm issue appears;
4. enter subtitle style optimization using the existing canonical lyric timing unchanged.
