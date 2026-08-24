# Schema Notes

`observed_works.csv` is the cumulative positive-evidence work fact table keyed by `aweme_id`.
`snapshots.csv` records each public refresh.
`song_normalization.csv` maps each observed work to `SONG_FAMILY` / `AUDIO_VERSION` when evidence is sufficient.
`song_repeat_candidates.csv` ranks only cross-account positive repeats.
`direct_douyin_evidence.json` stores exact core-account work links used for HG01 review.
