# MV Runtime Consolidation｜P1 Controlled Legacy Migration Receipt v1

- Date: 2026-08-26
- Branch: `refactor/mv-runtime-consolidation-v2`
- Status: `P1 LEGACY MIGRATION PASS / CANDIDATE`
- Production default: `NO`

## Problem

Historical R1/R2/R3 projects contain useful evidence but use inconsistent filenames and may contain multiple revisions, e.g. `DIRECTOR_PLAN_v1.md` and `DIRECTOR_PLAN_v2.md`.

The Runtime must not infer that the lexically newest file is authoritative.

## Delivered

Tool:
`04_HARNESS/tools/mv_runtime_migrate.py`

Commands:
- `plan`
- `promote`
- `verify`

Migration contract:

`AUDIT LEGACY SLOT`
→ `REPORT MISSING / LEGACY / AMBIGUOUS`
→ `EXPLICIT MAINTAINER SOURCE SELECTION`
→ `VALIDATE SELECTED SOURCE`
→ `MATERIALIZE IDENTICAL CANONICAL COPY`
→ `WRITE SOURCE + CANONICAL HASH PROVENANCE`
→ `VERIFY MIGRATION MAP`.

## Hard behavior

- no automatic latest-version selection;
- ambiguous legacy artifacts remain BLOCKED until a source is explicitly selected;
- historical files are never deleted or overwritten;
- canonical artifacts are never overwritten by a second migration;
- source must match the Artifact Registry alias family;
- source must remain inside the slot root;
- selected source must pass the artifact's validation checks;
- implicit cross-format copy is forbidden, e.g. legacy Markdown Human Gate receipt cannot silently become canonical JSON;
- every promoted artifact is recorded in `00_STATE/LEGACY_MIGRATION_MAP.json` with source and canonical SHA-256 hashes, selector and reason.

## Regression fixture

Historical source: `D01-B`, copied to a disposable CI directory.

Verified:
1. migration plan detects `DIRECTOR_PLAN_v1.md` + `DIRECTOR_PLAN_v2.md` as ambiguous;
2. tool does not guess;
3. CI explicitly selects `DIRECTOR_PLAN_v2.md`;
4. canonical `05_DIRECTOR/DIRECTOR_PLAN.md` is materialized;
5. v1 and v2 historical originals remain untouched;
6. canonical artifact validates;
7. migration map hashes verify;
8. second overwrite attempt is rejected;
9. Markdown-to-JSON Human Gate migration without explicit conversion is rejected.

## CI evidence

Workflow:
`.github/workflows/r3-mv-runtime-p1-migration-tests.yml`

Run ID: `32979259007`
Conclusion: `success`
Commit: `88b74d3ba9d0ddac04630b8736446020c29e0038`

## Boundary

This tool does not magically reconstruct artifacts that never existed. A missing Natural Beat, first-frame manifest, Visual Source Map, etc. remains missing and must remain visible in historical audit.

Migration improves authority resolution; it does not rewrite history.
