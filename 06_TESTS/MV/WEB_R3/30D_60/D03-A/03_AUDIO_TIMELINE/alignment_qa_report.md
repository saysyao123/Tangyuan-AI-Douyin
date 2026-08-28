# Audio Timeline Alignment QA

Status: `PASS / P2_CTC_RESOLVED`

- Slot: `D03-A`
- Exact audio SHA-256: `f298e1c7d99fe3cba9a2beed2fc6ecab406f946a3427895e5aad1aa4dfdf4769`
- Duration: `31.921625s`
- P0 timed lyric song id: `3419913748`
- P2: pinned Xingyu trusted-lyrics Chinese CTC on exact locked audio
- Trusted lyric lines: `14`
- P0/P2 median start delta: `0.200s`
- P0/P2 max start delta: `0.367s`

## >0.50s conflict review
- none

Decision: P2 direct exact-audio forced alignment is canonical timing truth; P0 remains retained supporting evidence. Lyrics/order/bounds are machine-validated; no threshold was relaxed.
