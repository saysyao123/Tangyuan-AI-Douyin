# S0 SONG_SELECTION — Test Run01 Report

Status: DELIVERED_TO_HUMAN_GATE

## What was tested

1. Chinese-language hard filter.
2. Historical selected/deep-project dedupe.
3. Regression/test-material exclusion.
4. Song Family dedupe.
5. Core-vs-supplemental evidence separation.
6. Max-3 shortlist.
7. No automatic winner.
8. No S1 timeline leakage.

## Result

PASS for pre-Human-Gate mechanics.

Primary shortlist:
- A 向山河林响
- B 若爱有尽头
- C 阳光洒落

All three:
- are treated as Chinese-language candidates;
- are not HARD_EXCLUDE / REGRESSION_ONLY in the current ledger;
- represent unique Song Families;
- have historical verified trusted-core reference URLs;
- are delivered without detailed Audio Version / Timeline analysis.

## Freshness limitation

The fresh 2026-09-24 public recheck did not reliably expose current direct works for the full trusted 9-account registry.

Therefore this run demonstrates selection mechanics with:
`HISTORICAL_CORE_VERIFIED`

It does not claim a complete "latest 9-core-account catalog".

## Why current platform songs are not in Primary Top 3

Current public signals for 茶花开了，该回家了 / 雀跃 / 小半 / 九月底 are useful WATCH evidence.

But the S0 contract intentionally does not allow supplemental platform signals to silently replace trusted-core direct evidence.

## Current stop point

S0 is now at:
`HUMAN_REFERENCE_GATE`

No S1 work is allowed until the user selects one concrete reference or rejects all and requests another S0 round.
