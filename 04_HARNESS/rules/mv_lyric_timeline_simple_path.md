# Rules｜MV Lyric Timeline Simple Path v1.0

> Status: `EXPERIMENT / ACTIVE FOR OSS_OPT_R1`
> Goal: one simple, stable, repeatable path that answers only two questions:
> 1. What are the complete lyrics actually sung in the locked BGM clip?
> 2. When does each lyric line start and end?

## 1. Single Happy Path

`HG02 exact BGM locked`
→ `verify locked audio SHA`
→ `FULL-CLIP ASR TRANSCRIPT on the exact locked audio`
→ `ONE lyric-text audit against the same audio`
→ `trusted_lyrics.txt locked`
→ `Xingyu forced alignment on the same locked audio + trusted lyrics`
→ `ONE automatic timing QA`
→ `line_timeline.csv + lyrics_exact.srt`
→ `LYRIC_TIMELINE_LOCKED`
→ `S03`

No alternate route is attempted on a normal PASS path.

## 2. Complete lyric text｜HARD

The full locked audio clip is the authority for lyric completeness.

The following are discovery/support only and MUST NOT be treated as the complete lyric text by themselves:
- Douyin work caption;
- creator description;
- hashtags;
- a partial lyric quote;
- another MV's visible text;
- public Web lyrics that have not been checked against the locked clip.

A caption containing four lines does not prove a 15-second clip contains only four lines.

Default method:
- run one full-clip Chinese ASR pass over the exact HG02 audio;
- preserve every sung line from first sung syllable to last sung syllable;
- perform one lyric-text audit against the same audio;
- correct transcription mistakes once if needed;
- after the audit, write `trusted_lyrics.txt` and do not reopen lyric discovery unless the user/audio proves it wrong.

## 3. Timing｜HARD

After trusted lyrics are locked, use one primary timing engine only:
- `xingyu-lyrics-aligner 0.7.0` from the locked shared runtime;
- same exact HG02 audio SHA;
- Chinese forced alignment;
- prefer explicit `alignment.json` line start/end and character timestamps;
- do not infer final-line end from clip duration when raw alignment provides an explicit end.

## 4. One-pass automatic QA

AUTO PASS only when all are true:
- audio SHA equals HG02 locked SHA;
- transcript audit says complete lyric text from first to last sung line;
- trusted lyric line order matches the audited transcript;
- alignment reports every trusted line aligned;
- missing character timestamps = 0;
- alignment warnings = 0;
- line times are monotonic and within the locked audio duration;
- every line end comes from raw alignment evidence or an explicitly documented boundary;
- SRT exactly matches locked line text and times.

If any item fails:
- stay `AUDIO_TIMELINE_BLOCKED`;
- fix the specific lyric text or alignment issue;
- rerun the same path once;
- do NOT automatically introduce a second model, Web evidence sweep, waveform guessing, or a new per-song tool.

## 5. Minimal locked deliverables

Only these assets are required to pass lyric timing:
1. `audio_identity.json`
2. `trusted_lyrics.txt`
3. `raw_evidence/xingyu/alignment.json` (plus engine report if produced)
4. `line_timeline.csv`
5. `lyrics_exact.srt`
6. `lyric_timeline_qa.json`
7. `package_manifest.json`

`anchor_words.csv` and `music_events.csv` are NOT prerequisites for lyric-timeline lock in this experiment.
They are downstream Natural Beat / Director enrichment assets.

## 6. One audit, not repeated evidence hunting

Normal production must not run multiple independent lyric/timing solutions merely to feel safer.
The safety model is:

`one exact audio + one full-clip transcript + one text audit + one forced alignment + one automatic QA`

Only a concrete failure opens an exception path.

## 7. Current D02-B correction

The previous four-line trusted lyric set for `有几次想你了` is INVALID because it came from a core creator caption and does not cover the complete locked BGM clip.
Do not seal or promote that four-line timeline.
Rebuild D02-B from the full locked BGM using this simple path before S03.
