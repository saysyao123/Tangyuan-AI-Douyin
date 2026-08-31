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

No existing real Dola Gate is reclassified by T-000 through T-004.

## Next test targets

1. Finish compatibility/import behavior for existing AppData-based account/task data.
2. Begin F2 account registry + per-account lease/global worker-pool tests.
3. Prepare F5 recoverable lifecycle changes before real Windows G1.
4. Real Windows G1 only after lifecycle + resolver/download integration is ready.
