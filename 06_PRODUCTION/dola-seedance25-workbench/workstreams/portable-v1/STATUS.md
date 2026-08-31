# STATUS — Portable V1

Updated: 2026-08-31
Branch: `work/dola-portable-v1`

## Current phase

`RC2 — WINDOWS PORTABLE UI FIX READY / REAL DOLA G1 RETEST NEXT`

## Product execution rule

Continue independently unless a user decision or real Windows/Dola evidence Gate is required. Do not claim a real Dola capability merely because code, CI, packaging or simulation exists. No account-creation automation, CAPTCHA/MFA bypass, login bypass, entitlement/quota bypass, rate-limit evasion, 403 bypass, or provider restriction circumvention is part of Portable V1.

## RC1 Windows feedback

User-side RC1 test did **not** pass the first interaction Gate:

- `+ 添加 Dola 账号` appeared to do nothing;
- `修改保险库密码` appeared to do nothing.

Code review found that RC1 depended on browser-native `window.prompt / window.alert / window.confirm` dialogs for these primary actions. This is not accepted as a reliable packaged-Electron product interaction contract. RC1 is therefore recorded as **FAIL at UI interaction Gate**, before real Dola G1 could start.

Detailed redesign record: `RC2_UI_AND_INTERACTION_REDESIGN_2026-08-31.md`.

## RC2 changes completed

- [x] Added real in-app account-creation modal; no browser prompt dependency.
- [x] Added real in-app vault-password-change form; no browser prompt/alert dependency.
- [x] Added in-app confirmation modal and visible toast/status feedback.
- [x] Retained mature three-pane workbench structure: left account pool / center current Dola page / right Seedance tasks.
- [x] Account list now shows account count and login/session state.
- [x] Added explicit `检查登录` action and current-account health badge.
- [x] Kept only one visible manual-login/debug WebView at a time while preserving independent per-account partitions.
- [x] Simplified V1 primary provider UI to Dola Web / Seedance 2.5.
- [x] Added T2V / I2V selector.
- [x] Added native Windows image picker for I2V first-frame selection.
- [x] Changed primary task action to `创建并开始`; retained `仅加入队列` for batch/Codex use.
- [x] Retained recover-without-resubmit behavior for observation timeout.
- [x] Added packaged-renderer regression tests covering account/password/image-picker wiring.
- [x] Bumped Windows build to `0.3.1-portable-v1-rc2`.

## RC2 automated validation

Foundation workflow:

- `Dola Portable V1`
- run `#114`
- source revision `8ae18c12b090056803305064d94ad136bcbd39bc`
- result: PASS

This run includes the new renderer interaction regression tests.

RC2 release workflow:

- `Dola Portable Release ZIP`
- run `#12`
- run id `33366897316`
- source revision `cd70c83e7f7b4e4757ead177796cfc61a4b7c8af`
- result: PASS
- artifact id: `9748651669`
- artifact digest: `sha256:5881ad5cfb4ad4de13e405127cf100353551e715d24ddc8cadcfad25cbef7075`

End-user RC2 ZIP:

`Dola-Seedance-Workbench-Portable-v1-RC2.zip`

Verified SHA-256:

`d7820460870dc8a662ffc8cf13d339b242c47afe903e261e2e9fafc020326ecc`

Executable inside ZIP:

`Dola-Seedance-Workbench-Portable-0.3.1-portable-v1-rc2-x64.exe`

ZIP integrity test passed and the executable was checked for Windows PE container signatures (`MZ` and `PE\0\0`).

## Engineering foundation retained

- [x] Portable Windows data/runtime layout.
- [x] Durable ProjectStore, revisions, idempotency and project completion calculation.
- [x] Portable HTTP/CLI project and job routes.
- [x] Dynamic account registry without hard-coded A/B/C accounts.
- [x] Global configurable worker semaphore (default 3) and one-generation-per-account lease policy foundation.
- [x] ProfileVault with password-derived encryption, per-account authenticated encryption, dirty/reseal/recovery markers, password rekey and encrypted backup support.
- [x] Fail-closed profile reseal foundation.
- [x] Recoverable provider lifecycle foundation; observation timeout does not blindly resubmit.
- [x] Media resolver/download adapter foundation with candidate ranking, `.part` download, atomic finalize, MP4 signature/size/hash checks and permission failure preservation.
- [x] Codex/local control contract for accounts/workers/tasks/projects/jobs/recovery/outputs.

## Real-world Gates

These remain intentionally **not PASS** until the user's Windows/Dola evidence exists:

- G1A account UI: RC2 READY_FOR_USER_RETEST / NOT_PASSED_YET.
- G1B one-account manual login: BLOCKED_BY_G1A.
- G1C 5s generation -> result observation -> highest-quality accessible download: BLOCKED_BY_G1B.
- real Windows clean shutdown -> restart -> vault unlock -> Dola login session persistence: BLOCKED_BY_G1B.
- G2 two-account isolation/parallel: BLOCKED_BY_G1.
- G5 scheduler/batch: BLOCKED_BY_G2.
- G20 pooled operation: BLOCKED_BY_G5.
- 30s: EXPERIMENTAL / entitlement-gated / no bypass.

## Highest current technical risk

`P0: real packaged Electron + Dola page behavior` — RC2 fixes the first confirmed UI interaction defect and adds regression coverage. The next evidence must come from an actual Windows launch: account modal -> independent Dola page -> manual login. Only after that should provider lifecycle/result-resolution issues be debugged.

## Next action

Run RC2 from a fresh writable folder. First verify that `+ 添加 Dola 账号` opens the in-app modal and `创建并打开登录页` opens Dola. Then complete one normal user-owned login and run a 5-second T2V job. Do not expand to multiple accounts until this G1 chain is closed.
