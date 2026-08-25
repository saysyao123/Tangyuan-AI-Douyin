# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-D1 / PACKAGING CANDIDATES READY / REAL-PUBLISH SELECTION PENDING`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / R3_A_PASS / HG01_PASS / BGM_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED / R3_B_CURRENT_CALIBRATION_PASS / HG03_PASS / FIRST_FRAME_SET_LOCKED / CAMERA_CALIBRATION_COMPLETE_FOR_CURRENT_LOOP / PHYSICAL_PLAUSIBILITY_ITERATION_COMPLETE / DOUBAO_PROMPT_REWRITE_VALIDATED / FINAL_MATERIAL_REVIEW_COMPLETE / WEB_SOURCE_ROUGH_CUT_GATE_PASS / HG04_PASS / PICTURE_EDIT_LOCKED / SUBTITLE_STYLE_QA_PASS / SUBTITLE_IMPLEMENTATION_QA_PASS / FINAL_TECH_QA_PASS / DELIVERABLE_RENDERED / HG05_PASS / R3_C_FULL_MV_INTEGRATION_PASS / RETROSPECTIVE_COMPLETE / R3_D1_PACKAGING_CANDIDATES_READY / REAL_PUBLISH_SELECTION_PENDING`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

## Program-level status

- `R3-A Music Radar / Benchmark Calibration = PASS`
- `R3-B Healing Visual Calibration = PASS FOR CURRENT CALIBRATION`
- `R3-C Full MV Integration = PASS / HG05`
- `R3-D1 Publish Packaging Benchmark = CANDIDATES READY`
- `R3-D2 Live Data Feedback = NOT STARTED`

Therefore:
`R3_PROGRAM_COMPLETE = NO`

## Accepted production asset

Song family: `如果风会替我说话`
Final accepted MV:
`如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`
SHA-256:
`b96ddb81395772395ed8946b3fc30341f124bef14124f47a203dda87a3ef9f42`

Upstream production remains locked:
- `BGM_LOCKED = YES`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `HG03_PASS = YES`
- `WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`
- `HG04_PASS = YES`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
- `FINAL_TECH_QA_PASS = YES`
- `HG05_PASS = YES`
- `R3_C_FULL_MV_INTEGRATION_PASS = YES`

Do not reopen production variables during D-series packaging/data tests.

## R3-D1 authority

Artifact:
`R3_D1_PUBLISH_PACKAGING_BENCHMARK_v1.md`

Two controlled packaging candidates:

### Candidate A — `MUSIC_FIRST`
Core strategy:
- exact song identity first;
- one restrained emotional reason to stay;
- search clarity highest;
- AI remains production attribute, not first content identity.

Recommended cover frame:
`S01` close eye/veil/wind frame.

Recommended title:
`如果风会替我说话｜有些话没说出口，就让风替我说吧`

Recommended tags:
`#如果风会替我说话 #音乐推荐 #治愈系 #氛围感 #AI视觉`

### Candidate B — `EMOTION_FIRST`
Core strategy:
- unsaid-feeling hook first;
- song identity second;
- stronger self-projection/comment potential;
- larger packaging variable, therefore weaker attribution clarity for first live test.

Recommended cover frame:
`S08` world-opening release frame.

Recommended title:
`没说出口的话，风真的会替你说吗？｜如果风会替我说话`

Recommended tags:
`#如果风会替我说话 #氛围感 #治愈系 #音乐推荐 #AI视觉`

## Controlled-test recommendation

Recommended first real publish:
`MUSIC_FIRST`

Reason:
The R3 production song itself came from the new Music Radar. The first live-data test should keep song identity explicit so D2 can more cleanly evaluate whether:
`radar-selected song + exact Douyin version + improved visual system`
works in real publication.

Do NOT post both packages with the same video.
The alternate remains a counterfactual candidate for a later different MV.

`R3_D1_PACKAGING_CANDIDATES_READY = YES`
`REAL_PUBLISH_SELECTION = PENDING HUMAN CHOICE`

## R3-D2 metric contract after publication

Record at:
- `1h`
- `3h`
- `24h`

When visible:
- views;
- likes;
- comments;
- favorites;
- shares;
- profile visits;
- new follows;
- followers before/after;
- completion rate;
- average watch time.

Primary normalized metric:
`follows_per_1000_views = new_follows / views * 1000`.

Single-post evidence remains `EXPERIMENT`, not `PERFORMANCE_VALIDATED`.

## Main branch / promotion boundary

Do not blindly merge the entire test branch.
Curated production promotion remains the correct path for Harness runtime/rules/templates/selected tools/knowledge. R3 packaging conclusions cannot be promoted until live-data repetition exists.

## Next action

Human selects exactly one real-publish candidate:
- `MUSIC_FIRST` (recommended), or
- `EMOTION_FIRST`.

After explicit selection:
→ create `R3_D1_REAL_PUBLISH_RECEIPT`
→ record exact final package
→ record actual publish timestamp after posting
→ enter `R3-D2 Live Data Feedback`.
