# D02-B｜Dynamic Source QA v1.0

Status: `PASS_WITH_TRIM_AND_NORMALIZATION / NO_REGEN_REQUIRED`
Stage target: `S08_DYNAMIC_SOURCE_QA_LOCKED`
Authority: actual uploaded/generated source pixels > prompt prose.

## 1. Source identity / role mapping

The four reviewed user-uploaded sources are mapped by actual visible action, not filename order:

| Source | Uploaded filename | SHA256 | Actual role |
|---|---|---|---|
| S1 / B01 | `AI动画人物克制靠近与停住.mp4` | `693f2950fe280eb45f883162e69e3f69e478a28dd2f05dff24291d8c55ae8d92` | APPROACH / hook |
| S2 / B02 | `AI动画人物克制靠近与停住 (4)(1).mp4` | `91835f8752879b02e928500481976baaff82ea50f4386137ade3cf6449be24ff` | BOUNDARY HOLD -> PASSAGE |
| S3 / B03 | `AI动画人物克制靠近与停住 (5).mp4` | `9cf119dd0cebc6f61a795346b35aa679697f2eb743e666b776142e952070e440` | LOOK-BACK -> CONTINUE / FOLLOW |
| S4 / B04 | `AI动画人物克制靠近与停住 (1).mp4` | `96ed21561555fc852208ee4a49ef1a001dedb9d95205e9d616cf6e34704b6e25` | DISTANCE / RELEASE |

All are ~5.056s, H.264, 24fps. S1/S3/S4 are 720x1280. S2 is 720x960 and therefore requires geometry normalization before Picture Edit.

## 2. Face Reconstruction validation

### S1
- K0 black square grid visible at frame 0.
- Grid is already gone by approximately 0.1s in sampled frames.
- Completed face remains stable through the usable approach window.
- No repeated grid return observed.

Result: `FACE_RECONSTRUCTION_PASS`.

### S2
- K0 black square grid visible at frame 0.
- Grid is already gone by approximately 0.1s.
- Completed face remains stable while holding, turning and passing the pillar boundary.
- This is the strongest direct validation of the new `standard square black grid -> reconstruction` production path.

Result: `FACE_RECONSTRUCTION_PASS`.

### S3
- K0 black square grid visible at frame 0 at a rear-three-quarter / looking-back angle.
- Grid is already gone by approximately 0.1s.
- The same completed identity survives the subsequent head turn from look-back to forward direction.
- No second face or identity jump observed in reviewed samples.

Result: `FACE_RECONSTRUCTION_PASS / CROSS_ANGLE_VALIDATED`.

### S4
- Face is not readable at release distance; no visible reconstruction event is required.
- Identity continuity is carried by silhouette, hair, wardrobe and body proportions.

Result: `DISTANT_FACE_NOT_APPLICABLE / PASS`.

## 3. Source-by-source director / edit QA

### S1 / B01｜APPROACH
Prompt intent: `APPROACH -> RESTRAINT / LEAD -> HOLD`.

Actual source:
- technically stable;
- attractive, readable forward approach;
- face reconstruction stable;
- camera/subject relation communicates approach well;
- however the subject does NOT complete the planned restraint/stop;
- after roughly the middle of the source the facial performance gradually becomes a warmer smile / commercial-model feeling.

Decision:
`TRIM_REQUIRED / KEEP_APPROACH_ATOM / NO_REGEN`.

Recommended main edit window:
`raw 0.10s -> ~1.80s`.

Use it for `有几次想你了` only. Cut before the smile becomes the dominant semantic signal. Do not force this source to also prove `忍住了`.

### S2 / B02｜BOUNDARY -> PASSAGE
Prompt intent: `HOLD -> YIELD`.

Actual source:
- face reconstruction is fast and stable;
- ~first 2s maintains an effective held/contained boundary state;
- then the subject turns and commits to outward passage;
- the transition is natural, with stable anatomy and architecture;
- camera movement is restrained but the semantic passage is readable;
- performance stays much closer to the desired restrained emotional tone than S1.

Decision:
`PASS_FULL_AFTER_GRID_TRIM / PRIMARY SOURCE`.

Recommended main edit window:
`raw 0.10s -> 5.00s`.

This source should carry the semantic chain:
`忍住 -> 想说 -> 算了`.

### S3 / B03｜LOOK-BACK -> CONTINUE
Prompt intent: `FOLLOW / DISCOVER`, weather already passed.

Actual source:
- square-grid reconstruction succeeds at the harder look-back angle;
- the look-back remains readable long enough to register;
- the head then resolves forward naturally;
- body direction and gait remain stable;
- the source transitions from relational look-back into clear forward travel;
- environmental motion is restrained; no unwanted rain event appears;
- camera grammar is still conservative, but source is highly editable and coherent.

Decision:
`PASS_FULL_AFTER_GRID_TRIM / PRIMARY SOURCE`.

Recommended main edit window:
`raw 0.10s -> ~4.20s` for current first-pass edit; remainder may stay in reserve.

### S4 / B04｜RELEASE
Prompt intent: `STOP PURSUING -> WORLD OPEN`.

Actual source:
- stable wide colonnade composition;
- subject remains small and continues away;
- camera does not restore intimacy;
- strong negative space / architectural rhythm;
- no face/topology burden;
- clean visual tail and good final-release usability.

Decision:
`PASS_FULL / PRIMARY RELEASE SOURCE`.

Recommended main edit window:
`raw 0.00s -> ~4.69s` for current timeline; extra tail remains available.

## 4. Whole-set result

Face / identity stability: `PASS`.
First-frame square-grid reconstruction path: `PASS / S2 + S3 VALIDATED`.
Topology / hands / gait: `PASS_FOR_EDIT`.
Environment continuity: `PASS`.
Shot-role differentiation: `PASS`.
Camera-director ambition: `SERVICEABLE / FUTURE_OPTIMIZATION_CANDIDATE`.
Regeneration requirement: `NO`.

The most important creative limitation is S1: it proves approach/attraction but not restraint. This is an edit-local issue, not a generation failure. Apply `TRIM BEFORE REGENERATE`.

## 5. Edit-local compensation

Do not regenerate S1 merely to recover the missing stop.

Use:
- S1 = `想你` approach hook;
- S2 early hold = anticipatory / direct visual answer for `忍住`;
- S2 passage = `想说 -> 算了`;
- S3 = `算了` residue -> `雨停 / 风过` continuation;
- S4 = `舍不得 -> 放下` release.

This produces a stronger relational arc than forcing each generated source to carry its full original prompt assignment.

## 6. Gate result

`DYNAMIC_SOURCE_QA = PASS_WITH_TRIM_AND_NORMALIZATION`
`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = READY`
`REGENERATE_REQUIRED = NO`
`TRIM_BEFORE_REGENERATE = APPLIED`
