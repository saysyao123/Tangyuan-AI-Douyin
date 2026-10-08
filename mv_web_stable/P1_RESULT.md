# P1 · Cloud MP4 Smoke · PASS

**Date:** 2026-10-08

**Actual successful run:** https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37723404840

**Artifact:** [mv-web-stable-p1-37723404840](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37723404840) (artifact id `11526711881`, 14-day retention, expires 2026-10-22).

## What ran

GitHub-hosted ubuntu-24.04 runner → Playwright Chromium 1.51.0 → restored pinned Open Font License fonts → generated 2-second synthetic 440Hz audio → executed actual Run01 Huashu Skill-derived Canvas `render.py` (60 frames) → ffmpeg H.264/AAC → `verify_smoke.py` full decode/ffprobe → uploaded Artifact.

The first run (https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37723317216) failed because FFmpeg was absent from ubuntu runner. Workflow dependency was corrected in commit `2b60de04713f46faa27cee57904920f1b6bfb1f5`; rerun 37723404840 completed successfully.

## Actual PASS evidence

| Assertion | Result |
|---|---|
| Dimensions | 1080×1920 PASS |
| Video | H.264 30fps, 60 frames PASS |
| Duration | 2.000s PASS |
| Audio | AAC stereo, 44100Hz PASS |
| Complete decode | PASS, no errors |
| PNG middle-frame preview | PASS |
| Artifact uploaded | PASS |
| Video SHA256 | `61acc58a40bf179174f8a71d5f8be0f2cf15261bef7eefc386fb9b3b5a6890c6` |

Successful output filename: `mv_2sec_smoke.mp4`; Artifact also includes `smoke_report.json` and `smoke_preview.png`.

**Scope:** P1 proves an internet-hosted GitHub Actions workflow can invoke the existing Huashu-derived animation renderer and produce a working browser-downloadable MP4. It does NOT prove eight lyric-specific new images, real lyric timing, full 21.36-second final MV, organic body animation, or automatic use of ChatGPT's image generation credits. These require separate P2–P5 validation.

## Next gate

P2 is READY but unstarted. Work only on scene isolation, one-lyric-one-shot timing, independent regeneration and seam checks as stated in `P2_SHOT_CONTRACT.md`. Do not change the previously frozen S0/S1 results in unrelated Fresh Project runs.
