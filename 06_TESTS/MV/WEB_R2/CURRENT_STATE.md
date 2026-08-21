# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08/W09`
- STAGE_NAME: `Audio-led second-cut review / subtitle sync validation`
- STATE: `SECOND_CUT_REVIEW_RENDERED / INTERNAL_QA_PASS / AWAITING_VIEWING_GATE`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.2
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md`
- FULL_BATCH_QA: `06_TESTS/MV/WEB_R2/W07_FULL_BATCH_QA_v1.md`
- W08_GATE: `06_TESTS/MV/WEB_R2/W08_AUDIO_LYRIC_TIMELINE_GATE_v2.md`
- W08_V2_QA: `06_TESTS/MV/WEB_R2/W08_V2_REBUILD_QA.md`
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

Classification: `TECHNICAL_RESCUE`.

Root cause: picture edit/subtitles were allowed to proceed before a durable line-level lyric timing map had been rebuilt from the locked audio; subtitle styling also drifted from R1 Golden.

Do not use v1 timing as truth.

## W08 v2 — current review cut

Output:
`如果你也刚好抬头看树_MV_WEB_R2_第二版成片.mp4`

SHA-256:
`ff1bbb67427b0067001ebe97f5e0d7bcb3e4c9c434606c2c833ba280647adc3b`

Technical state:
- ~37.125s at 24fps frame quantization against locked 37.120s BGM;
- 720×1280;
- SAR `1:1` / DAR `9:16`;
- H.264 video;
- AAC stereo 44.1kHz;
- only locked-BGM-derived audio is present; Seedance source audio is not mapped.

## v2 lyric line map

1. `0.470–4.810` 如果你也刚好抬头看树
2. `5.451–10.680` 我要学着树叶翩翩起舞
3. `10.954–13.189` 喊几声布谷布谷
4. `13.827–15.850` 或许少有人知道
5. `16.788–18.800` 有鸟儿是这样叫
6. `19.702–21.980` 好吧 哎哟哎哟
7. `23.470–26.770` 一颗心叽叽喳喳飞过了树梢
8. `28.439–32.540` 如果你也刚好抬头看树
9. `32.618–35.650` 向一朵白云学习如何漂浮

No Whisper / faster-whisper claim.

Method: exact known lyric order constrained against the locked audio using phrase onsets, vocal-band energy, breath/phrase valleys, beat evidence, repeated-chorus correspondence and final vocal resolution. Durable SRT/CSV timing assets were generated locally for the rebuild.

This is a project-level line map used for the requested v2 review cut. Cross-round promotion still prefers actual ASR/forced alignment or reliable same-version timed lyric evidence.

## v2 edit decisions

- edit rebuilt from the line/phrase map, not from v1;
- S1 scale opening + S2 Arc serve L1;
- S3 + S4 serve leaf-dance L2;
- S6 handles call/discovery for L3/L5;
- S5 is the L4 breathing/unknown-space beat;
- S4/S3 provide playful L6 motion;
- S7 uses only clean early peak for L7;
- final self-audit removed S7 late fabric-tail material entirely;
- S1 canopy resolves the peak, then S8 enters early during the instrumental gap and carries L8;
- S9 carries L9 and the visual tail.

## Subtitle Golden restoration

R1 accepted base style is restored:
- light Chinese text;
- dark semi-transparent rounded box tightly fitted to line;
- horizontal + vertical centering;
- consistent padding;
- fixed lower safe-area position;
- restrained fade;
- no karaoke / word-by-word effect.

Representative first/middle/longest/final frames were visually inspected.

## Internal QA

PASS:
- subtitle appearance/disappearance sampled before/inside/after every line window;
- subtitle box safe area / centering / overflow checked;
- known S1 repeated middle material excluded;
- known S7 late topology-risk fabric excluded;
- no black-frame event detected;
- final aspect/pixel aspect valid;
- final audio stream is identical before/after subtitle burn-in;
- no AI source audio leakage;
- retained-frame platform marks cropped consistently.

Detailed record:
`W08_V2_REBUILD_QA.md`.

## Current Gate

`VIEWING_GATE / SECOND_CUT`.

User is reviewing v2 for actual song-picture feel and lyric sync. If an objective timing error remains, classify as `TECHNICAL_RESCUE` and correct the timing asset before polish. If v2 passes, proceed to final polish / Round close without reopening approved visual-generation stages.