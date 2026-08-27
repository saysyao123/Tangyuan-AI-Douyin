# OSS_OPT_R1｜Audio Timeline Route Policy v1.1

Status: `EXPERIMENT LOCKED / D02-B P1 VALIDATED / PROMOTE_RULE_CANDIDATE`
Scope: `test/mv-oss-optimization-r1` only. Stable `test/mv-web-r3` is unchanged until OSS_OPT_R1 close audit.

## Production goal

For short-form MV production, Audio Timeline answers only:
1. What complete lyrics are actually sung in the locked HG02 BGM?
2. When does each lyric line start and end?

The default path optimizes for: `accurate + stable + fast + one audit`.

## Route priority

### P0｜Same-version timed lyric / LRC

Use when a reliable same-version LRC or official timed lyric is available and matches the locked BGM occurrence.

Path:
`HG02 exact BGM -> verify identity -> same-version LRC/timed lyric -> clip offset/occurrence mapping -> one QA -> line timeline + SRT -> LOCK`

Reference production evidence: D01-A `如果风会替我说话`.

This is the fastest route and should be tried first when the source is genuinely same-version.

### P1｜D01-B Lightweight Faster-Whisper｜DEFAULT AI ROUTE

Use when P0 is unavailable, ambiguous, or not sufficiently trustworthy.

Locked implementation:
- `faster-whisper==1.2.1`
- model: `small`
- device: `cpu`
- compute: `int8`
- language: `zh`
- `word_timestamps=true`
- audited trusted-text mapping by normalized Chinese character sequence

Happy Path:
`HG02 exact BGM`
-> `verify audio SHA`
-> `one full-clip Faster-Whisper pass with word timestamps`
-> `one lyric-text audit against the same locked BGM`
-> `trusted lyrics locked`
-> `trusted-text -> Faster-Whisper timestamp mapping`
-> `one automatic coverage + monotonic QA`
-> `line timeline + SRT`
-> `LOCK`

A first unprompted transcript is candidate text, not unquestionable lyric truth. The single lyric audit may correct ASR wording once. After that audit passes, do not reopen lyric discovery unless the audio/user proves it wrong.

P1 PASS criteria:
- exact HG02 audio SHA matches;
- complete sung-line set confirmed in the one audit;
- every trusted line maps in order;
- line coverage = 100% for the normal PASS path;
- line starts are strictly monotonic;
- line boundaries remain inside the locked BGM duration;
- no unresolved repeated-occurrence ambiguity;
- canonical S03 QA artifact and manifest exist.

Reference production evidence: D01-B `我救自己于人间水火`.
Reference D02-B validation: workflow runs `33059906090` and `33060055071`.

Measured D02-B result:
- cold first pass model work: `7.523s` total (`3.097s` init + `4.426s` transcript);
- warm/cached trusted-text pass: `6.002s` total (`1.227s` init + `4.775s` transcript);
- lightweight cache: about `547 MB` / `573,157,329 bytes`;
- user lyric audit: `PASS / 歌词OK`;
- seven-line trusted text: `7/7` lines, `45/45` normalized characters, `100%` coverage each;
- line starts monotonic;
- `sequence_ratio=1.0`;
- canonical Runtime advanced to `S03_AUDIO_TIMELINE_LOCKED / AUDIO_TIMELINE_PACKAGE_LOCKED`;
- decision: `LIGHTWEIGHT_ALIGNMENT_PASS`.

### P2｜Xingyu CTC forced alignment fallback

Use only when P1 has a concrete failure signal or materially higher timing precision is explicitly required.

Typical triggers:
- incomplete full-clip ASR after the one audit;
- one or more trusted lines cannot reach acceptable coverage;
- non-monotonic mapping;
- repeated chorus/occurrence ambiguity remains unresolved;
- difficult vocal/mix causes Faster-Whisper timing failure;
- explicit word/character-level precision requirement beyond normal MV line timing.

P2 is NOT the default production route.
Do not restore/install the heavy Xingyu runtime unless a P2 trigger is present.

Canonical fallback implementation and D02-B validation evidence remain preserved in:
`06_TESTS/MV/OSS_OPT_R1/XINGYU_FALLBACK_ARCHIVE_v1.md`.

## Rules that apply to all routes

- `creator caption != complete lyric truth`.
- The locked HG02 audio is the completeness authority.
- Do not run P0 + P1 + P2 merely for reassurance.
- Stop at the first route that passes its QA.
- A concrete failure escalates to the next route; absence of failure does not.
- One normal P1 path contains one human lyric-text audit, not repeated evidence hunting.
- `anchor_words.csv` and `music_events.csv` belong downstream to Natural Beat / Director and do not block lyric-timeline lock in this experiment.
- Waveform/BPM may support music structure but must not invent lyric timestamps.
- Stable R3 branch remains unchanged until this experiment is formally promoted through the OSS_OPT_R1 close audit.

## Durable close evidence

- Route close receipt: `06_TESTS/MV/OSS_OPT_R1/AUDIO_TIMELINE_ROUTE_CLOSE_RECEIPT_v1.json`
- D02-B package: `06_TESTS/MV/WEB_R3/30D_60/D02-B/03_AUDIO_TIMELINE/package_manifest.json`
- Canonical QA: `06_TESTS/MV/WEB_R3/30D_60/D02-B/03_AUDIO_TIMELINE/alignment_qa_report.md`
- Lock receipt: `06_TESTS/MV/WEB_R3/30D_60/D02-B/03_AUDIO_TIMELINE/LYRIC_TIMELINE_LOCK_RECEIPT.json`
- Runtime state: `S03_AUDIO_TIMELINE_LOCKED`
