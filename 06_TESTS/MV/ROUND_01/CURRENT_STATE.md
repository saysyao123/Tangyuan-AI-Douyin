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
- CODEX_REQUIREMENT: `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/CODEX_TEST_REQUIREMENT.md`
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
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/CODEX_TEST_REQUIREMENT.md`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/requirements.txt`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/probe_creator_music.py`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/extract_music_entities.py`
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/build_preview.py`

Reference implementations under investigation:
- `zJay26/douyin-skills` for Creator Center music-panel interaction and account-side availability;
- `jiji262/douyin-downloader` for `/music/{music_id}`, music detail, related aweme and direct audio download;
- `zhangshuai/douyin-go` for official Douyin billboard structures including music `rank / use_count / share_url`.

## Latest Test Result｜Local Environment Blocked

The user's first local Windows attempt did not reach the PoC itself:

- `git` was not available in PATH;
- the repository/test branch therefore was not present locally;
- `pip` was not available;
- venv/Playwright setup could not be trusted on that computer.

Classification: `ENVIRONMENT_DEPENDENCY_FAILURE`.

This is **not** evidence that the Douyin datasource approach failed.

The full browser/API/audio proof is deferred to the user's Codex-capable computer and is specified in `CODEX_TEST_REQUIREMENT.md`.

## Alternate No-Local-Runtime Path｜Allowed Now

While the Codex proof is pending, R1S01 may continue with a lightweight link-assisted proof that requires no Git/Python environment on the user's current computer:

1. User supplies a Douyin music-share link or one representative Douyin video link using the target hot BGM (a screenshot of the music page is useful but optional).
2. System resolves the exact public content/music entity as far as public access permits.
3. System verifies title/author/version/music identity against multiple public signals.
4. If a public playable source can be lawfully accessed without bypassing login/DRM, system creates or references only a short listening preview for identification/evaluation.
5. Account-level `AVAILABLE_AT_BUILD` remains pending until the same entity is confirmed in the user's Douyin music selector.

This alternate proof may validate entity identity and preview workflow, but it **does not replace** the later Codex account-side availability test.

## User Role For Current Proof

Current-computer path:
- provide one Douyin music share link or representative video share link when testing a concrete BGM;
- optionally provide a screenshot showing the audio/music title in Douyin;
- listen to the returned short preview/reference and confirm whether it matches the familiar hot version.

Codex-computer path:
- only complete Douyin login/CAPTCHA when prompted;
- let Codex execute the rest of the PoC automatically.

No manual JSON editing, prompt rescue, MV production, or technical diagnosis is required from the user.

## Current Risks / Unknowns

- Creator Center DOM / network fields may differ from the referenced open-source implementation and need one live calibration.
- The music panel may expose song names but not music_id directly; network interception is included to test this.
- Douyin web APIs are subject to login state, WAF / CAPTCHA and rate limits.
- The exact 7-day audio-level history remains a separate data-collection problem; first prove the current-day exact-entity pipeline.
- Public link-assisted proof may identify an entity but cannot prove the user's account can still select it.
- `AVAILABLE_AT_BUILD` does not guarantee future availability; final production will also require `AVAILABLE_AT_PUBLISH`.

## Next Allowed Action

**Only execute `BGM_DATASOURCE_READY` proof.**

Preferred full proof: run the Codex requirement on the capable computer.

Allowed interim proof: use one real Douyin music/video share link to test exact-entity identification and short-preview handling without local Git/Python.

Do not begin music-structure analysis, Beat design, director design, first-frame generation, Seedance generation, editing, or final BGM selection before this Gate passes.
