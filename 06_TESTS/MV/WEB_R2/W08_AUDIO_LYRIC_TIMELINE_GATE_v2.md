# WEB R2｜W08 Audio / Lyric Timeline Gate v2

> Status: `BLOCKING_GATE / NOT YET LOCKED`
> Purpose: prevent any edit / beat-cut / subtitle render before the locked BGM has an independently verified lyric timeline.
> Trigger: W08 first-cut technical rescue on 2026-08-21.

## 1. Why this gate exists

The first WEB R2 edit was rendered before the lyric timeline itself had been locked. The assistant used exact lyric text plus waveform / phrase-valley estimates, but treated that as sufficient timing evidence and proceeded to picture editing and subtitle burn-in.

That was a process failure.

Consequences:
- subtitle line boundaries were wrong;
- picture cuts were mapped to an unverified lyric/phrase timing model;
- perceived beat / lyric hit was therefore also unreliable;
- the user had to identify a failure that should have been blocked before rendering.

Classification: `TECHNICAL_RESCUE`, not `AESTHETIC_GATE`.

The first cut remains only as a failure artifact and must not be used as timing truth.

---

## 2. Golden R1 evidence restored

Round 01 already established and user-accepted:

1. subtitle timing comes from the **locked audio itself**, never visual segment boundaries;
2. v3 timing derived from visual segmentation was wrong;
3. corrected same-version lyric timing was user-reviewed as accurate;
4. accepted subtitle visual baseline:
   - Chinese lyrics;
   - light text;
   - dark semi-transparent rounded box tightly fitted to text;
   - text visually centered horizontally and vertically inside box;
   - fixed comfortable lower safe-area placement;
   - restrained fade;
   - max 2 lines;
   - no base karaoke / word-by-word effect.

R1 preferred timing evidence order:
`actual ASR/forced alignment -> constrain/correct against exact known lyrics -> same-version LRC when reliable -> boundary spot-check -> final subtitle asset`.

---

## 3. Locked WEB R2 audio identity

Song: `如果你也刚好抬头看树` — 孙天宇

Source excerpt:
- source interval: `139.930s–177.050s`
- rendered duration: `37.120s`
- fade in: `0.020s`
- fade out: `0.950s`
- locked file SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`

No downstream process may silently substitute another audio file/version.

---

## 4. Exact lyric text lock

The locked excerpt contains these nine lyric lines, in this exact order:

1. 如果你也刚好抬头看树
2. 我要学着树叶翩翩起舞
3. 喊几声布谷布谷
4. 或许少有人知道
5. 有鸟儿是这样叫
6. 好吧哎哟哎哟
7. 一颗心叽叽喳喳飞过了树梢
8. 如果你也刚好抬头看树
9. 向一朵白云学习如何漂浮

`LYRIC_TEXT_LOCKED = YES`

---

## 5. Acoustic candidates — NOT timing truth

The following are only acoustic candidates derived from beat/onset/energy evidence. They are explicitly **not** allowed to drive the edit or subtitles until independently verified:

- L1 candidate start: ~`0.49s`
- L2 candidate start: ~`5.14–5.46s`
- L3 candidate start: ~`10.97s`
- L4 candidate start: ~`13.27–13.85s`
- L5 candidate start: ~`16.3–16.8s`
- L6 candidate start: ~`19.4–19.7s`
- L7 candidate start: ~`23.2–23.8s`
- L8 candidate start: ~`28.45s`
- L9 candidate start: ~`32.6–33.1s`
- likely lyric resolution before ~`35.65s`, followed by musical/fade tail.

Known breath / phrase valleys include roughly:
`4.81–5.33 / 10.68 / 15.85–16.35 / 18.80–19.39 / 21.98–23.34 / 26.77–28.38 / 32.54–32.82 / 35.65–37.12`.

These values are diagnostic evidence only.

`LYRIC_TIMELINE_LOCKED = NO`

---

## 6. Mandatory timing evidence hierarchy

A lyric timeline may be promoted to `LOCKED` only after at least one strong timing source exists and is cross-checked against the locked audio:

### Preferred evidence
1. actual ASR / forced alignment on the locked 37.120s audio;
2. reliable same-version LRC / timed lyric source;
3. exact timestamps from an official same-version lyric video/source when directly verifiable.

### Required correction layer
Regardless of source, constrain transcription/alignment to the exact nine-line lyric text and verify:
- line ordering;
- no omitted/repeated words;
- start boundary;
- end boundary;
- repeated title line distinguished correctly;
- final release line ends before the locked fade tail.

### Forbidden downgrade
Plain waveform valleys, BPM grid, rough phrase-length estimation, or picture-cut boundaries **cannot by themselves** promote the timeline to locked status.

If strong timing evidence is unavailable:
`STATE = LYRIC_TIMELINE_BLOCKED`

Do not guess and do not render.

---

## 7. Mandatory boundary self-audit

Before `LYRIC_TIMELINE_LOCKED = YES`, perform and record all checks:

1. verify locked audio hash/version;
2. verify exact nine-line lyric text;
3. create line-level start/end timestamps from strong timing evidence;
4. cross-check every line against acoustic onset/valley evidence;
5. inspect/listen around every line start and end, approximately ±0.5s where tooling permits;
6. independently inspect the first ~3s and last ~4s;
7. replay/inspect the whole excerpt end-to-end against the provisional timestamps;
8. confirm repeated title line L1 and L8 are mapped to distinct occurrences;
9. export a durable timing asset (`.srt` / `.lrc` / structured CSV/MD);
10. only then mark the timeline locked.

Any failed boundary sends the task back to alignment; it must not be deferred to the user as first-cut feedback.

---

## 8. Edit must come AFTER this gate

Only after both are true:

- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_TIMELINE_LOCKED = YES`

may the system create `EDIT_MAP_LOCKED`.

The edit map must be derived from:
- exact lyric line windows;
- beat/downbeat/onset map;
- semantic turns;
- visual source motion arcs;
- internal source clip clean windows;
- release/tail requirements.

Each picture cut should have a reason. Picture cuts may occur inside a lyric when musically/directorially justified, but lyric subtitle timing remains independent of picture boundaries.

---

## 9. Subtitle visual Golden Gate

Before burning subtitles:

1. reload the R1 Golden subtitle specification;
2. do not invent a new visual system from memory;
3. verify:
   - light Chinese text;
   - dark semi-transparent rounded box;
   - box tightly fits the actual line;
   - horizontal + vertical centering inside box;
   - consistent padding;
   - comfortable fixed lower safe area;
   - restrained fade;
   - max 2 lines;
   - no accidental lyric overflow;
4. render/check representative first / middle / final lyric frames before full export.

`SUBTITLE_STYLE_QA_PASS` is required before final render.

---

## 10. W08 no-skip state chain

The runtime state chain is now:

`BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_SYNC_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

A later state is invalid if any previous state is missing.

---

## 11. Current WEB R2 state

- `BGM_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_TIMELINE_LOCKED = NO`
- `BEAT_MAP_VERIFIED = PARTIAL / diagnostic only`
- `EDIT_MAP_LOCKED = NO`
- `DELIVERABLE_RENDERED = NO`

The previous first cut is explicitly revoked as a valid W08 deliverable.
