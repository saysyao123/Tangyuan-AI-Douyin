# TEST LOG — Portable V1

> Only tests/evidence from `work/dola-portable-v1` belong here. Historical D0-D6/evidence remains in its original files and is referenced, not copied as new PASS evidence.

## 2026-08-31 — Workstream initialization

### T-000 Branch isolation

- Action: created branch `work/dola-portable-v1` from `main`.
- Result: PASS.
- Evidence type: Git branch creation.

### T-001 Initial source audit

Reviewed at minimum:

- `control-plane/AGENTS.md`
- `control-plane/README.md`
- `control-plane/docs/CODEX_CONTROL_PLANE.md`
- `control-plane/docs/MULTI_ACCOUNT_DESKTOP_ARCHITECTURE.md`
- `control-plane/apps/desktop/src/main.js`
- `control-plane/apps/desktop/src/control-server.js`
- `control-plane/apps/desktop/src/background-dola.js`
- top-level `resolver/` structure

Findings recorded in `CODE_AUDIT_2026-08-31.md`.

Result: AUDIT COMPLETE FOR FOUNDATION PLANNING.

### T-002 Initial local-runtime test availability

- Direct local container execution was not available for this public repository because the current container has no GitHub network access.
- Status: NOT_RUN LOCALLY.

This does not affect later GitHub Actions validation.

### T-003 Portable path/layout Windows CI

Code under test:

- `apps/desktop/src/core/portable-paths.js`
- `apps/desktop/src/portable-main.js`
- `apps/desktop/test/portable-paths.test.js`
- updated desktop `npm run check`

CI:

- Workflow: `Dola Portable V1`
- Platform: `windows-latest`
- Node: 22
- Run: `#2`
- Head: `0a0453d44e067a0d89df1b606b92cdc7795047fb`
- Result: PASS / `conclusion=success`.

Validated at this level:

- portable-root precedence rules parse and execute on Windows Node;
- portable layout creation/version marker tests pass;
- new bootstrap and existing desktop JavaScript syntax checks pass;
- current package check command is Windows-compatible.

Not validated by this CI:

- Electron visible launch;
- real Dola login/session persistence;
- Dola submit/result/download;
- cross-machine profile session continuity.

### T-004 F1 durable project/job/idempotency + API Windows CI

Code under test includes:

- `src/core/atomic-json.js`;
- `src/core/project-store.js`;
- `test/project-store.test.js`;
- Portable V1 project/job routes in `src/control-server.js`;
- `portable-main.js` integration of the durable ProjectStore into the existing control plane;
- portable CLI discovery + `projects` / `jobs` JSON commands;
- `test/control-server-projects.test.js`.

Behavior covered:

- stable project creation;
- deterministic project+shot+revision job identity;
- same request is idempotent and returns the same job;
- conflicting inputs under the same revision are rejected;
- explicit new revision creates a distinct job;
- I2V local source must be an absolute path and is staged under project inputs;
- project result emits `PROJECT_COMPLETE` only after all created jobs succeed;
- HTTP project routes preserve idempotency and expose durable result state;
- CLI remains syntax-valid after portable discovery/project command changes.

CI:

- Workflow: `Dola Portable V1`
- Platform: `windows-latest`
- Node: 22
- Run: `#15`
- Head: `40b3267d4ad5a3996d5fae6a699d432bee281b27`
- Job: `foundation-check`
- Result: PASS / `conclusion=success`.

This is an F1 foundation PASS at the platform-independent/control-contract level. It is not a real Dola generation Gate.

### T-005 F2 dynamic account registry + worker scheduler Windows CI

Code under test includes:

- `src/core/account-registry.js`;
- `src/core/worker-scheduler.js`;
- `src/core/worker-config.js`;
- account/worker integration in `portable-main.js`;
- account health/pause/resume/debug and worker status/settings/sweep routes in `control-server.js`;
- matching JSON CLI commands;
- `test/account-registry.test.js`;
- `test/worker-scheduler.test.js`;
- `test/control-server-workers.test.js`.

Behavior covered:

- dynamic import/registration of 20 accounts without A/B/C hard-coding;
- manual PAUSED state remains preserved when legacy READY metadata refreshes;
- login health can transition READY ↔ NEEDS_LOGIN;
- quota/entitlement restrictions surface as explicit non-schedulable reasons;
- one account cannot hold two simultaneous generation leases;
- global active lease count never exceeds configured max workers;
- max workers defaults to 3 and is persistently configurable;
- a forced unavailable/busy account fails instead of silently switching to another account;
- automatic selection ignores login-required, paused and restricted accounts;
- released accounts become reusable;
- idle worker state can be lazily evicted;
- debug-promoted account stays awake at the scheduler-policy level;
- repeated acquire of the same job is idempotent;
- account/worker Control Plane endpoints return machine-readable JSON.

CI:

- Workflow: `Dola Portable V1`
- Platform: `windows-latest`
- Node: 22
- Run: `#30`
- Head: `f1f6c0f205afcb687cd05f840fd81767d2d99569`
- Job: `foundation-check`
- Result: PASS / `conclusion=success`.

Boundary:

This is the F2 **unit/simulation/control-contract Gate**. The scheduler is not yet proof of real concurrent Dola generation. Real G2 validation still requires user-side Windows evidence.

### T-006 RC1 integrated foundation Windows CI

Build source revision:

`4369bf0f28d9a817b1d8dbee6fdc62526091b367`

Workflow:

- `Dola Portable V1`
- run `#103`
- result: PASS / `conclusion=success`

The current check suite includes the portable layout/project/account/worker tests plus vault, vault rekey/default policy, fail-closed Electron profile bridge, lifecycle/resolver/recovery and Control Plane syntax/test coverage included in the RC1 source revision.

Boundary:

This validates implementation contracts on `windows-latest`; it does not prove that a particular user's Dola account/session/UI currently exposes the expected controls or result shapes.

### T-007 Windows Portable release build

Workflow:

- `Dola Portable Release ZIP`
- run `#3`
- run id `33364676266`
- source revision `4369bf0f28d9a817b1d8dbee6fdc62526091b367`
- result: PASS

Successful steps included:

- checkout;
- Node 22 setup;
- dependency install;
- Portable V1 checks;
- Windows x64 portable executable build;
- end-user ZIP assembly;
- artifact upload.

GitHub Actions artifact:

- id: `9747918027`
- name: `Dola-Seedance-Workbench-Portable-v1`
- GitHub artifact digest: `sha256:ac8f8feaa61eda2a41abd96440a7cc752272f7f9fee21e78fbe5cf7c8d802818`

Result: PACKAGING PASS.

### T-008 Downloaded end-user ZIP integrity check

The GitHub Actions artifact was downloaded and the nested end-user ZIP was extracted for delivery.

End-user file:

`Dola-Seedance-Workbench-Portable-v1.zip`

Verified SHA-256:

`377768cd5b8e631bb679b8718572dc8d68d09ae4485aa722c3eb43c147174d8f`

The hash matches the SHA256 receipt generated by the Windows release workflow.

The ZIP contains:

- `Dola-Seedance-Workbench-Portable-0.3.0-portable-v1-x64.exe`
- `START_HERE.txt`
- `USER_QUICKSTART.md`
- `PRESET_PASSWORD.txt`
- `KNOWN_LIMITATIONS.md`
- `RECOVERY.md`
- `SECURITY_BOUNDARY.md`
- `PORTABLE_LAYOUT.md`
- `BUILD_DELIVERY.md`

The executable was checked for Windows PE container signatures (`MZ` and `PE\0\0`). This verifies file/container integrity only; it is not an Electron launch test or a real Dola generation Gate.

## Current real-world Gate status

- G1 one-account end-to-end: READY_FOR_USER_TEST / NOT_PASSED_YET.
- real Windows clean shutdown/restart session persistence: READY_FOR_USER_TEST / NOT_PASSED_YET.
- G2 two-account isolation/parallel: BLOCKED_BY_G1.
- G5 scheduler/batch: BLOCKED_BY_G2.
- G20 pooled operation: BLOCKED_BY_G5.
- 30s: EXPERIMENTAL / entitlement-gated / no bypass.

No real Dola Gate is reclassified as PASS merely because source tests or packaging succeeded.

## Next test target

Run RC1 on the user's Windows machine with one authorized Dola account: manual login -> one normal 5s job -> result observation/download -> clean exit -> restart/unlock -> verify session persistence. Capture any UI/provider mismatch as new Portable V1 evidence before expanding to multi-account Gates.
