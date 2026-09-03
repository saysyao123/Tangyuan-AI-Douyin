# MV Prompt Compiler Contract v0.1

> Status: `EXPERIMENTAL / SEEDANCE 2.5 BENCHMARK ONLY`
> Input: one validated `mv_production_card`.
> Output: one provider-ready generation prompt + compile metadata.
> Non-goal: replace Canonical Runtime, Director judgment, provider policy, or material QA.

## 1. Core idea

The compiler describes **what success looks like** before describing failure cases.

Default compiled prompt has only six semantic blocks:

1. `INTENT / LYRIC HIT`
2. `K0 / START STATE`（I2V/Reference only）
3. `PERFORMANCE / PRIMARY VISUAL EVENT`
4. `CAMERA RELATIONSHIP / PATH`
5. `PHYSICAL FEEDBACK + CLEAN END STATE`
6. `HARD CONSTRAINTS`

Provider-specific formatting may merge these blocks into natural prose. The six blocks are a planning contract, not a requirement to print six headings to the model.

## 2. Constraint compiler

Every candidate negative/constraint must be classified before emission:

- `KEEP_HARD`: frequent/high-cost failure that makes the source unusable and is difficult to repair later;
- `REWRITE_POSITIVE`: express the desired state instead of a prohibition;
- `MOVE_TO_PARAMETER`: aspect ratio, duration, resolution, audio toggle or similar capability belongs in provider parameters when available;
- `MOVE_TO_VALIDATOR`: detectable after generation and cheap to reject/trim/repair;
- `DROP_HISTORY_PATCH`: old or out-of-scope patch with no current evidence.

Trial budget:
- target: `0–3` emitted Hard Constraints;
- `4–5`: emit `PROMPT_COMPLEXITY_WARNING` and record why each extra item is necessary;
- `>5`: benchmark compiler should reject the card as `PROMPT_COMPLEXITY_BLOCKED` until simplified.

This budget is experimental and must not be promoted to Production Rule before benchmark evidence.

## 3. Conditional modules

The compiler may add **one or more small modules only when current-card evidence triggers them**.

### FACE_HAND
Trigger when the primary event depends on hand-face interaction, large face rotation, near-camera hands, or identity-sensitive micro-performance.
Add only the minimum spatial/sequence guidance needed to preserve the interaction.

### PHYSICS
Trigger for liquid, cloth under strong force, fragile objects, glass/reflection, complex contact, or other high-risk physical causality.
Prefer one causal chain and reduce competing subject/camera motion.

### OCCLUSION
Trigger when a foreground object must reveal/conceal the subject or act as a transition.
Define which solid edge/plane performs the occlusion and the camera path relative to it.

### MULTISHOT
Trigger only when separate internal shots perform genuinely different director tasks.
Do not activate merely to make the source feel more cinematic.

### CAMERA_PRECISION
Trigger when camera execution itself is the experiment or lyric mechanism.
Define start position, subject direction, relative distance/speed change, physical path, and endpoint.

If no trigger exists, no module is loaded.

## 4. Duration router

Duration is selected from the Production Card, not from a separate workflow:

- `PRECISION_5_8`: one difficult action, identity-sensitive interaction, physics-sensitive event, or single strong visual hit;
- `STANDARD_8_15`: default for one complete lyric/visual beat with meaningful development;
- `EXTENDED_15_20`: only when the same beat needs real emotional/spatial progression that cannot be expressed cleanly in a shorter source.

Do not use extra duration merely because the provider allows it.
30-second source design is outside the current benchmark.

## 5. Reference/K0 authority

If a real accepted K0/Reference exists, compile from the actual accepted asset state.
Do not ask the model to reconstruct an older abandoned Director description.

The compiler may include only facts verified from the current asset/project metadata.

### Provider safety/identity declarations
Any declaration such as “this reference is AI-generated / fictional / not a real person” may be emitted **only when that statement is factually established by the project asset metadata**.

Never fabricate or force such a declaration to bypass a provider's safety, identity, copyright, or portrait checks. If provenance is unknown or the reference depicts a real person, omit the false declaration and follow the provider's actual policy/capabilities.

## 6. Motion-load rule

The compiler should prefer one dominant relationship rather than maximizing all motion axes.

Default planning heuristic:
- one primary subject event;
- one primary camera relationship/path;
- environmental/physical motion supports the event.

If a conditional module introduces high complexity in one axis, simplify the others before adding more constraints.

## 7. End-state rule

Every source should specify an editor-useful endpoint when the task permits it:
- action completes or clearly settles;
- no new major event begins at the tail;
- remaining cloth/hair/water/light/environment motion can continue as residue;
- endpoint can be held, trimmed, or transitioned cleanly.

## 8. Compile output metadata

Each compile should record at minimum:

```json
{
  "card_id": "...",
  "provider": "...",
  "model": "...",
  "duration_strategy": "...",
  "modules_loaded": [],
  "constraints": {
    "candidate": 0,
    "emitted": 0,
    "rewritten_positive": 0,
    "moved_to_parameter": 0,
    "moved_to_validator": 0,
    "dropped_history_patch": 0
  },
  "complexity_status": "OK | WARNING | BLOCKED",
  "compiler_version": "0.1"
}
```

This metadata exists for benchmark comparison; it is not a new Human Gate.

## 9. Benchmark requirement

Do not replace `rules/ai_video.md` with this compiler based on one successful generation.
Compare legacy-vs-lean outputs using usable material yield, repair count, failure type, and human interruption before promotion.
