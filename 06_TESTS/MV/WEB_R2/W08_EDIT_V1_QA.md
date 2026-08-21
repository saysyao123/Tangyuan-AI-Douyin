# WEB R2｜W08 Edit v1 + Pre-delivery QA

> Status: `FIRST_CUT_RENDERED / AWAITING_VIEWING_GATE`
> Output: `如果你也刚好抬头看树_MV_WEB_R2_第一版成片.mp4`

## 1. Final file technical state

- duration: audio `37.120s`; video `37.125s` (24fps frame quantization)
- raster: `720×1280`
- SAR: `1:1`
- DAR: `9:16`
- video: H.264 / yuv420p / 24fps
- audio: AAC stereo 44.1kHz
- final file SHA-256: `e7f4855b862c2df8bca303028a826f474775f5fd153760c4b047e213a9148f9f`

## 2. Ingest policy

All Seedance source audio was discarded. Final audio maps only the W02 locked BGM:
`如果你也刚好抬头看树_WEB_R2_W02_副歌扩展试听_v3.mp3`.

No AI-generated source audio survives in the first cut.

Platform marks were handled by a consistent safe crop rather than blur-box covering:
- crop keeps exact 9:16 ratio;
- top / lower-right generator marks are outside the retained image area;
- output is forced to `SAR 1:1` to prevent player-dependent stretching.

This crop is acceptable for first-cut viewing. Publish-grade W10 can still replace with watermark-free HD sources without retiming the approved edit.

## 3. Edit structure

Editing priority followed workflow:
`emotion flow > internal action integrity > musical cut point > equal clip duration`.

The edit is NOT S1–S9 full-clip concatenation.

### Timeline logic

1. opening lyric / `如果你也刚好抬头看树`
   - S1 monumental opening fragment
   - S2 orbit fragment
   - purpose: scale hook → character-space parallax

2. `我要学着树叶翩翩起舞`
   - S3 emotional close detail
   - S4 body / fabric movement
   - purpose: intimate texture → actual movement

3. bird section
   - S6 notice/reveal fragment
   - S5 breathing-space fragment
   - S6 bird/relation tail
   - purpose: call / mystery / discovery without overusing a single source

4. `好吧哎哟哎哟`
   - later S2 orbit material used as playful visual rise

5. `一颗心叽叽喳喳飞过了树梢`
   - S7 clean early peak
   - short S1 canopy insert
   - S7 clean final canopy resolve
   - the ambiguous large-fabric loop section around the middle/late S7 source was excluded

6. repeated title line
   - S8 rooftop/sky reset, shortened

7. final cloud release
   - S9 slowed for longer visual breathing
   - final frame held for the musical release / fade

## 4. Whole-set trim decisions implemented

- S1 duplicated middle low-angle beats: removed from edit.
- S1 vs S5 giant-tree repetition: S5 is used only as a short bird-section breathing fragment.
- S7 risky fabric topology: ambiguous ~middle/late material excluded.
- S8 vs S9 repetition: S8 shortened; S9 receives the long ending.

## 5. Subtitle v1

No Whisper / faster-whisper was claimed or used.

Known exact same-version lyric sequence + locked-audio waveform/phrase-resolution valleys + W03 tempo/structure evidence were used for a **basic line-level first-cut alignment**.

Line-level working boundaries:
- `0.48–3.55` 如果你也刚好抬头看树
- `3.60–7.62` 我要学着树叶翩翩起舞
- `7.68–10.68` 喊几声布谷布谷
- `10.74–12.81` 或许少有人知道
- `12.87–15.79` 有鸟儿是这样叫
- `15.85–18.88` 好吧 哎哟哎哟
- `18.94–22.95` 一颗心叽叽喳喳飞过了树梢
- `23.01–27.60` 如果你也刚好抬头看树
- `27.66–36.28` 向一朵白云学习如何漂浮

Style:
- light CJK text;
- dark semi-transparent tight box;
- lower safe area;
- horizontally centered;
- restrained fade;
- one line for current lyrics.

This is a first-cut subtitle layer. Viewing gate may still reveal small line-edge adjustments; do not claim word-level ASR precision.

## 6. Pre-delivery QA

PASS:
- exact locked BGM used;
- no Seedance source audio mapped;
- total audio duration = 37.120s;
- standard 720×1280 / SAR1:1 / 9:16 output;
- no visible generator marks in sampled delivery frames after safe crop;
- S1 repeat removed;
- S7 topology-risk fabric section removed;
- S8 shortened relative to S9;
- final cloud release gets long tail;
- subtitle box stays in lower safe zone in sampled frames;
- final fade completes after lyric release.

Technical rescue caught before delivery:
- an intermediate crop preserved non-square SAR; pre-delivery ffprobe detected it and the file was rebuilt at SAR1:1 before handoff. User did not need to identify this issue.

## 7. Current gate

`AESTHETIC_GATE / FIRST-CUT VIEWING`.

Next action after viewing:
- if edit/lyric timing needs adjustment: W08 v2 only;
- if accepted: enter W09 retrospective / promotion decision;
- do not redo generation unless a specific source shortage is exposed by the cut.
