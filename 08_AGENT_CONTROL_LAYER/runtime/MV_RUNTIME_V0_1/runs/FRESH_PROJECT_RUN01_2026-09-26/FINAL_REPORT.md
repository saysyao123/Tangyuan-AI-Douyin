# Fresh Project Run01 — Final S0 + S1 Test Report

Date: 2026-09-28
Run: FRESH_PROJECT_RUN01_2026-09-26

## Isolation rule

This run did not reuse prior project song choices, prior S0 shortlist, prior S1
media, or prior project timeline decisions.

Only frozen Runtime contracts/control rules were reused.

## S0 result

Fresh shortlist:
1. 告别 — 桃子假象 Peach Illusion
2. 一个人在家 — 想想XiangXiang
3. 阁楼上的广广 — 张醒婵 / Nono

Selected:
`告别`

Selection mode:
`AUTO_CONFIRMED_FOR_TEST`

S0:
`SEALED / PASS`

## S1A result

The selected Bandcamp page exposed a public full stream that the cloud runtime
could acquire without user upload.

Result:
`FULL_SOURCE_ACQUIRED`

Source duration:
201.978776s

This is the first fresh-project test in this runtime where S1A independently
acquired the complete selected song.

## S1B result

Source identity:
桃子假象 Peach Illusion — 告别

Release:
2026-05-15

Public lyric page:
available

S1B:
`PASS`

## S1C result

Audio structure:
- tempo approx 63.024 BPM
- first major boundary: 46.068s
- second major boundary: 78.437s
- repeated verse region begins ~78.437s
- later high-energy repeated region begins ~122.207s
- final decay begins ~192.702s

Strong repeated-structure evidence:
- verse-region similarity approx 0.992
- chorus-family similarity approx 0.982

### ASR failure and correction

Normal Whisper:
FAILED semantically / hallucinated text

Tiny Whisper:
FAILED semantically / hallucinated text

Demucs vocal separation + Whisper:
FAILED semantically / hallucinated text

The pipeline did not promote these transcripts into timeline truth.

Correct fallback:
`OFFICIAL_LYRIC_STRUCTURE + AUDIO_SELF_SIMILARITY`

Therefore S1C is sealed at:
`SECTION_LEVEL_VERIFIED`

Line-level lyric timestamps:
`NOT_VERIFIED`

This is an intentional evidence boundary, not a silent approximation.

## Selected production segment

`46.068390s -> 78.437007s`

Role:
first complete chorus region

Source duration:
32.368617s

Rendered artifact duration:
32.417959s

Artifact:
`桃子假象_告别_S1核心副歌_46.068-78.437s.mp3`

Why this segment:
- structural boundary lands on detected beat;
- entire repeated high-energy section is preserved;
- official lyric structure supports a verse -> chorus transition around this region;
- no arbitrary 15/20s truncation is used without semantic evidence.

## S1D

Mode:
`AUTO_CONFIRMED_FOR_TEST`

Decision:
use first complete chorus region

S1:
`SEALED / PASS_SECTION_LEVEL`

## Final verdict

`FRESH_S0_S1_RUN01 = PASS`

Important limitation:
line-by-line lyric timing is not validated for this song because all tested ASR
routes were unreliable. The Runtime correctly degraded to section-level truth
instead of hallucinating a line timeline.

This is considered a successful control-flow result.
