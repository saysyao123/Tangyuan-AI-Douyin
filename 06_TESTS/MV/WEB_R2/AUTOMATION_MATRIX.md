# WEB R2｜AUTOMATION MATRIX

> 只记录自动化/人工 Gate 状态；方法论细节放在 rules 文件。

## Overall

- Current Stage: `W09 / SUBTITLE_STYLE_OPTIMIZATION`
- Overall State: `W02A_PASS / W07_PASS / SHOT_LIBRARY_READY / EDITOR_AUDIO_GATE_PASS / V3_2_PICTURE_LOCKED / EDIT_PREVIEW_QA_PASS / SUBTITLE_STYLE_PENDING`
- Audio timeline hard gate: `PASS`
- Source normalization layer: `PASS / PROMOTED`
- Picture edit human gate: `PASS`
- Subtitle style: `NOT LOCKED`

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
| **W08B** | **Picture Edit** | **PASS / V3.2 LOCKED** | 用户确认“这次效果不错，按这个方案固化” |
| **W09** | **Subtitle** | **IN PROGRESS / STYLE OPTIMIZATION** | timing锁定；只优化形式与实现 |
| W10 | Final QA | NOT STARTED | |
| W11 | Close | NOT STARTED | |

## V3.2 locked picture basis

- accepted Edit Map: `W08B_V3_2_ATOMIC_ROUGH_EDIT_MAP.csv`
- receipt: `W08B_V3_2_PICTURE_GATE_PASS_RECEIPT.json`
- 13 selected visible units
- Atom-first; coherent Arc retained only when explicitly justified
- 891 frames / 24fps / 37.125s
- locked audio 37.120s
- preview-vs-locked-BGM lag `0.000000s`
- accepted preview SHA `797ac52cf470fb871f312b7699247b9f0bbc46120d1124813e39a459f4f1812f`

## Current states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`
- `SHOT_LIBRARY_READY = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next

W09 Subtitle Style Optimization:
- keep canonical `lyrics_exact.srt` timing unchanged;
- optimize typography, size, tight semi-transparent box, centering, padding, safe area, long-line wrap and restrained fade;
- inspect first/middle/longest/final lines;
- then run subtitle implementation QA against the canonical SRT.

After W09 PASS:
`W10 Final Polish + full-watch technical QA -> DELIVERABLE_RENDERED`.
