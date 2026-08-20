# R1S06 Subtitle Alignment｜Audio-first timing lock

## Problem found
The first lyric-burn pass timed subtitles by visual segment boundaries. That is invalid because the edit overlaps/crossfades the eight source clips and the sung lyric onsets do not equal the segment cut points.

## Hard rule
Subtitle timing must be derived from the **locked audio itself**, never from video-segment boundaries.

Preferred production path:
1. lock final Reference BGM audio;
2. run Whisper / word timestamps on that exact file;
3. use the known target lyrics as constrained text to correct transcription errors;
4. produce sentence-level and, when useful, word-level timestamps;
5. manually spot-check waveform/onset for ambiguous sung phrases;
6. burn subtitles only after the timestamp file is locked.

Fallback for this R1 before Codex Whisper is available:
- source track: `你有没有真的爱过我｜阿图表妹`
- locked source interval: `01:23.800 -> 02:00.600`
- exact-version public LRC used as timing anchor:
  - 01:24 你的回应是一直沉默
  - 01:29 只剩下落寞
  - 01:32 我有什么错
  - 01:34 短暂柔情似流星划落
  - 01:39 你有没有真的爱过我
  - 01:44 我是你诗的哪个段落
  - 01:49 落款第几页
  - 01:52 第几次临摹
  - 01:54 还是匆匆一瞥就略过

Converted to the 36.8s locked clip timeline by subtracting `01:23.800`:
- 00:00.200 你的回应是一直沉默
- 00:05.200 只剩下落寞
- 00:08.200 我有什么错
- 00:10.200 短暂柔情似流星划落
- 00:15.200 你有没有真的爱过我
- 00:20.200 我是你诗的哪个段落
- 00:25.200 落款第几页
- 00:28.200 第几次临摹
- 00:30.200 还是匆匆一瞥就略过

## Deliverable
R1 correction output:
- `R1_MV_v3_1_lyrics_timing_fixed.mp4`
- `lyrics_exact_v3_1.srt`

## Codex hardening requirement
When Codex/Whisper is available, rerun the exact 36.8s locked audio with word timestamps and compare against this LRC-derived timing. Preserve the same subtitle visual style; only adjust timestamps if Whisper/audio inspection shows a meaningful onset difference.
