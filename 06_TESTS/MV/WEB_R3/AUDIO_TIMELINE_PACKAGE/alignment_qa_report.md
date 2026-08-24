# WEB R3｜Audio Timeline Alignment QA

Status: `PASS_FOR_LINE_TIMELINE / WORD_LEVEL_NOT_CLAIMED`

## Identity
- production audio SHA-256 matches locked HG02 receipt: PASS
- duration container 24.320s / decoded content 24.286621s: PASS
- Douyin asset id `7670880580757867270`: PASS

## Strong timing route
Primary: same-title / same-artist public LRC, first occurrence.

Canonical line starts preserved from source:
`0 / 3 / 6 / 8 / 12 / 15 / 18 / 20s`.

## Independent structure checks
Supporting RMS valleys around expected transitions:
- 3s -> ~3.12s
- 6s -> ~6.03s
- 8s -> ~8.51s
- 12s -> ~12.07s
- 15s -> ~15.59s
- 18s -> ~18.11s
- 20s -> ~20.54s

The LRC is integer-second precision; waveform is not promoted to timing truth and is used only as structural confirmation.

## Lyric order / repeated occurrence
- the locked trend-native clip is the first hook occurrence;
- eight-line order matches the public full-release first occurrence;
- no repeated-occurrence ambiguity exists inside the 24.32s clip.

## Tail
The next public LRC line is timestamped 24s, while the decoded trend asset reaches near-silence at ~24.277s and HG02 user listening passed. No new downstream timing is inferred beyond 24.000s; 24.000–24.320 remains release/tail headroom.

## Gate decision
- line-level timeline: PASS
- canonical SRT: PASS
- semantic anchor windows: PASS for director use
- exact word-level karaoke timing: NOT CLAIMED / not required for R3-B visual calibration

`AUDIO_TIMELINE_PACKAGE_LOCKED = YES` for line-level MV production coordinates.

If future karaoke/word-by-word treatment is requested, run a Chinese-capable forced alignment sub-pass without changing the locked BGM identity.
