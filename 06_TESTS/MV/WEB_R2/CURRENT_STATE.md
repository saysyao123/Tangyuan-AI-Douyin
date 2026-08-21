# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W02`
- STAGE_NAME: `Reference BGM acquisition + exact clip lock`
- STATE: `REFERENCE_VERSION_CONFIRMED / SOURCE_FILE_REQUIRED`
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

User passed the aesthetic gate and selected:

- Reference song: `如果你也刚好抬头看树`
- Artist / official vocal version: `孙天宇`
- Selection reason from user: prefers this song over the other shortlist options.

No R1 re-explanation was requested.

## W02 Current Evidence

### Official reference version confirmed

Primary version to lock:
- Title: `如果你也刚好抬头看树`
- Artist: `孙天宇`
- Type: official vocal master
- Official streaming duration evidence: `3:16`
- Companion instrumental version: `如果你也刚好抬头看树 - 伴奏`, also `3:16`
- International release metadata: `2026-07-22`
- Rights metadata: `℗ 2026 Columbia Records China`

Cross-platform identity evidence:
- Artist's verified social post on `2026-07-20` linked the same song to QQ Music, NetEase Cloud Music, Kugou, Kuwo and Qishui Music.
- Apple Music also lists the vocal and instrumental versions under the same 2026 Single.

### Rejected as exact source

- A Bilibili user upload indexed at about `3:12` is not treated as the locked source because its duration differs from the official `3:16` master.
- Public streaming / user-uploaded copies may be used for identification or listening position only; they are not treated as a redistributable production source.

### Acquisition boundary

The Web can verify the exact version, but the current tools do not expose a lawful downloadable full audio file from the official streaming services.

Therefore W02 has now reached a legitimate `FILE_INPUT` boundary: to perform exact waveform analysis, choose the excerpt, render preview, and lock downstream timing, the actual official vocal master file must be supplied as MP3/WAV (or another directly processable audio file).

## Expected Automation Hypothesis

Initial hypothesis to test, not pre-declared truth:
- W01: mostly AUTO, user only final song preference gate. **Validated.**
- W02: AUTO if usable audio file/source is available; otherwise may require minimal user upload. **Current result: version discovery AUTO; source acquisition requires FILE_INPUT.**
- W03: AUTO.
- W04: AUTO + optional user creative review.
- W05: prompts AUTO, image generation AUTO in ChatGPT, user review is HUMAN_GATE.
- W06: prompt design AUTO; Seedance execution currently expected `EXTERNAL_REQUIRED`.
- W07: AUTO after user uploads generated clips.
- W08: AUTO once source clips and locked audio are available; subtitle alignment method depends on available audio/ASR resources.
- W09: AUTO.

These must be updated from real execution evidence.

## Next Allowed Action

`FILE_INPUT`:
- obtain the actual `孙天宇 - 如果你也刚好抬头看树` official vocal master as a processable audio file;
- do not substitute the 3:12 Bilibili upload or another cover / derivative version.

Once the file is available, Web should automatically:
1. verify duration/version against the confirmed 3:16 master;
2. analyze waveform + musical / lyrical structure;
3. choose the strongest semantically complete short-MV excerpt;
4. render a natural-fade preview;
5. request only a `PASS / 重新选段` aesthetic gate.
