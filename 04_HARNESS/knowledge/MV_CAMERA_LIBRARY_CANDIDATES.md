# Knowledge｜MV Camera Language Candidates v1

> Status: `POSITIVE_EVIDENCE / EXPERIMENTAL CAMERA LIBRARY`
> Evidence base: WEB R3 `如果风会替我说话` camera calibration + final accepted edit.
> Rule: camera grammar is not promoted to Golden Runtime from a single-song success. Reproduce on at least one additional song / scene family first.

---

## 1. Why this library exists

Avoid vague prompt language such as `电影级运镜` without a defined camera task.

Each camera test should specify:
- lyric/emotional job;
- one primary camera path;
- movement amplitude;
- environment complexity;
- subject action budget;
- clean endpoint;
- actual model execution result.

The library records **what the model actually executed**, not only what the prompt requested.

---

## 2. Current R3 evidence table

| Grammar | R3 source | Current evidence | Main use | Risk / note |
|---|---|---|---|---|
| Mild Slow Dolly-out Reveal | S03 | POSITIVE | absence, memory, negative space | amplitude tends to be milder than requested |
| Foreground Partial Occlusion / Reveal | S04 | POSITIVE | architecture, reveal, transition setup | near-full cover can reconstruct scene |
| Near-full Occlusion Hidden Cut | S04 edit | POSITIVE EDITORIAL | motivated transition | use as cut point, not same-scene continuity proof |
| Rack Focus Object -> Face | S06 | POSITIVE | metaphor -> emotion | works best after physical event stabilizes |
| Rack Focus Object Pair -> Face | S07 | POSITIVE | object metaphor -> observer | requested slider path may collapse into generic reframe |
| World-opening Crane / Retreat | S08 | STRONG POSITIVE / BENCHMARK | release, healing, final expansion | current best R3 camera-emotion integration |
| Portrait Dolly-in | S01 | AESTHETIC POSITIVE / CONTROL UNCERTAIN | hook/intimacy | tends to amplify into beauty push |
| Glass-parallel Slider | S02 | NOT PROVEN | reflection / parallax | liquid event consumed control budget |
| Mini Orbit / Arc | S05 | NOT PROVEN | truth/dream geometry | model produced weaker motion than requested |
| Diagonal Slider | S07 | NOT PROVEN | object parallax | often simplified to push/reframe |

---

## 3. Benchmark grammar: World-opening Release

Current best reference: R3 S08.

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

## 4. Controlled test families for next round

### Dolly
Test separately:
- micro / mild / medium;
- close portrait vs medium-space scene;
- no difficult liquid/reflection during first calibration.

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
Test:
- 3° / 6° / 10°;
- static subject / simple background;
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

## 5. Camera-control budget

Candidate operational rule:

`1 primary camera move + 1 primary subject action + 1 secondary physical motion`

If the camera path itself is the experiment:
- simplify physics;
- simplify hands;
- avoid transparent material transformation;
- preserve geometry anchors.

Camera ability should be calibrated on simple scenes before combining it with high-risk physics.

---

## 6. Scoring protocol

Each future camera test should score:
- `CAMERA_EXECUTION` — did the requested movement actually happen?
- `AMPLITUDE_ACCURACY` — was it micro/mild/medium as requested?
- `IDENTITY_STABILITY`
- `TOPOLOGY_STABILITY`
- `PHYSICAL_PLAUSIBILITY`
- `LYRIC_FIT`
- `EDITABILITY`
- `CLEAN_ENDPOINT`

A beautiful output does not prove camera-control success if the model substituted another movement.

---

## 7. Promotion rule

Promote a camera grammar to active runtime only when:
- it succeeds on at least two different song/scene contexts;
- requested and executed movement are materially the same;
- identity/topology remain acceptable;
- it creates measurable edit/director value;
- failure conditions are understood.

Until then this file is a candidate library, not a recipe book.
