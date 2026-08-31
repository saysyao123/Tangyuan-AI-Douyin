# Dola Seedance Portable V1 — RC2 Delivery Receipt

Date: 2026-08-31
Workstream: `portable-v1`
Branch: `work/dola-portable-v1`

## Why RC2 exists

RC1 user-side Windows test stopped at the first interaction Gate: `+ 添加 Dola 账号` and `修改保险库密码` did not produce a usable visible workflow. Code review identified a shared cause: those product actions depended on browser-native `window.prompt / window.alert / window.confirm` dialogs.

RC2 replaces those interactions with first-class Electron workbench UI and adds renderer regression tests so this failure mode is no longer accepted by CI.

## Reference direction

RC2 deliberately returns to the stronger structure already present in the earlier workbench and in the clean-room lessons from the user's uploaded Windows multi-account reference app:

- left account pool;
- center current account's Dola browser;
- right Seedance task control;
- explicit per-account Chromium partitions;
- one visible manual-login/debug account at a time;
- hidden workers separated from visible login/debug UI;
- task/output identity bound to account identity.

No proprietary code/assets are copied from the reference application.

## Release build identity

- Package version: `0.3.1-portable-v1-rc2`
- Release source revision: `cd70c83e7f7b4e4757ead177796cfc61a4b7c8af`
- Release workflow: `Dola Portable Release ZIP`
- Release workflow run: `#12`
- Release workflow run id: `33366897316`
- Release workflow result: PASS
- GitHub Actions artifact id: `9748651669`
- GitHub artifact digest: `sha256:5881ad5cfb4ad4de13e405127cf100353551e715d24ddc8cadcfad25cbef7075`

## End-user ZIP

Delivery file:

`Dola-Seedance-Workbench-Portable-v1-RC2.zip`

Verified SHA-256:

`d7820460870dc8a662ffc8cf13d339b242c47afe903e261e2e9fafc020326ecc`

Executable inside the ZIP:

`Dola-Seedance-Workbench-Portable-0.3.1-portable-v1-rc2-x64.exe`

The nested ZIP passed archive integrity testing. The executable was checked for Windows PE container signatures (`MZ` and `PE\0\0`).

## RC2 interaction changes

1. `+ 添加 Dola 账号` now opens an in-app account modal and calls the account IPC directly.
2. `创建并打开登录页` immediately selects the new account and prepares its independent Dola session.
3. `修改保险库密码` now uses a dedicated in-app password form with visible validation/errors.
4. Preset-password state is visible; while the preset is active the user only has to enter the new password twice.
5. Login/session health is visible through an account badge and `检查登录` button.
6. T2V/I2V are explicit modes.
7. I2V uses a native Windows image file picker.
8. The default primary task action is `创建并开始`; `仅加入队列` remains for batch/Codex workflows.
9. Renderer actions no longer depend on browser-native prompt/alert/confirm dialogs.

## Automated evidence

Foundation workflow `Dola Portable V1` run `#114` completed successfully on Windows and includes `test/renderer-contract.test.js`.

That regression test asserts at least:

- no `window.prompt / alert / confirm` dependency in the main renderer;
- in-app account/password UI exists;
- account creation reaches the IPC bridge;
- password change reaches the IPC bridge;
- I2V native image picker is wired through preload and portable main;
- Dola Web / Seedance 2.5 remains the V1 task path.

## First-run vault credential

Preset vault password:

`Tangyuan-Portable-2026!`

For RC2 user validation, the recommended order is to change this preset password before saving long-lived account sessions.

## What is NOT yet a production PASS

RC2 packaging and interaction regression tests do not prove real Dola behavior. The following still require user-side Windows evidence with an authorized Dola account:

- account modal -> independent Dola page actually opens;
- normal manual Dola/Google login;
- 5s Seedance 2.5 submit;
- result observation;
- highest-quality accessible MP4 download;
- clean shutdown/restart login-session persistence;
- two-account isolation/concurrency;
- larger pooled operation;
- 30s capability, which remains entitlement-gated and experimental.

No CAPTCHA/MFA bypass, login bypass, quota/entitlement bypass, rate-limit evasion, 403 bypass or provider restriction circumvention is part of RC2.
