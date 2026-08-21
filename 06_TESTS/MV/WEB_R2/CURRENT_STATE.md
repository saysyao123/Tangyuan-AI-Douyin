# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W02`
- STAGE_NAME: `Reference BGM acquisition + exact clip lock`
- STATE: `PREVIEW_RENDERED / AWAITING_AUDIO_GATE`
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
- embedded title: `如果你也刚好抬头看树`
- embedded artist: `孙天宇`
- embedded album: `如果你也刚好抬头看树`
- source SHA-256: `ad30cefef4e4a5ffedab81b26b1e38a0b679bf2b32752b6ebd29f5d97f18d7ab`

Conclusion:
- duration and metadata match the confirmed official 3:16 vocal master;
- the file is accepted as the W02 production source;
- the rejected 3:12 Bilibili user upload is not used.

### Preview v1 rendered automatically

Recommended excerpt:
- source in: `130.72s`
- source out: `163.82s`
- rendered duration: `33.149388s`
- content intent: second chorus, beginning with `我要学着树叶翩翩起舞` and closing on `如果你也刚好抬头看树`
- fade in: `0.08s`
- fade out: `0.90s`, beginning after the final vocal close
- preview SHA-256: `6d831c7bb1dadc13de79161677285d46d8a47cdaca76e5c83b508fdc36b8bf2d`

Selection rationale:
- contains the song's highest-recognition chorus and title return;
- provides multiple lyric-specific visual events: leaves dancing, cuckoo call, a heart flying over the treetop, and looking up at the tree;
- forms a semantically complete short-MV unit;
- stronger first-round MV recognition than using only the lower-energy final bridge.

## W02 Automation Result So Far

- official version discovery: `AUTO`
- source acquisition: `FILE_INPUT` completed by user
- version/file verification: `AUTO`
- waveform/structure analysis: `AUTO`
- excerpt selection and preview render: `AUTO`
- final audio lock: waiting for one designed `AESTHETIC_GATE`

## Expected Automation Hypothesis

- W01: mostly AUTO, user only final song preference gate. **Validated.**
- W02: AUTO if usable audio file/source is available; otherwise may require minimal user upload. **Validated as PARTIAL: one FILE_INPUT, all processing after upload AUTO, final listening remains HUMAN_GATE.**
- W03: AUTO.
- W04: AUTO + optional user creative review.
- W05: prompts AUTO, image generation AUTO in ChatGPT, user review is HUMAN_GATE.
- W06: prompt design AUTO; Seedance execution currently expected `EXTERNAL_REQUIRED`.
- W07: AUTO after user uploads generated clips.
- W08: AUTO once source clips and locked audio are available; subtitle alignment method depends on available audio/ASR resources.
- W09: AUTO.

## Next Allowed Action

`AESTHETIC_GATE`:
- user listens to W02 preview v1;
- valid responses: `PASS` or `重新选段`.

Do not enter W03 until the exact audio excerpt is locked.
If `PASS`:
1. record exact locked source in/out, render duration and fades;
2. update `AUTOMATION_MATRIX.md` and this file;
3. move to W03 and perform music / lyric / Beat analysis automatically.
