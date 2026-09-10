# 《爱让人脑袋空空》｜Full Timeline Lock v1

> Project: MV Reference Director Skill / first real run
> Status: `TIMELINE_LOCKED`
> Primary Reference: user-selected Douyin clip from 乐♩青春 candidate
> Source clip duration: `15.370998s`
> Video probe: `1920x1080 / 30fps / H.264`
> Audio probe: `AAC / 44.1kHz / stereo / 15.370998s`
> Locked audio policy: use the exact audio extracted from the selected reference video as the project BGM / Audio Version. Do not substitute another cover/remix/full-song master unless explicitly re-locked.

## 1. Timeline-First hard rule

This file is the authoritative timeline for the current project.

No Reference Deconstruction, Animation Director, K0, Dynamic Prompt, or Generation may contradict this timeline.

If the BGM / Audio Version changes, this Timeline and all downstream outputs become invalid and must be rebuilt.

---

## 2. Exact lyric / visual-caption timeline

Timing evidence comes from the selected 30fps reference clip. Subtitle/shot boundaries were refined at frame level. Audio beat/onset analysis is used as secondary evidence, not as a replacement for lyric timing.

| # | Start | End | Duration | Lyric / Audio Function | Boundary Evidence |
|---|---:|---:|---:|---|---|
| T00 | 0.000 | 0.400 | 0.400 | musical pickup / opening accent | strong initial audio onset; lyric text not yet fully visible |
| T01 | 0.400 | 0.780 | 0.380 | `爱 爱` | subtitle pickup appears |
| T02 | 0.780 | 1.567 | 0.787 | `爱总是` | subtitle wording expands; next shot/line at 1.567 |
| T03 | 1.567 | 2.517 | 0.950 | `好了疤` | exact visual boundary; next lyric at ~2.517 |
| T04 | 2.517 | 3.400 | 0.883 | `忘了痛` | exact lyric/visual boundary at 3.400 |
| T05 | 3.400 | 4.933 | 1.533 | `让人脑袋空空` | shot + subtitle boundary |
| T06 | 4.933 | 6.633 | 1.700 | `直到心破了洞` | shot + subtitle boundary |
| T07 | 6.633 | 7.333 | 0.700 | `见了红` | shot + subtitle boundary |
| T08 | 7.333 | 8.700 | 1.367 | `换来步履匆匆` | shot + subtitle boundary |
| T09 | 8.700 | 10.533 | 1.833 | `从开始情有独钟` | major semantic reset + shot/subtitle boundary |
| T10 | 10.533 | 12.333 | 1.800 | `到最后泪眼汹涌` | shot/subtitle boundary |
| T11 | 12.333 | 13.767 | 1.434 | `承诺全被风吹得` | shot/subtitle boundary |
| T12 | 13.767 | 15.371 | 1.604 | `无影无踪` | final lyric unit to clip end; internal visual cut at ~14.433 does not change lyric unit |

Total locked duration: `15.370998s`.

---

## 3. Beat / accent analysis

Automated onset/beat analysis on the exact extracted audio gives an estimated tempo of approximately `129.2 BPM` (median beat interval ~`0.4644s`; possible half-time feel ~64.6 BPM).

Representative beat grid / accents:

`0.081, 0.673, 1.138, 1.591, 2.055, 2.508, 2.949, 3.425, 3.913, 4.354, 4.841, 5.294, 5.759, 6.211, 6.641, 7.140, 7.593, 8.069, 8.533, 8.986, 9.451, 9.903, 10.379, 10.832, 11.297, 11.761, 12.225, 12.678, 13.119 ...`

Strong useful accents include approximately:

- `0.08s` opening hit
- `3.40s` / nearby beat `3.425s`: `让人脑袋空空`
- `4.93s` / nearby onset `5.03s`: `直到心破了洞`
- `6.63s` / beat `6.641s`: `见了红`
- `7.33s` / onset cluster `7.37–7.59s`: `换来步履匆匆`
- `8.70s` / onset `8.707s`: **major structural reset**
- `10.53s` / onset `10.588s`: `到最后泪眼汹涌`
- `12.33s` / onset `12.353s`: `承诺全被风吹得`
- `13.77s` / onset `13.804s`: `无影无踪`
- `~14.99s` late ending accent inside the final lyric hold

Beat estimates guide motion/camera accents; lyric boundaries remain the primary editing truth.

---

## 4. Emotional structure

### E1｜0.000–3.400
`爱 爱 / 爱总是 / 好了疤 / 忘了痛`

Function: hook + habitual emotional cycle.

### E2｜3.400–8.700
`让人脑袋空空 / 直到心破了洞 / 见了红 / 换来步履匆匆`

Function: consequence escalates from emptiness → wound → visible cost → hurried movement.

### E3｜8.700–12.333
`从开始情有独钟 / 到最后泪眼汹涌`

Function: retrospective contrast; clear new emotional paragraph.

### E4｜12.333–15.371
`承诺全被风吹得 / 无影无踪`

Function: release / disappearance / ending residue.

---

## 5. Legal segment cut points

Candidate cut points must preserve lyric syntax, emotional meaning, and musical structure.

### Preferred hard cut｜`8.700s`

Why:

- completes the full first consequence unit through `换来步履匆匆`;
- `从开始情有独钟` begins a new semantic paragraph;
- exact shot/subtitle boundary;
- strong local onset around `8.707s`;
- creates two valid generation units within the 5–15s policy.

Result:

- **Segment A: 0.000–8.700s = 8.700s**
- **Segment B: 8.700–15.371s = 6.671s**

### Secondary possible boundaries

- `3.400s`: lyric hook → consequence, too short as a standalone production segment under current default.
- `4.933s`: strong phrase transition, but produces an imbalanced remainder.
- `7.333s`: valid shot/lyric boundary but splits `见了红 → 换来步履匆匆`, therefore not preferred.
- `10.533s`: valid lyric boundary but leaves only ~4.84s remainder, below current preferred minimum.
- `12.333s`: valid emotional boundary but leaves only ~3.04s remainder, not preferred for standalone I2V.

**LOCKED segment plan candidate for next phase: `8.700s + 6.671s`.**

The Segment Plan itself becomes formally locked in Phase E, after this Timeline Lock is accepted as the upstream truth.

---

## 6. Timeline QA

- [x] Exact media duration probed.
- [x] Exact selected audio version defined by extracted reference audio.
- [x] Full lyric / audio-event coverage from 0.000 to 15.371.
- [x] Key beat / accent evidence measured.
- [x] Emotional boundaries defined.
- [x] Candidate cut points evaluated.
- [x] No unresolved timing ambiguity blocks downstream work.
- [x] `TIMELINE_LOCKED`.

---

## 7. Downstream contract

Next stage must consume this timeline rather than recreate it.

Required sequence:

`TIMELINE_LOCKED → Segment/Duration Plan → Reference Deconstruction → Animation Director → K0-A/K0-B → Dynamic Prompts → Generation`

Do not return to the previous estimated `~7.7s` split. That estimate is superseded by the frame/lyric/beat-aligned `8.700s` primary cut.