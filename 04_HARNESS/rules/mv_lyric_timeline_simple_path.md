# Rules｜MV Lyric Timeline Simple Path v1.1

> Status: `EXPERIMENT / D02-B VALIDATED`
> Goal: accurate complete lyrics + accurate line timing with the shortest proven path.

## 1. Route priority｜HARD

Stop at the first route that passes QA.
Do not run multiple alignment systems merely for reassurance.

### P0｜Same-version timed lyric / LRC

Use first when a reliable same-version LRC or official timed lyric exists and its occurrence matches the locked HG02 audio.

`HG02 exact BGM -> verify audio identity -> timed lyric/LRC -> clip offset or occurrence mapping -> one QA -> line timeline + SRT -> LOCK`

Reference: D01-A `如果风会替我说话`.

### P1｜D01-B Lightweight Faster-Whisper｜DEFAULT AI ROUTE

Use when P0 is unavailable, ambiguous, or not sufficiently accurate.

Locked implementation:
- `faster-whisper==1.2.1`
- model `small`
- CPU `int8`
- language `zh`
- word timestamps enabled
- normalized Chinese trusted-text mapping in sequence order

Happy Path:

`HG02 exact BGM locked`
→ `verify locked audio SHA`
→ `ONE full-clip Faster-Whisper pass with word timestamps`
→ `ONE lyric-text audit against the same locked audio`
→ `trusted lyrics locked`
→ `map audited trusted text to the Faster-Whisper timestamp stream`
→ `ONE automatic coverage/monotonic QA`
→ `line_timeline.csv + lyrics_exact.srt`
→ `LYRIC_TIMELINE_LOCKED`
→ `S03`

The transcript is a candidate, not unquestionable lyric truth. The single lyric-text audit may correct ASR wording once. After that audit passes, do not reopen lyric discovery unless the audio/user proves the text wrong.

### P2｜Xingyu CTC forced alignment｜FALLBACK ONLY

Use only when P1 produces a concrete failure signal or when materially higher character/word timing precision is explicitly required.

Triggers include:
- incomplete lyric recovery after the single audit;
- unresolved low mapping coverage;
- non-monotonic line timing;
- repeated-occurrence ambiguity;
- difficult vocal/mix causing P1 timing failure;
- explicit high-precision word/character timing requirement.

Xingyu remains preserved and pinned, but it is not loaded/restored during a normal P0/P1 PASS path.
See: `06_TESTS/MV/OSS_OPT_R1/XINGYU_FALLBACK_ARCHIVE_v1.md`.

## 2. Complete lyric text｜HARD

The full locked HG02 audio is the authority for completeness.

The following are support/discovery only and MUST NOT be treated as the complete lyric text by themselves:
- Douyin work caption;
- creator description;
- hashtags;
- a partial lyric quote;
- another MV's visible text;
- public Web lyrics not checked against the locked clip.

`creator caption != complete lyric truth`.

Normal P1 text procedure:
- listen/transcribe the whole locked clip from first sung syllable to last sung syllable;
- preserve every sung line;
- perform one lyric-text audit against that same audio;
- correct ASR text once if needed;
- remove non-sung punctuation from timing truth if necessary;
- lock trusted lyrics.

## 3. P1 automatic timing QA

AUTO PASS only when all are true:
- audio SHA equals HG02 locked SHA;
- complete lyric text has passed the one audit;
- every trusted lyric line maps in order;
- normal PASS line coverage = 100%;
- starts are strictly monotonic;
- line times are within the locked audio duration;
- no unresolved repeated-occurrence ambiguity;
- generated SRT exactly matches locked line text and selected line timing.

If P1 fails a concrete QA item:
- stay `AUDIO_TIMELINE_BLOCKED`;
- diagnose that specific failure;
- escalate to P2 Xingyu only when the P1 failure cannot be corrected within the same lightweight route.

Do not automatically add Web evidence sweeps, waveform timing guesses, a second lightweight model, or a per-song helper.

## 4. Minimal lyric-timeline lock assets

Required in this experiment:
1. `audio_identity.json`
2. `trusted_lyrics.txt`
3. one raw timing evidence artifact from the selected route
4. `line_timeline.csv`
5. `lyrics_exact.srt`
6. `lyric_timeline_qa.json`
7. `package_manifest.json`

For P1, raw evidence is the Faster-Whisper timestamp/mapping report.
For P2, raw evidence is Xingyu `alignment.json` plus its engine report.

`anchor_words.csv` and `music_events.csv` are NOT prerequisites for lyric-timeline lock. They belong downstream to Natural Beat / Director enrichment.

## 5. D02-B validation

The previous four-line trusted lyric set for `有几次想你了` is INVALID because it came from a creator caption and did not cover the full locked BGM.

P1 validation on the full locked B audio produced seven audited lyric lines and then achieved:
- `7/7` lines mapped;
- `100%` character coverage for every line;
- `sequence_ratio = 1.0`;
- strictly monotonic line starts;
- Faster-Whisper model work about `6.002s` on the cached trusted-text run;
- lightweight cache about `547 MB`.

Decision: `D01B_LIGHTWEIGHT_FASTER_WHISPER = P1 PASS / DEFAULT AI ROUTE CANDIDATE`.

Xingyu remains archived as P2 fallback and is not required for normal D02-B continuation.
