# Dola Seedance Portable V1 — RC1 Delivery Receipt

Date: 2026-08-31
Workstream: `portable-v1`
Branch: `work/dola-portable-v1`

## Release build identity

- Build commit: `4369bf0f28d9a817b1d8dbee6fdc62526091b367`
- Build commit message: `build(portable-v1): include compact workbench CLI checks`
- Foundation workflow: `Dola Portable V1`
- Foundation workflow result at build commit: PASS
- Release workflow: `Dola Portable Release ZIP`
- Release workflow run: `#3`
- Release workflow run id: `33364676266`
- Release workflow result: PASS
- GitHub Actions artifact id: `9747918027`
- GitHub artifact digest: `sha256:ac8f8feaa61eda2a41abd96440a7cc752272f7f9fee21e78fbe5cf7c8d802818`

## End-user ZIP

File:

`Dola-Seedance-Workbench-Portable-v1.zip`

Verified SHA-256:

`377768cd5b8e631bb679b8718572dc8d68d09ae4485aa722c3eb43c147174d8f`

The ZIP contains the Windows portable executable and the end-user docs assembled by the release workflow.

Primary executable:

`Dola-Seedance-Workbench-Portable-0.3.0-portable-v1-x64.exe`

The downloaded executable was checked for a valid Windows PE container signature (`MZ` + `PE\0\0`). This is a packaging/container integrity check, not a substitute for a real Dola login/generation Gate.

## First-run vault credential

Preset vault password:

`Tangyuan-Portable-2026!`

This is only a first-run convenience credential. After the first successful local verification, the user should change it from the workbench Vault/Settings UI so the durable encrypted profile vault is protected by a private password.

## Included user documentation

- `START_HERE.txt`
- `USER_QUICKSTART.md`
- `PRESET_PASSWORD.txt`
- `KNOWN_LIMITATIONS.md`
- `RECOVERY.md`
- `SECURITY_BOUNDARY.md`
- `PORTABLE_LAYOUT.md`
- `BUILD_DELIVERY.md`

## What is validated in RC1

- Windows x64 Electron portable packaging completes on GitHub Actions `windows-latest`.
- Portable V1 automated checks pass before packaging.
- Release ZIP assembly and artifact upload complete successfully.
- The end-user ZIP hash matches the workflow-produced SHA256 receipt.
- The packaged executable has a valid Windows PE file signature.
- Portable account/project/worker/vault/lifecycle/resolver foundations are included in the built source revision.

## What is NOT yet a production PASS

The following still require user-side Windows evidence with an account the user is authorized to use:

- G1: one-account Dola login -> 5s/10s submit -> result observation -> highest-quality accessible download.
- clean shutdown/restart persistence of the real Dola login session on the user's Windows environment.
- G2: two-account isolation and concurrent worker behavior.
- G5/G20 pooled operation.
- 30s capability, which remains entitlement-gated and experimental.

No CAPTCHA/MFA bypass, login bypass, quota/entitlement bypass, rate-limit evasion, 403 bypass, or automatic account switching to evade provider restrictions is part of this release.

## Next Gate

Run RC1 on the user's Windows machine with one Dola account first. If G1 succeeds, progress through the staged multi-account Gates without changing the release contract.