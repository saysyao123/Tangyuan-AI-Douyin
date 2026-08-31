# STATUS — Portable V1

Updated: 2026-08-31
Branch: `work/dola-portable-v1`

## Current phase

`RC1 — WINDOWS PORTABLE BUILD READY / REAL DOLA G1 USER GATE NEXT`

## Product execution rule

Continue independently unless a user decision or real Windows/Dola evidence Gate is required. Do not claim a real Dola capability merely because code, CI, packaging or simulation exists. No account-creation automation, CAPTCHA/MFA bypass, login bypass, entitlement/quota bypass, rate-limit evasion, 403 bypass, or provider restriction circumvention is part of Portable V1.

## Completed engineering / CI foundation

- [x] Requirements/product contract locked.
- [x] Dedicated branch and isolated `workstreams/portable-v1/` records.
- [x] Portable Windows data/runtime layout.
- [x] Durable ProjectStore, revisions, idempotency and project completion calculation.
- [x] Portable HTTP/CLI project and job routes.
- [x] Dynamic account registry without hard-coded A/B/C accounts.
- [x] Global configurable worker semaphore (default 3) and one-generation-per-account lease policy foundation.
- [x] Account pause/resume/debug/health/capability state foundation.
- [x] ProfileVault with password-derived encryption, per-account authenticated encryption, dirty/reseal/recovery markers, password rekey and encrypted backup support.
- [x] Fail-closed profile reseal foundation: plaintext runtime cleanup failure cannot be silently treated as a safe reseal.
- [x] Electron sessionData/profile bridge foundation and desktop vault unlock Gate.
- [x] Renderer keeps only one visible Dola debug WebView active instead of pre-creating one per account.
- [x] Preset first-run vault password policy and change-password path included in RC1.
- [x] Recoverable provider lifecycle foundation: post-submit observation timeout moves to recoverable observation state instead of blind resubmission.
- [x] Recovery path retries existing evidence/page observation without clicking Generate again.
- [x] Media resolver/download adapter foundation with candidate ranking, `.part` download, atomic finalize, MP4 signature/size/hash checks and permission failure preservation.
- [x] Codex/local control contract includes account/worker/task/project/job state plus recovery/output surfaces.
- [x] Windows x64 portable Electron packaging configured.
- [x] End-user release ZIP workflow configured and successfully built.

## RC1 build receipt

Release source revision:

`4369bf0f28d9a817b1d8dbee6fdc62526091b367`

Release workflow:

- `Dola Portable Release ZIP`
- run `#3`
- run id `33364676266`
- result: PASS
- artifact id: `9747918027`

End-user ZIP:

`Dola-Seedance-Workbench-Portable-v1.zip`

Verified SHA-256:

`377768cd5b8e631bb679b8718572dc8d68d09ae4485aa722c3eb43c147174d8f`

Detailed receipt: `DELIVERY_RC1_2026-08-31.md`.

## Real-world Gates

These are intentionally **not** upgraded to PASS by CI or packaging alone:

- G1 one-account login -> generation -> result observation -> highest-quality accessible download: READY_FOR_USER_TEST / NOT_PASSED_YET.
- real Windows clean shutdown -> restart -> vault unlock -> Dola login session persistence: READY_FOR_USER_TEST / NOT_PASSED_YET.
- G2 two-account isolation/parallel: BLOCKED_BY_G1.
- G5 scheduler/batch: BLOCKED_BY_G2.
- G20 pooled operation: BLOCKED_BY_G5.
- 30s: EXPERIMENTAL / entitlement-gated / no bypass.

## Highest current technical risk

`P0: real provider lifecycle variability` — RC1 now has a recoverable lifecycle/resolver foundation, but Dola page/control/result shapes still must be proven against the user's actual Windows session. A real provider/UI change may require adapter fixes after G1 evidence.

## Next action

Use the RC1 ZIP on Windows with one authorized Dola account. Verify manual login, one normal 5s job, result observation/download, then clean shutdown/restart persistence. Record all resulting evidence in this workstream before expanding to G2/G5/G20.
