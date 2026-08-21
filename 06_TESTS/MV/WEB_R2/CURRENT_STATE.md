# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W02`
- STAGE_NAME: `Reference BGM acquisition + exact clip lock`
- STATE: `PREVIEW_V3_RENDERED / AWAITING_AUDIO_GATE`
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

Actual state: `AUTO`.
GitHub/Web/Files/Image interface/local ffmpeg stack verified. Dedicated Whisper/faster-whisper and direct Seedance execution are unavailable in the current exposed toolset.

## W01 Result — LOCKED

Research state: `AUTO`.
Total stage state: `HUMAN_GATE`.
Selected reference song: `如果你也刚好抬头看树` — `孙天宇` official vocal version.

## W02 Current Evidence

### Production source

Uploaded file: `如果你也刚好抬头看树-孙天宇.mp3`
- duration: `196.127347s` (`3:16.127`)
- MP3 / 320 kbps / 44.1 kHz / stereo
- embedded metadata matches confirmed official master
- source SHA-256: `ad30cefef4e4a5ffedab81b26b1e38a0b679bf2b32752b6ebd29f5d97f18d7ab`

Accepted as W02 production source.

### Preview v1 — REJECTED

- source range: `130.72s–163.82s`
- issue: opening included pre-chorus material and ending cut a lyric line.
- root cause: excerpt boundaries were based on a broad lyrical region rather than repeated-section structural alignment.

### Preview v2 — REJECTED / LOCAL CORRECTION REQUESTED

- source range: `140.430s–168.900s`
- duration: `28.470s`
- corrected the v1 structural error and isolated the full second repeated chorus.
- user feedback: the opening would feel smoother with about `0.5s` additional pre-roll; the ending should include one more complete lyric line so the fade resolves more naturally.
- this is a local boundary refinement only; the selected chorus body remains locked.

### Preview v3 — CURRENT

User-requested refinement applied without changing the approved chorus body:
- source in: `139.930s` (`02:19.930`), exactly `0.500s` earlier than v2;
- source out: `177.050s` (`02:57.050`);
- rendered duration: `37.120s`;
- added exactly one complete lyric line after the title-line chorus close: `向一朵白云学习如何漂浮`;
- lyric sequence cross-check confirms the following line begins the next tail section (`在某天某个随机的清晨或是下午...`), so it is intentionally excluded;
- audio energy shows a clear phrase-resolution / breathing valley around `176.7–176.9s`, supporting the new out-point;
- fade in: `0.020s`;
- fade out: `0.950s` after the added line resolves.

Rationale:
- preserves the structurally correct second chorus established in v2;
- gives the opening a small musical pickup rather than beginning exactly on the structural downbeat;
- avoids the abrupt title-line stop by allowing one semantically complete release line;
- still avoids dragging the full outro/bridge into the short-MV excerpt.

## W02 Automation Result So Far

- official version discovery: `AUTO`
- source acquisition: `FILE_INPUT` completed by user
- version/file verification: `AUTO`
- waveform/structure analysis: `AUTO`
- v1 selection/render: `AUTO`, failed quality gate
- v2 root-cause correction/render: `AUTO`
- v3 local boundary refinement/render: `AUTO`
- final audio lock: awaiting designed `AESTHETIC_GATE`

## Next Allowed Action

`AESTHETIC_GATE`:
- user listens to W02 preview v3;
- valid responses: `PASS` or further local boundary correction.

Do not enter W03 until the exact audio excerpt is locked.
If `PASS`:
1. lock `139.930s–177.050s` as the reference BGM;
2. update `AUTOMATION_MATRIX.md` and this file;
3. move to W03 and perform music / lyric / Beat analysis automatically.
