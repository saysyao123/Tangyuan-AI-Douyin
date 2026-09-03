# RunningHub Seedance 2.5 Direct API｜Minimal Validation

## Goal
Verify whether a direct Seedance 2.5 provider surface produces more controllable MV material than Dola Expert Agent for the same accepted K0 and director intent.

This test does **not** attempt quota bypass, account rotation, cookie replay, or moderation circumvention.

## Why this test exists
Observed Dola Expert Agent result for `B_MOVING_CAMERA` generated successfully, but the resulting character behavior and camera relationship were poor. `A_FACE_HAND` and `C_PHYSICS` were blocked before a confirmed video job. Therefore provider-layer diagnosis is required before changing the creative rules again.

## Provider under test
RunningHub public Seedance 2.5 Global Multimodal API.

Authentication:
- Use one legitimate user-owned `RUNNINGHUB_API_KEY`.
- Keep the key only in a local environment variable / secret store.
- Never commit credentials to GitHub.

## Phase P1 — 5s Direct A/B sanity test
Use the already locked benchmark K0 assets.

### Test P1-B
- K0: locked `B_MOVING_CAMERA` image.
- duration: 5s
- ratio: 9:16
- generateAudio: false
- same positive director intent as R1-B
- single image reference only
- no prompt patching after submission

Purpose:
- compare character gait;
- compare camera displacement/parallax;
- determine whether `FOLLOW -> OVERTAKE` is actually executed;
- compare usable seconds against Dola Expert B.

### Test P1-A or P1-C
Only after P1-B succeeds technically, run one additional low-risk control:
- A: near-face hand arc without physical contact; or
- C: container-to-basin water causality.

Purpose:
- determine whether Dola Expert blocking was upstream-agent specific rather than model-level.

## Acceptance record
For every run record only:

```text
STATUS
USABLE_SECONDS
VISUAL_HIT
IDENTITY_STABILITY
MOTION_EXECUTION
CAMERA_EXECUTION
FAILURE
NEXT
```

## Decision gate

### PASS_DIRECT
If RunningHub direct P1-B materially improves camera/behavior execution over Dola Expert B, add RunningHub as a production provider candidate.

### NO_ADVANTAGE
If both surfaces show the same motion failure, the likely problem is prompt/reference/model behavior rather than Dola Expert routing.

### PROVIDER_FAIL
If API/auth/upload fails, diagnose provider integration separately; do not change director prompt to compensate.

## Phase P2 — duration test
Only if P1 demonstrates useful control:
- 5s
- 10s
- 15s

Same K0 and same director task. Compare accepted material per generation cost. Do not test 30s in the current MV benchmark.
