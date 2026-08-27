# CODEX R2｜Result Report Template

> Write the completed report to `06_TESTS/MV/CODEX_R2/reports/CODEX_R2_RESULT.md`.

## 1. Run identity

- Branch:
- Baseline commit:
- Target slot/lane:
- Song:
- Final Canonical stage reached:
- Final state token:
- Start time / finish time:
- Codex environment:

## 2. Outcome

Choose one:
- `PASS_FOR_PROMOTION_REVIEW`
- `PASS_WITH_BLOCKED_EXTERNAL_CAPABILITY`
- `PARTIAL_NEEDS_RUNTIME_FIX`
- `FAIL_CODEX_OPERATOR`

Summary:

## 3. Human Gates

| Gate | Decision source | Exact user decision preserved? | Approved artifact(s) | Receipt | Result |
|---|---|---:|---|---|---|
| HG01 | | | | | |
| HG02 | | | | | |
| HG03 | | | | | |
| HG04 | | | | | |
| HG05 | | | | | |

## 4. Runtime / operator efficiency

- Startup core files read before first resume:
- Total `codex_mv_operator.py` invocations:
- `resume` count:
- `init` count:
- `accept-gate` count:
- `run-until` count:
- other mutation commands:
- Web Bridge request/response transport used by Codex: YES/NO
- Human interactions excluding required five gates:
- Git commits:

## 5. External handoffs

| Type | Stage | Reason | User action required | Resume succeeded? |
|---|---|---|---|---|

## 6. Audio Timeline

- Locked BGM identity:
- Route used: P0 / P1 / P2
- Why earlier route failed or was unavailable:
- Did processing stop at first passing route?:
- New model/dependency installed per slot?:
- Canonical package/final gate result:

## 7. Creative pipeline

- Director Thesis:
- Primary Visual Engine:
- Lyric-hit strategy:
- Camera/subject/space strategy:
- WHY CUT HERE implementation:
- Creative Drift issues found and nearest-layer patches:
- First-frame generation method:
- Dynamic generation method:
- Regeneration count and reasons:

## 8. Source normalization / edit

- Normalization triggered?:
- Trigger reason:
- Source atom count if multi-shot:
- Edit Map result:
- Picture Preview QA:
- HG04 result:

## 9. Subtitle / final

- Subtitle baseline reused?:
- Subtitle QA:
- Final Tech QA:
- Final file identity/hash:
- HG05 result:
- Release Package result:

## 10. Maintainability audit

- Core Runtime files modified?:
- If yes, generic reproducible reason:
- New helper scripts created under core?:
- Any D03-B-specific core code?:
- Any second state machine introduced?:
- Any manual Canonical state/receipt edits?:
- Any secrets or large media committed?:

## 11. Failures / blockers

For each:
- stage;
- symptom;
- root cause;
- nearest-layer patch;
- retry count;
- whether it is a Codex limitation, environment limitation, content failure, or Runtime defect.

## 12. Quality assessment

Compare with accepted Tangyuan MV baseline:
- lyric visual hit:
- continuity:
- camera grammar:
- emotional arc:
- cut motivation:
- subtitle readability:
- technical cleanliness:
- overall quality delta vs current accepted baseline:

## 13. Promotion recommendation

Choose:
- `PROMOTE_CODEX_ADAPTER`
- `PROMOTE_WITH_PATCHES`
- `KEEP_EXPERIMENTAL`
- `REJECT`

Specify exactly which files/ideas should be promoted. Do not recommend wholesale merge of the Codex test branch without a clean promotion diff.