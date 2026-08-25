# 汤圆音乐映像｜30天60条｜D01-B HG02 Boundary Correction v1

Status: `CHG-A / USER LISTENING REQUIRED`
Slot: `D01-B`
Lane: `S / Stable-Fast`
Song family: `我救自己于人间水火`

## Why HG02 was re-opened

The user preferred variant B (`soft fade`) by listening. Subsequent strong lyric-timing evidence exposed a boundary conflict that must be corrected before Director work.

Public timed-LRC evidence for the same title/artist places the selected second-chorus occurrence at:
- semantic L1 start: source `91.11s` -> clip `0.00s`
- semantic L2 start: source `94.84s` -> clip `3.73s`
- semantic L3 start: source `98.71s` -> clip `7.60s`
- semantic L4 start: source `102.60s` -> clip `11.49s`
- next-verse semantic line starts: source `105.96s` -> clip `14.85s`

The locked raw Douyin asset is ~`15.9608s`, so a 15.96s ending includes roughly `1.11s` of the next lyric line. Machine music-event analysis independently detected a strong transition near `14.814s`, consistent with the timed-LRC boundary.

Therefore variant B is aesthetically preferred but violates the R3 hard rule: do not enter a new lyric line and then truncate it with a fade.

## Corrected listening candidate

### C | clean-line-end soft fade
- source recording unchanged: `DOUYIN_MUSIC_ASSET:7673442361086610233`
- content trim target: `14.82s`, immediately before the `~14.85s` next-line boundary
- fade: `14.30s -> 14.82s`, qsin soft fade
- container-reported MP3 duration: `14.863673s` (encoder padding included)
- audio: `MP3 / 44.1kHz / stereo / 192kbps`
- SHA-256: `f62f245251950dd7f25f3df2c55d551f5c051ee5cd707f0e5097768679add117`

## Gate behavior

- `HG01 = PASS` remains unchanged.
- song family and recording family remain unchanged.
- this is a **boundary-only correction**, not a version change.
- no Director / first-frame generation is authorized until the user approves C or rejects it.

Pass condition:
`user confirms C is comfortable / acceptable`.

After PASS:
`BGM_LOCKED -> copyright-safe Audio Timeline Package -> Natural Beat -> Director Allocation -> full first-frame set -> HG03`.
