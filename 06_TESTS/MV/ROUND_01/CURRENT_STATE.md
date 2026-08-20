# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S01`
- STAGE_NAME: `最近 7 天热门 BGM 筛选`
- STATE: `IN_PROGRESS_DATASOURCE_PROOF`
- PREVIOUS_LOCK: `ROUND_CHARTER_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- CHARTER_COMMIT: `e112e602ad1e9f66c390bab3341e2db7f8258960`
- PRELIMINARY_OUTPUT: `06_TESTS/MV/ROUND_01/R1S01_BGM_SELECTION.md`
- PRELIMINARY_OUTPUT_STATUS: `NOT_LOCKABLE`
- ACTIVE_POC: `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/README.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Why R1S01 Was Reopened

The first S01 pass produced song-name-level candidates, but it did not prove a stable path to the exact Douyin music entity / version, a short directly playable preview, or account-level availability. That is insufficient for an MV production system because the same song can have multiple original / remix / cover assets and a locally available audio file does not prove the user's Douyin account can publish with that exact asset.

Therefore the previous five-candidate shortlist is retained as a real test artifact, but it cannot be LOCKED.

## New Hard Gate｜BGM_DATASOURCE_READY

R1S01 cannot return to `READY_FOR_REVIEW` until at least one real BGM completes this chain:

1. Read the current account's Douyin Creator Center `选择音乐 / 热门榜`;
2. prove that the candidate currently exposes a usable `使用` action;
3. lock the concrete music entity as far as possible: `music_id / exact version / author / share or play URL`;
4. obtain the corresponding audio file;
5. cut a 15–30 second preview;
6. user can directly listen and judge whether it matches the currently familiar Douyin hot version.

After this proof succeeds, regenerate the 5-candidate shortlist using exact music entities instead of song names.

## Active PoC Files

- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/README.md`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/requirements.txt`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/probe_creator_music.py`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/extract_music_entities.py`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/build_preview.py`

Reference implementations under investigation:
- `zJay26/douyin-skills` for Creator Center music-panel interaction and account-side availability;
- `jiji262/douyin-downloader` for `/music/{music_id}`, music detail, related aweme and direct audio download;
- `zhangshuai/douyin-go` for official Douyin billboard structures including music `rank / use_count / share_url`.

## User Role For Current Proof

The user is only required to:
1. run the local Creator Center probe;
2. complete Douyin login / CAPTCHA if prompted;
3. return the untouched probe output files;
4. later listen to the generated short preview and confirm whether it matches the expected Douyin hot version.

No manual song research, manual JSON editing, prompt rescue, or MV production is required.

## Current Risks / Unknowns

- Creator Center DOM / network fields may differ from the referenced open-source implementation and need one live calibration.
- The music panel may expose song names but not music_id directly; network interception is included to test this.
- Douyin web APIs are subject to login state, WAF / CAPTCHA and rate limits.
- The exact 7-day audio-level history remains a separate data-collection problem; first prove the current-day exact-entity pipeline.
- `AVAILABLE_AT_BUILD` does not guarantee future availability; final production will also require `AVAILABLE_AT_PUBLISH`.

## Next Allowed Action

**Only execute `BGM_DATASOURCE_READY` proof.**

First run Step A + Step B from `R1S01_DATASOURCE/README.md`, return the raw outputs, then inspect the real fields before proceeding to music download and preview cutting.

Do not begin music-structure analysis, Beat design, director design, first-frame generation, Seedance generation, editing, or final BGM selection before this Gate passes.
