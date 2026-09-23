# S1 PROJECT_AUDIO — Test Report Run02 / Contract v0.2

Status: DELIVERED / READY_FOR_FRESH_REVIEW

Representative project: 《爱让人脑袋空空》

## 1. Why v0.2 exists

Run01 exposed one stage-boundary defect:

`target_aspect_ratio` was incorrectly included inside PROJECT_AUDIO.

That is project-level metadata, not audio/timeline truth.

v0.2 removes aspect ratio from S1 and places it in Runtime Project Metadata.

This is a scope correction, not a change to the locked audio/timeline itself.

## 2. Deterministic validation

Result: PASS 6/6

- D01 segment_end > segment_start: PASS
- D02 locked duration matches start/end: PASS
- D03 selected audio version present: PASS
- D04 timeline begins/ends at locked segment boundaries: PASS
- D05 timeline units ordered and contiguous: PASS
- D06 Human Audio Lock present: PASS

Derived duration:
`15.370998s`

Timeline:
T00–T12 continuous within 0.001s tolerance.

## 3. Semantic evidence

Authoritative audio/timeline:
`07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`

Existing downstream Director:
`07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v3_LOCKED.md`

Observed downstream consumption:
- BGM 0.000–8.700 is preserved as Segment A;
- BGM 8.700–15.370998 is preserved as Segment B;
- 8.700 semantic reset is preserved;
- Director adds generation duration, shot structure, camera and visual design downstream rather than redefining S1 timeline truth.

This supports the intended separation:

`PROJECT_AUDIO truth -> DIRECTOR creative interpretation`

## 4. Scope test

v0.2 does not lock:
- aspect ratio / output format;
- generation duration;
- shot count;
- character;
- scene;
- camera;
- motion.

Those belong to Project Metadata or later Stages.

## 5. Reliability interpretation

The current S1 structure has demonstrated:

1. deterministic state can be checked without GPT;
2. a real historical project can be represented by a compact S1 handoff;
3. downstream Director actually consumed the same timeline successfully;
4. stage-boundary testing detected and removed an unnecessary dependency;
5. the current handoff is smaller and cleaner than the previous long-form project history.

## 6. Remaining gate

Independent Fresh Judge must still evaluate J01–J05 under `S1_JUDGE_CONTRACT_v0.2`.

Do not seal S1 or start S2 until that independent review returns PASS.
