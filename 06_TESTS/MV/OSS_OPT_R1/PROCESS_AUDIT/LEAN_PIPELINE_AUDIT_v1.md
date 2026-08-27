# MV Runtime｜Lean Pipeline Deep Audit v1

Status: `RECOMMEND PROCESS COMPRESSION / KEEP CORRECTNESS`  
Date: `2026-08-28`  
Evidence baseline: `OSS_OPT_R1 / D02-B / S16 RELEASE_READY`

## 1. Executive conclusion

The D02-B experiment proved that the current Canonical Runtime is strong at correctness, rollback, durable evidence and zero-context state recovery, but it also exposed a production-efficiency problem:

**Canonical evidence granularity and operator workflow granularity are currently too tightly coupled.**

The system has 19 canonical stages (S00-S18). This is acceptable as an internal evidence/state graph, but it should not mean 19 visible production steps, repeated full-context reads, or a separate external Bridge round-trip for every machine-only transition.

The target architecture should become:

`fine-grained evidence internally + coarse-grained production phases externally`.

Keep the five fixed Human Gates. Compress machine-only stages into automatic runs between Gates. Preserve per-stage artifacts and transition receipts only where they protect rollback/reproducibility.

## 2. What actually caused slowness

### A. Transport/state round-trip overhead

The D02-B test repeatedly used:

`write artifact -> RESUME -> obtain guard -> ADVANCE -> wait Bridge -> RESUME next stage`.

This is safe but inefficient for machine-only stages. Many of those round-trips do not add a human decision or new external evidence boundary.

Recommendation:
- add a controller-level `RUN_UNTIL_GATE_OR_BLOCK` candidate;
- internally preserve each stage validation/transition receipt;
- externally return only when a Human Gate, external capability handoff, or real BLOCK is reached.

### B. Human Gate record/advance is two transport calls

Current semantics correctly separate `RECORD_HUMAN_GATE` and `ADVANCE`. Keep the two-phase internal audit semantics, but expose one transactional command such as `ACCEPT_GATE` that:
1. records the Human Gate receipt;
2. refreshes guard internally;
3. advances only if the receipt validates;
4. returns the next stage/next action.

This halves normal Gate transport calls without weakening evidence.

### C. Startup context is too heavy

Current new-chat startup asks the agent to read nine Runtime/router files before real work. Executor-First is correct, but the Controller should resolve most of this internally.

Lean target:
- startup reads no more than Tracker/account identity plus one Runtime entrypoint/RESUME result;
- RESUME response directly includes resolved `executor_id`, execution class, JIT paths and block reason;
- the agent does not load full Stage Registry / Executor Registry / MANIFEST unless debugging or explicitly needed.

### D. Registry/checklist duplication

Current information is repeated across:
- `mv_stage_registry.json`;
- `mv_resume_contract.json`;
- `mv_stage_executor_registry.json`;
- `mv_stage_entry_checklist.md`;
- `mv_human_gates.md`;
- `MANIFEST.md`;
- startup prompt.

The concepts are useful, but overlapping stage-specific details increase maintenance cost and context size.

Recommended authority split:
- Stage prerequisites/evidence: `mv_stage_registry.json` only;
- HOW/executor/dependency policy: executor registry only;
- Human decision UX: `mv_human_gates.md` only;
- startup: thin router only;
- stage-entry checklist: generic invariants only, no large duplicated per-stage rules;
- `mv_resume_contract`: next-action routing only, ideally derived/validated against Stage + Executor registries.

## 3. Stage-by-stage necessity audit

| Current stage | Value | Recommendation | Reason |
|---|---|---|---|
| S00 SLOT_CREATED | HIGH | KEEP | slot identity / lane / state root is foundational |
| S01 HG01 SONG_LOCKED | HIGH | KEEP | true human aesthetic authority |
| S02 HG02 BGM_LOCKED | HIGH | KEEP | exact audio/clip changes invalidate all timing downstream |
| S03 AUDIO_TIMELINE_LOCKED | VERY HIGH | KEEP HARD | single timing truth is foundational |
| S04 NATURAL_BEAT_LOCKED | MEDIUM | KEEP ARTIFACT, REMOVE AS VISIBLE STEP | useful semantic bridge, but can be generated automatically as Director input |
| S05 DIRECTOR_PLAN_LOCKED | HIGH | KEEP ARTIFACT/ROLLBACK POINT, AUTO-CHAIN | important creative authority but no default Human Gate |
| S06 HG03 FIRST_FRAMES_LOCKED | VERY HIGH | KEEP | major visual/aesthetic approval boundary |
| S07 DYNAMIC_PROMPT_SET_READY | HIGH | KEEP RESUMABLE HANDOFF | external video generation creates a real pause/handoff boundary |
| S08 DYNAMIC_SOURCE_QA_LOCKED | VERY HIGH | KEEP | decides PASS/TRIM/REGEN and source eligibility |
| S09 SOURCE_NORMALIZATION_READY | MEDIUM | CONDITIONAL + AUTO | required only when multi-shot / WEB cleaning / proxy normalization is actually needed |
| S10 EDITOR_AUDIO_GATE_PASS | LOW AS STANDALONE STAGE | MERGE INTO EDIT ENTRY INVARIANT | if BGM hash is unchanged, full separate stage adds little; block only on mismatch |
| S11 EDIT_MAP_LOCKED | HIGH ARTIFACT, LOW AS EXTERNAL STEP | AUTO-BUILD + RENDER PREVIEW | rollback value exists, but no reason to externally pause before HG04 |
| S12 HG04 PICTURE_EDIT_PASS | VERY HIGH | KEEP | human rhythm/director judgment is irreplaceable |
| S13 SUBTITLE_IMPLEMENTATION_QA_PASS | MEDIUM | KEEP QA ARTIFACT, AUTO-CHAIN | deterministic implementation; surface only on failure |
| S14 FINAL_TECH_QA_PASS | HIGH | KEEP MACHINE GATE, AUTO-CHAIN TO HG05 | protects delivery correctness; no separate user wait needed |
| S15 HG05 FINAL_ACCEPTANCE_PASS | VERY HIGH | KEEP | final human authority |
| S16 RELEASE_PACKAGE_READY | HIGH | KEEP END-OF-PRODUCTION STATE | clean publish-ready boundary |
| S17 PUBLISHED_DATA_COLLECTION_ACTIVE | HIGH | KEEP SEPARATE REAL-WORLD STATE | must depend on actual publication |
| S18 POST_PUBLISH_REVIEWED | HIGH | KEEP | closes the learning loop |

Net conclusion:
- five Human Gates remain correct;
- several machine stages remain valuable as artifacts/invariants but should no longer feel like separate workflow steps;
- S10 is the clearest candidate for standalone-stage removal;
- S04/S09/S11/S13 should be operationally compressed even if evidence remains durable.

## 4. Recommended macro production flow

The production experience should be approximately eight macro phases, not nineteen visible steps:

### P0｜Start / Allocate
Slot allocation + Runtime resume.

### P1｜Song + BGM
HG01 -> exact BGM discovery -> HG02.

### P2｜Audio Truth
Audio Timeline -> automatic Natural Beat derivation.

### P3｜Director + First Frames
Director Thesis/Plan -> First Frames -> machine QA -> HG03.

### P4｜Dynamic Source Production
Dynamic prompts -> external generation -> source QA -> conditional atomization/normalization.

### P5｜Picture Edit
Audio identity invariant -> Edit Map -> preview render/QA -> HG04.

### P6｜Finish
Subtitles -> Final Tech QA -> HG05.

### P7｜Release
Release package -> S16. Publishing remains a separate real-world transaction.

## 5. Human Gates audit

The current five-gate design is substantially correct and should not be reduced yet:

- HG01 Song: KEEP;
- HG02 BGM listening: KEEP;
- HG03 First-frame visual direction: KEEP;
- HG04 Picture rhythm: KEEP;
- HG05 Final acceptance: KEEP.

However, the user should experience exactly these five normal decision points. Technical checks between them should not appear as extra approvals.

Conditional Gates remain exception-only.

## 6. Audio Timeline simplification

The experiment validated a simpler route:

`P0 same-version timed lyric -> P1 lightweight Faster-Whisper -> P2 Xingyu fallback`.

Important efficiency rules:
- stop at first route that passes;
- no default second-model verification;
- no repeated lyric evidence hunt after one audited trusted-text pass;
- no per-song model installation;
- P2 heavy alignment only on concrete failure.

This is a strong candidate for stable promotion.

## 7. Creative workflow simplification

The OSS Director layer added value, but should remain a compact knowledge overlay rather than another heavy stage hierarchy.

Keep only seven portable ideas:
1. Director Thesis;
2. Primary Visual Engine;
3. explicit audiovisual relationship;
4. motive-first camera-subject-space reasoning;
5. WHY CUT HERE;
6. optional-element stop conditions;
7. Creative Drift QA.

Do not import H3 container, four-panel or RunningHub execution contracts.

## 8. Repository / Git history hygiene

The experiment branch is intentionally noisy. Compared with the stable R3 branch, it contains hundreds of experiment commits and many immutable Bridge request/response files.

Future production should distinguish:

### Canonical durable evidence that belongs with the slot
- CURRENT_STATE;
- transition/context/revision receipts;
- Human Gate receipts;
- authoritative production artifacts;
- final/release identity.

### Transport/debug evidence that should not pollute the content branch indefinitely
- read-only RESUME request/response pairs;
- repeated probe retries;
- experiment-only executor requests;
- transient environment request retries.

Recommendation:
- mutation receipts remain in canonical slot history;
- read-only RESUME transport logs move to a compact audit ledger / separate runtime-log branch or retained CI artifact policy;
- do not require one repository commit for every read-only state query.

## 9. Workflow file hygiene

OSS_OPT_R1 added multiple Audio Timeline workflows for bootstrap, environment, executor, finalizer and tests. This was useful during R&D but should not all become permanent top-level workflows.

Promotion target should consolidate them into approximately:
- one reusable/on-demand Audio Timeline execution workflow with modes (`doctor/align/finalize`), or one executor + one environment setup workflow;
- one combined Audio Timeline regression workflow;
- retain HG01 delivery guard tests if they protect a proven failure mode.

Do not promote test-probe workflows whose only purpose was diagnosing D02-B.

## 10. Final recommendation

Do **not** simplify by deleting correctness checks first.

Simplify in this order:
1. compress transport round-trips;
2. reduce startup/JIT reads;
3. remove duplicated rule text;
4. make normalization conditional;
5. merge Editor Audio Gate into Edit entry invariant;
6. auto-chain subtitle/final QA;
7. only after another real MV proves equivalence, consider reducing the canonical Stage schema itself.

The next experiment should therefore test **interaction compression without immediately destroying evidence granularity**.
