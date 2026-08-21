# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W02`
- STAGE_NAME: `Reference BGM acquisition + exact clip lock`
- STATE: `PREVIEW_V2_RENDERED / AWAITING_AUDIO_GATE`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Objective

从一首新的候选歌开始，在网页端重新跑完整 MV 流程，并逐 Stage 标记：

- `AUTO`
- `HUMAN_GATE`
- `EXTERNAL_REQUIRED`
- `PARTIAL`
- `BLOCKED`

重点不是假装全自动，而是测出网页端的真实自动化边界。

## Golden Quality Floor

R1 Golden Sample 是质量下限，不要求复制纸墨视觉：
- 单帧美感不得明显更低；
- 歌词视觉命中不得明显更低；
- 导演/运镜重复度不得更高；
- 动态失败必须做根因分析；
- 剪辑与字幕时间不得低于 R1 最终通过水平。

## Stage Map

- `W00` Bootstrap / capability baseline
- `W01` Song discovery / benchmark-assisted selection
- `W02` Reference BGM acquisition + exact clip lock
- `W03` Music / lyric / Beat analysis
- `W04` Director concept + production-unit allocation
- `W05` First-frame prompts + image generation
- `W06` Dynamic prompts + external Seedance generation gate
- `W07` Dynamic QA + retry design
- `W08` Edit + subtitle alignment + final polish
- `W09` Automation retrospective / Round close

## W00 Result — LOCKED

Actual state: `AUTO`

Verified capability baseline:
- GitHub connector read/write: available and verified on `test/mv-web-r2`.
- Public Web research: available; W01 validated actual discovery use.
- Files / conversation uploads / Library analysis: available.
- Image Generation interface: available; production quality is not pre-claimed and will be tested in W05.
- Local audio/video processing: ffmpeg, ffprobe, MoviePy, pydub and OpenCV available.
- Dedicated Whisper / faster-whisper: not present in current local environment; later subtitle work must not pretend Whisper ran.
- Direct Seedance execution: not available in current exposed toolset; do not assume browser/login control.
- User local machine/browser control: unavailable.

No user intervention was required in W00.

## W01 Result — LOCKED

Research state: `AUTO`.
Total stage state: `HUMAN_GATE`.

User selected:
- Reference song: `如果你也刚好抬头看树`
- Artist / official vocal version: `孙天宇`

## W02 Current Evidence

### Official reference version confirmed

Primary version:
- Title: `如果你也刚好抬头看树`
- Artist: `孙天宇`
- Type: official vocal master
- Official streaming duration evidence: `3:16`
- Companion instrumental version: `如果你也刚好抬头看树 - 伴奏`, also `3:16`
- International release metadata: `2026-07-22`
- Rights metadata: `℗ 2026 Columbia Records China`

### User file received and verified

Uploaded source:
- filename: `如果你也刚好抬头看树-孙天宇.mp3`
- measured duration: `196.127347s` (`3:16.127`)
- codec: `MP3`
- bitrate: `320 kbps`
- sample rate: `44.1 kHz`
- channels: `stereo`
- embedded title / artist / album match the confirmed master
- source SHA-256: `ad30cefef4e4a5ffedab81b26b1e38a0b679bf2b32752b6ebd29f5d97f18d7ab`

Conclusion:
- accepted as the W02 production source;
- the rejected 3:12 Bilibili user upload is not used.

### Preview v1 — REJECTED

- source range: `130.72s–163.82s`
- rendered duration: `33.149388s`
- user feedback: opening contains material before the true chorus start; ending cuts the final lyric before completion.
- root cause: excerpt boundary detection was too loose and treated a broader lyrical region as the chorus instead of structurally aligning the repeated chorus itself.
- result: `REJECTED / LOCAL_CORRECTION_ONLY`; no downstream stage was changed.

### Re-analysis and structural alignment

The supplied master was re-analyzed using repeated-section alignment rather than approximate lyrical location.

Evidence:
- first repeated chorus structural downbeat: approx `58.86s`;
- second repeated chorus structural downbeat: approx `140.43s`;
- repeated-section offset: approx `81.55s`;
- first chorus close / section boundary: approx `87.03s`;
- corresponding second chorus close: approx `168.58s`.

Web cross-check:
- the song had active short-video/BGM diffusion after release, including fan-curated collections of posts using the song as BGM and an official artist short video around 39 seconds;
- Sony's own promotion repeatedly highlighted the title / tree-gift lyric cluster, confirming that short-form usage centers on the song's high-recognition tree hook rather than arbitrary verse fragments;
- exact source timestamps are derived from the supplied master because public short-video indexes do not expose reliable source-audio in/out timestamps.

### Preview v2 rendered automatically

Corrected excerpt:
- source in: `140.43s` (`02:20.430`)
- source out: `168.90s` (`02:48.900`)
- rendered duration: `28.470s`
- content: one complete second repeated chorus, starting on the chorus structural downbeat and ending only after the final title-line resolution;
- fade in: `0.025s`
- fade out: `0.420s`
- preview SHA-256: `b957a9e31bf7bc48a993cfdac51515cfb4f0978822abd72d7b5433c7fae8546d`

Rationale:
- removes the ~9.7s pre-chorus/preceding material mistakenly included in v1;
- restores the ~5s of missing chorus ending that v1 cut off;
- stays near the natural ~30s short-video music unit without padding with non-chorus lyrics just to reach a round duration;
- second chorus is preferred over the first because the arrangement is fuller while the lyrical/melodic unit is the same.

## W02 Automation Result So Far

- official version discovery: `AUTO`
- source acquisition: `FILE_INPUT` completed by user
- version/file verification: `AUTO`
- waveform/structure analysis: `AUTO`
- v1 selection/render: `AUTO`, but failed quality gate
- v2 root-cause correction and re-render: `AUTO`
- final audio lock: waiting for the designed `AESTHETIC_GATE`

## Next Allowed Action

`AESTHETIC_GATE`:
- user listens to W02 preview v2;
- valid responses: `PASS` or `重新选段`.

Do not enter W03 until the exact audio excerpt is locked.
If `PASS`:
1. lock `140.43s–168.90s` as the reference BGM;
2. update `AUTOMATION_MATRIX.md` and this file;
3. move to W03 and perform music / lyric / Beat analysis automatically.
