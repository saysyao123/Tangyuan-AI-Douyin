# Recovery

If the app reports `recoveryRequired`, do not delete `runtime/` or `data/`. Unlock the vault first. The application will treat dirty runtime profile data as newer than the last sealed package and will require resealing before a clean lock/exit.

If plaintext cleanup fails because Windows/Chromium still holds a file handle, the vault remains `RESEAL_REQUIRED`; this is deliberate fail-closed behavior. Close visible Dola/debug windows, retry reseal, and only then exit cleanly.
