# Seedance 2.5 Lean Prompt Benchmark — Run Protocol v0.1

> Status: EXPERIMENTAL
> Matrix: `benchmark_matrix.yaml`

## Goal

Measure whether the Lean Prompt Compiler produces **more usable MV material per generation/repair cost** than the legacy full prompt-control skeleton.

Do not judge the experiment by one visually impressive sample.

## Controlled variables

Within a comparison cell keep constant:
- accepted K0/reference asset;
- lyric/beat intent;
- primary visual event;
- target duration;
- provider/model and generation settings;
- aspect ratio / resolution class;
- character/world identity;
- evaluation rubric.

The intended variable is the prompt-control strategy.

## Variant A｜LEGACY_FULL_SKELETON

Use the current production logic in `rules/ai_video.md` as the legacy baseline.

Do not add new fixes during a cell. If the baseline prompt needs a new patch, create a new explicit variant rather than silently changing it.

Any identity/provenance statement must still be factually true. A legacy template does not authorize a false claim intended to bypass provider safety/portrait checks.

## Variant B｜LEAN_CORE_PLUS_TRIGGERED_MODULE

Input one `mv_production_card` and compile using:
`tools/mv_prompt_compiler/CONTRACT.md`.

Only load modules triggered by current task evidence.
Target emitted Hard Constraints: 0–3.

## Evaluation

For every output create one `mv_material_record`.

Primary evidence:
- accepted material yes/no;
- usable seconds and usable ratio;
- repair count;
- regeneration count.

Secondary evidence:
- visual hit;
- identity stability;
- motion execution;
- editability;
- prompt size / constraint count / modules loaded;
- human interruption count.

## Repair discipline

If 0–N seconds are usable and only a later window fails:
- preserve the usable window;
- record the actual failure interval;
- repair/regenerate only the smallest necessary region/source when the provider workflow permits.

Do not convert a local failure into an automatic whole-set regeneration.

## No mid-cell rule mutation

During one comparison cell:
- do not add a new negative after seeing Variant A fail and then omit that chance from Variant B;
- do not change camera path, subject task, K0, duration, or provider settings;
- do not discard failed output records.

If a new hypothesis appears, finish/close the current cell and create a new variant/cell.

## Decision rule

Lean is eligible to advance only when repeated cells show it is non-inferior on usable material quality and equal/better on repair or complexity cost.

Legacy remains valid when it clearly wins difficult archetypes. The target is not ideological prompt minimalism; the target is the smallest control surface that reliably produces editable material.
