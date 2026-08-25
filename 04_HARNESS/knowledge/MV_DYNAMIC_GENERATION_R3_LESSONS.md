# Knowledge｜MV Dynamic Generation R3 Lessons v1

> Status: `POSITIVE_EVIDENCE / JIT KNOWLEDGE / NOT HARD RULE`
> Evidence: WEB R3 `如果风会替我说话` multi-shot production loop, repeated S02/S04/S05/S06 failures + repairs, user-authored Doubao prompt rewrite validation, final accepted MV.
> Promotion boundary: use these as default hypotheses in the next MV calibration; do not claim universal model truth until cross-song replication.

---

## 1. Core production finding

Current Doubao / Seedance 2 mini production improves when the director does **less simultaneous control**, not more.

Most useful summary:

`CONTAIN -> DE-EMPHASIZE -> SERIALIZE`

- contain the scene and material field;
- de-emphasize high-risk physics;
- execute hard events sequentially rather than concurrently.

The successful objective is not perfect simulation. It is a believable, editable source clip whose weak regions can be trimmed without harming the lyric.

---

## 2. Weakest Sufficient Motion

Use the weakest motion that makes the lyric readable.

If a wet window, soft rain texture and reflection already communicate rain, do not require:
- droplet birth;
- merging;
- macro rivulet growth;
- large refraction events.

If wet ice + rack focus already communicates melting/release, do not require a perfectly simulated drop to carry the lyric.

Candidate principle:
`PHYSICALLY BELIEVABLE > VISUALLY LOUD`.

---

## 3. First-frame State Preload

High-risk objects should already exist clearly at frame 0.

Especially:
- transparent objects;
- water / droplets;
- ice;
- mirror / reflection geometry;
- deforming fabric;
- foreground occluders that matter to camera grammar.

Do not ask I2V to invent a difficult object mid-shot and then immediately transform it.

Frame 0 should define:
- object identity;
- position;
- material state;
- surface ownership;
- action-ready state.

---

## 4. Static Base -> One Allowed Event

Before motion, explicitly define what stays still.

Pattern:

`STATIC BASE`
- freeze non-target material / geometry / people.

`ONE ALLOWED EVENT`
- permit exactly one small primary change.

This performed better than merely listing many prohibitions after a cinematic description.

For high-risk liquid scenes:
`ALL NON-TARGET LIQUID = STATIC / NEAR-STATIC`
`TARGET = ONE SHORT LOCAL TRACK`

---

## 5. Control Budget

Do not maximize camera, character and physics complexity in the same 5s source.

If physics complexity is HIGH:
- camera LOW;
- character action LOW;
- one object/material event only.

If camera complexity is HIGH:
- physics SIMPLE;
- no phase-change event;
- avoid mirror + fluid + hand + face stack.

If character topology is HIGH:
- camera preferably fixed / simple;
- no new transparent-object manipulation unless indispensable.

---

## 6. Surface Ownership

Before writing camera motion, define the spatial owner of rain / condensation / reflection / glass / mirror.

Example contract:
- camera is inside;
- subject is inside;
- exterior glass is one vertical boundary;
- rain belongs only to exterior glass surface;
- interior surface stays dry;
- reflection belongs to the optical glass plane;
- no suspended liquid between camera and subject.

Positive spatial statements are more useful than only writing `不要...` at the end.

---

## 7. Weak verbs for high-risk materials

Avoid making risky materials the semantic hero through strong verbs.

Higher-risk wording:
- flow / stream;
- merge;
- swell;
- visibly melt;
- pour;
- explode / splash.

Safer candidate wording:
- micro displacement;
- slight local change;
- nearly static;
- one short downward movement;
- local contact mark;
- subtle settling.

Quantified bounds are preferred over vague material language.

---

## 8. Serialize physics and camera/focus

Avoid:
`fluid change + rack focus + camera move + facial performance simultaneously`.

Prefer:
`PHASE A material event`
→ event ends / stabilizes
→ `PHASE B camera or rack focus`
→ `PHASE C small character residue`.

R3 S02/S06 user-rewritten prompts improved usability mainly through this separation, although exact fluid physics remained imperfect.

---

## 9. Rain strategy candidate

Current Seedance text-only default hypothesis:

### P1 production default
Rain as atmosphere:
- fine mostly-static exterior glass marks;
- wet-glass sheen;
- distant rain curtain;
- bokeh/reflection;
- wet ground;
- subtle wind response.

### P2 use only when narratively important
One pre-existing small surface-bound track.

### P3 R&D only by default
- droplet creation;
- droplet merging;
- macro fluid transformation;
- hero liquid physics.

Do not promote this hierarchy to universal model law until another song/scene family reproduces it.

---

## 10. Occlusion strategy candidate

R3 evidence:
- partial foreground occlusion can support same-scene continuity and parallax;
- near-full / full occlusion gives the model an opportunity to reconstruct topology.

Production hypothesis:
- partial cover = continuity grammar;
- near-full cover = motivated hidden cut / transition point.

Do not demand identical scene reconstruction after full-frame cover unless independently validated.

---

## 11. Trim before regenerate

This is consistent with the existing R2 `TRIM_REQUIRED` philosophy and was reinforced by R3.

If a 5s source has a coherent clean 2–4s arc:
- trim the weak edge;
- use rack focus / occlusion / fabric / blur as motivated edit windows when appropriate;
- regenerate only when clean duration or semantic event is insufficient.

`RAW SOURCE != FINAL SHOT`.

---

## 12. Prompt-control hierarchy candidate

For current Doubao / Seedance difficult scenes, test this order:

1. `HARD FREEZE / NON-NEGOTIABLES`
2. `FRAME-0 STATE`
3. `STATIC BASE`
4. `ONE ALLOWED EVENT`
5. `BOUND / quantified local change`
6. `PHASE A material/event`
7. `PHASE B camera/focus`
8. `CHARACTER RESIDUE`
9. `SOUND POLICY`
10. short `AVOID` list

Important: R3 supports this as an empirical workflow heuristic, not proof that the model literally reads tokens with a strict top-to-bottom numerical weighting.

---

## 13. Next-song validation checklist

For the next full MV, deliberately reuse at least 3 of these hypotheses on different scene families and record:
- source success rate;
- first-generation usability;
- number of regeneration loops;
- physical plausibility;
- clean usable duration;
- final edit salvage rate.

If cross-song evidence repeats, promote only the stable items into `rules/ai_video.md`; keep style-specific preferences in Knowledge.
