# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录自动化程度，不因“渲染出文件”就高估正确性。

## Overall

- Current Stage: `W08A / RETROFIT_STAGE_2A`
- Overall State: `V1_REVOKED / V2_REVOKED / AUDIO_TIMELINE_PACKAGE_BLOCKED`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Timing technical rescues: `2 major edit failures`

## Stage Board

| Stage | 内容 | 实际状态 | 备注 |
|---|---|---|---|
| W00 | 能力基线 | AUTO / PASS | |
| W01 | 选歌 | HUMAN_GATE / PASSED | 用户选歌 |
| W02 | BGM截取 | LOCKED | 37.120s + hash |
| **W02A** | **AUDIO_TIMELINE_PACKAGE** | **RETROFIT / BLOCKED** | v1.3新增首个post-BGM硬节点；当前R2必须补齐后才能V3 |
| W03 | 语义/Natural Beat | HISTORICAL PASS | 视觉语义仍有效；时间部分以后必须由W02A Package驱动 |
| W04 | 导演 | PASSED | `树影之外`；已生成素材不作废 |
| W05 | 首帧 | PASSED | 9/9 |
| W06 | 动态提示词 | PASS / EXPERIMENTAL | Camera selector有效 |
| W06-X | Seedance生成 | EXTERNAL_REQUIRED / COMPLETE | S1–S9 |
| W07 | 动态QA | PASS WITH TRIM | 素材池有效 |
| W08A | Editor Audio Gate | BLOCKED | 当前等价于补W02A；Package未锁 |
| W08B | Picture Edit | INVALIDATED | v1/v2撤销 |
| W09 | Subtitle | INVALIDATED | 样式可继承；timing未锁 |
| W10 | Final QA | INVALIDATED | 封装PASS不能代替同步PASS |
| W11 | Close | NOT_STARTED | |

## Why V1/V2 are revoked

### V1
- 未建立真实歌词时间轴就进入Picture Edit/Subtitle；
- 字幕样式也发生R1 Golden漂移。

### V2
- 把早先已标为 `DIAGNOSTIC_ONLY` 的声学候选重新包装成 `exact` SRT/CSV；
- 没有独立ASR/forced alignment/可靠同版本LRC；
- QA只证明视频服从SRT，没有证明SRT服从真实人声。

分类：
`TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`。

AAC/FFmpeg全局偏移已排除：
- lag `0.000s`；
- correlation ~`0.999`。

## New process truth after retrofit

Authoritative runtime now requires：

`BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ semantic Beat / Director timing allocation
→ visual production
→ Editor Package revalidation
→ Picture Edit
→ Subtitle implementation
→ Final QA。

Package rule：
`04_HARNESS/rules/mv_audio_timeline.md`

Contract：
`04_HARNESS/templates/mv_audio_timeline_package_contract.md`

Current package path：
`06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`

## Current timing evidence status

- locked audio identity: YES
- exact lyric text/order: YES
- public timed lyric candidate found: YES, but rejected as truth because timestamps conflict with locked audio/version ordering
- strong accepted raw timing evidence: NO
- provenance verified: NO
- ground-truth alignment QA: NO
- Package locked: NO

Preferred resolution：
1. trusted Chinese lyrics + Chinese CTC forced alignment on locked audio;
2. independent CJK/song alignment cross-check;
3. if a truly same-version platform LRC is later found, use it as fast-path/cross-check after version verification.

## Manual Intervention lesson

The user should not need to catch timing failures after final render.
A future timing problem counts as `TECHNICAL_RESCUE` if:
- Package was claimed PASS without strong raw evidence/provenance；or
- ground-truth QA was replaced by render-vs-SRT implementation QA。

## Next

Only valid next path：
`AUDIO_TIMELINE_PACKAGE -> raw evidence -> provenance -> ground-truth QA -> Package LOCK -> Editor Audio Gate`。

No V3 render until Package passes.
