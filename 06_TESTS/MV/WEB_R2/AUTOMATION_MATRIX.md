# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录自动化程度，不因“渲染出文件”就高估正确性。

## Overall

- Current Stage: `W08B / V3_EDIT_PREVIEW_VIEWING_GATE`
- Overall State: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS / EDIT_MAP_LOCKED / PICTURE_PREVIEW_RENDERED / TECH_QA_PASS / AESTHETIC_VIEWING_PENDING`
- Human aesthetic gates passed: `4`
- External-required stages encountered: `1`
- Timing technical rescues: `2 major edit failures`
- Audio timeline hard gate: `PASS`

## Stage Board

| Stage | 内容 | 实际状态 | 备注 |
|---|---|---|---|
| W00 | 能力基线 | AUTO / PASS | |
| W01 | 选歌 | HUMAN_GATE / PASSED | 用户选歌 |
| W02 | BGM截取 | LOCKED | 37.120s + SHA |
| **W02A** | **AUDIO_TIMELINE_PACKAGE** | **PASS / LOCKED** | trusted-lyrics Chinese CTC forced alignment；两层机器 Gate PASS |
| W03 | 语义/Natural Beat | HISTORICAL PASS / TIMING REBOUND | 视觉语义继续使用；V3 时间全部重新绑定 canonical Package |
| W04 | 导演 | PASSED | `树影之外`；已生成素材不作废 |
| W05 | 首帧 | PASSED | 9/9 |
| W06 | 动态提示词 | PASS / EXPERIMENTAL | mixed shot structure有效 |
| W06-X | Seedance生成 | EXTERNAL_REQUIRED / COMPLETE | 2S1–2S9 |
| W07 | 动态QA | PASS WITH TRIM | S1重复窗/S7风险窗已在V3剔除 |
| W08A | Editor Audio Gate | PASS | Package manifest + locked BGM SHA revalidated |
| **W08B** | **Picture Edit / V3 Edit Map** | **EDIT_MAP_LOCKED / PREVIEW_RENDERED / TECH_QA_PASS / HUMAN_VIEW_PENDING** | 当前 Gate |
| W09 | Subtitle | BLOCKED_BY_VIEWING_GATE | timing已锁；只等待Picture Preview审美通过 |
| W10 | Final QA | NOT_STARTED_FOR_V3 | |
| W11 | Close | NOT_STARTED | |

## Why V1/V2 remain revoked

V1:
- 在真实歌词时间轴建立前进入Picture Edit/Subtitle；
- subtitle style发生R1 Golden漂移。

V2:
- `DIAGNOSTIC_ONLY`声学候选被错误包装为exact；
- 当时没有Strong Route raw evidence/provenance；
- QA只证明render follows SRT，没有证明SRT follows vocal。

V1/V2 timing不可复用；已验证视觉素材选择经验可复用。

## W02A resolution

- locked BGM SHA: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- canonical lyrics: 10 lines
- Strong Route: Chinese CTC forced alignment
- model revision: `d2af85f00e501bb8b8bcedef3b5c51eabb883088`
- 92 target tokens -> 92 aligned spans
- repeated chorus QA: median shift `81.527s`, max deviation `0.061s`
- Timing Core Gate: PASS / 0 errors/warnings
- Complete Package Gate: PASS / 10 lines / 10 anchors / 21 music events / 0 errors/warnings
- `AUDIO_TIMELINE_PACKAGE_LOCKED=true`
- canonical package sync run: `32655263045`

## W08B V3 result so far

Canonical edit map:
`W08B_V3_EDIT_MAP_v1.csv`

Preview QA:
`W08B_V3_EDIT_PREVIEW_QA_v1.md`

V3 key corrections:
- real L01 is `我要学着树叶翩翩起舞`, so leaf/dance visuals now open the edit;
- title line `如果你也刚好抬头看树` begins at `19.090s`, so S1 moved to that region;
- S6 bird reveal lands ~`8.542s` vs `鸟儿` anchor `8.525s`;
- S7 clean peak enters at `14.958s` for `飞过树梢 15.008–18.290s`;
- S1 low-angle and eye close-up cover `抬头 / 看树` anchors;
- S8/S3 cover literal `白云` -> physical `漂浮`;
- S9 starts `32.833s`, ~5ms before L10 entry and carries the final release/tail.

Risk/repetition handling:
- S1 source frames `58–75` removed;
- S7 source frames `65–97` removed;
- S8 shortened (~2.917s) vs S9 long final hold (~4.292s).

Preview technical state:
- `720×1280`, 24fps, SAR 1:1;
- 891 frames / video 37.125s;
- audio 37.120s;
- Preview SHA: `09e68c852d50fd43059fa70b8555ec7a742451af27ca2e3c177595ae5f240111`;
- decoded Preview audio vs locked BGM lag `0.000s`, correlation ~`0.99960`;
- all Seedance source audio discarded.

## Current states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = YES`
- `PICTURE_PREVIEW_RENDERED = YES`
- `EDIT_PREVIEW_TECH_QA_PASS = YES`
- `EDIT_PREVIEW_QA_PASS = NO / AESTHETIC_VIEWING_PENDING`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next

Only valid next action:
**user views V3 Picture+BGM Preview.**

Accepted -> `EDIT_PREVIEW_QA_PASS -> W09 Subtitle Style + Implementation QA` using canonical `lyrics_exact.srt` only.

Specific visual issue -> adjust only affected W08B fragment(s). Do not reopen W02A or regeneration by default.
