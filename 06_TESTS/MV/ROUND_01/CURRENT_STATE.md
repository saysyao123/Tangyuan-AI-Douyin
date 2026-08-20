# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S01`
- STAGE_NAME: `热门 BGM 发现 / 用户选歌 / Reference BGM Lock`
- STATE: `REFERENCE_BGM_SELECTED`
- PREVIOUS_LOCK: `ROUND_CHARTER_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- SELECTED_REFERENCE_BGM: `你有没有真的爱过我｜阿图表妹`
- REFERENCE_ANCHOR: `AI MV导演曹斌Johnny 的《你有没有真的爱过我》MV参考版本`
- USER_DECISION: `2026-08-21 选择候选A，作为R1第一首制作歌曲`
- BACKUP_BGM: `午后树下微风`
- SELECTION_OBSERVER_POOL: `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- ACTIVE_POC: `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/README.md`
- CODEX_REQUIREMENT: `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/CODEX_TEST_REQUIREMENT.md`
- MV_BENCHMARK_LAYER: `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Latest User Decision

User selected candidate A:

`《你有没有真的爱过我》— 阿图表妹`

The user had directly watched the Johnny MV reference and judged the song acceptable, then explicitly chose it as the first R1 song to make.

Other recent taste feedback:
- `午后树下微风`: acceptable / backup.
- `踏马寻花向自由`: average / downgrade.
- `起势`: dislike / remove from current R1 path.
- `借一页童话`: does not feel enough like an MV / downgrade.
- `山风山风等等我`: dislike / remove.

## Process Correction Validated by R1

The earlier S01 design coupled two different objects too tightly:

1. `REFERENCE_BGM` — the exact song/version/reference used to make the MV;
2. `PUBLISH_BGM` — the platform music entity that the user's account can legally/technically attach at publish time.

This caused unnecessary blocking before the user could begin production.

### New separation

#### REFERENCE_BGM Gate｜before production
Required:
- user has directly listened to / watched the chosen reference;
- song and performer/version direction are identified;
- a concrete public reference work is anchored;
- lyrics / timing / music structure can be analyzed from the chosen reference version.

For R1 this gate is now satisfied by:
- `你有没有真的爱过我｜阿图表妹`;
- reference anchor = Johnny's corresponding MV version that the user watched and selected.

#### PUBLISH_BGM Gate｜before final publishing
Still HARD:
- exact Douyin music entity / music_id as far as available;
- distinguish original / cover / DJ / Remix;
- current account can select/use the exact target asset;
- `AVAILABLE_AT_PUBLISH = TRUE`;
- if unavailable, do not publish with an external embedded copyrighted copy as a substitute.

The Codex-side datasource proof remains required for hardening the long-term system, but it no longer blocks R1 visual production after a user-selected Reference BGM is locked.

## Song Observer Pool｜Active

Use `R1S01_SELECTION_OBSERVER_POOL.md` for future discovery. Current simplified logic:
- observe ~5 music/MV sources over the last 30 days;
- repeated song in >=2 sources -> candidate;
- >=3 -> strong cross-account lead;
- verify broader diffusion when possible;
- give the user direct real MV/video links;
- user taste can immediately reject a hot song.

## Rolling MV Benchmark Layer｜Active Knowledge

Full aesthetic/director Benchmark Pool remains separate:
- `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

JIT usage:
- Opening Hook: same-BGM + relevant benchmark works;
- Director: 3–5 relevant works;
- First-frame: 2–3 Beauty references;
- Dynamic: 2–3 Director/Action references;
- Final QA: 2–3 completion/market references.

External benchmark observations never directly become hard Rules / Golden References.

## Current Public Version Evidence

Public search currently supports:
- song identity: `你有没有真的爱过我`;
- performer direction: `阿图表妹`;
- original song credited to `谈柒柒` in public lyric/music sources;
- multiple alternate assets exist, including `节奏版` and `DJ白豆版`, so production must not silently swap versions later;
- the user's reference anchor remains the Johnny MV version already heard, not an arbitrary alternate version.

## Current Risks / Unknowns

- Exact Douyin music_id is still pending.
- Creator Center account availability remains pending Codex-side live calibration.
- Alternate versions exist; later audio acquisition must match the selected Reference BGM closely.
- `AVAILABLE_AT_PUBLISH` remains mandatory before release.

## Next Allowed Action

`REFERENCE_BGM_SELECTED` is sufficient to begin the next production-analysis stage.

Next:
1. lock the short working interval from the chosen reference;
2. analyze music / lyric structure and emotional strength curve;
3. propose natural Beats;
4. stop for review before director/first-frame production if required by Round Charter.

Do not silently replace the chosen song with another version during music analysis.