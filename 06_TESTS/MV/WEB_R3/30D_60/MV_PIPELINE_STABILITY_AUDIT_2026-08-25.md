# 汤圆音乐映像｜MV Pipeline Stability Audit｜2026-08-25

## Executive conclusion

Current system status:

`REPEATABLE WITH HUMAN AESTHETIC CONTROL / TECHNICALLY STABLE / NOT YET UNATTENDED-AUTOMATION STABLE`

The production path can repeatedly produce publishable MV masters across different song lengths, visual worlds and segment counts. The strongest stable region is Audio Timeline -> Dynamic QA -> Picture Edit -> Subtitle -> Final QA. The main remaining variability is Director aesthetics / first-frame set generation and execution discipline around already-defined technical gates.

Production stability must not be confused with distribution performance. Early published data is still insufficient to judge account strategy.

---

## Formal completed evidence set

### R1 Golden Sample
- song: `你有没有真的爱过我｜阿图表妹`
- duration: `36.80s`
- structure: `8 first frames + 8 × 5s dynamic clips`
- final: `R1_MV_v4_final_polish.mp4`
- state: `COMPLETE_LOCKED`
- contribution: first end-to-end human Golden Sample; established BGM lock, 0-second first frames, mixed camera structure, action-integrity editing and audio-derived lyric timing.

### WEB R2
- song: `如果你也刚好抬头看树｜孙天宇`
- duration: `37.120s`
- first frames: `9/9 accepted`
- state: `COMPLETE_LOCKED`
- contribution: promoted Audio Timeline Package, Human Gate contract, Atom/Arc normalization, long-cut-first edit, WEB uniform watermark-safe crop and subtitle geometry QA into Runtime.

### WEB R3 / D01-A
- song: `如果风会替我说话`
- accepted MV: `如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`
- state in R3 creative chain: `HG05 PASS / accepted production asset`
- contribution: exact Douyin music-asset discovery, stronger dynamic-generation control heuristics, publish packaging calibration and account-level MUSIC_FIRST direction.
- publication: user has confirmed the post is live; exact tracker timestamp remains to be synchronized.

### 30D/60 D01-B
- song: `我救自己于人间水火`
- lane: `S / Stable-Fast`
- duration: `15.986939s`
- structure: `4 semantic segments / 4 final dynamic sources`
- state: `COMPLETE_LOCKED`; user subsequently confirmed publication.
- contribution: first cross-song replication of several R3 dynamic-generation heuristics inside the 30D/60 production system; three of four initial dynamic sources were directly usable, one local S03 regeneration completed the set.

---

## Stability by production stage

| Stage | Stability | Audit result |
|---|---|---|
| Song / trend discovery | HIGH-MEDIUM | Current Douyin-first path is reusable; evidence tiers are defined. |
| Exact BGM version discovery | HIGH | Real Douyin asset id / provenance / fingerprint route is now strong. |
| HG02 excerpt listening | HIGH with one process risk | Human listening decision is reliable; downstream evidence must never silently override a user-approved BGM. |
| Audio Timeline Package | HIGH | Forced alignment + trusted lyric hash + provenance now gives a reproducible time truth. Occurrence selection must be resolved before boundary decisions. |
| Natural Beat | HIGH | Semantic beat model replicated cleanly across different song lengths. |
| Director Concept | MEDIUM | Semantics are generally correct, but beauty/world translation can still fail badly before user review. D01-B v1 industrial greenhouse was the clearest example. |
| First-frame Set | MEDIUM | 0-second anchor rule is strong, but set-level beauty, shot differentiation and actual generation compliance still require active review. |
| Dynamic Prompt | HIGH-MEDIUM | HARD FREEZE -> FRAME-0 -> STATIC BASE -> ONE EVENT -> BOUND -> PHASES -> RESIDUE replicated successfully across songs. |
| Dynamic Generation | HIGH-MEDIUM | D01-B achieved 3/4 first-pass usable sources and one local repair. Still external-model dependent. |
| Dynamic QA / nearest-cause repair | HIGH | Local S03 regen without cascading upstream proved Patch, Don't Cascade works. |
| WEB rough-cut / watermark safety | HIGH as a rule, execution guard missing | Runtime is validated, but D01-B first HG04 preview accidentally skipped this gate and required a retrofit. |
| Picture Edit | HIGH | Long-cut-first + locked lyric clock + source action windows are now dependable. |
| Subtitle | VERY HIGH | R2 baseline reproduced; timing/geometry QA is deterministic. |
| Final technical QA | VERY HIGH | Codec/SAR/audio leakage/watermark/subtitle checks are reproducible. |
| Publish packaging | MEDIUM-HIGH | MUSIC_FIRST direction is defined, but title/caption/cover implementation still needs account-level consistency enforcement. |
| Tracker / state synchronization | MEDIUM-LOW | D01-A/D01-B publication truth is not yet synchronized across Tracker/root state/per-slot state. |
| Zero-context Codex reproduction | NOT PROVEN | `CODEX_R1` remains at C00 READY_TO_START; current system is not yet validated as unattended Codex automation. |
| 2 posts/day throughput | NOT YET PROVEN | The operating target exists, but only early samples are live and D01-B still required multiple first-frame/director corrections. |

---

## D01-B process failures that must be treated as system evidence

### 1. BGM was almost modified to satisfy weak downstream timing evidence
A public LRC occurrence was initially over-weighted, causing an unnecessary Candidate C trim. Correct resolution was to keep user-approved B locked and align evidence to B.

Promotion candidate:
`HG02 USER-APPROVED BGM > downstream weak/uncertain timing evidence`.
Only strong same-version proof or an explicit user audio change may reopen BGM.

### 2. Semantically correct Director concept can still be aesthetically wrong
Industrial greenhouse v1 matched self-rescue semantics but failed the beauty target and conflicted with the chosen veil / pearl-glow heroine.

Required pre-generation machine QA:
`lyric-specific hit + beautiful standalone still + coherent world/wardrobe + set-level shot differentiation + performable 0-second anchor`.

### 3. First-frame actual state must outrank old text plans
Later accepted images evolved away from earlier Director prose. Dynamic prompts must read the actual accepted first frame as K0 truth, not attempt to restore an obsolete plan.

### 4. Dynamic prompt completeness was initially under-specified
The first D01-B dynamic prompt set omitted several already-known control layers. After reinstating HARD FREEZE / FRAME-0 / STATIC BASE / ONE EVENT / motion weights / phase actions / residue / settled end state, generation became more controllable.

Cross-song replication now supports promoting the stable part of this hierarchy from R3 Knowledge into active AI-video Runtime.

### 5. S03 proved nearest-cause rollback works
Three sources remained locked; only S03 was regenerated. This should remain the default production behavior.

### 6. WEB rough-cut gate was executed late
The rule already required watermark-safe proxies before formal Picture Edit, but the first D01-B HG04 preview skipped it. The omission was repaired using the same EDL after HG04.

This is an execution-discipline defect, not a missing method. Add an automated stage-entry checklist so a formal HG04 artifact cannot render unless:
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`.

### 7. Packaging consistency is not yet fully locked
D01-A uses one-line song-name cover + restrained caption structure. D01-B package introduced a separate title format `song｜emotion line`, and cover generation briefly drifted from the previous account-level cover grammar.

Need one account-level packaging implementation contract distinguishing:
- Douyin caption;
- cover text;
- optional internal project title.

### 8. State ledger is diverging
The user has confirmed publication of D01-A and D01-B, while the central tracker / some state files still show `SCHEDULED`, `FIRST_FRAME_IN_PRODUCTION` or `READY_TO_PUBLISH`.

Before scaling, define one publication state sync operation that updates:
`per-slot CURRENT_STATE -> MV_30D_60_TRACKER -> program data state`.

---

## What is already stable enough to freeze

1. Five Human Gates: HG01/HG02/HG03/HG04/HG05.
2. Douyin-first exact asset discovery.
3. BGM lock before Audio Timeline Package.
4. Audio Timeline Package as the only timing truth.
5. Natural Beat before Director Allocation.
6. First frame as 0-second dynamic anchor.
7. First-frame character closure.
8. Dynamic source = RAW SOURCE, not final 5s clip.
9. 1–2 shot default / 3 shot task-driven, not automatic multi-shot density.
10. Static Base + One Allowed Event + Control Budget for difficult generation.
11. Dynamic QA + VISUAL_SOURCE_MAP + trim before regenerate.
12. WEB uniform watermark-safe proxy geometry.
13. Long-cut-first Picture Edit.
14. Subtitle timing from audio truth, not visual cuts.
15. R2 subtitle geometry baseline and all-line QA.
16. Patch, Don't Cascade / nearest-cause rollback.
17. Final technical QA before HG05.
18. MUSIC_FIRST as the initial controlled packaging baseline.

---

## Minimum hardening before D02

Do not redesign the whole system. Apply a small v1.9 hardening pass:

A. `STAGE ENTRY CHECKLIST`
Machine-readable prerequisites before Stage 5, 6, 8B, 9 and 10. Prevent a known Gate from being accidentally skipped.

B. `FIRST-FRAME BEAUTY + DIFFERENTIATION QA`
Before HG03, automatically reject a set when it is semantically correct but aesthetically utilitarian, repetitive in scale/composition, or wardrobe/world incoherent.

C. `ACTUAL-FIRST-FRAME > PLAN`
Write this explicitly into Stage 6: accepted image pixels/K0 state are authoritative for I2V.

D. `PROMPT CONTROL HIERARCHY PROMOTION`
Promote cross-song-stable items into `rules/ai_video.md`:
`HARD FREEZE -> FRAME-0 -> STATIC BASE -> ONE EVENT -> BOUND -> PHASES -> CAMERA -> RESIDUE -> SETTLED END STATE -> SOUND -> AVOID`.

E. `PACKAGING CONTRACT`
Lock account-level cover family and distinguish final Douyin caption from internal project title so consecutive posts look like one account system.

F. `STATE SYNC`
One post-publish operation updates slot state + tracker + data checkpoint status. Do not allow published posts to remain `READY_TO_PUBLISH` in durable state.

---

## Final maturity assessment

### Can it reliably make another MV?
`YES`.

### Can it reproduce different durations / segment counts / visual worlds?
`YES`, formally demonstrated from ~16s / 4 segments through ~37s / 9 segments.

### Is the technical finishing path stable?
`YES / HIGH CONFIDENCE`.

### Is dynamic-video generation meaningfully more stable than earlier rounds?
`YES`. D01-B provides cross-song evidence, especially for one-event bounded prompts and local-regeneration policy.

### Is Director / first-frame production fully stabilized?
`NO`. It is currently the largest remaining creative-production variance and the main threat to 2/day throughput.

### Is zero-context unattended automation proven?
`NO`. Current Runtime supports new-chat reuse, but Codex engineering reproduction remains unexecuted at C00.

### Is 2/day sustained throughput proven?
`NO`. This remains the next operational experiment.

### Is current low-view performance evidence enough to change production strategy?
`NO`. Production correctness and account distribution are separate hypotheses; early post data must accumulate before promotion/rejection of packaging or content rules.

Overall maturity:
`PRODUCTION PIPELINE = BETA-STABLE / HUMAN-CREATIVE-IN-THE-LOOP`

Recommended next state after hardening:
`D02 production should start from the same single path, not a new workflow.`
