# DECISION LOG — Portable V1

Date started: 2026-08-31

## Locked product decisions

1. Product form: hybrid — Electron desktop session/runtime layer + complete localhost web workbench.
2. V1 access: localhost only.
3. Codex integration: full account/task/project management after user unlock.
4. Login: first login and re-login are manual; Codex never handles passwords/MFA/CAPTCHA.
5. Control interfaces: HTTP API + JSON CLI + machine-readable state files.
6. Account selection: automatic by default with explicit-account override.
7. Generation scope: T2V + I2V, Seedance 2.5, common durations/ratios; 5/10s stable target.
8. Concurrency: one generation per account; different accounts may run in parallel.
9. Download target: highest-quality accessible media; visual representative-frame watermark QA is not mandatory in V1.
10. Output organization: project/shot/revision based.
11. Submission: single job and batch project both supported.
12. Failure handling: classify and recover same task first; regenerate only after confirmed generation failure/new revision decision.
13. Distribution: Windows portable/green version.
14. Runtime view: hidden background by default + visible debug/login mode on demand.
15. Scale: around 20 registered accounts, dynamically extensible.
16. Worker strategy: hybrid pool, not all accounts resident.
17. Active pool limit: configurable, default 3.
18. Browser runtime: bundled Electron/Chromium, independent from daily Chrome.
19. Profile portability: encrypted profile data may move with portable bundle; service may still require re-authentication on another machine.
20. Vault: local password-protected vault.
21. Vault unlock: manual once per run.
22. Startup: manual by default, optional Windows startup; vault remains locked until user unlock.
23. Codex state surface: API + CLI + state files.
24. Codex permission mode: configurable; default fully automatic after unlock.
25. Audit: complete non-secret audit logs.
26. Network: normal shared Windows network in V1; no per-account proxy rotation.
27. Codex may start/stop Workbench but may not unlock vault.
28. Vault readiness: Codex can auto-detect locked/unlocked state; user may also explicitly tell it to continue.
29. Task delivery: per-job output path + full result JSON + project-level completion event.
30. Local inputs: Codex may pass absolute Windows paths; Workbench stages inputs.
31. V1 provider: Dola Web only; provider abstraction preserved for future official APIs.
32. Validation scale: 1 → 2 → 5 → ~20 accounts.
33. Development base: upgrade existing `dola-seedance25-workbench`, not a separate new project.
34. Compatibility: internals may refactor; major existing Codex API/CLI concepts remain compatible with migration notes.
35. Upgrade model: app/runtime replaceable; data isolated; migration backup and rollback.
36. Crash/restart: complete task recovery; no automatic duplicate resubmit.
37. Local control auth: per-run localhost bearer token; expires on process exit.
38. Web UI: complete workbench, sharing the exact core/state with Codex.
39. Idempotency: strong project+shot+revision identity; explicit new revision required for a new generation.
40. Restricted account behavior: pause on explicit quota/permission/entitlement; non-invasive health recheck; no quota-evasion rotation.
41. 30s: exposed as experimental Gate, promoted only after real account validation.
42. Dola submission path: real web UI drive.
43. Media acquisition: page download + lifecycle candidates + resolver chain, choose highest-quality accessible candidate with fallback.
44. Account health/capability: available in web/API/CLI/state.
45. Production PASS: after one manual vault unlock, Codex can submit a multi-shot project and reach archived outputs/PROJECT_COMPLETE without user touching Dola except legitimate login/MFA/CAPTCHA/major UI-change intervention.

## Additional engineering decisions made during audit

### D-ENG-001 — Separate records and branch

All new records live under `workstreams/portable-v1/` on branch `work/dola-portable-v1`. Historical `evidence/` and prior `docs/TEST_LOG.md` are not reused as this workstream's log.

### D-ENG-002 — Incremental refactor before TypeScript rewrite

Do not block functional Gates on a full JS→TypeScript rewrite. Introduce boundaries/modules first, then migrate selectively after behavior is covered.

### D-ENG-003 — Portable vault promise is best-effort cross-machine session continuity

The software can encrypt/move profile material, but Dola/Google/Chromium may legitimately require re-authentication on another Windows machine. Do not promise otherwise.

### D-ENG-004 — Raw network captures are debug-only

Normal state/audit/event files must be redacted. Raw response capture, when temporarily enabled for local diagnostics, is local-only and excluded from Git/export/default Codex state.
