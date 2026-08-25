# WEB R3｜Doubao Prompt Rewrite Validation v1

Status: `VALIDATED IN CURRENT R3 / EXPERIMENTAL REUSABLE GUIDANCE`
Song: `如果风会替我说话`
Model family: Doubao / Seedance 2 mini image-to-video
Scope: user-rewritten S02 rain-window + S06 ice-drop prompts and resulting 5s clips

## 1. Executive finding
The user-authored prompt rewrite materially improves overall video usability, but it does **not** prove exact liquid-physics control.

Observed in actual outputs:
- S02: the overall rain-window shot is calmer and more usable, but the selected moving water trace can still become an over-thick vertical tube for part of the clip.
- S06: ice geometry is more stable and the later rack-focus-to-eyes transition reads well, but the liquid connection / droplet can still elongate unnaturally before focus leaves the foreground.

Therefore the success mechanism is best described as:
`CONTAIN + DE-EMPHASIZE + SERIALIZE`
not:
`PERFECT FLUID SIMULATION`.

The rewrite succeeds mainly because it reduces motion amplitude, freezes most of the scene, permits only one small event, separates fluid motion from rack focus in time, and prevents camera motion from competing for control budget.

## 2. Prompt-structure improvements worth keeping

### 2.1 Front-loaded constraint block
The prompt places a concise hard-constraint section before the descriptive timeline.

R3 interpretation:
- treat this as an **empirical Doubao/Seedance heuristic**, not a universal claim about all video models;
- front-load the few constraints whose violation would make the shot unusable;
- do not dump dozens of low-value prohibitions at the top.

Recommended top block categories:
1. no extra objects / droplets / people;
2. preserve primary geometry;
3. freeze non-target liquids/objects;
4. define the only allowed event.

### 2.2 STATIC BASELINE before motion
The strongest improvement is not the negative wording itself, but the explicit declaration that almost everything stays still.

Pattern:
`STATIC BASE -> ONE ALLOWED EVENT`

Examples:
- rain shot: all water marks except one remain nearly static;
- ice shot: ice, tray, background and all other water states stay stable; only one pre-existing bead may change.

This reduces the model's tendency to animate the entire material system.

### 2.3 Weak action verbs / low-amplitude motion
Avoid strong positive liquid verbs such as:
- flow;
- stream;
- merge;
- swell;
- melt visibly;
- pour.

Prefer:
- micro displacement;
- slight local change;
- nearly static;
- one short downward motion;
- tiny local contact mark.

New candidate rule:
`WEAK VERB FOR HIGH-RISK MATERIALS`.

### 2.4 Quantified containment
Concrete bounds outperform vague emotional material descriptions.

Useful forms:
- total movement only 20–30% of frame height;
- only one existing bead may change;
- one local contact mark;
- no spread beyond the contact point;
- only a narrow optical distortion band.

Avoid vague phrases such as:
- "more wet";
- "melts gradually";
- "rain flows naturally";
- "water becomes heavier" without a hard limit.

### 2.5 SERIAL PHASES instead of concurrent tasks
This is one of the strongest reusable lessons.

Bad stack:
`fluid motion + rack focus + camera movement + facial action at the same time`

Better:
`PHYSICS PHASE -> END PHYSICS -> FOCUS PHASE -> SMALL CHARACTER RESIDUE`

S02/S06 rewrite explicitly delays rack focus until the liquid event is finished or nearly finished.

R3 candidate rule:
`DO NOT RUN HIGH-RISK MATERIAL CHANGE AND FOCUS/CAMERA CHANGE CONCURRENTLY`.

### 2.6 One active liquid; freeze the rest
For high-risk fluid scenes, do not merely say "only one droplet matters".
Explicitly freeze the rest of the material field.

Pattern:
`ALL NON-TARGET LIQUID = STATIC / NEAR-STATIC`
`TARGET LIQUID = ONE SHORT TRACK ONLY`

This is stronger and more operational than only adding a final avoid-list.

## 3. What still fails despite the improved prompts

### S02 rain
Even with the improved constraints, the moving rain trace can still become visually too thick and tube-like.

Interpretation:
- positive motion command still causes the model to allocate salience to the liquid path;
- exact thin-rivulet conservation is not reliable enough for production-critical hero physics;
- the prompt reduced the failure footprint but did not eliminate the underlying liquid-simulation weakness.

Production consequence:
For future emotional rain MV shots, default to:
`RAIN AS ATMOSPHERE`, not `RAIN AS HERO OBJECT`.

Preferred visual cues:
- many fine mostly-static exterior marks;
- wet-glass sheen;
- distant rain curtain;
- bokeh/reflection;
- wet ground;
- post-added rain ambience.

Only create a moving droplet/rivulet when the droplet itself is narratively indispensable.

### S06 ice/drop
The rewrite improves object stability and makes the foreground-to-eyes rack focus much more readable.
However, the liquid still risks stretching into an unnatural vertical connection before the focus transition.

Interpretation:
- ice + transparent water + gravity separation remains a difficult material event;
- the shot works primarily because the event is brief and later de-emphasized by rack focus;
- the emotional readability comes more from `wet ice -> focus to eyes` than from a perfect drop simulation.

Production consequence:
Do not require a visibly perfect droplet to carry the lyric if wet ice + focus change already communicates release.

## 4. Updated control hierarchy for difficult dynamic prompts

Recommended prompt order for current Doubao/Seedance production:

1. `HARD FREEZE / NON-NEGOTIABLE CONSTRAINTS`
2. `FRAME-0 STATE / EXISTING OBJECTS`
3. `STATIC BASELINE`
4. `ONE ALLOWED EVENT`
5. `QUANTIFIED TRACK / LOCAL CHANGE`
6. `TIME-SERIALIZED PHASES`
7. `CAMERA / FOCUS`
8. `CHARACTER RESIDUE`
9. `SOUND POLICY`
10. `SHORT AVOID LIST`

This differs from earlier verbose prompts by making the control hierarchy obvious before the cinematic prose.

## 5. New candidate template

```text
[HARD FREEZE]
Freeze geometry and all non-target material states.
No new objects / droplets / people.

[FRAME-0 STATE]
List only what visibly exists at frame 0.

[STATIC BASE]
Everything except TARGET remains static / near-static.

[ONE EVENT]
TARGET performs exactly one small event.

[BOUND]
Quantify direction, distance, scale and local area.

[PHASE A]
Execute the material event only.

[PHASE B]
Material event ends; then execute rack focus / camera action.

[RESIDUE]
One blink / gaze shift / cloth settling / light hold.

[AVOID]
Only the 5–8 highest-risk failure modes.
```

## 6. Relationship to earlier R3 rules

This validation strengthens:
- `WEAKEST SUFFICIENT MOTION`
- `FIRST-FRAME STATE PRELOAD`
- `ONE DIFFICULT PHYSICS EVENT PER SOURCE`
- `CONTROL BUDGET`
- `SURFACE OWNERSHIP`
- `PHYSICALLY BELIEVABLE > VISUALLY LOUD`

New experimental additions:
- `STATIC BASE -> ONE ALLOWED EVENT`
- `WEAK VERB FOR HIGH-RISK MATERIALS`
- `SERIALIZE PHYSICS AND FOCUS/CAMERA`
- `FREEZE NON-TARGET MATERIAL FIELD`
- `QUANTIFIED LOCAL CHANGE > VAGUE MATERIAL LANGUAGE`

## 7. Promotion policy
These are **current-project validated heuristics**, not universal model truths.

Do NOT state as a guaranteed architectural fact that:
- the model always reads strictly top-to-bottom;
- prohibitions always have lower weight than positive instructions;
- moving a rule earlier always increases its numerical weight.

What R3 does support empirically:
- the rewritten hierarchy produced more usable outputs;
- motion suppression and task serialization reduced the visible failure footprint;
- exact liquid behavior remained imperfect.

Promote to long-term runtime only after the same structure improves at least one additional song / scene family.

## 8. Current production recommendation
Use these two rewritten outputs as edit candidates rather than regenerate again solely for liquid perfection.

Editing should:
- keep the visually calm portions;
- avoid lingering on the thickest liquid-tube frames if they are noticeable at final speed;
- favor the later stable emotional/focus region;
- never force the final edit to prove a perfect droplet simulation.

`VALIDATION_RESULT = POSITIVE_WITH_LIMITS`
`EXACT_LIQUID_CONTROL = NOT_PROVEN`
`PROMPT_HIERARCHY_REUSABLE_CANDIDATE = YES`
