# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08`
- STAGE_NAME: `Edit v1 / subtitle / pre-delivery QA`
- STATE: `FIRST_CUT_RENDERED / AWAITING_AESTHETIC_GATE`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- FULL_BATCH_QA: `06_TESTS/MV/WEB_R2/W07_FULL_BATCH_QA_v1.md`
- EDIT_V1_QA: `06_TESTS/MV/WEB_R2/W08_EDIT_V1_QA.md`
- DIRECTOR_SELECTOR: `06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked Results

- W00: `AUTO / LOCKED`
- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `PARTIAL / LOCKED` — BGM `139.930s–177.050s`, rendered `37.120s`
- W03: `AUTO / LOCKED` — six Natural Beats
- W04: `HUMAN_GATE / PASSED` — `树影之外`
- W05: `HUMAN_GATE / PASSED` — first frames `9/9`
- W06: `AUTO / EXPERIMENTAL` — dynamic prompt / Director Selector calibrated
- W06-X: `EXTERNAL_REQUIRED / COMPLETED FOR CURRENT BATCH` — S1–S9 returned
- W07: `AUTO / LOCKED FOR EDIT` — visual batch pass with trim

## W08 First Cut

Output:
`如果你也刚好抬头看树_MV_WEB_R2_第一版成片.mp4`

Technical state:
- audio duration: `37.120s`
- video duration: `37.125s` (24fps frame quantization)
- 720×1280
- SAR `1:1`
- DAR `9:16`
- H.264 video / AAC 44.1kHz stereo
- SHA-256: `e7f4855b862c2df8bca303028a826f474775f5fd153760c4b047e213a9148f9f`

## Edit decisions implemented

- no equal-duration clip concatenation;
- S1 opening + S2 orbit share the first title phrase;
- S3 close detail + S4 body movement carry the leaf-dance phrase;
- S6/S5/S6 are interleaved for call / mystery / bird discovery;
- later S2 material is reused as playful rise before the motion peak;
- S7 uses only clean early peak + canopy resolve; ambiguous large-fabric loop material is excluded;
- S8 is shortened as rooftop/sky reset;
- S9 is slowed and extended as the long cloud release.

## Audio hard state

All Seedance source audio is discarded.

Final first cut maps ONLY the W02 locked BGM. AI source audio cannot influence edit timing or subtitle timing.

## Watermark / display cleanup

First-cut viewing source uses a consistent safe crop to move the visible generator marks outside the retained image area.

Pre-delivery QA caught an intermediate non-square SAR caused by crop scaling. The delivery file was rebuilt and verified at `SAR 1:1 / DAR 9:16` before handoff.

Publish-grade W10 may still replace these first-cut sources with watermark-free HD equivalents without changing approved timing.

## Subtitle v1

No Whisper / faster-whisper claim.

Basic line-level lyric timing uses:
- exact same-version known lyrics;
- locked audio waveform / phrase-resolution valleys;
- W03 tempo / structure evidence.

This is not word-level ASR precision. First-cut viewing remains the appropriate gate for tiny line-edge adjustments.

## Current Gate

`AESTHETIC_GATE / FIRST-CUT VIEWING`.

After user review:
- local edit/subtitle fixes -> W08 v2;
- pass -> W09 retrospective / rule-promotion decision;
- no generation restart unless the actual cut exposes a specific missing source need.
