# Portable Layout

```
DolaWorkbench/
  DolaWorkbench.exe
  app/                 replaceable application payload
  runtime/             ephemeral control/browser working state
    control/
    tmp/
    unlocked-profiles/
  data/                durable state
    accounts/
    projects/
    outputs/
    vault/              encrypted account profile packages
    logs/
    backups/
    state/
```

Do not manually copy plaintext Chromium profile folders into `data/vault`. Use the application migration/profile bridge so the vault can preserve dirty/recovery state.
