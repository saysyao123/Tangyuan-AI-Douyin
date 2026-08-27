# D02-B｜Director A/B Evaluation v1

Status: `COMPLETE / CANDIDATE B SELECTED FOR DOWNSTREAM TEST`

Compared candidates:
- A: `AB/R3_BASELINE.md`
- B: `AB/OSS_OVERLAY.md`

Fair-test constants:
- same song / HG02 audio / seven-line Audio Timeline;
- same five Natural Beats;
- same male protagonist, world, wardrobe, palette and Face-Degrade -> Face-Completion constraints;
- same 9:16 output and Seedance-class ~5s source strategy;
- same four-source production count;
- same Human Gate criteria.

## Evaluation

Scores use 1–5 only as an internal comparison aid; written reasons are authoritative.

| Dimension | A R3 | B OSS | Decision / reason |
|---|---:|---:|---|
| Lyric visual hit | 4.3 | 4.6 | B preserves the same direct lyric hits but strengthens `忍住`, `算了`, and `放下` through camera behavior rather than only scene/action description. |
| Whole-MV coherence | 3.9 | 4.8 | Clear B advantage: one relational-distance thesis governs all four sources. A is coherent spatially but more episodic. |
| Director/camera motivation | 4.4 | 4.9 | A uses strong camera grammars; B additionally explains why each relationship starts/stops and how it changes the emotional relation. |
| Shot diversity without incoherence | 4.5 | 4.7 | Both are varied. B’s variation reads as a progression rather than a library selection. |
| First-frame performability | 4.6 | 4.6 | Tie. Both use simple K0 states and avoid overloaded props/actions. |
| Expected dynamic stability | 4.7 | 4.6 | Slight A advantage because B encodes more relational intent, but B keeps the same 1-shot/low-load source count and does not add complex action stacks. |
| Edit-source usability | 4.4 | 4.8 | B adds explicit WHY CUT HERE / do-not-cut rules and a motivated NB03 occlusion handoff. |
| Character/identity continuity | 4.7 | 4.7 | Tie; same single-character policy and similar face/action load. |
| Production burden | 4.8 | 4.5 | A is simpler to describe. B requires more Director reasoning, but does not increase generation count or model dependencies. |
| Runtime compatibility | 5.0 | 4.9 | B is a bounded Stage overlay only; no Runtime/audio/H3 container changes. |
| Zero-context reproducibility | 4.3 | 4.9 | B explicitly records Thesis, engine, audiovisual relation, camera motive, optional-element stop conditions and drift constraints. |

## Key test questions

### A. Does Director Thesis + Primary Visual Engine improve coherence?

`YES / STRONG PLAN-LEVEL SIGNAL`.

A progression:
`good approach shot -> good restraint shot -> good weather shot -> good release shot`.

B progression:
`camera meets him -> camera stops with him -> camera yields passage -> camera witnesses time passing -> camera stops pursuing`.

B provides a single authored law that can be checked at First Frame and Dynamic Prompt stages.

### B. Do explicit audiovisual relationships reduce “逐句插图感”?

`YES / PLAN-LEVEL SIGNAL`.

B explicitly keeps `想说 -> 算了`, `雨停 -> 风过`, and `舍不得 -> 放下` inside continuous semantic arcs and includes do-not-cut conditions. It does not assign one shot per lyric line.

### C. Does motive-first camera design improve direction without gimmicks?

`YES / PLAN-LEVEL SIGNAL`.

The same camera families available to R3 are used, but B specifies relational reason and stop condition. The improvement is therefore Director logic, not a new camera-effects library.

### D. Is the gain bought with materially higher generation complexity?

`NO / CURRENT DESIGN`.

Both candidates use four raw ~5s sources. B still keeps one primary camera relation, one primary subject action and one secondary physical system per source. No additional model/runtime/tool dependency is introduced.

## B risks to test downstream

1. The relational-distance thesis may become too conceptual if first-frame composition does not make camera/subject distance readable.
2. NB03 linen occlusion can become decorative or reconstruct space if coverage is excessive; it is optional and threshold-only.
3. B-S03 after-rain + wind must remain an after-state, not become a weather-effects demo.
4. B-S04 must visibly stop re-chasing intimacy after `放下`; otherwise the thesis collapses even if the shot is beautiful.

## Selection

`WINNER_FOR_DOWNSTREAM_TEST = B / R3_PLUS_OSS_OVERLAY`.

Reason:
B shows meaningful gains in coherence, camera motivation, edit handoff and zero-context reproducibility while holding source count and expected generation load essentially constant.

This is **not yet a final promotion of OSS rules**. The selected B plan must still prove:
- first-frame beauty and performability;
- actual model camera execution;
- identity/gait/topology stability;
- edit usability;
- no increase in regeneration/manual intervention.

`NEXT = write selected B into canonical DIRECTOR_BEAT_MAP + DIRECTOR_PLAN, then S05 lock`.
