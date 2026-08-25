# Knowledge｜MV Dynamic Generation R3 Lessons v2

> Status: `POSITIVE EVIDENCE / JIT KNOWLEDGE / PARTIALLY CROSS-VALIDATED`
> Evidence:
> - WEB R3 `如果风会替我说话` multi-shot production loop;
> - D01-B `我救自己于人间水火` cross-song dynamic control replication;
> - Face R&D 02 `Healing Tension + Moving Camera`, 2026-08-25, S01/S02/S03 all positive.
> Promotion boundary: the main control skeleton is already HARD in `rules/ai_video.md`; face-degrade and the new moving-character camera families remain `PRODUCTION-READY EXPERIMENTAL` until a real song-driven MV reproduces them.

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

Operational principle:
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
- foreground occluders that matter to camera grammar;
- near-camera hands;
- walking / turning body phase when movement is the main test.

Do not ask I2V to invent a difficult object mid-shot and then immediately transform it.

Frame 0 should define:
- object identity;
- position;
- material state;
- surface ownership;
- action-ready state;
- current body / hand / gaze phase.

---

## 4. K0 Action Phase Continuation

Face R&D 02 reinforced a stronger version of First-frame State Preload:

**K0 is not merely an object inventory. It is the actual motion phase at 0.0s.**

If the accepted first frame already shows an action in progress, continue it instead of restarting it.

Positive examples:
- S01: character already walking -> continue gait immediately;
- S02: hand already near foreground -> move from that near position to clear the fabric; do not retract and re-reach;
- S03: character already walking + partially looking back -> continue / resolve that head angle; do not reset to a fully back-facing pose.

Candidate operational rule:
`K0 PHASE CONTINUITY > OLD DIRECTOR ACTION ORDER`.

This is consistent with the existing HARD authority rule that accepted K0 pixels outrank older Director prose.

---

## 5. Static Base -> One Allowed Event

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

For moving-character scenes:
- continuous walking may be the single primary subject event;
- towel lowering / slight gaze / one head turn is secondary, bounded performance;
- do not add a second story action just because the body is already moving.

---

## 6. Control Budget

Do not maximize camera, character and physics complexity in the same 5s source.

If physics complexity is HIGH:
- camera LOW;
- character action LOW;
- one object/material event only.

If camera complexity is HIGH:
- physics SIMPLE;
- body travel direction STABLE;
- face/head performance SMALL;
- no phase-change event;
- avoid mirror + fluid + hand + face stack.

If character topology is HIGH:
- camera preferably fixed / simple unless camera is the explicit experiment;
- no new transparent-object manipulation unless indispensable.

Face R&D 02 S03 validated a useful allocation:
- subject locomotion = medium;
- camera overtake = medium-high;
- head/gaze action = small;
- environment = small.

That combination was more stable than making both body performance and camera path equally complex.

---

## 7. Moving Subject × Moving Camera｜positive R&D evidence

Face R&D 02 provides three positive camera–subject patterns:

### S01 — LEAD
`subject walks forward + camera retreats in front`

Useful detail:
- relative speed can intentionally shrink distance;
- do not use a separate synthetic push-in when the subject's own motion can create approach.

### S02 — YIELD
`subject keeps moving + camera retreats diagonally to give path`

Useful detail:
- near foreground hand was preloaded in K0;
- fabric opening / return served as secondary physical feedback;
- camera movement stayed short and functional.

### S03 — FOLLOW -> OVERTAKE -> LEAD
`camera follows from rear 3/4, travels forward along the subject, catches up and slightly leads`

Useful detail:
- subject kept one walking direction;
- camera carried most of the directional complexity;
- head rotation remained small;
- relative view changed without requiring a stationary orbit.

Status:
`PRODUCTION-READY EXPERIMENTAL`.

These are eligible for the next real MV when lyric fit is strong; they are not mandatory camera recipes for every beat.

---

## 8. Gait and body-motion stability

When a subject walks or travels, add explicit checks only when needed:
- alternating leg cycle;
- real foot contact;
- natural weight transfer;
- plausible shoulder / hip coordination;
- small opposite arm swing;
- stable screen direction;
- no sliding / hovering / backward drift.

Do not over-specify anatomical micro-mechanics in every prompt. Use this as a QA / prompt patch layer when locomotion is important.

---

## 9. Near-camera hand safety

Face R&D 02 S02 provides positive evidence that a near-camera hand can remain usable when:
- the hand already exists in K0;
- the movement is one short continuation, not a new reach from off-screen;
- hand path is bounded;
- shallow depth of field is allowed;
- camera does not simultaneously perform a large orbit / push.

Recommended fragile anchors:
- five fingers;
- normal palm/wrist connection;
- no fusion with fabric / glass;
- hand may be naturally soft in focus when extremely close.

Do not demand both near hand and face to be tack-sharp if depth of field would make that physically implausible.

---

## 10. Surface Ownership

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

## 11. Weak verbs for high-risk materials

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

## 12. Serialize physics and camera/focus

Avoid:
`fluid change + rack focus + camera move + facial performance simultaneously`.

Prefer:
`PHASE A material event`
→ event ends / stabilizes
→ `PHASE B camera or rack focus`
→ `PHASE C small character residue`.

For moving-character camera shots, a parallel version is:
`BODY TRAVEL remains continuous`
→ camera relationship changes
→ only one small gaze/head response
→ physical residue continues.

---

## 13. Face Degrade -> Face Completion｜PRODUCTION-READY EXPERIMENTAL

Face R&D 01 and Face R&D 02 provide positive evidence for an unveiled fictional-character route:
- first-frame face carries low-frequency identity structure rather than high-resolution facial detail;
- video model completes a clear fictional adult face;
- perceived identity remained usable through close view, walking, near foreground interaction and camera-relative angle change.

This path is **not** a universal replacement for veil/mask production.

Use when:
- exposed facial performance materially benefits the lyric / character design;
- reference is a fictional character asset;
- the team accepts small facial micro-drift if continuous viewing still reads as one identity.

Keep veil / mask path for scenes where maximum stability or aesthetic design benefits from it.

QA:
- `FACE_COMPLETION`
- `IDENTITY_STABILITY`
- `FACE_ROTATION_STABILITY`
- `AGE_STABILITY`
- `HAIR / SILHOUETTE IDENTITY`

Next requirement:
reproduce in a real song-driven MV before wider promotion.

---

## 14. Safety wording rewrite must preserve the production skeleton

Face R&D 02 exposed an important workflow issue:
platform-sensitive wording may need rewriting, but **safety wording cleanup must not collapse the control structure**.

Keep the full production skeleton:
`HARD FREEZE -> FRAME-0 -> STATIC BASE -> ONE EVENT -> BOUND -> MOTION LOAD -> PHASES -> CAMERA -> FEEDBACK -> RESIDUE -> END STATE -> SOUND -> AVOID`.

Rewrite abstract or high-risk intent words into physical direction:
- abstract attraction -> distance / gaze / path / blocking;
- “almost touch” -> hand occupies near foreground, camera yields space;
- “dynamic cinematic” -> exact camera start/path/speed/endpoint.

Operational lesson:
`SAFE WORDING != SIMPLIFIED CONTROL`.

---

## 15. Bright / healing world as a useful aesthetic lane

The first dark rain-night face tests were technically useful but visually heavy.
Face R&D 02 showed that bright, low-contrast, airy environments can preserve character attraction while creating a more comfortable / healing viewing tone.

Reusable aesthetic ingredients (not hard template):
- luminous soft daylight;
- low-to-moderate contrast;
- readable skin / face shadows rather than crushed blacks;
- fabric / hair / breeze as soft physical motion;
- open exterior depth / plants / water / sky where lyric fit supports it.

Do **not** hard-code white shirt, seaside, male lead or morning light into future projects. The reusable principle is:
`COMFORTABLE WORLD + CONTROLLED HUMAN PROXIMITY / MOTION` when the lyric calls for it.

---

## 16. Rain strategy candidate

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

---

## 17. Occlusion strategy candidate

R3 + Face R&D evidence:
- partial foreground occlusion can support same-scene continuity and parallax;
- soft fabric can work when its initial state is preloaded and its motion is bounded;
- near-full / full occlusion gives the model an opportunity to reconstruct topology.

Production hypothesis:
- partial cover = continuity / discovery grammar;
- bounded fabric reveal = positive when geometry is simple;
- near-full cover = motivated hidden cut / transition point.

Do not demand identical scene reconstruction after full-frame cover unless independently validated.

---

## 18. Trim before regenerate

If a 5s source has a coherent clean 2–4s arc:
- trim the weak edge;
- use rack focus / occlusion / fabric / blur as motivated edit windows when appropriate;
- regenerate only when clean duration or semantic event is insufficient.

`RAW SOURCE != FINAL SHOT`.

---

## 19. Prompt-control hierarchy

Current production hierarchy:

1. `HARD FREEZE / NON-NEGOTIABLES`
2. `FRAME-0 STATE / K0 PHASE`
3. `STATIC BASE`
4. `ONE ALLOWED EVENT`
5. `BOUND`
6. `MOTION LOAD`
7. `PHASES`
8. `CAMERA–SUBJECT RELATIONSHIP + CAMERA CONTRACT`
9. `PHYSICAL FEEDBACK`
10. `RESIDUE`
11. `END STATE / EDIT HANDOFF`
12. `SOUND POLICY`
13. short `AVOID` list

This is an empirical production workflow, not a claim that the model literally assigns strict token priorities.

---

## 20. Next real-MV validation checklist

For the next full MV, selectively reuse the new capabilities only when lyric fit supports them.

Record:
- moving-character source success rate;
- camera relationship execution accuracy;
- face completion / identity continuity if Face-Degrade path is used;
- gait stability;
- first-generation usability;
- regeneration loops;
- clean usable duration;
- final edit salvage rate;
- whether the movement improved the lyric rather than merely adding spectacle.

Primary creative order remains:
`LYRIC VISUAL HIT > LIGHT NARRATIVE CONTINUITY > CAMERA / MOTION SHOWCASE`.
