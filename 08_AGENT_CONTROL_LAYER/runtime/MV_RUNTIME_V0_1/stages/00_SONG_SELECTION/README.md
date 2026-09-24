# S0 SONG_SELECTION

Status: DESIGNING  
Current candidate contract: v0.1-draft

## Purpose

Choose **which song family and which concrete reference work** should enter MV production.

S0 ends before audio extraction, detailed lyric transcription, beat analysis, segment timing, or full timeline construction.

Those belong to S1 PROJECT_AUDIO.

## Core boundary

S0 answers:

- What songs are worth considering?
- Which concrete reference works support each song?
- Which 1–3 candidates best fit the current MV production goal?
- Which single concrete work does the user choose?

S0 does **not** answer:

- exact locked Audio Version;
- exact start/end of final segment;
- lyric timestamp timeline;
- BPM / beat grid;
- semantic cut-point timing;
- generated clip duration;
- Director design.

## Successful historical logic retained

1. All 9 trusted core accounts contribute songs.
2. Account role changes signal interpretation/weight, not eligibility.
3. Work-level records are normalized into SONG_FAMILY.
4. Cross-core-account repetition increases confidence that the song is worth examining.
5. Visual / animation / motion suitability are evaluated against the current MV goal.
6. Historical project reuse is surfaced as a risk/context signal.
7. Each round delivers at most 3 primary candidates.
8. Every primary candidate must include a concrete reference work/link.
9. The user opens/reviews the candidates and chooses one concrete reference.
10. If all candidates are rejected, run another round from the trusted pool; do not silently jump to random platform charts.
11. Only after Human Reference Lock does S1 begin Audio Version + Timeline Lock.

## S0 target flow

Core Account / Trusted Song Pool
-> Normalize Song Family
-> Qualify candidates
-> Build max-3 shortlist
-> Human Reference Gate
-> SONG_SELECTION_HANDOFF
-> S1 PROJECT_AUDIO

## Current status

Framework/design only.

Next action:
Review the v0.1 S0 method and then test it against the historical successful Round 01 before using a new live selection round.
