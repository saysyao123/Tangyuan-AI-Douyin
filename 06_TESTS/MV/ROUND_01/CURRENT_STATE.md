# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S02`
- STAGE_NAME: `Music / Lyric Structure`
- STATE: `READY_FOR_REVIEW`
- PREVIOUS_LOCK: `REFERENCE_BGM_SELECTED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- SELECTED_REFERENCE_BGM: `你有没有真的爱过我｜阿图表妹`
- REFERENCE_ANCHOR: `AI MV导演曹斌Johnny 的《你有没有真的爱过我》MV参考版本`
- R1S02_OUTPUT: `06_TESTS/MV/ROUND_01/R1S02_MUSIC_STRUCTURE.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked / Effective Decisions

### R1 song direction
User selected:
`《你有没有真的爱过我》— 阿图表妹`

Reference anchor is the Johnny MV version directly watched and accepted by the user.

Backup retained:
`午后树下微风`

### S01 simplified song-selection path｜Temporarily LOCKED
For the current R1 and near-term manual testing, use the simplified observer workflow:

`5-source MV/music observer pool -> scan recent ~30-day songs -> prefer songs repeated across multiple observers / recent wider Douyin diffusion -> give direct real MV/video links -> user judges song + visual together -> choose one Reference BGM`

This lightweight path is intentionally retained for current production speed.

The deeper datasource path (`exact music_id / creator-center probe / account-side availability / automated preview acquisition`) is **not abandoned**. It is deferred to the Codex-capable computer for later hardening and automation tests.

Do not block current visual-production calibration on that deeper datasource engineering.

### Reference vs Publish BGM
R1 separates:
- `REFERENCE_BGM`: required before music/visual production analysis; current reference is locked by the Johnny MV the user actually heard and accepted.
- `PUBLISH_BGM`: exact Douyin platform asset / account availability, required before final publishing.

The full Codex datasource proof remains a system-hardening requirement.

`AVAILABLE_AT_PUBLISH = TRUE` remains HARD before release.

## R1S02 Proposed Working Interval

Approximate source-song interval:
`01:24 → 01:55` (~31s)

Working lyric sequence:
- 你的回应是一直沉默
- 只剩下落寞
- 我有什么错
- 短暂柔情似流星划落
- 你有没有真的爱过我
- 我是你诗的哪个段落
- 落款第几页
- 第几次临摹
- 还是匆匆一瞥就略过

Reason:
- full emotional movement;
- strong visual-bearing lyrics;
- avoids over-reliance on literal fog / wine / moon imagery;
- gives the title line an earned emotional peak rather than opening with repeated hook.

## Preliminary Natural Beats

1. `你的回应是一直沉默` — absence / no response.
2. `只剩下落寞 / 我有什么错` — inward collapse / self-question.
3. `短暂柔情似流星划落` — first visual peak.
4. `你有没有真的爱过我` — central emotional confrontation.
5. `我是你诗的哪个段落` — metaphorical turn.
6. `落款第几页 / 第几次临摹` — trace / copy / archived identity.
7. `还是匆匆一瞥就略过` — cold final answer / release / negative space.

Strength curve:
`M → L → M → H → H → M-H → M → L`

## Timing Confidence

The current seconds come from public lyric timing for the 阿图表妹 version and are provisional until the exact Reference BGM audio / waveform is available.

Before editing:
- actual audio must be re-synced;
- do not assume 0.1s precision yet.

If the user provides a local audio or MV file containing the accepted Reference BGM, use that exact supplied media as the source for clipping and waveform alignment; do not silently substitute another online version.

## Current Benchmark / Observer System

Song discovery observer pool and rolling MV benchmark remain active:
- `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

Future use is JIT, not full-pool analysis at every stage.

## Current Risks / Pending

- exact Douyin music_id pending Codex hardening test;
- exact account publish availability pending Codex-side verification;
- exact waveform timing pending access to the accepted audio source;
- alternate versions (standard / rhythm / DJ) exist, so no silent version swap is allowed.

## Next Allowed Action

Human review of `R1S02_MUSIC_STRUCTURE.md` and exact Reference BGM clip preparation when the accepted media source is available.

If user approves the working lyric interval and Beat structure:
1. create separate LOCK commit for R1S02;
2. advance to Director / visual-system planning;
3. run focused Benchmark analysis for 3–5 relevant visual/director works before first-frame design.

Do not begin first-frame generation before R1S02 receives user PASS.