# WEB R2｜AUTOMATION MATRIX

> 只记录自动化/人工 Gate 状态；方法论细节放在 rules 文件。

## Overall

- Current Stage: `W08B / V3.2_ATOMIC_ROUGH_VIEWING_GATE`
- Overall State: `W02A_PASS / W07_PASS / SHOT_LIBRARY_READY / EDITOR_AUDIO_GATE_PASS / V3_1_BETTER / V3_2_RENDERED / HUMAN_VIEW_PENDING`
- Audio timeline hard gate: `PASS`
- Source normalization layer: `IMPLEMENTED`
- Subtitle style: `NOT LOCKED`

## Stage Board

| Stage | 内容 | 实际状态 | 备注 |
|---|---|---|---|
| W00 | 能力基线 | PASS | |
| W01 | 选歌 | HUMAN PASS | |
| W02 | BGM截取 | LOCKED | 37.120s + SHA |
| W02A | Audio Timeline Package | PASS / LOCKED | Director/Edit/Subtitle 唯一时间真源 |
| W03 | Natural Beat | PASS | 使用 canonical Package |
| W04 | Director | PASS | `树影之外` |
| W05 | 首帧 | PASS | 9/9 |
| W06 | 动态提示词 | PASS | 1–3镜混合素材 |
| W06-X | Seedance生成 | COMPLETE | 2S1–2S9 |
| W07 | Dynamic Source QA | PASS WITH TRIM | 风险窗已识别 |
| **W07.5** | **Shot Normalization** | **PASS / SHOT_LIBRARY_READY** | 9原片保留；22 Atom/Arc；统一WEB安全放大裁切 |
| W08A | Editor Audio Gate | PASS | locked BGM + Package revalidated |
| **W08B** | **Picture Edit** | **V3.1 better / V3.2 atomic rough rendered / HUMAN VIEW** | 需要决定 Atom 或 Atom-first Hybrid |
| W09 | Subtitle | PENDING | timing锁定；style未锁 |
| W10 | Final QA | NOT STARTED | |
| W11 | Close | NOT STARTED | |

## W07.5 normalization result

- authority rule: `04_HARNESS/rules/mv_source_normalization.md` v1.0
- map: `W07_5_NORMALIZED_SHOT_LIBRARY_MAP.csv`
- 22 usable derived Atom/Arc units
- rejected: duplicate / topology-risk / meaningless micro-shots
- source audio removed from derived WEB proxies
- WEB transform: `crop 576×1024 @ (72,128) -> scale 720×1280`, approx `1.25×`
- reviewed corner marks: clear in normalized contact review

## V3.2 result

- Edit Map: `W08B_V3_2_ATOMIC_ROUGH_EDIT_MAP.csv`
- QA: `W07_5_W08B_V3_2_ATOMIC_ROUGH_QA.md`
- 13 explicitly selected visible Atom units
- 891 frames / 24fps / 37.125s
- audio 37.120s
- preview-vs-locked-BGM lag: `0.000000s`
- preview SHA: `797ac52cf470fb871f312b7699247b9f0bbc46120d1124813e39a459f4f1812f`

## Current decision Gate

V3.2 is not auto-accepted merely because it is more controllable.
Human viewing must choose:
- `ATOM` final basis; or
- `ATOM-FIRST HYBRID`, retaining only intentionally valuable coherent Arcs.

After picture basis passes:
`EDIT_MAP_LOCKED -> EDIT_PREVIEW_QA_PASS -> W09 Subtitle Style -> Subtitle Implementation -> W10 Final QA`.

## Current states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`
- `SHOT_LIBRARY_READY = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = NO`
- `V3_2_ATOMIC_ROUGH_RENDERED = YES`
- `V3_2_TECH_QA_PASS = YES`
- `EDIT_PREVIEW_QA_PASS = NO / HUMAN_VIEW_PENDING`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`
