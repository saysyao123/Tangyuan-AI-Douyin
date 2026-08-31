# STATUS — Portable V1

Updated: 2026-08-31
Branch: `work/dola-portable-v1`

## Current phase

`F1 — DURABLE PROJECT/JOB/IDEMPOTENCY FOUNDATION` (first slice PASS)

## Completed

- [x] Requirements interview completed and product contract locked.
- [x] Dedicated branch created.
- [x] Dedicated record path created; no new workstream notes are mixed into historical evidence/logs.
- [x] Initial code audit completed.
- [x] Reuse/refactor/new-build areas identified.
- [x] Implementation Gates defined.
- [x] Portable path/data-root module added.
- [x] Electron portable bootstrap added and set as desktop entrypoint.
- [x] Existing hard-coded Dola artifact default is overridden by portable bootstrap before `main.js` loads.
- [x] Durable `data/` and ephemeral `runtime/` roots reserved with a versioned layout marker.
- [x] Dev portable runtime is Git-ignored.
- [x] Isolated Windows GitHub Actions check added.
- [x] Windows CI portable foundation PASS.
- [x] Durable `ProjectStore` added.
- [x] project + shot + revision deterministic job identity added.
- [x] Strong create idempotency and explicit new-revision flow added.
- [x] I2V absolute local input staging added.
- [x] Project output path reservation and `PROJECT_COMPLETE` calculation added.
- [x] Portable project/job HTTP routes added alongside legacy `/v1/tasks` routes.
- [x] Portable CLI discovery fixed for portable/dev roots.
- [x] CLI `projects` / `jobs` commands added.
- [x] Windows CI run #15 passed project-store + project Control Plane integration checks.

## In progress / next engineering slice

- [ ] Compatibility/import behavior for existing AppData-based account/task data when upgrading from the old POC.
- [ ] Move account/task metadata out of the compatibility Electron `userData` root into dedicated durable stores.
- [ ] F2: dynamic account registry + per-account generation lease + global configurable worker semaphore (default 3).
- [ ] F2: lazy account runtime wake/sleep/idle eviction.

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