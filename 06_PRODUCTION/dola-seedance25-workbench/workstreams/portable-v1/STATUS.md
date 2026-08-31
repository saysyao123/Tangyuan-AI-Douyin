# STATUS — Portable V1

Updated: 2026-08-31
Branch: `work/dola-portable-v1`

## Current phase

`F2 — ACCOUNT REGISTRY / WORKER SCHEDULER FOUNDATION` — UNIT/SIMULATION PASS

## Completed

- [x] Requirements interview completed and product contract locked.
- [x] Dedicated branch created.
- [x] Dedicated record path created; new workstream notes remain separate from historical evidence/logs.
- [x] Initial code audit completed; reuse/refactor/new-build areas identified.
- [x] Portable `app/runtime/data` layout + Electron bootstrap added.
- [x] Hard-coded developer artifact default overridden by portable data root.
- [x] Durable ProjectStore, project/shot/revision identity and strong idempotency added.
- [x] I2V local absolute-path staging and project output reservation added.
- [x] `PROJECT_COMPLETE` calculation and project/job HTTP + CLI contract added.
- [x] Dynamic durable AccountRegistry added under `data/accounts/registry.json`.
- [x] Existing POC account metadata can be mirrored/imported into the registry without hard-coded A/B/C assumptions.
- [x] Manual PAUSED / RESTRICTED state is preserved across legacy metadata refresh.
- [x] Account health model exposes login state, quota, entitlement, 5s/10s/30s capability state and schedulability reason.
- [x] Per-account generation lease rule added: one active generation lease per account.
- [x] Global worker semaphore added; default max workers = 3, configurable 1-20.
- [x] Forced-account scheduling is strict: unavailable forced account is not silently replaced.
- [x] Auto-assignment only considers enabled, READY, non-restricted accounts.
- [x] Idle worker state + lazy eviction policy foundation added.
- [x] Debug-account promotion state added.
- [x] Worker settings persist under portable `data/state/worker-settings.json`.
- [x] Control Plane routes added for account health, pause/resume/debug and worker status/config/sweep.
- [x] CLI commands added for the same F2 controls.
- [x] Windows GitHub Actions run #30 completed successfully with F0/F1/F2 syntax, unit and Control Plane integration checks.

## Important F2 boundary

The F2 scheduler policy is currently a **control/runtime foundation**. Its lease, semaphore and idle-eviction behavior is tested, but it is not yet wired to create/destroy the real Dola hidden BrowserWindow slots. That real binding is intentionally deferred to F4/F5 so the monolithic `background-dola.js` is not modified before the provider lifecycle is decomposed.

Therefore:

- F2 unit/simulation Gate: PASS.
- Real G2 two-account concurrent Dola generation: NOT YET TESTED.
- No claim is made that 3 real Dola generations can already run concurrently.

## Next engineering slice

`F3 — Vault facade + portable profile lifecycle`

Planned next:

- [ ] vault LOCKED / UNLOCKING / UNLOCKED / RESEAL_REQUIRED state machine;
- [ ] password-derived in-memory master key + authenticated encryption;
- [ ] encrypted per-account profile packages/index;
- [ ] controlled `runtime/unlocked-profiles/` working area;
- [ ] abnormal-shutdown recovery marker;
- [ ] reseal hooks for worker sleep / app exit;
- [ ] Codex-visible vault state without exposing password/key/profile secrets;
- [ ] migration/backup hooks.

After F3 foundation, proceed to F4 provider decomposition and F5 recoverable result lifecycle.

## Highest current technical risk

`P0: recoverable Dola result lifecycle` — current background runner can submit successfully but may fail after a fixed observation window when final media identity is delivered later or through a different conversation/result path. This remains the highest real-generation risk and must be solved before G1 can pass.

## Real-world Gates

- G1 one-account end-to-end: NOT_READY.
- G2 two-account isolation/parallel: NOT_READY.
- G5 scheduler/batch: NOT_READY.
- G20 pooled operation: NOT_READY.
- 30s: EXPERIMENTAL / NOT_REVERIFIED.

## Evidence discipline

No real Windows/Dola capability is marked PASS merely because code exists. Real session-dependent Gates require user-side Windows evidence.
