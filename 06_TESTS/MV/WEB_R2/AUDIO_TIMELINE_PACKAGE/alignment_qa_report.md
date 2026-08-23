# WEB R2｜AUDIO_TIMELINE_PACKAGE Ground-truth QA

Status: **PASS for Route B timing evidence; pending machine-gate execution at report creation time.**

## Locked audio
- SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- content timeline: `37.120s`
- MP3 container: `37.146122s`
- source offset: `139.930s`

## Strong Route
- class: `ASR_FORCED_ALIGNMENT`
- method: trusted Chinese lyrics -> CTC emissions -> forced alignment; no free ASR transcription
- model: `jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn`
- revision: `d2af85f00e501bb8b8bcedef3b5c51eabb883088`
- model weight SHA-256: `de031fd4b29e0c0667e5346450fadfe1326c89936b888b59c4ede608db763ee4`
- 92 target tokens -> 92 aligned spans

## Line-start QA
- CTC vs prior diagnostic acoustic candidate median absolute delta: `0.125s`
- maximum: `0.593s`
- >0.50s: `L03=0.593s, L04=0.524s, L06=0.543s`
- Those diagnostic conflicts are not silently averaged. L03/L04/L06 are supported by the same-recording coarse LRC much closer to the CTC boundary.
- CTC vs public same-recording whole-second LRC median absolute delta: `0.290s` (supporting only; coarse LRC is not promoted).
- >0.50s coarse-LRC conflicts: `L02=0.632s, L10=0.768s`; L02/L10 are instead strongly supported by the prior locked-audio acoustic candidate.

## Repeated-occurrence QA
The first and second chorus occurrences of L01-L07 were independently aligned on two different source regions of the same master.
- second-minus-first source-time shift median: `81.527s`
- max absolute deviation from median across 7 lines: `0.061s`
- total shift range: `0.082s`
- result: highly consistent repeated-occurrence mapping; no chorus-occurrence swap detected.

## Vocabulary warnings
`翩 / 叽 / 喳 / 梢` map to `<unk>` in this Chinese CTC vocabulary. None is the first character of a lyric line, so canonical line starts are not dependent on these unknown tokens. Canonical line ends use the next aligned line start; phrase releases are kept in `music_events.csv`. The `飞过树梢` anchor includes a terminal unknown token and is explicitly review-noted.

## Canonical clock decision
- Lyric line start: first CTC-aligned token of the trusted line.
- Lyric line end: next aligned lyric line start; final line ends at `37.120s`. This matches the existing project xingyu adapter semantics.
- Phrase release / reverb / rests: separate music-event clock, never used to rewrite lyric starts.

## Final QA conclusion
**PASS.** Strong Route B raw evidence is retained with exact model/audio identity and supporting conflict analysis. No diagnostic timing was renamed or promoted. Machine gates must still independently validate the finished package before `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`.
