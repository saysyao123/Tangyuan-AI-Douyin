# P1 Publish / Tracker Transaction Receipt v1

Status: **PASS / CANDIDATE / NOT PRODUCTION DEFAULT**

Branch: `refactor/mv-runtime-consolidation-v2`

## Scope

This receipt covers the canonical 30D/60 publish transaction from `S16_RELEASE_PACKAGE_READY` to `S17_PUBLISHED_DATA_COLLECTION_ACTIVE`.

Implemented controller:
- `04_HARNESS/tools/mv_runtime_publish.py`

Regression workflow:
- `.github/workflows/r3-mv-runtime-p1-publish-sync-tests.yml`

GitHub Actions run:
- run id: `32982693184`
- job id: `98222993849`
- conclusion: `success`

## Enforced behavior

1. Publish sync is rejected unless the canonical slot is exactly at S16 and the state/hash chain verifies.
2. `program_30d60=true` is required by the current controller.
3. Tracker schema is validated before writes.
4. Exactly one tracker row must match `slot_id`; zero or duplicate matches block.
5. `DNN-X` slot identity is checked against tracker `day` and `slot`; canonical slot lane must match tracker lane.
6. Explicit song family and audio asset are required. A conflicting nonblank tracker value blocks instead of being overwritten.
7. Existing packaging is preserved unless an explicit non-conflicting packaging value is supplied.
8. Unknown publish time is represented only as `timestamp_pending_backfill`; the controller never invents a timestamp.
9. Existing metric columns are preserved when publication fields are synchronized.
10. Notes are append-only for the publish-sync marker.
11. Tracker before/after SHA-256 values and publish-critical row snapshots are written into durable receipts.
12. Canonical `TRACKER_SYNC_RECEIPT` and `POST_PUBLISH_SYNC_RECEIPT` are created before state advancement.
13. S17 evidence is machine-audited after tracker/receipt preparation.
14. State advancement is delegated to `mv_runtime_state.py`; the publish controller does not directly mutate `CURRENT_STATE`.
15. A refused S16 -> S17 state transition restores the tracker bytes and removes transaction receipts created by the controller.
16. A second publish transaction is rejected after S17.
17. Post-publish metric evolution is allowed without invalidating publish identity.
18. Later changes to publish-critical tracker fields are detected by `mv_runtime_publish.py verify`.

## CI evidence

All steps passed:
- Build canonical 30D60 slot through S16.
- Reject duplicate and conflicting tracker state.
- Prove pending timestamp handling and transaction rollback.
- Commit publish transaction and advance exactly S16 -> S17.
- Allow metric evolution while detecting publish-critical tracker tampering.

## Remaining boundary

The current transaction uses atomic file replacement for tracker/receipt writes and rolls back ordinary controller/state failures. A process/host failure occurring between two separate filesystem writes is not claimed to be a filesystem-level ACID transaction. This is acceptable for the current Candidate Runtime and remains a later hardening concern if production evidence shows it matters.

## Promotion decision

`P1_PUBLISH_TRACKER_TRANSACTION = PASS_CANDIDATE`

Do not merge to `test/mv-web-r3` solely from this receipt. Continue Runtime consolidation and require a brand-new end-to-end MV regression before Production Default promotion.
