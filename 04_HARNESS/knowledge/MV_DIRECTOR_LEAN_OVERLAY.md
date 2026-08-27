# Knowledge｜MV Director Lean Overlay v1

Status: `PROMOTED_TO_LEAN_TEST / NOT YET STABLE HARD RULE`
Source evidence: OSS_OPT_R1 / D02-B.

This file intentionally keeps only the portable director/montage knowledge that proved useful. It does not import H3 container/input/orchestration constraints.

## 1. Director Thesis
Before segment prompts, state one sentence describing the whole MV's emotional/cinematic proposition. It should constrain choices, not decorate the document.

## 2. Primary Visual Engine
Choose one dominant visual mechanism that holds the MV together: e.g. distance, threshold, wind, reflection, release, changing light, spatial approach/withdrawal. Individual lyric images may vary, but the engine keeps one-world coherence.

## 3. Audiovisual Relationship
For each important lyric beat, explicitly choose how picture relates to lyric/music: direct hit, emotional counterpoint, delayed answer, environmental echo, spatial metaphor, or release. Avoid one-shot-per-line literal illustration when a stronger relationship exists.

## 4. Motive-first camera / subject / space
Camera movement and framing must answer an intention: approach, resist, reveal, separate, follow, hold, release. Do not add camera motion merely to make a shot feel active.

## 5. WHY CUT HERE
Every meaningful cut should have a reason visible in action, intention, lyric change, music event, spatial information or emotional state. Internal multi-shot atoms are valid edit sources when the cut reason is readable.

## 6. Optional element stop condition
For wind, cloth, rain, particles, flare, props or secondary motion, define trigger + narrative function + allowed range + stop condition. Optional beauty elements must stop before they become the subject without reason.

## 7. Creative Drift QA
At Director -> K0 -> Dynamic Prompt -> generated source, compare intended function with actual pixels. Accepted actual K0/source pixels outrank superseded prose. Patch the nearest layer; do not force downstream models to reconstruct an abandoned text plan.

## Non-goals / rejected imports
- no H3 10–15 second integer container requirement;
- no 16:9 four-panel Picture-1 package requirement;
- no RunningHub/H3 orchestration requirement;
- no extra Human Gate for reading a text Director Plan in normal production.
