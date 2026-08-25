# D01-B｜Audio Timeline Alignment QA v1

Status: `PASS / AUDIO_TIMELINE_PACKAGE READY`

## Audio identity

- Locked BGM: user-approved variant B
- Douyin asset: `7673442361086610233`
- Canonical B SHA-256: `cc3da15b00cd554c810c590e61ccc97bedc72db058202bdf850bcefd5bba00e5`
- Duration: `15.986939s`
- Speed/time-stretch: none
- Fade: `15.1608s + 0.8s`, linear

## Ground-truth route

Primary:
`trusted lyric identity -> exact-B time-domain decode -> faster-whisper zh word timestamps -> character-level trusted-text mapping`

Two audio inputs were evaluated:
1. canonical B mix decoded to PCM;
2. time-identical vocal-enhanced PCM for silent-failure comparison.

The canonical mix provided the selected timeline. Enhancement never changed the time origin.

## Occurrence audit

A prior public-LRC interpretation selected the second chorus. That interpretation was rejected because its third and fourth semantic lines failed alignment against the locked audio.

The exact audio matches the **first chorus**:
- L01 self-rescue;
- L02 self-love;
- L03 remember the bloom;
- L04 continue seeking.

This correction changed only the lyric occurrence mapping. The locked BGM did not change.

## Line audit

| Line | Start | Vocal end | Coverage | Order | QA |
|---|---:|---:|---:|---|---|
| L01_SELF_RESCUE | 0.000 | 4.260 | 100% | 1 | PASS |
| L02_SELF_LOVE | 4.540 | 7.840 | 100% | 2 | PASS |
| L03_REMEMBER_BLOOM | 8.420 | 11.880 | 100% | 3 | PASS |
| L04_SEEKING | 12.360 | 15.560 | 100% | 4 | PASS |

All starts are monotonic. All normalized trusted characters mapped. No following repeated hook was detected inside the file.

## Boundary audit

- Opening begins directly with L01; no previous-line pollution detected.
- Gaps `4.260–4.540`, `7.840–8.420`, `11.880–12.360` are musical/respiratory transitions, not missing lyric lines.
- L04 completes at approximately `15.560s`.
- `15.560–15.987s` is the approved fade tail; no fifth subtitle line is created.

## Evidence status

- Audio identity: PASS
- Lyric occurrence: PASS
- Line order: PASS
- First/middle/final line audit: PASS
- Repeated occurrence audit: PASS
- Music-event map: PASS as supporting evidence
- Plaintext persistence: intentionally replaced by semantic IDs + normalized hashes; authorized text must hash-match before subtitle rendering.

`ALIGNMENT_GROUND_TRUTH_QA_PASS = YES`
`LYRIC_TIMELINE_LOCKED = YES`
`MUSIC_EVENT_MAP_VERIFIED = YES`
