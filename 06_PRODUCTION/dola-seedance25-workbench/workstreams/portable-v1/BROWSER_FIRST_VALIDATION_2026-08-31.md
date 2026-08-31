# Browser-first Validation — 2026-08-31

## Why this track exists

Portable EXE iteration is temporarily paused because packaged-Windows feedback is too slow for rapid Dola UI/lifecycle discovery. The next phase prioritizes browser-first validation in ChatGPT Work / a shared browser session, then writes confirmed behavior back into this workstream before deciding whether to resume desktop implementation.

## User-side evidence confirmed so far

### E1 — 10-second I2V works

Observed by user on the real Dola page:

- mode: image-to-video;
- model selected by the user: Seedance 2.5;
- duration: 10 seconds;
- face-degraded / face-occluded reference image path;
- result: generation completed successfully.

Conclusion: for this tested account/session, 10s Seedance 2.5 I2V is a real observed capability. The earlier software failure must not be interpreted as proof that Dola I2V itself is unavailable.

### E2 — observed credit consumption for 10s Seedance 2.5

User observed that one 10-second Seedance 2.5 generation consumed 4 credits, exhausting the currently available credit balance on that account/session.

Treat this as account/session-specific observed behavior, not a universal Dola pricing/entitlement rule until separately verified.

Operational implication: avoid repeated blind submissions during validation. Prefer one controlled test per unknown behavior and record the result before spending another generation.

### E3 — expert-mode 30-second path exists, model identity not yet confirmed

User observed an Expert Mode path where an image can be uploaded and a 30-second video request can be sent. The request appears to produce two 15-second video generations.

Current status:

- 30s request acceptance: OBSERVED;
- output topology: appears to be 2 × 15s generations;
- final generation result: pending at time of this note;
- whether this path is actually Seedance 2.5: UNCONFIRMED.

Do not label Expert Mode 30s as Seedance 2.5 until UI/model metadata or request/result evidence confirms it.

## Browser-first validation priorities

1. Reproduce one 10s I2V success in the shared browser with minimal manual intervention.
2. Record exact visible controls and page states for model, duration, ratio, image attachment, prompt, submit, generating and completion.
3. Record the 10s credit balance before/after if visible, without intentionally spending extra credits just to re-prove a known value.
4. Inspect the Expert Mode 30s path and determine model identity from normal UI/request/result metadata.
5. Determine whether the 2 × 15s outputs are independent generations, sequential continuation segments, or a stitched 30s logical task.
6. Test normal accessible download and highest-quality rendition after a successful generation.
7. Only after single-account browser behavior is understood should multi-account desktop automation resume.

## Safety / scope

No account-registration automation, CAPTCHA/MFA bypass, credential extraction, Cookie/Token export, quota/entitlement bypass, rate-limit evasion, 403 bypass, or provider restriction circumvention is part of this validation track.
