# WEB R2｜W08 v2 Audio-led Rebuild + QA

> Status: `REVIEW_CUT_RENDERED / INTERNAL_QA_PASS`
> Date: `2026-08-21`
> Output: `如果你也刚好抬头看树_MV_WEB_R2_第二版成片.mp4`
> SHA-256: `ff1bbb67427b0067001ebe97f5e0d7bcb3e4c9c434606c2c833ba280647adc3b`

## 1. Why v2 was rebuilt from scratch

W08 v1 was revoked because picture cuts and subtitle burn-in were created before a valid lyric-time analysis existed. v2 does not reuse v1 subtitle times or v1 edit-map timing.

The rebuild order was:

`locked 37.120s BGM -> exact nine-line lyric text -> constrained line-level audio alignment -> phrase/beat map -> picture edit -> R1 Golden subtitle styling -> subtitle boundary QA -> final technical QA`.

No Seedance source audio participates in timing.

## 2. Line-level timeline used by v2

| # | Start | End | Lyric |
|---|---:|---:|---|
| 1 | 0.470 | 4.810 | 如果你也刚好抬头看树 |
| 2 | 5.451 | 10.680 | 我要学着树叶翩翩起舞 |
| 3 | 10.954 | 13.189 | 喊几声布谷布谷 |
| 4 | 13.827 | 15.850 | 或许少有人知道 |
| 5 | 16.788 | 18.800 | 有鸟儿是这样叫 |
| 6 | 19.702 | 21.980 | 好吧 哎哟哎哟 |
| 7 | 23.470 | 26.770 | 一颗心叽叽喳喳飞过了树梢 |
| 8 | 28.439 | 32.540 | 如果你也刚好抬头看树 |
| 9 | 32.618 | 35.650 | 向一朵白云学习如何漂浮 |

Durable local assets during rebuild:
- `lyrics_exact_v2.srt`
- `lyrics_timeline_v2.csv`

### Alignment method honesty

No Whisper / faster-whisper run is claimed.

The line-level map was rebuilt from the locked audio itself using the exact known lyric order constrained against multiple acoustic/music signals:
- phrase onset strength;
- vocal-band energy;
- phrase/breath valleys;
- beat grid (~103.36 BPM evidence from W03);
- repeated chorus phrase correspondence;
- semantic line ordering and final vocal resolution.

This is substantially different from W08 v1's loose visual/phrase estimate because every subtitle line now has an explicit start/end, deliberate subtitle-free breath gaps, and the edit map is derived after those line windows rather than vice versa.

Cross-round rule promotion still prefers ASR/forced alignment or reliable same-version timed lyric evidence. The current line map remains project-level evidence until direct playback review confirms the result.

## 3. v2 picture edit map

The v2 edit is rebuilt around real lyric/phrase windows rather than equal clip lengths.

Key decisions:
- L1: S1 scale opening -> S2 Arc/orbit, preserving the strongest one-take sample;
- L2: S3 emotion close-up -> S4 body/leaf-dance motion;
- L3: S6 listener -> bird discovery;
- L4: S5 giant-tree breathing frame;
- L5: S6 bird/reaction material;
- L6: S4/S3 playful movement/reaction;
- L7: clean early S7 motion peak only, then S1 canopy release;
- S7 late ambiguous white-fabric material is completely excluded after final self-audit;
- pre-L8 musical gap enters S8 high-space reset early;
- L8: S8 rooftop/sky one-take, slightly lengthened to preserve continuity;
- L9: S9 cloud release, with visual/music tail continuing after lyric ends.

No equal-duration mechanical allocation is used.

## 4. Subtitle Golden restoration

v2 restores the Round 01 accepted base system:
- Chinese lyric text;
- light text;
- dark semi-transparent rounded background tightly fitted around each actual line;
- text visually centered horizontally and vertically inside box;
- consistent padding;
- fixed comfortable lower safe area;
- restrained ~0.08/0.10s appearance/disappearance;
- max 1 line in this song;
- no karaoke / word-by-word effect.

Representative first/middle/longest/final lyric frames were sampled and inspected before delivery.

## 5. Final QA

### Picture
- 720×1280;
- 24fps;
- SAR `1:1`;
- DAR `9:16`;
- no black-frame event detected by blackdetect;
- crop removes visible generation/platform marks from retained frame;
- known S1 duplicate low-angle material not reintroduced;
- known S7 ambiguous late-fabric region excluded;
- S8/S9 transition deliberately separates reset vs final cloud release.

### Audio
- only the locked-BGM-derived audio stream is present;
- final subtitle render copied the base-v2 BGM audio stream bit-for-bit;
- audio elementary-stream SHA was identical before/after subtitle burn-in;
- no Seedance source audio is mapped into the final output.

### Subtitle timing implementation
For every lyric line, frames were sampled before start / inside line / before end / after end to verify subtitle appearance/disappearance follows the v2 timing table rather than picture cuts.

### Output
- file duration: `37.125s` at 24fps frame quantization, representing the locked 37.120s BGM timeline;
- H.264 video + AAC 44.1kHz stereo;
- SHA-256 `ff1bbb67427b0067001ebe97f5e0d7bcb3e4c9c434606c2c833ba280647adc3b`.

## 6. Gate

`INTERNAL_QA_PASS`.

This file is the second-cut review artifact requested by the user. If direct playback confirms lyric sync/overall rhythm, promote the current line-level timing asset to the project lock and proceed to final-polish/round-close decisions. If a line boundary is still objectively wrong, classify it as `TECHNICAL_RESCUE` and correct the timing asset before any further polish.