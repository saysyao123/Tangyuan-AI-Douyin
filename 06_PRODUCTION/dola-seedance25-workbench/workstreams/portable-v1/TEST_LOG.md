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

No existing real Dola Gate is reclassified by T-000 through T-003.

## Next test targets

1. Complete F0 compatibility/import behavior for existing userData if needed.
2. F1 idempotency/project schema unit tests.
3. Real Windows G1 only after lifecycle/download integration is ready.
