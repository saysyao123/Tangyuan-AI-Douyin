# S1C Repair — Selected-Segment Quality Gate

## Problem

Whole-song trusted-lyrics CTC alignment matched all 28 official lyric lines and
all 178 alignment characters, but verse1 line 1 was stretched across ~28.2s.

Therefore the whole-song line-level alignment is not globally trustworthy.

## Repair

S1 does not require every unused part of a full source to have perfect line-level
timing. It requires the FINAL PRODUCTION SEGMENT to have sufficient evidence.

New decision rule:

- Whole-song alignment may be PARTIAL_LOW_CONFIDENCE.
- A production segment may still seal at LINE_LEVEL if every lyric line inside
  that selected segment passes deterministic timing checks.
- Low-confidence lines outside the selected segment do not contaminate the
  selected-segment timeline.

## Current selected segment

Section:
CHORUS_2

Trusted lyric line IDs:
21-28

Aligned lyric range:
122.747s -> 138.410s

Rendered range with handles:
122.547s -> 138.710s

Selected line quality:
- 8/8 lines timed
- monotonic
- zero missing character timestamps in upstream report
- maximum selected line duration: 3.820s
- all selected lines are inside the structurally detected high-energy section

Verdict:
PASS_LINE_LEVEL_SELECTED_SEGMENT
