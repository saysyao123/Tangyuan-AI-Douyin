# WEB R2｜Audio Timeline Provenance v1

Status: `HIGH_CONFIDENCE_LINE_TIMELINE / NOT YET FORCED_ALIGNMENT_LOCKED`

## Locked audio identity
- Source: `如果你也刚好抬头看树-孙天宇.mp3`
- Source duration: `196.127347s`
- Locked excerpt: `如果你也刚好抬头看树_WEB_R2_W02_副歌扩展试听_v3.mp3`
- Fingerprint-measured source offset: `139.930s`
- Locked excerpt duration: ~`37.12s`
- Prior locked SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`

## Evidence chain
1. Audio fingerprint cross-correlation between the locked excerpt and original master gives offset `139.930s` with normalized correlation ~`0.99997`; therefore W02 source offset is correct.
2. Public timed-LRC candidate for the exact title/artist/release gives the second chorus sequence around source `02:20–02:52`; official/JOOX lyric text and the 3:16 commercial release structure agree with that sequence.
3. The public LRC is integer-second coarse timing, so it is not used directly as final subtitle timing.
4. Acoustic phrase-boundary analysis was run on the locked 37.12s master itself (stereo center/harmonic activity, phrase valleys/rises) to refine line starts/ends.
5. Refined source-time starts remain close to the timed-LRC anchors and preserve the same monotonic lyric order.

## Critical correction
The previously assumed excerpt lyric order was wrong. The locked excerpt does **not** begin with a complete `如果你也刚好抬头看树` line. The first full sung line is `我要学着树叶翩翩起舞`, and the excerpt continues through `坐下来别那么严肃` before the fade/tail.

This explains why WEB R2 V1/V2 could not be fixed merely by shifting the old nine-line SRT.

## Confidence boundary
The new CSV is suitable as a high-confidence line-level edit/subtitle planning timeline and is materially stronger than V1/V2. However, under `mv_audio_timeline.md`, `AUDIO_TIMELINE_PACKAGE_LOCKED` remains reserved for a true Strong Route with retained raw evidence (preferably same-version platform timed lyrics with stable provenance and/or trusted-lyrics forced alignment). Do not rename this file to `lyrics_exact.srt` until that final Gate passes.
