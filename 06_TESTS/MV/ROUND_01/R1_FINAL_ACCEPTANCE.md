# Round 01｜Final Acceptance & Golden Sample

> Status: `USER_PASS`
> Date: `2026-08-21`
> Branch: `test/mv-round-01`

## 1. Final accepted work

- Song: `你有没有真的爱过我｜阿图表妹`
- Locked reference audio: `你有没有真的爱过我_建议剪辑片段_v1.mp3`
- Source interval: `00:01:23.800 -> 00:02:00.600`
- Final audio duration: `36.80s`
- Production structure: `8 first frames + 8 × 5s dynamic clips`
- Final accepted edit family: `R1_MV_v4_final_polish.mp4`
- Accurate subtitle timing source: `lyrics_exact_v3_1.srt`
- User final review: `整体效果不错`

This work is the first **Golden Sample** of the MV workflow.

## 2. Golden Sample meaning

Future MV work does not copy this song, paper/ink imagery, heroine, or exact shot list. It must not obviously fall below this sample in:

1. single-frame beauty;
2. lyric-to-visual hit;
3. director / camera variety;
4. dynamic stability;
5. editing rhythm;
6. subtitle readability and sync;
7. overall visual consistency.

## 3. Accepted visual system

Golden visual baseline for this round:

`新东方电影感 + 写实电影底层 + 克制诗意超现实`

Validated principles:
- lyric visual hit before decorative complexity;
- first frame is a `0-second dynamic anchor`, not a poster;
- world / material / palette continuity matters more than locking one permanent face across songs;
- one dominant visual event per 5s segment is stable;
- key segments may use 3-shot grammar inside 5s;
- restrained segments should not all degrade into `standing + slow push + robe movement`.

## 4. Validated production structure

For a ~36.8s song excerpt, this round validated:

- conceptual visual units: `6`
- production segments: `8`
- first frames: `8`
- raw dynamic material: `40s`
- final audio: `36.8s`

This provided enough trim / overlap / transition headroom.

This ratio is a validated reference, not a universal fixed quota for every future song.

## 5. Dynamic portrait-safety prompt rule

For any character-containing image-to-video prompt, the prompt must begin with this exact line, including the leading `***`:

`*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。`

R1 evidence:
- earlier wording triggered Seedance portrait-protection blocking on several clips;
- restoring this AI-fictional-character framing allowed the affected image-to-video generations to complete.

## 6. Editing findings accepted

### v1
Simple trimming to fit 36.8s was usable but some cut points felt less accurate.

### v2
Keeping more of each 5s internal action and compressing the 40s raw sequence through short overlaps / transitions produced noticeably better rhythm and more accurate perceived cut points.

User review: v2 was clearly better than v1.

### v3 / v3.1
Subtitle style was acceptable, but subtitle timing based on visual segment boundaries was wrong.

Fix:
- subtitle timing must come from the locked audio itself;
- use same-version LRC / ASR / forced alignment;
- never infer lyric times from the edit segment boundaries.

The corrected timing was user-reviewed as accurate.

### v4
Final polish kept the approved edit and lyric timing, only applying restrained finishing / tail treatment.

## 7. Subtitle Golden Reference

Basic subtitle system accepted for R1:
- Chinese lyrics required;
- light text;
- dark semi-transparent rounded background tightly fitted around the lyric;
- text visually centered vertically and horizontally inside the box;
- fixed comfortable lower safe-area placement;
- restrained fade behavior;
- no complex karaoke / word-by-word effects in the base system.

Timing source order for future Codex runtime:

`Whisper word timestamps -> known lyric constraint correction -> human spot check`

If same-version reliable LRC exists, it can be used as an additional alignment reference.

## 8. Watermark / source-quality status

Watermarks visible in this manual R1 test are **not treated as a creative or workflow failure**.

Reason:
- the manual test used watermarked generated video downloads;
- the Codex production environment can fetch / use the watermark-free HD outputs.

Codex hardening task:
- replace R1 manual watermarked sources with watermark-free HD equivalents before a publish-grade render;
- do not change the approved directing / timing / subtitle system merely to solve watermark removal.

Status: `DEFERRED_TO_CODEX_SOURCE_PIPELINE`

## 9. Items intentionally NOT promoted to hard rules yet

The following stay experimental:
- a larger cinematic camera-movement library for single-shot segments;
- automatic BGM discovery / exact music_id / Creator Center availability;
- automated publish-ready watermark-free asset retrieval;
- complex lyric effects;
- fixed universal first-frame-to-duration ratios.

These require more rounds / Codex tests before promotion.

## 10. Final acceptance

Round 01 creative output: `PASS`

Golden Sample status: `LOCKED`

Publish is not required for R1 completion. Platform music availability and watermark-free source replacement remain pre-publish / Codex tasks.
