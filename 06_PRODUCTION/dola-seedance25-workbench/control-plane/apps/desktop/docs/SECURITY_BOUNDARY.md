# Portable V1 Security / Provider Boundary

Portable V1 is a local workbench for accounts the operator is authorized to use. It deliberately does **not** implement account farming, automated sign-up, CAPTCHA/SMS bypass, credential harvesting, provider restriction bypass, quota evasion, entitlement spoofing, rate-limit evasion, or hidden 30-second request forcing.

Provider capability is evidence-driven. If Dola reports login required, quota exhausted, entitlement unavailable, or refuses a request, the job is recorded with that state and is not silently re-routed through evasion logic.

The encrypted profile vault protects local stored Chromium profile material at rest only after the default first-run password is changed to a private password. The public bootstrap password exists for setup convenience and must not be treated as secret.
