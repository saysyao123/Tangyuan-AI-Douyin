# WEB R2｜AUDIO_TIMELINE_PACKAGE

> Status: `BLOCKED / NOT LOCKED`
> Rule: `04_HARNESS/rules/mv_audio_timeline.md`
> Contract: `04_HARNESS/templates/mv_audio_timeline_package_contract.md`

## Locked audio identity

- Song: `如果你也刚好抬头看树` — 孙天宇
- Source clip: `139.930s–177.050s`
- Rendered duration: `37.120s`
- Locked SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- BGM state: `LOCKED`

## Current truth

- exact lyric text/order: available / previously locked
- old WEB R2 v2 SRT/CSV: `REVOKED / FAILURE EVIDENCE ONLY`
- acoustic candidate timings: `DIAGNOSTIC_ONLY`
- strong timing source: `NOT YET ACCEPTED`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`

## Candidate public timed lyric found — REJECTED AS TRUTH

A public web result currently exposes a line-timed LRC for the same title/artist, but its later chorus timing places the relevant title/chorus family around roughly `02:14 / 02:20 / 02:23...`.

This conflicts materially with the locked WEB R2 source interval and actual clip lyric order around `02:19.930+`.

Classification:
`CANDIDATE_TIMED_LYRIC / VERSION_OR_TIMING_MISMATCH / NOT TRUSTED`

Lesson:
`same title + artist + visible timestamps != verified same-version LRC`.

Do not use this source to create `lyrics_exact.srt` unless a later version audit proves it matches the locked audio.

## Preferred resolution plan

### Primary route
Trusted known Chinese lyrics + Chinese-capable CTC forced alignment on the locked 37.120s audio.

Current implementation candidate:
`wangjiqing/xingyu-lyrics-aligner`

Why:
- accepts local audio + trusted lyric lines;
- builds Chinese CTC alignment text;
- runs forced alignment without letting ASR rewrite the official lyrics;
- exports raw `alignment.json`, `lyrics.lrc`, `report.json` needed for provenance.

### Independent cross-check
CJK/song-oriented known-lyrics alignment such as:
`ijuinryukichi/lyric-align`

Useful property:
- can use vocal separation + ASR word timings;
- matches official lyrics at character level;
- explicitly reports `unmatched` instead of silently inventing timestamps.

### Fast path if discovered later
A reliable same-version platform LRC may still be used, but only after:
- exact version/duration check;
- source ID/reference saved;
- original timestamps saved;
- exact `source_song_time - 139.930s` transformation recorded;
- ground-truth cross-check against the locked audio.

## Required files before PASS

- `audio_identity.json`
- `trusted_lyrics.txt`
- `alignment_raw.*`
- `alignment_provenance.json`
- `line_timeline.csv`
- `lyrics_exact.srt`
- `anchor_words.csv`
- `music_events.csv`
- `alignment_qa_report.md`
- `package_manifest.json`

## Hard Gate

Until every required Package state passes:
`STATE = AUDIO_TIMELINE_PACKAGE_BLOCKED`

No V3 edit, no new subtitle render, and no re-use of V2 timings.
