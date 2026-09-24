# S0 Song Pool Fresh Refresh — 2026-09-24

Status: BEST_EFFORT / CORE_INDEX_PENDING

## 1. Hard filters for this run

1. Only Chinese-language songs may enter the primary shortlist.
2. Historical formal/deep projects are removed from new-project Primary Candidates.
3. Regression/test songs may remain in archive but cannot enter new-project Top 3.
4. Candidate-only songs are not treated as used songs.
5. Song Family dedupe occurs before shortlist construction.
6. Same Song Family across original/cover/remix remains one family until a concrete reference is chosen.
7. A concrete reference URL/ref is still required for every Primary Candidate.

## 2. Core-account refresh

Primary ecosystem:
the existing 9 trusted core accounts in `01_REFERENCE_ACCOUNT_REGISTRY.md`.

A fresh public-web recheck was performed on 2026-09-24.

Result:
- public search/indexing still did not reliably surface current direct works for the named 9-core-account registry;
- therefore this run must NOT claim "all 9 core accounts updated to 2026-09-24";
- unresolved accounts remain `INDEX_PENDING`;
- historical verified direct works remain valid pool evidence;
- supplemental current platform evidence may update WATCH priority, but cannot impersonate core-account direct evidence.

This follows the earlier 2026-09-09 rule:
"not found in public index" != "account posted nothing".

## 3. Current supplemental Chinese-song signals

These are NOT promoted to core-primary merely from platform evidence.

### 茶花开了，该回家了
Current public evidence remains active in early/mid September:
- multiple direct Douyin works around 2026-09-06 to 2026-09-08;
- current Douyin/Qishui hot-song playlists still list the song.

Status:
`SUPPLEMENTAL_WATCH / CORE_RECHECK_PRIORITY`

### 雀跃
Current Qishui hot-song playlists still contain the song.

Status:
`SUPPLEMENTAL_WATCH / CORE_REFERENCE_NEEDED`

### 小半
Current hot-song playlists contain it; a 2026-09-03 Douyin cover also shows active reuse.

Status:
`SUPPLEMENTAL_WATCH / CORE_REFERENCE_NEEDED`

### 九月底
Multiple direct Douyin works were publicly indexed on 2026-09-23/24.

Status:
`SUPPLEMENTAL_FRESH_WATCH`

It is not yet a core-pool candidate without trusted-core evidence.

## 4. Primary-pool rule for S0 Test Run01

Because current core direct indexing is incomplete, this test uses:

`HISTORICAL_VERIFIED_CORE_POOL + CURRENT_DEDUPE + CHINESE_ONLY_FILTER`

Current platform signals are shown only as a supplemental watch layer.

This is sufficient to test S0 selection mechanics, but not sufficient to claim a full 2026-09-24 core-account refresh.

## 5. Next future improvement

When a trusted core-account new work is directly recoverable:
- append work-level evidence;
- normalize Song Family;
- apply Chinese-language filter;
- apply used-song ledger;
- then allow it to compete for Top 3.
