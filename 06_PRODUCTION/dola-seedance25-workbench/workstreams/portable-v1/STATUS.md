# STATUS — Portable V1

Updated: 2026-08-31
Branch: `work/dola-portable-v1`

## Current phase

`F3 — ENCRYPTED PROFILE VAULT / ELECTRON SESSION BINDING` (implementation active)

## Product execution rule

Continue independently through F3-F9 unless a user decision or real Windows/Dola evidence Gate is required. Do not claim a real Dola capability merely because code or CI exists. No account-creation automation, CAPTCHA bypass, entitlement bypass, rate-limit evasion, or provider restriction circumvention is part of Portable V1.

## Completed

- [x] Requirements/product contract locked.
- [x] Dedicated branch and workstream records.
- [x] Portable Windows data/runtime layout.
- [x] Durable ProjectStore, revisions, idempotency and project completion calculation.
- [x] Portable HTTP/CLI project and job routes.
- [x] Dynamic account registry without hard-coded A/B/C accounts.
- [x] Global configurable worker semaphore (default 3) and one-generation-per-account lease policy foundation.
- [x] Account pause/resume/debug/health/capability state foundation.
- [x] ProfileVault with password-derived encryption, per-account authenticated encryption, dirty/reseal/recovery markers and encrypted backup support.
- [x] Electron profile bridge foundation mapping account partitions to an ephemeral sessionData root.
- [x] Renderer changed to keep only one visible Dola debug WebView active instead of pre-creating a WebView for every account.
- [x] Vault wrong-password behavior clears the resident master key.

## Active F3 safety closeout

- [ ] Fail-closed reseal: encrypted package success must not clear dirty state if plaintext runtime removal fails.
- [ ] Desktop startup unlock Gate: no Dola partition may open before vault unlock.
- [ ] Default first-run password policy + forced-change recommendation in UI/docs.
- [ ] Clean shutdown reseal hook and explicit recovery status.
- [ ] Windows CI for the above foundation behaviors.

## Next engineering slices

- [ ] F4: split the current Dola background runner into session/UI/lifecycle/conversation/capability provider modules.
- [ ] F5: persist provider lifecycle and recover observation without blind resubmission after timeout.
- [ ] F6: resolver/download adapter + technical validation + project outputs.
- [ ] F7/F8: localhost workbench and Codex contract extension on the same stores.
- [ ] F9: Windows portable packaging + migration/readme + release ZIP/artifact.

## Highest current technical risk

`P0: recoverable Dola result lifecycle` — successful UI submission and final media observation are not yet one recoverable durable state machine. This must be solved before G1 can pass.

## Real-world Gates

- G1 one-account end-to-end: NOT_READY.
- G2 two-account isolation/parallel: NOT_READY.
- G5 scheduler/batch: NOT_READY.
- G20 pooled operation: NOT_READY.
- 30s: EXPERIMENTAL / entitlement-gated / no bypass.

## Evidence discipline

No real Windows/Dola capability is marked PASS merely because code exists. Real session-dependent Gates require user-side Windows evidence.
