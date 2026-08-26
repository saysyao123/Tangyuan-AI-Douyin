# MV Runtime Web Bridge v1

> Status: `CANDIDATE / WEB EXECUTION BRIDGE`
>
> Purpose: allow a GitHub-connected web ChatGPT session to drive the canonical MV Runtime without pretending it can execute repository Python directly.

## 1. Boundary

The web client may create immutable JSON requests in:

`04_HARNESS/runtime_bridge/requests/`

GitHub Actions executes the authoritative Runtime controllers and writes immutable responses to:

`04_HARNESS/runtime_bridge/responses/`

The Bridge does **not** replace the Runtime controllers. It only exposes a narrow request/response control plane around them.

## 2. Command whitelist

Only these commands are accepted:

- `RESUME`
- `INIT_SLOT`
- `RECORD_HUMAN_GATE`
- `ADVANCE`
- `UPDATE_CONTEXT`
- `ROLLBACK`
- `PUBLISH_SYNC`

No request may contain shell fragments, arbitrary repository paths, custom executable names, or unregistered payload fields.

## 3. Mandatory web flow

### A. Start or resume a chat

1. Create one `RESUME` request.
2. Wait until the matching response file exists.
3. Read `status`, `postflight`, `next_guard`, `next_action`, and JIT reads from the response/runtime packet.
4. Do not infer a stage from chat memory while the request is pending.

### B. Fresh slot

If `RESUME` returns `ALLOCATE_NEW_SLOT`:

1. copy the returned `next_guard` exactly;
2. create `INIT_SLOT` for the returned `slot_id`;
3. wait for the response;
4. continue only from the canonical `S00_SLOT_CREATED` response.

### C. Normal production work

Creative or machine artifacts are still created through the normal GitHub/file workflow. The Bridge is not a content generator.

After any durable slot file changes — for example a candidate set, BGM package, timeline artifact, first-frame manifest, Human Gate receipt, or revision archive — an older guard becomes stale by design.

Before a mutating Runtime command, use a fresh guard from the latest Bridge response. When in doubt, issue another `RESUME`.

### D. Human Gates

A web client may submit `RECORD_HUMAN_GATE` only after the user has actually made the corresponding Human Gate decision in the current production instance.

The request must include:

- exact gate ID;
- the user's decision text;
- at least one approved artifact identity;
- the latest canonical guard.

Recording a Gate does not itself advance state. A separate fresh-guard `ADVANCE` request is required.

This separation prevents an old chat window from consuming a Gate receipt it never observed.

### E. Publish

`PUBLISH_SYNC` remains a real-world transition. It requires a non-empty real publish confirmation source and delegates to `mv_runtime_publish.py`.

The Bridge must never invent a publish confirmation from planned metadata, chat intent, or a release-ready state.

## 4. Optimistic-concurrency guards

### Allocation guard

Locks:

- Tracker SHA-256;
- selected allocation mode;
- slot ID;
- lane.

### Canonical guard

Locks:

- `CURRENT_STATE` SHA-256;
- full durable slot fingerprint SHA-256;
- current stage/token;
- transition sequence + last transition receipt hash;
- context revision + last context receipt hash;
- revision sequence + last rollback receipt hash.

The full slot fingerprint is required because some important events add durable artifacts without immediately changing `CURRENT_STATE`.

Any mismatch causes a controlled `REJECTED` response. The Bridge must not silently refresh a stale guard and continue the mutation.

## 5. Request immutability

A response stores the SHA-256 of its request.

Once a response exists:

- the request must not be edited;
- the response must not be overwritten;
- changing the request under the same ID is treated as control-plane tampering and blocks processing.

To retry, create a new request ID after reading current repository truth.

## 6. Request ID

Format:

`BR-YYYYMMDDTHHMMSSZ-SUFFIX`

Example:

`BR-20260826T180000Z-ABC123`

The suffix is uppercase alphanumeric and should make the ID unique.

## 7. GitHub Actions write-back

Workflow:

`.github/workflows/r3-mv-runtime-web-bridge.yml`

Execution model:

1. checkout with full history;
2. pull/rebase latest branch truth before execution;
3. process pending immutable requests serially per branch;
4. stage only Runtime response/state/Tracker write-back paths;
5. assert that request files were not modified;
6. bot commit;
7. pull/rebase again;
8. push to the same branch.

The workflow uses `contents: write`; CI uses read-only permissions.

## 8. Authority order

For web operation, use this order:

`GitHub repository truth -> Bridge RESUME response -> canonical Runtime controllers -> durable artifacts/receipts -> chat prose`

Chat memory is never a state authority.

## 9. Candidate boundary

This Bridge remains `CANDIDATE` until all of the following are green:

- Revision / Rollback CI;
- Zero-context Resume CI;
- Web Bridge concurrency CI;
- one live read-only request produces a committed response through GitHub Actions.

Do not replace the formal new-chat startup prompt until those gates pass.
