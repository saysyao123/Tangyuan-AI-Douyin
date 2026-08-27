# OSS OPT R1｜HG01 Gate Hardening v1.2

Status: `CORRECTED / CORE DATABASE STRATEGY RESTORED / EXPERIMENT BRANCH ONLY`
Date: `2026-08-27`
Branch: `test/mv-oss-optimization-r1`

## Executive correction

D02-B exposed two separate problems that were initially mixed together:

1. **real correctness bug** — some supposed direct Douyin evidence URLs opened an older landing work whose page merely listed the desired new work;
2. **over-correction** — while fixing that URL bug, HG01 discovery drifted from the original R3 core-benchmark database strategy into broad public-Web candidate search.

The first problem must remain fixed.
The second change is rejected and reverted.

## Restored R3 HG01 path

Default production strategy is again:

`CORE BENCHMARK ACCOUNTS -> DATA CENTER UPDATE/READ -> SONG_FAMILY REPEAT/VALUE RANKING -> SIMPLE DIRECT MV HANDOFF -> USER HG01`

Meaning:
- use the user-locked benchmark accounts as the main observation universe;
- update/persist observed works into the Data Center;
- rank songs from database repeat/value signals;
- add a new supplemental benchmark account only when it is genuinely worth following long term;
- do not perform broad web-wide song search for every MV;
- do not let public-search metadata availability decide which songs are worthy candidates.

## Simple HG01 delivery

The human-facing Gate should contain only what helps the user choose:

1. song name / SONG_FAMILY;
2. one short reason it entered from the core database;
3. the corresponding creator's corresponding Douyin MV link(s);
4. one short risk note only when useful.

The user should not need to read Evidence taxonomy, Tier A/B/C, coverage reports or search methodology.

## Retained hardening｜LINK IDENTITY ONLY

The valid hardening discovered in D02-B remains:

`DELIVERED DIRECT WORK URL MUST OPEN THE CITED MV ITSELF`

A creator's older work page that merely lists a newer target work is:

`DISCOVERY_ONLY / NOT USER DELIVERY`

This check protects link integrity only. It must not become the song-discovery algorithm.

## Runtime separation principle

HG01 now explicitly separates three concerns:

### A. Discovery authority
`CORE BENCHMARK DATA CENTER`

### B. Delivery simplicity
`CORE CREATOR MV DIRECT`

### C. Link correctness guard
`LANDING WORK IDENTITY VERIFIED`

The Runtime Guard may block a bad link or incomplete Gate packet, but it must not decide creative/trend discovery by requiring web-wide evidence retrieval.

## D02-B correction

The temporary formal candidate set built mainly from public-Web evidence:
- 《雨后轻风有香》
- 《甲乙丙丁》
- 《差一步美满》

has been superseded as a Human Gate packet.

D02-B is reset to:

`HG01_CORE_DATABASE_REBUILD_REQUIRED`

No user song decision had been recorded, so no Canonical rollback is needed. Canonical slot state remains `S00_SLOT_CREATED`.

## CI policy

Workflow:
`.github/workflows/r3-hg01-delivery-guard-tests.yml`

The test no longer assumes the live slot must contain a web-wide Evidence Pack.
It now proves:

1. reset/incomplete D02-B cannot accidentally record HG01;
2. policy files explicitly require core-database-first discovery and reject broad web-wide song search as the default;
3. a synthetic core-database candidate packet with verified direct MV links can complete the real Canonical chain:

`RECORD_HUMAN_GATE -> ADVANCE -> VERIFY_STATE`

## Promotion decision correction

Previous classification:
`PROMOTE_RUNTIME_CANDIDATE / HG01 DELIVERY GUARD`

is narrowed to:

`PROMOTE_RULE_CANDIDATE / DIRECT-LINK IDENTITY GUARD`

Do **not** promote the broad Evidence Pack discovery requirements to stable production.

Stable `test/mv-web-r3` remains untouched during this experiment.
