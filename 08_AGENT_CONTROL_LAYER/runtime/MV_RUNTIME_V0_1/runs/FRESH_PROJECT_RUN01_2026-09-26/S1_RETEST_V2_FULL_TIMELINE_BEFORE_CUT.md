# S1 Retest V2 — Full Timeline Before Cut

Status: HUMAN_AUDIO_REVIEW_PENDING

## Why V1 failed

The previous S1 selected a structurally high-energy chorus region before verifying
that the words were actually perceptible. Human listening found the segment was
mostly sustained "ah" vocalization with no useful concrete lyric content.

Therefore:
- previous final segment is REJECTED;
- CTC forced alignment alone is not sufficient evidence of audible lyrics;
- S1 must model the full song before cutting.

## New S1C order

1. FULL_SOURCE_ACQUIRED
2. whole-song structural timeline
3. identify lexical-vocal vs atmospheric/vocalise regions
4. construct candidate lyric ranges
5. validate candidate line boundaries
6. score lyric intelligibility
7. select MV production segment
8. cut audio
9. Human Audio Review
10. seal only after review

## Full-source facts

Song: 告别 — 桃子假象 Peach Illusion
Source duration: 201.978776s
Source: public Bandcamp full stream
Tempo estimate: ~63.02 BPM

## Whole-song usable timeline

### 0.000–29.805s
Role: INTRO / ATMOSPHERIC VOCAL ENTRY
Confidence: MEDIUM
Notes:
- first trusted lyric line produced a 28s forced-alignment outlier;
- do not use as a precise lyric-production region.

### 29.805–46.048s
Role: VERSE1_CLEAR_LEXICAL_REGION
Confidence: HIGH
Evidence:
- five consecutive lyric units have normal ordered timestamps;
- no duration outlier;
- strongest acoustic lexical-change proxy among tested production candidates;
- official MV promotion highlights the opening verse content.

### 46.048–47.428s
Role: TRANSITION

### 47.428–75.556s
Role: HIGH_ENERGY / VOCALISE-DOMINANT REGION
Confidence as concrete lyric region: LOW
Notes:
- forced alignment can place text here, but acoustic variation is materially lower;
- do not select solely because it is structurally a chorus/high-energy section.

### 75.556–104.443s
Role: INTERLUDE / ATMOSPHERIC TO VERSE2 ENTRY
Confidence: MEDIUM-LOW
Notes:
- verse2 first line also produced a long forced-alignment outlier.

### 104.443–122.187s
Role: VERSE2_CLEAR_LEXICAL_REGION
Confidence: MEDIUM-HIGH
Evidence:
- five ordered lyric units without duration outliers.

### 122.187–122.747s
Role: TRANSITION

### 122.747–192.702s
Role: HIGH_ENERGY / VOCALISE / EXTENDED OUTRO REGION
Confidence as concrete lyric region: LOW
Human evidence:
- previous 122.547–138.710s delivery was heard as mostly "ah" vocalization and rejected.

### 192.702–201.979s
Role: OUTRO DECAY

## Candidate comparison

A — VERSE1_CLEAR
29.805–46.048s
duration: 16.243s
local acoustic lexical-change proxy:
- spectral flux: ~0.0420
- MFCC delta: ~47.99
Status: PREFERRED

B — VERSE2_CLEAR
104.443–122.187s
duration: 17.744s
local acoustic lexical-change proxy:
- spectral flux: ~0.0390
- MFCC delta: ~20.46
Status: SECONDARY

C — previous chorus2
122.747–138.410s
duration: 15.663s
local acoustic lexical-change proxy:
- spectral flux: ~0.0299
- MFCC delta: ~16.51
Human result: REJECTED

## New selected candidate

Lyric range:
29.805–46.048s

Render range with handles:
29.555–46.398s

Rendered duration:
~16.875s

Selection rule:
prefer concrete, readable lyrics over nominal chorus/high-energy status.

## Seal state

S1 is NOT SEALED yet.

Next:
user listens to the V2 candidate.
If concrete lyrics are audibly present and boundaries feel natural:
HUMAN_AUDIO_LOCK -> PASS
Otherwise revise S1C only.
