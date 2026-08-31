# IMPLEMENTATION PLAN — Portable V1

Status: ACTIVE
Branch: `work/dola-portable-v1`

## Principle

Incremental refactor. Preserve the existing `/v1` Codex API/CLI surface where practical. Every real Windows/Dola capability remains behind an evidence Gate.

## Phase F0 — Isolated workstream + portable foundation

Goal: make all new work separable from historical POC and remove developer-machine path assumptions.

Deliverables:

- dedicated workstream records under `workstreams/portable-v1/`;
- new branch `work/dola-portable-v1`;
- portable path module with deterministic `app/runtime/data` layout;
- schema/version marker for durable data;
- state snapshot root reserved;
- no hard-coded `D:\...` production path;
- compatibility migration for old `accounts.json` / `tasks.json` paths, read-only/import-first where possible.

Gate F0 PASS requires code review + automated tests where platform-independent. No Dola session claim.

## Phase F1 — Durable project/job model + idempotency

Goal: Codex/web can create either a single job or project batch without duplicate Dola submission.

Deliverables:

- project schema;
- job schema with `projectId`, `shotId`, `revision`, `idempotencyKey`;
- optional account assignment at create time;
- local absolute-path input staging;
- project output paths;
- terminal/project completion calculation;
- strong create-idempotency;
- explicit `new revision` flow;
- machine-readable state snapshots.

Gate F1 PASS: unit tests for duplicate create, new revision, project completion, absolute-path staging validation.

## Phase F2 — Account registry + worker scheduler

Goal: dynamic account pool (~20+) while only a configurable subset is active.

Deliverables:

- account registry independent of hard-coded A/B/C;
- per-account generation lease (max=1);
- global worker semaphore default=3 configurable;
- auto-select ready account + explicit account override;
- lazy wake/sleep/idle eviction;
- visible-debug promotion for a selected account;
- health/capability summary.

Gate F2 unit/simulation: no two concurrent jobs share one account; active worker count never exceeds configured max; forced-account obeyed.

Real 2-account isolation remains a later Windows Gate.

## Phase F3 — Vault facade + portable profile lifecycle

Goal: password-protected account/profile storage at rest, manual unlock once per run.

Deliverables:

- vault state machine: LOCKED / UNLOCKING / UNLOCKED / RESEAL_REQUIRED;
- password-based key derivation with authenticated encryption;
- encrypted per-account profile package/index;
- controlled unlocked profile working area;
- sync/reseal on worker sleep/exit;
- abnormal-shutdown recovery marker;
- Codex-visible state only, no password exposure;
- migration/backup hooks.

Important: cross-machine service session continuity is best-effort. Re-authentication may still be required.

Gate F3 PASS requires local crypto/state tests. Windows account-login behavior remains manual Gate.

## Phase F4 — Dola provider decomposition

Goal: keep real UI submission but split the monolithic background runner.

Modules:

- `DolaSessionRuntime` — account-bound BrowserWindow/WebContents;
- `DolaUiAdapter` — creator navigation/model/duration/ratio/input/prompt/submit;
- `DolaLifecycleObserver` — CDP/SSE/response events;
- `DolaConversationObserver` — recoverable post-submit result tracking;
- `DolaCapabilityObserver` — login/capability/quota/entitlement state;
- `DolaProvider` — stable submit/poll/recover contract.

Compatibility: old `dola-web-background` may temporarily map to new `dola-web` execution mode while CLI migrations are documented.

## Phase F5 — Recoverable generation lifecycle

Goal: eliminate the single 180s observation window as the definition of failure.

Persisted states:

`PREPARING → SUBMITTING → SUBMITTED → ACKNOWLEDGED → GENERATING → RESULT_OBSERVED → RESOLVING`

plus explicit `LOGIN_REQUIRED`, `PROVIDER_REJECTED`, `OBSERVATION_WAIT`, `RECOVERY_REQUIRED`, `FAILED`.

Deliverables:

- bind observed conversation/message identifiers to the job;
- bounded backoff observation/poll strategy;
- page/session wake and safe refresh/reconnect path;
- resume same job after app restart/unlock;
- do not resubmit merely because result observation timed out;
- clear evidence separating agent acknowledgement, provider creation, completion, and media delivery.

Gate F5 real Windows single-account test required.

## Phase F6 — Resolver/download integration

Goal: job reaches a real project output file.

Candidate priority:

1. explicit page download/original candidate;
2. normal lifecycle-returned candidates;
3. existing resolver identity chain.

Deliverables:

- stable Electron ↔ resolver adapter;
- candidate rank by technical quality/accessibility;
- download fallback;
- atomic output write;
- lightweight validation (valid media + actual duration/resolution/file size when available);
- output metadata saved to job/project state.

No mandatory visual watermark-frame QA in V1.

Gate F6 real Windows test: one generation → actual highest-quality accessible MP4 saved under project output.

## Phase F7 — Localhost Web Workbench

Goal: full human UI on the same core used by Codex.

Pages/features:

- unlock/start status;
- accounts + login/debug window + enable/pause;
- capability/health;
- projects/jobs;
- batch creation;
- queue/worker pool;
- recovery actions;
- outputs/logs;
- settings including max workers.

No separate web task database.

## Phase F8 — Codex V1 contract extension

Maintain old commands where practical and add:

- `vault status`;
- `accounts health`;
- `workers status`;
- `projects create/get/list`;
- `projects submit`;
- `tasks create` with project/shot/revision and optional account;
- `tasks retry --new-revision`;
- `tasks recover`;
- `outputs get/open`;
- machine-readable `PROJECT_COMPLETE`.

API and CLI continue to emit JSON for Codex.

## Phase F9 — Packaging / migration / startup

- portable Windows x64 bundle; no separate Node/Python install for normal use;
- app/runtime replaceable, data durable;
- migration backup + rollback;
- optional Windows startup entry while vault remains locked;
- Codex can start/stop service but not unlock.

## Real validation ladder

### G1 — 1 account

Manual login → restart persistence → Codex project/job submit → real Dola UI → lifecycle recovery → highest-quality accessible download.

### G2 — 2 accounts

- A/B cookie/session isolation;
- two simultaneous one-per-account jobs;
- no conversation/media/result cross-binding;
- forced account and auto scheduling both work.

### G5 — 5 accounts

Batch projects, pool scheduling, failure recovery, idle worker recycle, project completion.

### G20 — ~20 accounts

Sustained registration, default 3 active workers, configurable concurrency, state/log stability, no uncontrolled Chromium residency.

## 30s Gate

5s/10s are V1 stable targets. 30s remains `EXPERIMENTAL` until the current account's real Dola entitlement/UI path proves a complete submit/result/download lifecycle. Service refusal is recorded and not bypassed.