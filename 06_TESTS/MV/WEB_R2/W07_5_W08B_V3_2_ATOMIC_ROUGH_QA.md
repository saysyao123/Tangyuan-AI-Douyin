# WEB R2｜W07.5 Shot Normalization + V3.2 Atomic Rough Cut QA

## W07.5 normalized library

- source originals preserved: 9/9
- usable normalized Atom/Arc units rendered: 22
- rejected from main atom pool:
  - `S1_X01`: 0.375s micro-shot
  - `S1_X02`: duplicate low-angle family
  - `S7_X01`: topology-risk frames 65–97
  - `S7_X02` / `S7_X03`: too short as standalone atoms; retained only through limited release arc
- all normalized WEB-preview units:
  - source audio removed
  - 24fps / 720×1280 / SAR 1:1
  - consistent whole-source watermark fallback: `crop=576:1024:72:128 -> scale=720:1280`
  - equivalent visual zoom: 1.25×
- representative contact-sheet review: no top-left / bottom-right generator mark remained in reviewed normalized units.

The original 5s source remains canonical source evidence. Atom/Arc files are derived edit proxies and can be regenerated from the map.

## Why normalization is now a pipeline layer

V3.1 had only 9 external timeline fragments, but several fragments contained generated internal cuts. The viewer therefore perceived materially more than 9 actual shots.

V3.2 tests a more controllable model:
`raw 1–3 shot clip -> W07 QA -> non-destructive shot/arc normalization -> final picture edit`.

The editor can choose either:
- a single-state Atom when precise cut control is needed; or
- a coherent Arc only when its internal cut grammar has a clear director task.

## V3.2 atomic rough cut

- visible selected units: 13
- hidden/random internal cuts in selected Atom units: none
- total picture: 891 frames / 24fps / 37.125s
- locked audio: 37.120s
- decoded preview audio vs locked BGM best global lag: `0.000000s`
- normalized audio correlation: `0.999047`
- preview SHA-256: `797ac52cf470fb871f312b7699247b9f0bbc46120d1124813e39a459f4f1812f`
- subtitle overlay: canonical exact-timing diagnostic style only; W09 style remains unlocked.

## Current interpretation

V3.2 is a **rough-cut candidate**, not an automatic replacement for V3.1.
Its value is edit controllability: every visible cut is explicitly selected by the editor.
Human viewing should decide whether the final picture basis is:
1. V3.2 atomic cut; or
2. a V3.1/V3.2 hybrid using mostly Atoms plus only a few intentionally retained coherent Arcs.

No audio-timeline, lyric-timing, BGM, or source-generation stage is reopened.