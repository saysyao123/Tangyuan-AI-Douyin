# CODE AUDIT — 2026-08-31

Scope: existing `06_PRODUCTION/dola-seedance25-workbench` as inherited by branch `work/dola-portable-v1`.

This audit separates what is reusable from what must be refactored or newly built for Portable V1. It does not mark Windows/Dola behavior PASS without real evidence.

## A. Directly reusable foundations

### A1. Electron account isolation model — REUSE

Existing architecture already uses an account-specific persistent partition (`persist:dola_<accountId>`) and account-specific Electron WebContents/BrowserWindow runtime. This matches the required session-isolation direction.

Relevant code/docs:

- `control-plane/apps/desktop/src/main.js`
- `control-plane/apps/desktop/src/background-dola.js`
- `control-plane/docs/MULTI_ACCOUNT_DESKTOP_ARCHITECTURE.md`

Keep the account ID → partition binding stable. Strengthen validation and worker lifecycle around it rather than replacing it with multiple ordinary tabs.

### A2. Loopback Control Plane + JSON CLI contract — REUSE / EXTEND

Existing server already:

- binds only `127.0.0.1` on an ephemeral port;
- generates a random bearer token per run;
- exposes account/provider/task endpoints;
- has JSON-oriented CLI semantics documented for Codex.

Relevant code/docs:

- `control-plane/apps/desktop/src/control-server.js`
- `control-plane/docs/CODEX_CONTROL_PLANE.md`

The `/v1` contract should remain compatible while V2-style resources (projects/workers/outputs/vault state) are added.

### A3. Real Dola UI driving — REUSE / HARDEN

`background-dola.js` already contains an observation-first Electron implementation for navigating a logged-in Dola partition, detecting visible creator controls, choosing model/duration/ratio, uploading a local reference image through the actual file input, filling the visible prompt editor, and clicking the visible submit control.

This aligns with the locked V1 rule: real Dola Web UI drives submission; observed internal requests are not promoted to a private submission API.

### A4. Network observation and media-identity extraction — REUSE / SPLIT

The background runner already arms CDP `Network` before submit and extracts evidence for conversation/message IDs, task/generation IDs, `vid`, `node_id` / media key, `fallback_api`, `key_seed`, `video_list`, `original_media_info`, `media_info`, and `main_url`.

This is valuable and should become a dedicated lifecycle observer instead of remaining embedded in one large runner.

### A5. Python resolver — REUSE / INTEGRATE

The separate `resolver/` package already contains capture/discovery/download/production/QA code and tests. Previous project evidence records a successful chain from observed media identity to a real MP4. Portable V1 should integrate this resolver behind a stable local adapter instead of reimplementing ranking/download logic in the UI runner.

## B. Existing implementation that conflicts with Portable V1

### B1. Storage paths are not portable — MUST REFACTOR FIRST

Current `main.js` stores `accounts.json` and `tasks.json` under Electron `app.getPath('userData')`, while `backgroundArtifactRoot()` defaults to a hard-coded developer drive path.

Portable V1 requires a deterministic program/data split under a configurable portable data root. No production path may depend on a developer-specific drive.

### B2. Background runner is globally serialized — MUST REFACTOR

`DolaBackgroundRunner.run()` currently uses one global `queueTail`, intentionally serializing every task across every account.

Portable V1 requires max one generation per account, different accounts may run in parallel, and a configurable global active worker limit with default 3.

Replace the single queue tail with a scheduler + per-account mutex/lease + worker pool semaphore.

### B3. All opened account slots remain resident — MUST REFACTOR

`ensureSlot()` caches account BrowserWindows in `slots` until process close. There is no idle eviction, wake/sleep policy, or max active-worker pool.

Portable V1 needs lazy wake, configurable active pool, visible-debug promotion, and idle release while preserving persistent profile data.

### B4. Result lifecycle ends too early — P0 GAP

Current `waitForGeneration()` mainly waits up to `DEFAULT_WAIT_SECONDS=180` for a media identity to appear in responses already observed by the active page. On timeout it fails the task with `background generation timed out before media identity was captured`.

This directly matches the latest known failure mode: Dola acknowledged a generation request, but the final media identity was not observed in the 180-second capture window.

Portable V1 needs a recoverable lifecycle state machine that distinguishes `submitted/agent_ack → accepted/provider-created → generating → result-delivered → media-resolved` and persists conversation/message binding. It must continue observation through bounded conversation-chain polling/reconnect/page-refresh paths instead of treating one missing response as generation failure.

### B5. No durable restart recovery — MUST ADD

Current task JSON records basic state, but application restart does not reconstruct active generation observers or resume resolving/downloading the same server-side task.

Portable V1 must recover original tasks after restart/unlock and must not submit again unless the generation is confirmed failed and a new revision is explicitly requested.

### B6. Task schema has no project/shot/revision/idempotency — MUST ADD

Current tasks are random-ID records that require `accountId` at creation time. There is no project, shot ID, revision, idempotency key, input staging manifest, auto account selection, or project completion state.

These are core V1 requirements.

### B7. Provider model does not match final V1 surface — REFACTOR COMPATIBLY

Current providers include `dola-web` (dispatch blocked by D2), `dola-web-background` (experimental background provider), and planned `byteplus-seedance`.

Portable V1 should expose one production-facing `dola-web` provider whose execution mode can be background or visible debug. The experimental background provider ID may remain as a compatibility alias during migration, but should not become a second product concept.

V1 production scope is Dola only. Official API adapters remain future abstractions.

### B8. No integrated highest-quality download pipeline — P0 GAP

Current background success can stop at `generationIdentity`; it does not complete the locked V1 chain to project output.

Portable V1 must integrate: explicit Dola page download candidate when present; normal lifecycle-returned media candidates; existing resolver identity chain; candidate technical ranking; actual download + lightweight media validation; output staging/atomic rename/project archive.

### B9. Raw response persistence needs stricter separation — MUST HARDEN

`captureBody()` can persist response bodies under job artifacts. This may be useful for local debugging, but Portable V1 requires no raw secrets in Git, no secrets in Codex-readable state/audit files, redacted durable event/state as the normal path, and any raw capture mode explicitly local/debug-only and excluded from portable exports by default.

### B10. No vault implementation — MUST ADD

The existing project relies on Chromium persistent profiles but has no password-based portable vault. Portable V1 requires manual once-per-run unlock.

Important feasibility constraint: copying Chromium profile data across Windows machines may still trigger legitimate re-authentication because Chromium/service security material can be OS/device-bound. The product promise is therefore **portable encrypted profile storage with best-effort session continuity**, not guaranteed login continuity across machines.

Recommended V1 vault shape:

- encrypted profile archives/data at rest;
- after user unlock, materialize only the required account profile into a controlled runtime working area;
- on account sleep/process exit, sync/reseal;
- on abnormal shutdown, detect leftover unlocked workspace at next start and require explicit recovery/reseal before use;
- Codex receives only `LOCKED/UNLOCKED`, never the master password or profile secret files.

A future hardened build may replace this with a mounted encrypted container; do not pretend the first portable implementation has stronger at-rest guarantees than it actually does.

### B11. No full localhost Web Workbench — MUST ADD

Current Electron renderer provides desktop UI, but the locked V1 product also requires a complete browser-based localhost workbench sharing the same core as Codex.

Do not build a second independent task engine. The web UI must be a client of the same control/state layer.

### B12. Health endpoint does not expose required runtime state — EXTEND

Current unauthenticated `/health` reports basic service/gate status. V1 needs safe high-level status such as service version, vault locked/unlocked, accounts registered/ready, worker active/max, queue count, and recovery required. Sensitive detail remains behind auth.

## C. Recommended module boundary after refactor

```text
apps/desktop
  Electron shell + visible login/debug windows
apps/web
  localhost browser workbench
apps/cli
  Codex JSON CLI

core/
  paths + data versioning
  account registry
  vault facade
  projects/jobs/idempotency
  scheduler/worker leases
  event/audit store
  recovery coordinator

providers/dola-web/
  ui adapter
  account session runtime
  lifecycle observer
  conversation/result observer
  provider capability/health adapter

resolver/
  existing Python discovery/ranking/download logic
  exposed through a stable local command/adapter
```

The current JavaScript POC can be incrementally decomposed; a full TypeScript rewrite is not required before Gate 1.

## D. Priority order

### P0 — required before real single-account V1 Gate

1. Portable path/data-root foundation; remove hard-coded developer path.
2. Durable project/job schema + strong idempotency.
3. Recoverable Dola lifecycle observer beyond one 180s capture window.
4. Resolver/download integration to actual output file.
5. Account-bound recovery after process restart.

### P1 — required before 2/5-account Gate

6. Per-account lease + global configurable worker pool.
7. Lazy slot wake/sleep/idle eviction.
8. Auto scheduling + force-account override.
9. machine-readable state snapshots + project completion event.
10. full localhost Web Workbench.

### P2 — required before Portable V1 release

11. password vault and portable profile materialization/reseal flow.
12. data migration/backups/rollback.
13. portable packaging/runtime bundling.
14. startup integration and user-facing recovery UX.
15. 20-account sustained-operation validation.

## E. What is NOT being claimed by this audit

- Existing D0/D1 Windows behavior is not re-declared PASS.
- Current new-generation lifecycle is not declared fixed.
- Current highest-quality media download is not declared integrated.
- 5s/10s/30s account capacity is not inferred from UI text.
- Cross-machine session continuity is not guaranteed.
- 20-account operation is not claimed until real staged Gates pass.
