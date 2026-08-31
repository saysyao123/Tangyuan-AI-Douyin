# PRODUCT CONTRACT — Dola Workbench Portable V1

Date: 2026-08-31
Status: LOCKED

## 1. Product form

- Windows x64 portable/green distribution.
- Hybrid UI:
  - Electron desktop owns account sessions, isolated Chromium contexts, Dola UI execution, lifecycle observation.
  - Localhost web workbench owns account/project/task/queue/output/operator UI.
- Localhost only; no LAN/public exposure in V1.
- Software ships its own Electron/Chromium runtime; does not depend on the user's daily Chrome profile.

## 2. Account model

- Target: ~20 accounts initially, dynamically extensible.
- One account = one independent persistent Chromium partition + WebContents/runtime slot + task binding.
- First login and re-login after session expiry are manual user actions.
- No password/TOTP storage or automatic CAPTCHA/MFA handling.
- Shared normal Windows network; no per-account proxy rotation in V1.
- Account capability/health is exposed to Web/API/CLI/state files.
- Explicit quota/permission/entitlement rejection pauses the account. Health may later be rechecked non-invasively; re-enable is explicit.

## 3. Runtime pool / concurrency

- Hybrid worker pool: account profiles remain registered while only a configurable subset is active.
- Default max active workers: 3; configurable.
- Max generation tasks per account: 1.
- Different accounts may generate in parallel.
- Default account selection may be automatic, while callers can force a specific account.
- Automatic selection is based on readiness/busy/error/cooldown/queue health; it is not designed to evade quota/rate-limit/payment restrictions.

## 4. Codex control contract

Expose the same control core through:

1. localhost HTTP API;
2. JSON CLI;
3. machine-readable state files.

Codex may:

- start/stop Workbench;
- read account/worker/provider/project/job/output state;
- add/enable/disable account slots;
- request visible login/debug windows;
- submit single jobs and batch projects;
- force account assignment when requested;
- observe/recover jobs;
- obtain output paths/metadata/project completion events.

Codex may not:

- unlock the vault;
- read/print/save the master password;
- read raw browser passwords, Cookie headers, access/refresh tokens, raw profile secrets.

## 5. Vault / portability

- Portable directory may be moved between Windows systems.
- Account/profile data is intended to be migratable, but a moved profile may still legitimately require re-authentication due to service/browser/OS security behavior.
- Profile/session data is protected by a local password-based vault.
- User manually unlocks once per application run.
- Process exit re-locks the vault.
- Codex may start the service and detect `vault=locked/unlocked`, but cannot unlock it.

## 6. Program/data separation

```text
DolaWorkbench/
├─ app/          # replaceable
├─ runtime/      # replaceable
└─ data/         # durable, never overwritten by upgrades
   ├─ vault/
   ├─ profiles/
   ├─ accounts/
   ├─ projects/
   ├─ outputs/
   ├─ state/
   ├─ logs/
   └─ backups/
```

- Upgrades replace app/runtime, not data.
- Data/schema migrations create a backup first and roll back on failure.

## 7. Provider / generation scope

V1 production provider: `dola-web` only.

- Real Dola Web UI is the submission path.
- Internal observed requests are not promoted into a long-lived private API submission path.
- Observer watches lifecycle/result evidence only.
- Provider abstraction remains so an official provider may be added later.

Generation scope:

- T2V + I2V;
- Seedance 2.5;
- 5s/10s stable V1 target;
- common ratios including 9:16, 16:9, 1:1;
- 30s appears in UI/API as EXPERIMENTAL until its dedicated real-account Gate passes.

## 8. Job / project model

- Supports single job and batch project submission.
- Local source inputs may be passed by absolute Windows path; Workbench stages them into the project data area.
- Identity key includes at least `project + shot_id + revision`.
- Strong idempotency: retrying the same create request must not produce a second Dola generation.
- Explicit `new revision` is required for a new generation.
- Output is organized by project/shot/revision, independent of the account that generated it.

## 9. Lifecycle / recovery

Job state must distinguish at minimum:

`queued → preparing → submitting → accepted → generating → resolving → downloading → success`

plus recoverable/error/paused/cancelled states.

Failure policy:

- UI/observer/download interruption: recover the same account/task context first; do not regenerate.
- App crash/Windows reboot: on next unlock, recover persisted bindings/conversation/result/download state.
- Only confirmed generation failure may enter a new-generation decision.

## 10. Result / download policy

Use a layered highest-quality strategy, limited to media the normal authenticated session can actually access:

1. explicit Dola page download/original entry;
2. media candidates returned through normal generation/result lifecycle;
3. existing resolver identity chain (`vid`, `video_list`, `fallback_api`, etc.) when present and accessible.

Rank accessible candidates by actual technical quality such as resolution/bitrate/codec/file completeness. If the top candidate fails, fall back to the next accessible candidate.

V1 does NOT require visual first/middle/last-frame watermark QA. It should retain lightweight file validation (e.g. valid media/container and actual duration/resolution metadata).

## 11. Delivery to Codex

Per job return:

- job/project/shot/revision;
- account alias/id;
- provider/model/mode/duration/ratio;
- prompt/input references;
- state/error/recovery metadata;
- final output path;
- actual media metadata (at least duration/resolution/file size when available).

Per batch project emit a machine-readable `PROJECT_COMPLETE` event/state when all required shots reach terminal successful output.

## 12. Web workbench

The local web UI is a complete human workbench, not merely a monitor. It shares the exact same control core/state as Codex, and supports account management, login/debug window, job/project creation, queue, pause/recover/retry-new-revision, outputs and logs.

## 13. Audit/logging

- Full non-secret audit trail for account alias, job/project identity, model parameters, prompt/input references, state transitions, timestamps, result/download/recovery outcomes.
- Never persist secrets to audit/state/Git.

## 14. Gate rollout

Validation scale:

1. 1 account — complete end-to-end generation/result/download;
2. 2 accounts — session isolation + simultaneous one-per-account generation + no result cross-binding;
3. 5 accounts — scheduling/batch/recovery/worker pool;
4. ~20 accounts — configurable pooled runtime and sustained operation.

No later Gate is marked PASS based only on code or simulation; Windows real evidence is required where the behavior depends on Electron/Dola sessions.

## 15. V1 Production PASS

After one manual vault unlock, Codex can submit a multi-shot project and the system completes account selection, session wake, real Dola UI submission, lifecycle observation, recovery, highest-quality accessible media download, project/shot archival and `PROJECT_COMPLETE` without the user touching Dola, except when LOGIN_REQUIRED/MFA/CAPTCHA or an unrecognized major Dola UI change legitimately requires intervention.