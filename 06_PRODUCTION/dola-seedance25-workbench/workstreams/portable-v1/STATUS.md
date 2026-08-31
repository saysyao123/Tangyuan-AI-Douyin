# STATUS — Portable V1

Updated: 2026-08-31
Branch: `work/dola-portable-v1`

## Current phase

`RC3 — VISIBLE-WEBVIEW DESKTOP DISPATCH READY / REAL DOLA G1 RETEST NEXT`

## Product execution rule

Continue independently unless a user decision or real Windows/Dola evidence Gate is required. Do not claim a real Dola capability merely because code, CI, packaging or simulation exists. No account-creation automation, CAPTCHA/MFA bypass, login bypass, entitlement/quota bypass, rate-limit evasion, 403 bypass, or provider restriction circumvention is part of Portable V1.

## Latest real Windows evidence

RC2 user-side test produced a materially better diagnosis:

- the center embedded Dola page can generate successfully when operated directly by the user;
- the right Seedance Studio `创建并开始` task path failed;
- when I2V is selected, the extra image controls could push the lower task area below the fixed-height right panel.

This means the selected account/session/visible Dola page is usable for generation. The current G1 problem is the workbench dispatch/UI layer, not a generic assumption that Dola generation itself is unavailable.

## RC3 changes completed

- [x] Desktop `创建并开始` now prefers the exact currently visible center Dola WebView for the selected account.
- [x] The visible WebView is matched to the account by its Electron persistent partition; no password/Cookie/Token is read.
- [x] Visible-WebView dispatch still uses the existing WorkerScheduler lease, account binding, capture lifecycle, resolver and task state machinery.
- [x] Codex / loopback API dispatch remains the background-worker path; the foreground change is for the desktop interactive path.
- [x] If no matching visible WebView exists, desktop IPC can fall back to the existing local Control Plane dispatch path.
- [x] The entire right Seedance Studio now has an explicit vertical scrollbar, so T2V/I2V controls cannot permanently hide the task list.
- [x] Task cards now expose the persisted failure reason instead of showing only a generic `failed` badge.
- [x] Task cards show when execution used the center visible Dola page.
- [x] Renderer/IPC regression tests cover visible-WebView dispatch, background fallback, vertical scrolling and failure-detail rendering.
- [x] Windows build bumped to `0.3.2-portable-v1-rc3`.

## RC3 automated validation

Foundation workflow:

- `Dola Portable V1`
- run `#122`
- run id `33370534500`
- source revision `053d6756cb1ee58a77bf9fefe97cffe73d4ec1a9`
- result: PASS

RC3 release workflow:

- `Dola Portable Release ZIP`
- run `#16`
- run id `33370534517`
- source revision `053d6756cb1ee58a77bf9fefe97cffe73d4ec1a9`
- result: PASS
- artifact id: `9749952407`
- artifact digest: `sha256:6e160efaefca8bf025619d5e03a55412539f44e9d5f9f04bd43e2af3add35544`

End-user RC3 ZIP:

`Dola-Seedance-Workbench-Portable-v1-RC3.zip`

Verified SHA-256:

`e59d4fca2817e68bd5fc1e730804870b624b193712a17632effe769ddc9330a1`

Executable inside ZIP:

`Dola-Seedance-Workbench-Portable-0.3.2-portable-v1-rc3-x64.exe`

Detailed receipt: `DELIVERY_RC3_2026-08-31.md`.

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

- center visible Dola manual generation: OBSERVED SUCCESS on RC2.
- RC3 right-panel automatic visible-WebView submit: READY_FOR_USER_RETEST / NOT_PASSED_YET.
- G1 result observation -> highest-quality accessible MP4 download: NOT_PASSED_YET.
- real Windows clean shutdown -> restart -> vault unlock -> Dola login session persistence: requires explicit user evidence.
- G2 two-account isolation/parallel: BLOCKED_BY_G1.
- G5 scheduler/batch: BLOCKED_BY_G2.
- G20 pooled operation: BLOCKED_BY_G5.
- 30s: EXPERIMENTAL / entitlement-gated / no bypass.

## Highest current technical risk

`P0: visible Dola UI automation selectors and provider-result lifecycle variability` — the center page is now known to work manually. RC3 must prove that the automated model/duration/ratio/image/prompt/submit sequence can operate that same visible page and that the final media identity can be observed and downloaded.

## Next action

Run RC3 with the same authorized account selected and logged in in the center WebView. Start one simple 5-second T2V or I2V task from the right panel. The center page should visibly perform the automated setup and submit. If it fails, use the new task-card `失败原因` text as the next exact engineering input rather than repeating blind submissions.
