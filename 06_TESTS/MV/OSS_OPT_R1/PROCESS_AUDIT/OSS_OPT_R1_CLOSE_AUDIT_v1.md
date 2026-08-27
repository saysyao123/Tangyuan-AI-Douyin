# OSS_OPT_R1｜Final Close Audit v1

Status: `CLOSE PASS`
Date: `2026-08-28` (Asia/Tokyo project date)
Experiment branch: `test/mv-oss-optimization-r1`
Stable baseline branch: `test/mv-web-r3` — **not modified by this experiment closeout**.

## 1. Closure question

Did the experiment complete one real MV end-to-end under Canonical Runtime, test the selected OSS optimization layer without weakening state/gate correctness, and produce bounded promotion decisions?

Answer: `YES`.

## 2. Real MV proof

Experiment MV: `D02-B / 《有几次想你了》 / Lane S`.

Canonical Runtime reached:

`S16_RELEASE_PACKAGE_READY / RELEASE_READY / transition_sequence=16`.

Verified contiguous transition chain:

`INIT -> S00 -> S01 -> S02 -> S03 -> S04 -> S05 -> S06 -> S07 -> S08 -> S09 -> S10 -> S11 -> S12 -> S13 -> S14 -> S15 -> S16`.

Human Gates:
- HG01 song selection: PASS;
- HG02 BGM: PASS;
- HG03 first-frame set: PASS;
- HG04 picture rhythm: PASS;
- HG05 final acceptance: PASS.

Final accepted render:
- file: `D02-B_有几次想你了_最终候选_字幕版_v1.mp4`;
- SHA-256: `7f77a41a68db47d4f7992cb77161c86414eeb0fd1cf8233322956b4025bf43d9`;
- duration: `15.375s`;
- video: `H.264 / 720x1280 / 24fps / SAR 1:1`;
- audio: accepted HG04 audio stream identity preserved;
- subtitle QA: PASS;
- final technical QA: PASS;
- user final acceptance: PASS.

## 3. OSS source boundary

Locked external source:

`penposs/mvmaker-h3-skills@796797030275fe57afaba736771e8510c848799d`.

The experiment correctly separated:

- portable Director/Montage knowledge;
- H3-specific execution/container/input constraints.

Only the bounded knowledge/stage overlay was tested downstream. H3-specific 10-15s containers, four-panel input packaging and RunningHub orchestration were not imported into R3.

## 4. Creative result

Plan-level Director A/B selected `R3 + OSS overlay` over R3 baseline.

The selected overlay added:
- Director Thesis;
- Primary Visual Engine;
- explicit audiovisual relation;
- motive-first camera-subject-space logic;
- WHY CUT HERE montage reasons;
- optional-effect stop conditions;
- Creative Drift QA.

Downstream evidence did not collapse:
- First Frame QA: PASS;
- Dynamic Source QA: PASS / no regeneration required;
- five raw sources yielded ~13 useful visible atoms;
- all seven lyric lines received direct visual coverage;
- Shot Library QA: PASS, >=11 high/very-high edit-value atoms;
- HG04 dense lyric-first preview: user accepted;
- final emotional progression retained `靠近 -> 忍住 -> 算了 -> 雨停 -> 风过 -> 握住 -> 松手 -> 世界打开`;
- HG05 final render accepted.

Conclusion: the overlay is **production-viable as bounded knowledge**, but one real selected-B downstream run is insufficient to turn every heuristic into a hard Runtime rule.

## 5. Process / Runtime result

The experiment also exposed and repaired an independent executor-discovery defect:

`Runtime knew WHAT stage was next more strongly than HOW that stage was already implemented.`

Experiment-branch remediation:
- stage executor registry;
- Executor-First admission rule;
- canonical tool/capability discovery before new implementation;
- no per-slot production model install by default;
- no slot-specific core helper by default;
- Runtime Bridge kept as state transport rather than stage-specific job host.

Decision: `PROMOTE_RUNTIME_CANDIDATE`, not automatic stable deployment.

Audio Timeline route also reached a bounded conclusion:

`P0 SAME_VERSION_LRC -> P1 D01B_LIGHTWEIGHT_FASTER_WHISPER -> P2 XINGYU_CTC_FALLBACK`.

Decision: `PROMOTE_RULE_CANDIDATE`.

## 6. Failure handling proof

The experiment contained real failures and corrected them without falsifying history:

1. partial creator caption was initially mistaken for full lyrics;
2. incorrect four-line downstream state was formally rolled back;
3. seven-line audited lyric truth was rebuilt through the canonical path;
4. one-off executor/tooling pollution was classified and remediated;
5. later normalization naming issue was repaired locally rather than cascading upstream;
6. Runtime then resumed and completed through S16.

This is positive evidence for rollback, nearest-layer patching and durable auditability.

## 7. Promotion decisions

### Promote as knowledge now
- OSS-01 Director Thesis;
- OSS-02 Primary Visual Engine;
- OSS-03 audiovisual relationship modes;
- OSS-04 motive-first camera-subject-space reasoning;
- OSS-05 WHY CUT HERE as knowledge, with hard-rule promotion deferred;
- OSS-06 optional-element trigger/function/range/stop condition;
- OSS-07 Creative Drift QA checklist.

### Promotion candidates requiring explicit stable-branch review
- Executor-First Runtime routing / stage executor registry: `PROMOTE_RUNTIME_CANDIDATE`;
- P0/P1/P2 Audio Timeline priority: `PROMOTE_RULE_CANDIDATE`;
- WHY CUT HERE as a hard editing rule: require another real MV before promotion beyond knowledge.

### Reject for current R3 path
- H3 integer 10-15s container constraint;
- H3 16:9 four-panel Picture-1 input contract;
- RunningHub/H3 orchestration as replacement for current Web/Seedance execution.

## 8. No silent deployment

This close audit intentionally does **not** merge/cherry-pick experiment changes into `test/mv-web-r3`.

A future promotion action must:
1. review the exact experiment diff;
2. choose only approved candidate files/rules/knowledge;
3. preserve existing Runtime guards and tests;
4. run regressions;
5. produce a separate promotion/deployment receipt.

## 9. Publish boundary

D02-B stops at S16 because the user has accepted the final render but has not confirmed the real Douyin post is live.

Do not:
- set Tracker to PUBLISHED;
- invent a publish timestamp;
- advance S17 by hand.

After real-world publish confirmation, use the registered transactional publish executor / `PUBLISH_SYNC` path.

## 10. Final verdict

`OSS_OPT_R1 = CLOSE PASS / SELECTIVE VALUE PROVEN / NO STABLE DEPLOYMENT YET`.

The experiment fulfilled its purpose: test external OSS MV ideas on a real canonical slot, preserve Runtime correctness, identify useful bounded director knowledge, reject adapter-specific baggage, expose one real process architecture defect, and finish the selected MV as an accepted release-ready asset.
