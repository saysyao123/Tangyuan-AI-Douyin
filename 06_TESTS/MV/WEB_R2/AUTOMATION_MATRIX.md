# WEB R2｜AUTOMATION MATRIX｜CLOSED

> Round final status. 只记录自动化/人工边界与最终 Gate；方法论由 `04_HARNESS/workflows|rules/` 负责。

## Overall

- Round Status: `COMPLETE_LOCKED`
- User Final Acceptance: `PASS`
- Audio timeline hard gate: `PASS / PROMOTED`
- Source normalization: `PASS / PROMOTED`
- Picture edit: `PASS / V3.2 LOCKED`
- Subtitle baseline: `PASS / LOCKED`
- Subtitle implementation QA: `PASS / PROMOTED`
- Final technical QA: `PASS`

## Final Stage Board

| Stage | 内容 | 自动化边界 | 最终状态 |
|---|---|---|---|
| W00 | Bootstrap | AUTO | PASS |
| W01 | Song Discovery | AUTO shortlist + HUMAN taste | `REFERENCE_BGM_LOCKED` |
| W02 | Exact BGM Clip | AUTO analysis/render + HUMAN listening | `BGM_LOCKED` |
| W02A | Audio Timeline Package | AUTO strong-evidence pipeline; conditional exception only | PASS / LOCKED |
| W03 | Natural Beat | AUTO | PASS |
| W04 | Director Allocation | AUTO | PASS |
| W05 | First Frames | AUTO generation/QA + HUMAN visual set gate | 9/9 PASS |
| W06 | Dynamic Prompt | AUTO design；external generation handoff | PASS |
| W06-X | Seedance generation | EXTERNAL USER/CAPABILITY | COMPLETE |
| W07 | Dynamic Source QA | AUTO | PASS WITH TRIM |
| W07.5 | Atom/Arc Normalization | AUTO | `SHOT_LIBRARY_READY` |
| W08A | Editor Audio Gate | AUTO | PASS |
| W08B | Picture Edit | AUTO edit/tech QA + HUMAN rhythm gate | V3.2 PASS / LOCKED |
| W09 | Subtitle | AUTO baseline/render/geometry/timing QA | PASS / LOCKED |
| W10 | Final QA | AUTO technical/full-watch/package + HUMAN final acceptance | PASS |
| W11 | Close | AUTO after final acceptance | `COMPLETE_LOCKED` |

---

## Fixed Human Gates｜future default

Reusable authority:
`04_HARNESS/rules/mv_human_gates.md`

Normal project target = **5 human confirmations**:

1. `HG01 Song Aesthetic Gate`
2. `HG02 BGM Excerpt Listening Gate`
3. `HG03 Visual Direction / First-frame Set Gate`
4. `HG04 Picture Edit Rhythm Gate`
5. `HG05 Final Acceptance Gate`

Conditional only:
- `CHG-A Audio Alignment Exception`
- `CHG-B Dynamic Regeneration Decision`
- `CHG-C New Subtitle Style`

If a normal MV repeatedly needs more than 5 human confirmations, review which technical Gate is missing or late.

---

## Stable AUTO responsibilities after R2

System should complete before asking user:
- BGM boundary contamination/incomplete-line checks；
- audio hash/version identity；
- strong Audio Timeline evidence/provenance/package gate；
- repeated-occurrence/timing QA；
- Director Beat/Allocation；
- set-level first-frame QA；
- dynamic source risk/clean-window mapping；
- source-audio strip；
- internal-cut mapping + Atom/Arc library；
- WEB batch watermark-safe normalization；
- Editor Audio Gate；
- three-clock Edit Map；
- Fragmentation Gate using external + visible-shot counts；
- audio global-lag check；
- locked subtitle baseline render；
- all-line glyph bbox / 10px geometry QA；
- subtitle timing implementation QA；
- final black/SAR/fps/audio/subtitle/package QA。

Users should no longer be the first detector of these implementation defects.

---

## Locked final identity

Song: `如果你也刚好抬头看树` / 孙天宇

BGM:
- source `139.930–177.050s`
- content `37.120s`
- SHA `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`

Final:
- `720×1280 / 24fps / 891 frames`
- picture `37.125s`
- audio `37.120s`
- global lag `0.000000s`
- subtitle max implementation delta `0.005s`
- blackdetect `0`
- SHA `ac0cc8da59cebad3485a6da13c7d9a6d1ff00d4baaafbe2ffdfce2405b939286`

---

## Reusable promoted files

- `04_HARNESS/workflows/mv.md` v1.7
- `04_HARNESS/rules/mv_golden_runtime.md` v1.4
- `04_HARNESS/rules/mv_audio_timeline.md`
- `04_HARNESS/rules/mv_human_gates.md`
- `04_HARNESS/rules/mv_editing.md`
- `04_HARNESS/rules/mv_source_normalization.md`
- `04_HARNESS/rules/mv_subtitle.md`
- `04_HARNESS/rules/ai_video.md`
- `04_HARNESS/templates/mv_zero_context_start_prompt.md`

Round retrospective:
`06_TESTS/MV/WEB_R2/WEB_R2_FINAL_RETROSPECTIVE_AND_SOP_v1.md`

Close receipt:
`06_TESTS/MV/WEB_R2/W11_CLOSE_RECEIPT.json`
