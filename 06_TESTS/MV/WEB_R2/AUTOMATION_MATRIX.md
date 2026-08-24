# WEB R2｜AUTOMATION MATRIX

> 只记录自动化/人工 Gate 状态；方法论细节放在 rules 文件。

## Overall

- Current Stage: `W10 PASS / W11 CLOSE_PENDING`
- Overall State: `W02A_PASS / W07_PASS / SHOT_LIBRARY_READY / EDITOR_AUDIO_GATE_PASS / V3_2_PICTURE_LOCKED / EDIT_PREVIEW_QA_PASS / SUBTITLE_STYLE_QA_PASS / SUBTITLE_IMPLEMENTATION_QA_PASS / FINAL_TECH_QA_PASS / DELIVERABLE_RENDERED`
- Audio timeline hard gate: `PASS`
- Source normalization layer: `PASS / PROMOTED`
- Picture edit human gate: `PASS`
- Subtitle style: `PASS / LOCKED`
- Subtitle implementation: `PASS`
- Final technical QA: `PASS`

## Stage Board

| Stage | 内容 | 实际状态 | 备注 |
|---|---|---|---|
| W00 | 能力基线 | PASS | |
| W01 | 选歌 | HUMAN PASS | |
| W02 | BGM截取 | LOCKED | 37.120s + SHA |
| W02A | Audio Timeline Package | PASS / LOCKED | Director/Edit/Subtitle 唯一时间真源 |
| W03 | Natural Beat | PASS | canonical Package |
| W04 | Director | PASS | `树影之外` |
| W05 | 首帧 | PASS | 9/9 |
| W06 | 动态提示词 | PASS | 1–3镜混合素材 |
| W06-X | Seedance生成 | COMPLETE | 2S1–2S9 |
| W07 | Dynamic Source QA | PASS WITH TRIM | 风险窗已识别 |
| W07.5 | Shot Normalization | PASS / SHOT_LIBRARY_READY | 22 Atom/Arc；原片保留；WEB统一1.25×安全裁切 |
| W08A | Editor Audio Gate | PASS | locked BGM + Package revalidated |
| W08B | Picture Edit | PASS / V3.2 LOCKED | Atom-first；用户确认 |
| **W09** | **Subtitle** | **PASS / LOCKED** | R1-derived screenshot-calibrated baseline；padding10；bbox geometry gate |
| **W10** | **Final QA** | **PASS** | 0 audio lag；no black frames；watermark-risk sample clear |
| W11 | Close | HUMAN FINAL ACCEPTANCE PENDING | final package rendered |

## Locked subtitle baseline

Receipt:
`W09_SUBTITLE_STYLE_LOCK_RECEIPT.json`

At 720×1280:
- bold Chinese sans serif, nominal 46px;
- near-white text;
- center around `360,1009`;
- dark semi-transparent rounded box;
- four-side padding `10px`;
- max 2 lines;
- fade `100ms / 180ms`;
- actual rendered glyph bbox -> fresh box generation;
- no legacy rounded-path inset/scale;
- geometry auto QA: each side target ±1px and center error <=1px;
- mandatory short-line and two-line samples.

## W10 result

Receipt:
`W10_FINAL_TECH_QA_RECEIPT.json`

Final:
- 720×1280 / 24fps / 891 frames;
- picture 37.125s;
- audio 37.120s;
- global lag vs locked BGM `0.000000s`;
- subtitle max implementation delta `0.005s`;
- blackdetect events `0`;
- sampled top-left / bottom-right WEB watermark zones clear;
- final SHA `ac0cc8da59cebad3485a6da13c7d9a6d1ff00d4baaafbe2ffdfce2405b939286`.

## Current states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`
- `SHOT_LIBRARY_READY = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES`
- `SUBTITLE_STYLE_QA_PASS = YES`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
- `FINAL_TECH_QA_PASS = YES`
- `DELIVERABLE_RENDERED = YES`

## Next

W11 Close only:
- user final acceptance;
- close Round and preserve final reproducible assets / receipts / rules.
