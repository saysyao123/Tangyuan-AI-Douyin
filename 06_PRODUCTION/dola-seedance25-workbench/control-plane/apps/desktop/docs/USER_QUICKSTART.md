# Dola Seedance Portable V1 — Quick Start

1. Extract the release ZIP to a normal writable folder such as `D:\\AI\\DolaWorkbench`.
2. Run the portable executable from that folder.
3. On the first launch use the preset vault password `Tangyuan-Portable-2026!`.
4. Add a Dola account, open it, and complete login manually inside the visible Dola page. The application does not collect your Google password/TOTP.
5. After confirming the session works, change the vault password to a private password from the Vault/Settings panel.
6. Create a project/job from the UI or Codex CLI. Default worker concurrency is 3, while each account can hold only one generation lease at a time.
7. 5s/10s are normal targets. Use 30s only when the logged-in Dola UI/account entitlement exposes it normally; Portable V1 does not bypass service limits.
8. Keep the application open until active jobs finish. On clean exit, dirty account profiles are resealed into the encrypted local vault. If Windows reports a recovery state after an abnormal exit, unlock the vault and follow the recovery prompt before continuing.

## Files

- `app/` replaceable application payload
- `runtime/` ephemeral control/session data; safe to recreate only when the app is closed and no recovery is pending
- `data/` durable projects, outputs, account metadata, encrypted vault, logs, backups

Back up `data/` before moving the workbench to another machine. Cross-machine Dola session continuity is best-effort; the provider may require re-login.
