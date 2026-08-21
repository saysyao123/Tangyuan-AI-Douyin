# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W03`
- STAGE_NAME: `Music / lyric / Beat analysis`
- STATE: `READY_TO_START`
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

## W02 Result — LOCKED

Actual stage state: `PARTIAL`.
Final user gate: `PASSED` on preview v3.

### Locked production source

Uploaded file: `如果你也刚好抬头看树-孙天宇.mp3`
- duration: `196.127347s` (`3:16.127`)
- MP3 / 320 kbps / 44.1 kHz / stereo
- embedded metadata matches confirmed official master
- source SHA-256: `ad30cefef4e4a5ffedab81b26b1e38a0b679bf2b32752b6ebd29f5d97f18d7ab`

### Locked reference BGM excerpt

- source in: `139.930s` (`02:19.930`)
- source out: `177.050s` (`02:57.050`)
- rendered duration: `37.120s`
- fade in: `0.020s`
- fade out: `0.950s`
- preview file: `如果你也刚好抬头看树_WEB_R2_W02_副歌扩展试听_v3.mp3`
- preview SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- end strategy: after the core chorus/title-line close, include exactly one additional complete release line (`向一朵白云学习如何漂浮`), then fade after the vocal phrase resolves.

Downstream timing must use this exact locked audio interval/file. No silent version swap.

### W02 failure / intervention record

Preview v1 — rejected:
- `130.72s–163.82s`
- opening included preceding non-chorus material;
- final lyric line was truncated.
- root cause: broad lyrical-region selection without repeated-section structural alignment or mandatory edge QA.

Preview v2 — technically corrected but still required user boundary refinement:
- `140.430s–168.900s`
- isolated the correct repeated chorus;
- user identified that the opening needed ~0.5s pickup and the ending would resolve better with one additional complete lyric line.

Preview v3 — passed:
- `139.930s–177.050s`
- preserves the chorus body, adds musical pickup, includes one complete release line, and fades after a clear phrase-resolution/breath valley.

### W02 workflow promotion

`04_HARNESS/workflows/mv.md` upgraded to `v1.1` with a new W02 first-pass lock algorithm and mandatory `Audio Boundary Gate`.

New mandatory first-pass checks include:
- exact source/version verification;
- short-video/Douyin usage evidence when available before candidate selection;
- lyric + musical-section + repeated-structure mapping before timecodes;
- `0.3–0.8s` pickup test without previous-lyric contamination;
- no incomplete final lyric;
- one-extra-release-line test;
- fade only after vocal/semantic resolution;
- isolated first ~3s / last ~4s listen plus full excerpt listen;
- technical boundary failures must be recorded as `TECHNICAL_RESCUE`, not hidden inside a normal aesthetic gate.

## W02 Automation Conclusion

- official version discovery: `AUTO`
- source acquisition: `FILE_INPUT`
- source verification / waveform processing / rendering: `AUTO`
- one-shot excerpt selection quality: `FAILED_IN_THIS_ROUND`
- final excerpt achieved after two user boundary corrections
- final approval: designed `AESTHETIC_GATE`, passed
- W02 total: `PARTIAL`

This is not considered a successful one-shot automatic clip lock. The new Stage 2 workflow is intended to remove the two avoidable boundary interventions in the next song.

## Next Allowed Action

Run `W03` automatically using the exact locked v3 BGM.

W03 should establish:
- exact lyric phrases for the locked excerpt;
- music structure / rises / releases;
- Natural Beats;
- emotional curve;
- strong/weak distribution;
- key lyric visual opportunities;
- Opening Hook candidates.

Do not enter W04 until W03 output is complete.
