# D01-B｜Final Technical QA v1

Status: `PASS / READY_FOR_HG05`

Final local preview:
- file: `D01-B_FINAL_HG05_PREVIEW_v2.mp4`
- SHA-256: `ab85a5cbae917c4e3b3bbb0ad673df1178c8c6e55a73b84960dea4174f5b0fe4`

## Container / streams

- video: H.264
- geometry: `720x1280`
- SAR: `1:1`
- frame rate: `24fps`
- video frames: `384`
- video duration: `16.000s`
- audio: locked BGM lineage, AAC stereo, 44.1kHz
- audio duration: approx `15.961s`
- no generated-source audio leakage

## Upstream lock verification

- `BGM_LOCKED = YES`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `VIDEO_SET_PASS = YES`
- `WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`
- `HG04 = PASS`
- Picture EDL unchanged after HG04
- Subtitle timing derived only from canonical timeline

## Visual technical QA

PASS:
- no visible generator corner mark after uniform 1.25× safe crop;
- no mixed crop geometry;
- no SAR stretch;
- no black/missing video segment;
- S01 opening composition intact;
- S02 hand/water action intact;
- S03 flower remains readable and serves as the visual contraction/turn;
- S04 final ascent retains open negative space and release;
- subtle grade progression does not introduce clipping or style discontinuity.

## Subtitle QA

- all four events present through the full video;
- locked baseline style used;
- 10px equal padding on all lines;
- text/box center error 0px;
- 24fps implementation deltas within one frame;
- no face/eye obstruction;
- final line remains readable through the release/fade region.

## Full-watch logic QA

Narrative / visual sequence remains:
`reorientation -> self-care -> flower/life turn -> ascent/release`

No extra transition effects were added after HG04. Hard-cut rhythm remains the user-approved structure.

`FINAL_TECH_QA_PASS = YES`
`NEXT_HUMAN_GATE = HG05 / Final Acceptance`
