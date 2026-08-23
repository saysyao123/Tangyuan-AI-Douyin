# Template｜MV Audio Timeline Package Contract v1.0

> Use after `BGM_LOCKED` and before any timing-dependent downstream stage.
> Required state on success: `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`.

## A. Audio identity

- Song:
- Artist:
- Exact version:
- Locked BGM reference/path:
- Source clip start:
- Source clip end:
- Rendered duration:
- Fade in/out:
- Speed/time-stretch:
- SHA-256:
- `AUDIO_IDENTITY_LOCKED = YES/NO`

## B. Trusted lyrics

- Lyric source/reference:
- Exact line count:
- Repeated line occurrences mapped:
- Text normalization notes:
- `LYRIC_TEXT_LOCKED = YES/NO`

## C. Primary timing evidence

- Evidence class: `SAME_VERSION_LRC | ASR_FORCED_ALIGNMENT | OFFICIAL_TIMED_LYRIC`
- Source/platform/tool:
- Song/platform ID if available:
- Tool/model/version if applicable:
- Raw evidence path/reference:
- Raw evidence SHA:
- Original timestamp basis: `FULL_SONG | LOCKED_CLIP`
- Transformation formula:
- Warnings/unmatched:
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = YES/NO`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = YES/NO`

## D. Independent cross-check

- Secondary evidence/tool:
- Result:
- Median line-start delta:
- Max line-start delta:
- Conflicts > 0.50s:
- Conflict resolutions:

If no independent source exists, explain why the single strong source still passes full per-line boundary audit.

## E. Line timeline

| ID | Lyric | Start | End | Primary Evidence | Secondary Delta | Confidence | QA |
|---|---|---:|---:|---|---:|---|---|
| L01 |  |  |  |  |  |  |  |

Required file: `line_timeline.csv`

## F. Anchor words / semantic hits

Only include words/phrases that materially control a visual event or cut.

| Anchor ID | Line | Word/Phrase | Start | End | Visual use | Evidence | QA |
|---|---|---|---:|---:|---|---|---|
| A01 |  |  |  |  |  |  |  |

Required file: `anchor_words.csv`

## G. Music events

| Event ID | Time | Type | Description | Editing use | Evidence | QA |
|---|---:|---|---|---|---|---|
| M01 |  | DOWNBEAT / ONSET / PICKUP / BREATH / RELEASE / PEAK / TAIL |  |  |  |  |

Required file: `music_events.csv`

## H. Ground-truth QA

Mandatory checks:
- [ ] locked audio SHA reverified
- [ ] first lyric boundary checked
- [ ] every lyric line start checked
- [ ] every lyric line end/display handoff checked
- [ ] middle representative line checked
- [ ] longest line checked
- [ ] final lyric + tail checked
- [ ] repeated identical lines mapped to distinct occurrences
- [ ] no unmatched line silently interpolated
- [ ] all source conflicts documented
- [ ] no visual edit boundary used as timing evidence

`ALIGNMENT_GROUND_TRUTH_QA_PASS = YES/NO`

Required file: `alignment_qa_report.md`

## I. Final package state

- `AUDIO_IDENTITY_LOCKED =`
- `LYRIC_TEXT_LOCKED =`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED =`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED =`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS =`
- `LYRIC_TIMELINE_LOCKED =`
- `MUSIC_EVENT_MAP_VERIFIED =`
- `AUDIO_TIMELINE_PACKAGE_LOCKED =`

If any required state is NO:
`STATE = AUDIO_TIMELINE_PACKAGE_BLOCKED`

## J. Package manifest

Required canonical directory:
`<ROUND>/AUDIO_TIMELINE_PACKAGE/`

Required files:
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

Record SHA for every durable artifact.
