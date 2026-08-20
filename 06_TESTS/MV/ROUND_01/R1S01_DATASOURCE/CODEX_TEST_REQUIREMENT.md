# R1S01｜Codex Data Source Proof Requirement

> Purpose: run the full BGM datasource proof on a Codex-capable computer with Git, Python, Playwright and ffmpeg available.

## Background

The first manual attempt on the user's current Windows computer was blocked before the PoC itself could run:

- `git` command unavailable;
- repository checkout/path therefore unavailable;
- `pip` command unavailable;
- local Python/venv state is not reliable enough for this test.

This is recorded as an **environment dependency failure**, not a BGM datasource failure.

## Codex Must Do

1. Clone or update `saysyao123/Tangyuan-AI-Douyin`.
2. Checkout branch `test/mv-round-01`.
3. Read first:
   - `06_TESTS/MV/ROUND_01/CURRENT_STATE.md`
   - `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/README.md`
4. Verify/install only missing runtime dependencies:
   - Git
   - Python 3.10+
   - pip / venv
   - Playwright + Chromium
   - ffmpeg / ffprobe
5. Run Step A and Step B of the datasource proof without modifying the output JSON by hand.
6. If Douyin requests login / CAPTCHA, stop only for the user to complete the browser challenge, then continue automatically.
7. Inspect actual Creator Center fields and network payloads. Do not assume the referenced open-source selectors/field names are still correct.
8. If `music_id` is found, continue Step C:
   - use `jiji262/douyin-downloader` as an external reference/test dependency;
   - obtain the exact music entity's playable audio and metadata;
   - do not vendor the full third-party repository into Runtime.
9. Generate a 15–30s preview with `build_preview.py` / ffmpeg.
10. Return a structured result:

```text
CREATOR_HOT_PANEL: PASS/FAIL
ACCOUNT_USE_ACTION: PASS/FAIL
MUSIC_ID: <id or missing>
EXACT_VERSION: <title/author/version>
AUDIO_FETCH: PASS/FAIL
RELATED_AWEME_FETCH: PASS/FAIL
PREVIEW_PATH: <local path>
BLOCKER: <none or exact blocker>
ROOT_CAUSE: <environment / selector / login / risk-control / field-missing / downloader / ffmpeg>
```

## PASS Gate

`BGM_DATASOURCE_READY` requires at least one real Douyin music entity to complete:

`current account hot-music panel -> usable action -> exact entity/music_id -> audio -> 15–30s preview -> user listening confirmation`

## Security / Evidence Rules

- Never commit Cookie, session tokens, QR-login data, browser profile, signed URLs with private query parameters, or raw private network credentials.
- Raw private probe outputs stay local and are returned to the current conversation/Codex workspace only.
- GitHub stores sanitized conclusions, failure classification, field schema and reproducible code—not secrets.
- Failed attempts must also be recorded with root cause and next fix.

## Automation Direction After PASS

After the first live proof passes, refactor only the minimum stable capability into the project:

- account-side availability probe;
- exact music entity normalization;
- related-aweme sample collection;
- preview generation;
- `AVAILABLE_AT_BUILD` / `AVAILABLE_AT_PUBLISH` checks.

Do not promote the entire experimental downloader/browser stack into the Runtime before repeated validation.
