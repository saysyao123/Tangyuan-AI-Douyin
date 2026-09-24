# S0 Pre-Selection Gates v0.1

## Gate A — Chinese-language only

Current user lock:
`PRIMARY_LANGUAGE = CHINESE`

Primary shortlist eligibility requires:
- song is confirmed or strongly evidenced to be primarily Chinese-language;
- ambiguous bilingual/foreign-language candidates do not enter Top 3 until verified.

Title language alone is not enough to prove song language.

## Gate B — Historical dedupe

Three policies:

### HARD_EXCLUDE
Formally selected, deeply produced, completed, or published songs.
They cannot enter a new-project Top 3.

### REGRESSION_ONLY
Songs already reserved/used for process testing or historical regression.
They remain usable for regression but not for a fresh project shortlist.

### ELIGIBLE
Prior candidate exposure alone does not count as "used".
If never formally locked or deeply produced, it may re-enter.

## Gate C — Song Family dedupe

Before ranking:
- merge same-song original/cover/remix observations into one Song Family;
- retain concrete reference variants under that family;
- do not count each variant as a separate candidate.

Cross-account repeat increases signal but does not create duplicate shortlist entries.

## Gate D — Pool freshness

Freshness tiers:
- `CURRENT_CORE_DIRECT`
- `HISTORICAL_CORE_VERIFIED`
- `SUPPLEMENTAL_CURRENT`
- `INDEX_PENDING`

Primary shortlist prefers core evidence.

Supplemental evidence can trigger recheck priority but does not silently replace core evidence.

## Gate order

`LANGUAGE -> HISTORICAL_DEDUPE -> SONG_FAMILY_DEDUPE -> FRESHNESS/EVIDENCE -> QUALIFICATION -> TOP3 -> HUMAN_GATE`
