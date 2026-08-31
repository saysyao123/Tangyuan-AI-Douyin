# STATUS — Portable V1

Updated: 2026-08-31
Branch: `work/dola-portable-v1`

## Current phase

`PAUSED DESKTOP ITERATION — BROWSER-FIRST REAL DOLA VALIDATION`

## Product execution rule

Continue independently unless a user decision or real Dola evidence Gate is required. Do not claim a capability merely because code, CI, packaging or simulation exists. No account-creation automation, CAPTCHA/MFA bypass, login bypass, entitlement/quota bypass, rate-limit evasion, 403 bypass, or provider restriction circumvention is part of this workstream.

## Why desktop iteration is paused

Repeated EXE rebuild/download/reinstall cycles are too slow for the current discovery stage. The center embedded Dola page has already demonstrated that the user's real account/session can generate successfully, while the right-side packaged automation remains the failing layer. The project is therefore switching temporarily to browser-first validation so the exact Dola UI/lifecycle can be observed and stabilized before more desktop packaging work.

Detailed browser-first evidence: `BROWSER_FIRST_VALIDATION_2026-08-31.md`.

## Latest real Dola evidence

- Center visible Dola page manual generation: OBSERVED SUCCESS.
- 10-second I2V using Seedance 2.5 with a face-degraded / face-occluded reference image: OBSERVED SUCCESS on the user's tested account/session.
- One 10-second Seedance 2.5 generation was observed to consume 4 credits, exhausting the currently available credit balance for that account/session. Treat as observed account/session behavior, not a universal pricing rule.
- Expert Mode accepts a 30-second image-based request and appears to produce 2 × 15-second video generations. Whether this path is actually Seedance 2.5 remains UNCONFIRMED. Final result was still pending when recorded.

## Desktop RC3 state retained

RC3 remains available as the latest packaged reference but is not the active validation path.

- Desktop `创建并开始` prefers the current visible Dola WebView.
- Right Seedance Studio has vertical scrolling.
- Task cards expose failure details.
- WorkerScheduler / ProjectStore / ProfileVault / resolver foundations remain retained.

## Real-world Gates

- 10s Seedance 2.5 I2V on real Dola page: PASS for the tested account/session.
- Face-degraded / face-occluded reference acceptance for that 10s I2V test: PASS for the tested input/session.
- 10s observed credit cost: 4 credits for the tested account/session; scope-limited observation.
- Expert Mode 30s request acceptance: OBSERVED.
- Expert Mode 30s model identity: UNCONFIRMED.
- Expert Mode 30s final output behavior: PENDING / appears to be 2 × 15s.
- highest-quality accessible download path: still needs browser-first validation.
- RC3 right-panel automatic submit: no longer the immediate priority; desktop iteration paused.
- G2/G5/G20 multi-account desktop gates: PAUSED until browser-first single-account behavior is understood.

## Highest current technical question

`P0: identify the exact real Dola browser workflow and lifecycle for 10s/30s generation, including model identity, submit state, completion state and accessible media result.`

## Next action

Use ChatGPT Work / shared browser validation rather than another EXE build. Reproduce known-good 10s I2V only when necessary, inspect the Expert Mode 30s path without assuming model identity, and validate normal result/download behavior. Resume desktop engineering only after these browser behaviors are documented.
