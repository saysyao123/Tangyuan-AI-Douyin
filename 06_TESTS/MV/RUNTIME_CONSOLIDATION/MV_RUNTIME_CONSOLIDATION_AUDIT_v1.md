# MV Runtime Consolidation Audit v1

> Branch: `refactor/mv-runtime-consolidation-v2`
> Scope: R1 -> WEB R2 -> WEB R3 / 30D60
> Goal: turn the existing MV method into one reusable, closed-loop, stage-enforced production runtime where a later stage cannot become valid unless all required upstream artifacts and checks exist.

## 1. Executive conclusion

The repository already has a strong **designed process**, but the actual production loop is not yet equally strong at **execution enforcement**.

The main defect is not lack of rules. It is that rules, states and required artifacts are still too easy to satisfy by prose or manual status updates instead of machine-verifiable stage completion.

Current condition:

`METHOD COMPLETE -> RUNTIME PARTIALLY ENFORCED -> EXECUTION CAN DRIFT`

Target condition:

`ONE STATE MACHINE -> ONE ARTIFACT CONTRACT -> MACHINE ENTRY/EXIT GATES -> HUMAN AESTHETIC GATES -> DURABLE RECEIPTS -> POST-PUBLISH CLOSED LOOP`

No future MV should advance merely because the conversation has moved on.

---

## 2. Evidence from completed rounds

### R2
R2 is the strongest closed-loop historical Golden source. It demonstrated that a long-form run can be closed with durable evidence and later treated as regression-only history.

### D01-B
D01-B is currently the best 30D/60 execution specimen. Its slot directory contains durable artifacts including:
- Audio Timeline Package;
- Director Beat Map;
- Director Plan v1/v2;
- Video Set QA;
- Picture Edit Plan;
- WEB Source Rough-Cut map/QA;
- Subtitle Implementation QA;
- Final Tech QA;
- HG04 receipt;
- HG05 receipt;
- Publish Package.

It is not perfect, but it demonstrates the desired principle: each major stage leaves inspectable state.

### D02-A
D02-A produced a publishable result and reached `HG05_PASS / RELEASE_READY`, but its durable directory is incomplete relative to the current Golden Runtime state chain.

Present durable artifacts include:
- BGM discovery / HG01 / HG02;
- Audio Timeline Package;
- Natural Beat;
- WEB Source Rough-Cut map/QA;
- Subtitle implementation data;
- Final render receipt;
- Release package;
- final CURRENT_STATE.

Missing as distinct durable stage artifacts include at least:
- canonical `DIRECTOR_PLAN`;
- first-frame design/prompt set + HG03 receipt;
- stage-entry receipts for Stage 5/6/8B/9/10;
- canonical `DYNAMIC_PROMPT_SET`;
- canonical `VISUAL_SOURCE_MAP`;
- canonical `NORMALIZED_SHOT_LIBRARY_MAP` when normalization is required;
- canonical `EDITOR_AUDIO_GATE` receipt;
- canonical `EDIT_MAP` / Picture Edit Plan;
- HG04 Picture Edit PASS receipt;
- Subtitle Implementation QA receipt separate from implementation data;
- Final Tech QA receipt separate from generic final-render receipt;
- HG05 PASS receipt.

The final state was therefore able to jump across several states that the Golden Runtime declares mandatory.

This is the clearest current proof that **state progression is not coupled strongly enough to artifact existence**.

---

## 3. Root causes

### RC-01 | Stage rules are prose-enforced, not machine-enforced
`mv_stage_entry_checklist.md` correctly defines prerequisites, but most stages do not have an executable validator equivalent to the Audio Timeline final gate.

Result: an agent can know the rule and still skip it.

### RC-02 | State can be manually promoted without validating evidence
A `CURRENT_STATE` update can currently claim a late status without a machine checking the full required upstream chain.

Result: status truth can diverge from artifact truth.

### RC-03 | Artifact naming is not fully canonical
Different rounds use different names for similar evidence (`PICTURE_EDIT_PLAN`, `EDIT_MAP`, generic final receipts, etc.).

Result: a validator cannot reliably determine whether a stage is complete without round-specific knowledge.

### RC-04 | Human Gate PASS is not always materialized as a receipt
Conversation approval is sometimes treated as enough.

Result: a new chat can know a final state but cannot reconstruct exactly what the user approved and what machine QA preceded it.

### RC-05 | External media assets are not represented by a complete durable manifest
Images/videos may exist only in conversation/container history while the repo retains only later summaries.

Result: zero-context reproduction cannot audit actual source identity, K0 choice, video generation set or edit inputs.

### RC-06 | Multiple state layers are conceptually valid but operationally ambiguous
There are account/root states, per-round states, per-slot states and tracker rows. This is useful, but update ownership is not fully transactional.

Result: one layer can advance while another remains stale.

### RC-07 | Workflow maturity and creative R&D are mixed during production
A real production MV can become the place where director aesthetics, face route, prompt-control changes and packaging ideas are all being invented at once.

Result: high-value experiments succeed, but the required stage artifacts are sometimes bypassed in order to keep creative momentum.

### RC-08 | “Done in conversation” is still sometimes treated as “done in runtime”
The current system strongly externalizes state in principle, but production behavior still occasionally relies on chat continuity.

Result: new-chat recovery depends on summaries rather than only durable repository truth.

---

## 4. Core design decision for Runtime v2

Do **not** create a larger monolithic SOP.

Keep the current JIT architecture, but add one enforceable layer:

`MV STATE MACHINE + STAGE CONTRACT REGISTRY + ARTIFACT MANIFEST + VALIDATOR`

The existing Workflow / Rule / Template / Knowledge separation remains correct.

Runtime v2 must make invalid transitions impossible to certify.

---

## 5. Canonical lifecycle

Proposed single lifecycle:

`S00_SLOT_CREATED`
-> `S01_HG01_SONG_LOCKED`
-> `S02_BGM_VERSION_VERIFIED`
-> `S03_HG02_BGM_LOCKED`
-> `S04_AUDIO_TIMELINE_LOCKED`
-> `S05_BEAT_MAP_LOCKED`
-> `S06_AESTHETIC_DIRECTION_LOCKED`
-> `S07_DIRECTOR_PLAN_LOCKED`
-> `S08_HG03_FIRST_FRAMES_LOCKED`
-> `S09_DYNAMIC_PROMPTS_LOCKED`
-> `S10_DYNAMIC_SOURCE_QA_LOCKED`
-> `S11_SHOT_LIBRARY_READY`
-> `S12_WEB_SOURCE_ROUGH_CUT_PASS`
-> `S13_EDITOR_AUDIO_GATE_PASS`
-> `S14_EDIT_MAP_LOCKED`
-> `S15_HG04_PICTURE_EDIT_PASS`
-> `S16_SUBTITLE_QA_PASS`
-> `S17_FINAL_TECH_QA_PASS`
-> `S18_HG05_COMPLETE_LOCKED`
-> `S19_RELEASE_PACKAGE_READY`
-> `S20_PUBLISHED`
-> `S21_POST_PUBLISH_DATA_ACTIVE`
-> `S22_REVIEW_CLOSED / KNOWLEDGE_PROMOTED`

`S06_AESTHETIC_DIRECTION_LOCKED` is new and should be validated in the next MV before promotion to universal HARD. It addresses the remaining Director / first-frame aesthetic variance.

---

## 6. Every stage must have the same contract shape

Each stage must define:

1. `stage_id`
2. `purpose`
3. `required_upstream_states`
4. `required_input_artifacts`
5. `work`
6. `machine_checks`
7. `human_gate` if any
8. `required_output_artifacts`
9. `exit_state`
10. `rollback_target`
11. `invalidated_by`
12. `next_allowed_states`

A stage is complete only when:

`REQUIRED ARTIFACTS EXIST + MACHINE CHECK PASS + HUMAN GATE PASS IF REQUIRED + STATE TRANSITION VALIDATED`

---

## 7. Canonical per-slot artifact layout

Proposed future slot structure:

```text
<slot>/
  00_STATE/
    CURRENT_STATE.json
    STAGE_LEDGER.jsonl
    ARTIFACT_MANIFEST.json
  01_SONG/
    HG01_CANDIDATE_EVIDENCE.md
    HG01_PASS_RECEIPT.md
  02_BGM/
    BGM_DISCOVERY/
    HG02_LISTENING_PACK.md
    HG02_PASS_RECEIPT.md
  03_AUDIO_TIMELINE/
    AUDIO_TIMELINE_PACKAGE/
    AUDIO_TIMELINE_GATE_RECEIPT.json
  04_BEATS/
    NATURAL_BEAT.md
  05_AESTHETIC/
    AESTHETIC_THESIS.md
    VISUAL_DNA.json
    REFERENCE_PACK.md
    PREVIS_MATRIX.md
  06_DIRECTOR/
    DIRECTOR_PLAN.md
    MATERIAL_AUDIT.md
    STAGE_ENTRY_PASS.json
  07_FIRST_FRAMES/
    FRAME_DESIGN_CARDS.md
    FIRST_FRAME_PROMPTS.md
    FIRST_FRAME_ASSET_MANIFEST.json
    FIRST_FRAME_MACHINE_QA.md
    HG03_PASS_RECEIPT.md
  08_DYNAMIC/
    DYNAMIC_PROMPT_SET.md
    DYNAMIC_SOURCE_ASSET_MANIFEST.json
    VISUAL_SOURCE_MAP.csv
    DYNAMIC_SOURCE_QA.md
  09_NORMALIZATION/
    NORMALIZED_SHOT_LIBRARY_MAP.csv
    WEB_SOURCE_ROUGH_CUT_MAP.csv
    WEB_SOURCE_ROUGH_CUT_QA.md
  10_EDIT/
    EDITOR_AUDIO_GATE_RECEIPT.json
    EDIT_MAP.csv
    PICTURE_EDIT_MACHINE_QA.md
    HG04_PASS_RECEIPT.md
  11_SUBTITLE/
    SUBTITLE_IMPLEMENTATION.json
    SUBTITLE_IMPLEMENTATION_QA.md
  12_FINAL/
    FINAL_TECH_QA.md
    FINAL_ASSET_MANIFEST.json
    HG05_PASS_RECEIPT.md
  13_RELEASE/
    RELEASE_PACKAGE.md
    PUBLISH_RECEIPT.md
    POST_PUBLISH_METRICS.csv
    POST_PUBLISH_REVIEW.md
```

Physical media does not have to be committed to GitHub, but every external asset used in a locked stage must have a manifest identity: filename, role, source, duration/dimensions, hash when available, and durable reference/location.

---

## 8. Machine enforcement required

Build a single validator, e.g.:

`04_HARNESS/tools/mv_runtime/mv_runtime_gate.py`

Minimum commands:

```text
init-slot
validate-stage <stage>
advance <from> <to>
audit-slot
close-slot
post-publish-sync
```

Rules:
- `advance` fails if required artifacts are absent;
- `advance` fails if required machine QA receipt is not PASS;
- `advance` fails if a required Human Gate receipt does not exist;
- later states cannot be set manually without validator-generated transition evidence;
- `audit-slot` reports missing artifacts, stale state and tracker divergence;
- post-publish sync updates slot + tracker + program state as one operation or returns BLOCKED.

The Audio Timeline Final Gate is the model for this architecture.

---

## 9. Human Gate discipline

Keep exactly five default Human Gates.

But every Gate submission must be packaged as:

`MACHINE_QA_PASS + VIEWABLE_ARTIFACT + SINGLE USER DECISION + PASS RECEIPT`

A user reply in chat is not durable until a receipt is written.

The receipt must record:
- gate id;
- artifact identity/version;
- what user approved;
- known exceptions accepted by user;
- time/date if known;
- exact downstream state unlocked.

---

## 10. State ownership

Define three levels clearly:

### Slot State = production authority
The per-slot `CURRENT_STATE.json` is the authoritative state for that MV.

### Program Tracker = scheduling/index authority
`MV_30D_60_TRACKER.csv` mirrors summary status but cannot override slot state.

### Account / Root State = account strategy authority
Tracks account-level direction, not per-stage production detail.

Update direction:

`validated slot transition -> tracker sync -> account/program summary sync`

Never infer slot stage backwards from tracker prose.

---

## 11. Separation of production vs R&D

For every experiment introduced inside a production MV:
- production stage must still complete its required artifact contract;
- experiment gets a separate evidence receipt;
- experimental success does not silently rewrite the canonical workflow;
- promotion requires cross-song evidence where applicable.

This keeps creative discovery from breaking production bookkeeping.

---

## 12. Aesthetic layer integration

The new aesthetic work inspired by structured visual-reference systems should **not** be inserted as a huge style library into the core Skill.

Use JIT:

`Natural Beat -> Aesthetic Thesis / Visual DNA / Reference Pack -> Director Plan -> First Frames`

Aesthetic stage outputs should include:
- one-sentence Aesthetic Thesis;
- Visual DNA: palette, light, materials, optical character, texture, emotional register, signature motif;
- 3-5 focused reference cases with explicit `TAKE / DO NOT TAKE` notes;
- Parent / Mutation matrix;
- Director Previs Matrix;
- per-frame design cards.

This solves Director aesthetics without bloating the runtime context.

---

## 13. Migration policy

Do not rewrite R1/R2 history.

Use them as immutable evidence.

Migration steps:
1. define v2 stage registry;
2. define artifact registry;
3. implement validator;
4. map R2 and D01-B artifacts to v2 stages as regression fixtures;
5. run D02-A audit and record expected FAIL for missing stage artifacts;
6. create migration/backfill receipts where evidence genuinely exists;
7. never fabricate missing historical evidence;
8. update zero-context start prompt only after validator tests pass;
9. test one brand-new MV from `S00` using only durable repo state;
10. only then promote Runtime v2.

---

## 14. Definition of Done for this consolidation

Runtime consolidation is not complete until all of the following are proven:

- one canonical stage registry exists;
- one canonical artifact registry exists;
- slot state cannot legally skip a mandatory state;
- D02-A audit correctly flags historical missing artifacts;
- D01-B and R2 can be mapped as regression fixtures;
- new slot initialization is deterministic;
- five Human Gates generate durable receipts;
- stage entry/exit validation is executable;
- post-publish sync is executable;
- zero-context new chat can resume from slot state without conversation memory;
- a new real MV completes end-to-end using the v2 runtime without stage skipping.

Until the last item passes, status remains:

`RUNTIME_V2 = CANDIDATE / NOT PRODUCTION_DEFAULT`

---

## 15. Immediate next implementation order

P0. Canonical Stage Registry + Artifact Registry
P0. Runtime validator skeleton + audit-slot
P0. State transition receipts
P0. Gate receipt templates
P1. Canonical slot directory template + init-slot
P1. D01-B / D02-A regression fixtures
P1. Tracker/post-publish transactional sync
P1. Zero-context start prompt revision
P2. Aesthetic Director stage + frame design card
P2. Full new-MV end-to-end validation

The next coding task should therefore be **P0 Stage Registry + validator**, not another prose SOP rewrite.
