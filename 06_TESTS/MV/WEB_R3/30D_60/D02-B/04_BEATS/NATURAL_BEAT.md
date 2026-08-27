# D02-B｜Natural Beat v1

Status: `READY_FOR_S04_LOCK`
Song: `有几次想你了`
Lane: `S / Stable-Fast`
Audio authority: `03_AUDIO_TIMELINE / P1 D01-B Lightweight Faster-Whisper / LOCKED`
Locked audio duration: `15.386083s`

## Scope

This artifact contains semantic / emotional Natural Beats only.
It does **not** allocate characters, locations, props, camera grammar, first frames, generation segments, or final edit fragments.

Natural Beat rule:
`semantic/emotional unit != lyric line count != 5-second quota != production segment count`.

## Emotional spine

The excerpt moves through a restrained letting-go process:

`memory surfaces -> feeling is suppressed -> words are abandoned -> time/weather passes -> attachment remains, but release is chosen`.

The emotional direction is not a sudden recovery and not a dramatic breakup confrontation.
It is a quiet reduction of resistance: from repeated private impulses to an explicit final act of letting go.

## Natural Beats

### NB01｜0.000–1.880｜想起 / LONGING SURFACES｜HOOK

Lyrics:
`有几次想你了`

- Semantic task: longing becomes explicit immediately; the excerpt opens from an already-existing memory rather than introducing a relationship.
- Emotional state: involuntary recollection, soft ache, no outward action yet.
- Energy: low-to-medium opening pulse; emotionally legible from the first line.
- Key semantic anchor: `想你`.
- Role: `HOOK`.
- Boundary note: the line ends at `1.880s`; the short gap before the next line is breathing space, not a new beat.

### NB02｜2.020–3.640｜忍住 / SELF-RESTRAINT

Lyrics:
`有几次忍住了`

- Semantic task: converts passive longing into active restraint.
- Emotional state: feeling remains, but expression is intentionally held back.
- Energy: compressed inward; tension increases without becoming louder.
- Key semantic anchor: `忍住`.
- Role: `TENSION / HOLD`.
- Relationship to NB01: same emotional subject, opposite behavioral direction — first the feeling appears, then it is contained.

### NB03｜3.780–7.180｜想说 → 算了 / ABANDONED EXPRESSION｜TURN

Lyrics:
`有几句想说的`
`都变成算了`

- Semantic task: completes one cause-and-consequence unit: there are words ready to be spoken, but the speaker actively cancels them.
- Emotional state: hesitation becomes resignation.
- Energy: rises through `想说`, then drops on `算了`.
- Key semantic anchors: `想说` -> `算了`.
- Role: `TURN`.
- Grouping reason: these two lines should remain one Natural Beat because separating them would break the semantic action and its result.

### NB04｜7.320–10.700｜雨停 / 风过 / TIME PASSES

Lyrics:
`有几场雨停了`
`有几阵风过了`

- Semantic task: shifts from internal choices to accumulated passage of time.
- Emotional state: distance, repetition, gradual cooling rather than one decisive event.
- Energy: steadier and more spacious after the resignation of NB03.
- Key semantic anchors: `雨停` / `风过`.
- Role: `BRIDGE / EXPANSION`.
- Grouping reason: rain stopping and wind passing form one parallel temporal structure; they describe elapsed cycles, not two separate emotional decisions.

### NB05｜10.860–15.386｜舍不得 → 放下 / CHOSEN RELEASE｜PEAK + RELEASE

Lyrics:
`有多舍不得，也该放下了`

Vocal timing:
- lyric starts: `10.860s`
- sung line ends: `14.260s`
- post-lyric audio tail: `14.260–15.386s`

- Semantic task: states the central contradiction explicitly — attachment is still real, but release is chosen anyway.
- Emotional state: strongest admission of attachment followed by acceptance; not emotional erasure.
- Energy: emotional peak on `舍不得`, then downward release on `放下了`, followed by a short breathing tail.
- Key semantic anchors: `舍不得` -> `放下`.
- Role: `PEAK + RELEASE`.
- Ending rule: the final `1.126s` audio tail belongs to the release of this beat and should remain available to downstream directing/editing as breathing space.

## Beat summary

| Beat | Time | Semantic movement | Energy role |
|---|---|---|---|
| NB01 | 0.000–1.880 | memory / longing surfaces | HOOK |
| NB02 | 2.020–3.640 | longing is consciously restrained | TENSION / HOLD |
| NB03 | 3.780–7.180 | words form, then are abandoned | TURN |
| NB04 | 7.320–10.700 | repeated weather marks passing time | BRIDGE / EXPANSION |
| NB05 | 10.860–15.386 | attachment admitted, release chosen | PEAK + RELEASE |

## Downstream constraints

- Director may combine or split production segments differently; Natural Beat count does not dictate source count.
- Do not create one shot merely because one lyric line exists.
- Do not force a cut at every lyric start.
- Preserve the semantic pairings `想说 -> 算了`, `雨停 -> 风过`, and `舍不得 -> 放下` unless later production constraints require a justified adaptation.
- Specific visual answers begin only at Director stage.

`NATURAL_BEAT = READY`
`NEXT = S04_NATURAL_BEAT_LOCKED -> S05 DIRECTOR A/B`
