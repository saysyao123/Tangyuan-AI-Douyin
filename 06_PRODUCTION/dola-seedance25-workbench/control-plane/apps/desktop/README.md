# Seedance Desktop Studio v0.2

Clean-room Windows desktop POC for multi-account Dola sessions plus a Codex-operable local task control plane.

## Implemented in this branch

- Electron desktop shell.
- Multiple Dola account containers.
- One persistent Chromium partition per account.
- One long-lived Dola WebView per account.
- Manual visible login; no Google password/TOTP storage.
- Account switching and per-account session clearing.
- Local JSON task queue.
- Seedance task form in the desktop UI.
- Loopback-only control server with random bearer token.
- Machine-readable CLI for Codex: accounts/providers/tasks.
- Provider gate that blocks automatic Dola dispatch until D2 is actually verified.
- Experimental hidden-background Dola worker, one hidden BrowserWindow per persistent account partition.
- Durable per-job capture artifacts under the resolver runtime (raw response bodies stay local and ignored).

## Run

```powershell
cd apps/desktop
npm install
npm run check
npm start
```

For the no-foreground-window background worker:

```powershell
npm run check
npm run start -- --background --enable-experimental-dola
```

The background provider is deliberately explicit:

```powershell
node bin/seedance-studio.mjs tasks create --account Dola1 --provider dola-web-background --duration 5 --ratio 9:16 --prompt "..."
node bin/seedance-studio.mjs tasks dispatch --id <task-id>
node bin/seedance-studio.mjs tasks watch --id <task-id>
```

`Dola1` and `Dola2` are ordinal aliases for the first two locally managed Dola slots. A task dispatch is a real provider submission; perform it only after the user has confirmed the exact test prompt and account.

In another terminal:

```powershell
npm run studio -- health
npm run studio -- accounts list
```

See `../../docs/CODEX_CONTROL_PLANE.md` for the complete Codex workflow.

## D0 / D1 acceptance

```text
[ ] Desktop launches on Windows x64
[ ] Account A can log in manually
[ ] Account B can log in manually
[ ] A/B sessions do not leak into each other
[ ] Switching accounts does not require re-login
[ ] Restart keeps both Chromium sessions
[ ] Clear session only clears the selected account
[ ] npm run studio -- health works while desktop app is running
[ ] Codex CLI can list/open accounts and create/list/cancel local tasks
```

## Important current limitation

The production `dola-web` provider is implemented as a control/session shell, but its automatic Seedance dispatch is intentionally not enabled yet.

`tasks dispatch` for `dola-web` will return `D2_GATE_NOT_PASSED` until a real user session verifies the normal Seedance 2.5 10s submit/SSE/conversation/result lifecycle.

This keeps the product architecture stable without pretending the unverified provider path is complete.

`dola-web-background` is an explicitly experimental observation path. It does not bypass login, quota, country restrictions, or watermark policy. It currently proves the hidden session and pre-generation capture lifecycle; a real MP4, ffprobe result, clean-source decision, and visual watermark QA are still required before calling video delivery PASS.
