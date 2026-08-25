# Knowledge｜MV Camera Language Candidates v2

> Status: `POSITIVE EVIDENCE / ACTIVE DIRECTOR CANDIDATE LIBRARY`
> Evidence base:
> - WEB R3 `如果风会替我说话` camera calibration + final accepted edit;
> - Face R&D 02 `Healing Tension + Moving Camera`, 2026-08-25, S01/S02/S03 all positive.
> Rule: R&D success allows selective production use, but a grammar is not universal Golden Runtime until it also reproduces in a real cross-song MV context.

---

## 1. Why this library exists

Avoid vague prompt language such as `电影级运镜` without a defined camera task.

Each camera design should specify:
- lyric/emotional job;
- subject movement task;
- camera–subject relationship;
- camera start position;
- one primary physical camera path;
- relative speed / distance change;
- movement amplitude;
- environment complexity;
- subject action budget;
- fragile anchors;
- clean endpoint / extension handoff;
- actual model execution result.

The library records **what the model actually executed**, not only what the prompt requested.

---

## 2. Current evidence table

| Grammar | Evidence source | Current evidence | Main use | Risk / note |
|---|---|---|---|---|
| Mild Slow Dolly-out Reveal | WEB R3 S03 | POSITIVE | absence, memory, negative space | amplitude tends to be milder than requested |
| Foreground Partial Occlusion / Reveal | WEB R3 S04 | POSITIVE | architecture, reveal, transition setup | near-full cover can reconstruct scene |
| Near-full Occlusion Hidden Cut | WEB R3 S04 edit | POSITIVE EDITORIAL | motivated transition | use as cut point, not same-scene continuity proof |
| Rack Focus Object -> Face | WEB R3 S06 | POSITIVE | metaphor -> emotion | works best after physical event stabilizes |
| Rack Focus Object Pair -> Face | WEB R3 S07 | POSITIVE | object metaphor -> observer | requested slider path may collapse into generic reframe |
| World-opening Crane / Retreat | WEB R3 S08 | STRONG POSITIVE / BENCHMARK | release, healing, final expansion | strong camera-emotion integration |
| Portrait Dolly-in | WEB R3 S01 | AESTHETIC POSITIVE / CONTROL UNCERTAIN | hook/intimacy | can amplify into beauty push |
| Backward Leading Tracking | Face R&D 02 S01 | STRONG POSITIVE R&D | approach, intimacy, invitation, forward momentum | define relative speed; do not let subject collide with lens |
| Diagonal Yield / Retreat + Foreground Fabric | Face R&D 02 S02 | STRONG POSITIVE R&D | passage, reveal, near-distance, foreground depth | hand/fabric are fragile anchors; K0 phase must be continued |
| Follow -> Overtake -> Lead Tracking | Face R&D 02 S03 | STRONG POSITIVE R&D | recognition, discovery, kinetic relationship, walking reveal | translational path, NOT orbit; simplify subject action |
| Glass-parallel Slider | WEB R3 S02 | NOT PROVEN | reflection / parallax | liquid event consumed control budget |
| Mini Orbit / Arc | WEB R3 S05 | NOT PROVEN | truth/dream geometry | model produced weaker motion than requested |
| Diagonal Slider | WEB R3 S07 | NOT PROVEN | object parallax | often simplified to push/reframe |

---

## 3. Camera–Subject Relationship Grammar

The director should decide the viewer's position before choosing the named move.

### HOLD / OBSERVE
Camera stays stable while subject performance carries the beat.

Use for:
- delicate facial performance;
- precise object action;
- identity-sensitive close work;
- emotional hold.

### FOLLOW
Camera travels with the subject from rear / rear-three-quarter / side-rear.

Use for:
- departure;
- travel;
- pursuit;
- entering a world.

### LEAD
Camera stays in front of a moving subject and travels with them.

Face R&D 02 S01 positive pattern:
- subject walks forward;
- camera moves backward on the same axis;
- if emotional distance should close, subject speed is slightly greater than camera retreat speed;
- keep final safety distance instead of letting subject collide with lens.

### YIELD
Subject keeps moving through space; camera retreats and/or moves slightly sideways to give the subject a path.

Face R&D 02 S02 positive pattern:
- K0 hand already near foreground;
- subject continues forward;
- camera performs short diagonal retreat;
- foreground fabric opens and returns as secondary physical response.

### OVERTAKE
Camera begins behind or beside a moving subject, travels faster along a real translational path, catches up, then slightly leads.

Face R&D 02 S03 positive pattern:
`FOLLOW -> OVERTAKE -> LEAD`

Important:
- camera moves forward through world space;
- relative view changes from rear 3/4 -> side -> front 3/4;
- this is **not** an in-place orbit around the character;
- keep subject walk direction stable;
- use only a small head/gaze change while camera carries most of the complexity.

### DISCOVER / REVEAL
Camera reveals subject or information through foreground, architecture, focus or spatial movement.

Use for:
- lyric discovery;
- relationship reveal;
- metaphor -> person;
- transition setup.

---

## 4. Benchmark grammar: World-opening Release

Current best reference: WEB R3 S08.

Director logic:
- character begins as meaningful subject;
- camera retreats and/or rises slightly;
- frame gives increasing share to sky / horizon / environment;
- character becomes smaller without losing identity;
- environment movement remains simple and physically coherent;
- final state leaves breathing room.

Use cases:
- acceptance;
- healing;
- release;
- final lyric;
- world-is-larger-than-the-problem emotion.

Do not hard-code S08's exact scenery or character styling.

---

## 5. Moving-character positive family from Face R&D 02

### A. Backward Leading Tracking
Validated variables:
- moving subject;
- moving camera;
- moderate face visibility;
- simple prop motion;
- bright exterior/interior continuity.

Director value:
- turns camera into an active relational position rather than a passive observer;
- creates controlled approach without a synthetic push-in.

### B. Diagonal Yield Through Foreground
Validated variables:
- near-camera hand;
- shallow depth cue;
- moving subject;
- deforming fabric foreground;
- short camera retreat.

Director value:
- creates depth and reveal from physical blocking rather than extra cuts;
- allows one scene to contain `occlusion -> passage -> residue`.

### C. Moving-subject Overtake Tracking
Validated variables:
- sustained walking;
- camera speed change;
- rear-to-side-to-front relative angle change;
- head / face-angle change;
- stable bright exterior topology.

Director value:
- supports recognition / being-discovered / pursuit / change-of-POV beats;
- provides dynamic material without converting a 5s source into a multi-cut montage.

Current status for all three:
`PRODUCTION-READY EXPERIMENTAL`

Next requirement:
Use selectively in a real song-driven MV and verify `LYRIC_FIT + IDENTITY_STABILITY + EDITABILITY` before Golden promotion.

---

## 6. K0 phase rule for camera design

Actual accepted first-frame pixels define the camera/subject phase at 0.0s.

If K0 already contains:
- walking subject;
- near-camera hand;
- raised fabric;
- partial lookback;
- existing camera-side relationship;

then continue from that exact phase.

Never reset just to recreate a director plan.

Examples:
- hand already near lens -> continue sideways / upward, do not retract then re-reach;
- subject already walking -> continue gait, do not freeze then restart;
- head already turned -> continue or resolve that angle, do not reset to back-facing.

---

## 7. Camera-control budget

Operational rule:

`1 primary camera move/relationship + 1 primary subject action + 1 secondary physical motion`

If the camera path itself is complex:
- simplify physics;
- simplify hands unless the hand is the one intended fragile anchor;
- keep body travel direction stable;
- limit head rotation / facial performance;
- avoid mirror + fluid + hand + face stack;
- preserve geometry anchors.

If a near-camera hand is intentional:
- pre-load it in K0;
- preserve five fingers / wrist topology;
- allow natural shallow DOF rather than demanding sharp foreground hand + sharp face simultaneously.

---

## 8. Moving subject stability checks

For walking / travel shots add:
- `GAIT_STABILITY` — alternating feet, real footfall, no sliding;
- `WEIGHT_TRANSFER` — body mass shifts naturally;
- `LIMB_COORDINATION` — arm swing and shoulder/hip rhythm remain plausible;
- `SCREEN_DIRECTION` — subject does not reverse direction without story reason;
- `FACE_ROTATION_STABILITY` — one identity across changing view angles;
- `CAMERA_RELATIVE_PATH` — requested follow/lead/yield/overtake relation actually occurs.

---

## 9. Controlled test families still open

### Dolly
Test separately:
- micro / mild / medium;
- close portrait vs medium-space scene.

### Lateral Slider
Test:
- clean static room;
- foreground parallax object;
- no rain/glass during base test.

### Foreground Occlusion
Test cover ratios:
- 20–30%: same-scene continuity;
- 40–60%: stronger reveal / transition setup;
- 80–100%: hidden cut only unless same-scene continuity is explicitly revalidated.

### Arc / Orbit
Still separate from Overtake.
Test:
- small arc on mostly static subject;
- no mirror+fluid stack in initial calibration.

### Crane / Retreat
Test:
- low rise + retreat;
- retreat only;
- mild rise only;
- open exterior and large interior.

### Rack Focus
Test:
- object -> face;
- face -> empty space;
- foreground metaphor -> landscape;
- execute after primary material event, not concurrently.

---

## 10. Scoring protocol

Each future camera test should score:
- `CAMERA_EXECUTION`
- `CAMERA_RELATIONSHIP_ACCURACY`
- `AMPLITUDE_ACCURACY`
- `IDENTITY_STABILITY`
- `FACE_ROTATION_STABILITY` when applicable
- `GAIT_STABILITY` when applicable
- `TOPOLOGY_STABILITY`
- `PHYSICAL_PLAUSIBILITY`
- `LYRIC_FIT`
- `EDITABILITY`
- `CLEAN_ENDPOINT / EXTENSION_ANCHOR`

A beautiful output does not prove camera-control success if the model substituted another movement.

---

## 11. Promotion rule

Promote a camera grammar to universal active runtime only when:
- it succeeds on at least two different song/scene contexts;
- requested and executed movement are materially the same;
- identity/topology remain acceptable;
- it creates measurable edit/director value;
- failure conditions are understood.

R&D-proven grammars may be used selectively as `PRODUCTION-READY EXPERIMENTAL` in the next real MV, with explicit QA and rollback.
