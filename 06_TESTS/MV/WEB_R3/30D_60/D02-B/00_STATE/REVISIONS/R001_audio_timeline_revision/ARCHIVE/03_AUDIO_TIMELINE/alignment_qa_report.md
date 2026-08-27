# D02-B Audio Timeline Alignment QA Report

- Status: **PASS**
- Slot: `D02-B`
- Locked audio SHA-256: `6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4`
- Candidate workflow run: `33054700945`
- Primary evidence: `ASR_FORCED_ALIGNMENT / trusted lyrics / Xingyu alignment.json + SWLRC`
- Tool/model: xingyu-lyrics-aligner 0.7.0 -> WhisperX CTC -> jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn, CPU

## Ground-truth audit

PASS. The exact HG02-locked audio SHA was reverified. Xingyu aligned all four trusted lyric lines with explicit line starts and ends. The reviewed candidate preserves alignment.json boundaries exactly. The 0.8s render fade begins at 14.586083s, 7.603s after the final aligned vocal release at 6.983s, so the fade cannot alter lyric timing.

| Line | Lyric | Start | End | QA |
|---|---|---:|---:|---|
| L01 | 有几次想你了 | 0.300s | 2.061s | PASS |
| L02 | 有几次忍住了 | 2.061s | 3.802s | PASS |
| L03 | 有几句想说的 | 3.802s | 5.602s | PASS |
| L04 | 都变成算了 | 5.602s | 6.983s | PASS |

## Raw-evidence checks

- PASS — Exact HG02 option-B SHA-256 equals 6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4.
- PASS — Xingyu report: line_count=4, aligned_or_partial_lines=4, status aligned=4.
- PASS — Xingyu report: input_alignment_characters=23, timed_character_entries=23, missing_character_timestamps=0.
- PASS — Xingyu report: character_count_matches=true, non_monotonic_line_count=0, warnings=[], swlrc_warnings=[].
- PASS — alignment.json and SWLRC agree on explicit line boundaries including final line end 6.983s.
- PASS — Reviewed candidate line_timeline.candidate.csv matches all four reviewed start/end boundaries to <=0.005s.
- PASS — No repeated lyric occurrence ambiguity exists in this four-line excerpt.
- PASS — HG02 option-B fade starts at 14.586083s; final vocal release is 6.983s, therefore fade is downstream of all lyric timing truth.

## Warnings / unmatched / repeated occurrence

- No alignment warnings; no unmatched lyric lines; no repeated-occurrence ambiguity in this four-line excerpt.

## Music-event analysis note

Music-event clock supporting analysis used the exact locked audio decoded mono at 22050 Hz with librosa 0.11.0 onset_strength/onset diagnostics (hop_length=256). Approximate beat-tracker tempo was 135.999 BPM. Selected acoustic accents are editor/director support only; they do not override forced-alignment lyric truth. Fade start and content end come from the locked render transform/audio identity, while VOCAL_RELEASE comes from forced alignment.

## Gate conclusion

`ALIGNMENT_GROUND_TRUTH_QA_PASS = YES`

This report validates timing truth against the exact HG02-locked audio identity. Acoustic onset analysis is supporting evidence for the music-event clock only and does not override lyric forced-alignment truth.
