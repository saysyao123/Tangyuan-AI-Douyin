# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08A`
- STAGE_NAME: `Audio / Lyric Timeline Lock — mandatory pre-edit gate`
- STATE: `TECHNICAL_RESCUE / FIRST_CUT_REVOKED / LYRIC_TIMELINE_BLOCKED`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.2
- FULL_BATCH_QA: `06_TESTS/MV/WEB_R2/W07_FULL_BATCH_QA_v1.md`
- W08_GATE: `06_TESTS/MV/WEB_R2/W08_AUDIO_LYRIC_TIMELINE_GATE_v2.md`
- DIRECTOR_SELECTOR: `06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked upstream results

- W00: `AUTO / LOCKED`
- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `PARTIAL / LOCKED` — BGM source `139.930s–177.050s`, rendered `37.120s`, SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- W03: `AUTO / DIRECTOR-LEVEL LOCK` — exact lyric text + six Natural Beats; no false Whisper claim
- W04: `HUMAN_GATE / PASSED` — `树影之外`
- W05: `HUMAN_GATE / PASSED` — first frames `9/9`
- W06: `AUTO / EXPERIMENTAL` — dynamic prompt / Director Selector calibrated
- W06-X: `EXTERNAL_REQUIRED / COMPLETED FOR CURRENT BATCH` — S1–S9 returned
- W07: `AUTO / LOCKED FOR EDIT INPUT` — visual batch passed with trim

## W08 v1 — REVOKED

Historical artifact only:
`如果你也刚好抬头看树_MV_WEB_R2_第一版成片.mp4`

The file itself is technically valid as an MP4, but **it is not a valid W08 creative deliverable and must not be used as timing truth**.

### Root cause

Before rendering v1, the assistant did not produce an independently verified `LYRIC_TIMELINE_LOCKED` asset.

It proceeded using:
- exact known lyric text;
- waveform / phrase-valley estimates;
- approximate director-level structure.

Those inputs are useful diagnostics but are insufficient for exact lyric/subtitle timing. The resulting subtitle timing was wrong, which also means the picture cut / lyric-hit map was built against an unverified temporal model.

User correctly identified:
- subtitles do not match the sung lyrics;
- beat/cut choices built from those timings are therefore unreliable;
- subtitle visual specification also drifted from the previous Golden reference;
- the workflow skipped required self-audit instead of stopping.

Classification:
`TECHNICAL_RESCUE`.

This is **not** counted as an aesthetic-gate rejection.

## Golden R1 rule restored

Round 01 already proved:
- subtitle timing comes from locked audio, never visual segment boundaries;
- same-version timing must be established via reliable timed evidence / ASR / forced alignment and corrected against known lyrics;
- corrected timing was user-reviewed as accurate;
- accepted subtitle visual baseline = light Chinese text + dark semi-transparent rounded box tightly fitted around text + horizontal/vertical centering + comfortable fixed lower safe area + restrained fade + max 2 lines + no base karaoke effect.

W08 failed because this existing Golden requirement was not enforced as a blocking state transition.

## Workflow upgrade

`04_HARNESS/workflows/mv.md` upgraded to v1.2.

New mandatory pre-edit order:

`BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_SYNC_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

No later state is valid if an earlier state is absent.

## Current W08A evidence

### BGM identity
- locked duration: `37.120s`
- locked SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- `BGM_LOCKED = YES`

### Exact lyric text
1. 如果你也刚好抬头看树
2. 我要学着树叶翩翩起舞
3. 喊几声布谷布谷
4. 或许少有人知道
5. 有鸟儿是这样叫
6. 好吧哎哟哎哟
7. 一颗心叽叽喳喳飞过了树梢
8. 如果你也刚好抬头看树
9. 向一朵白云学习如何漂浮

`LYRIC_TEXT_LOCKED = YES`

### Timing status
Acoustic beat/onset/valley analysis exists, but it is diagnostic only and cannot lock lyric boundaries by itself.

Current strong timing evidence status:
- dedicated local Whisper/faster-whisper: not verified available;
- attempted local transcription/separation fallback did not produce a valid timing asset;
- reliable same-version LRC / official timestamp source: not yet locked.

Therefore:
`LYRIC_TIMELINE_LOCKED = NO`
`STATE = LYRIC_TIMELINE_BLOCKED`

No second picture edit / subtitle render is allowed until this Gate passes.

## Current allowed work

Continue automatically with timing-source acquisition / alignment only:
1. obtain strong same-version timed lyric evidence or a real ASR/forced-alignment result on the locked 37.120s audio;
2. constrain/correct it to the exact nine lyric lines;
3. boundary-audit every line;
4. export durable SRT/LRC/timing table;
5. set `LYRIC_TIMELINE_LOCKED = YES` only after audit;
6. then rebuild the picture edit from scratch against the locked timing + beat map.

Do not ask the user to manually time lyrics unless all automated/evidence-based routes are genuinely exhausted.
