# D02-B｜Dynamic Prompt Set v2 — Dense Lyric-First Multi-Shot

Status: `READY / GENERATED_AND_QA_VALIDATED`

Global production rules:
- 5s, 9:16, same fictional adult East Asian male, same pale limestone coastal colonnade, warm-white linen shirt + pale trousers.
- Actual accepted first-frame pixels are K0 authority.
- Standard 2D orthogonal black square grid is a temporary anonymity layer only; when face is readable, complete face reconstruction occurs first with low subject/camera load, then heavier action starts.
- No second person. No new prop. No AI dialogue, narration or BGM; only light physical environment sound. Final edit strips all source audio.
- Each source is editing material, not a final five-second shot. Internal cuts require a semantic/action reason.

## H-S01 | 有几次想你了 -> 有几次忍住了
Structure: 2 authored shots, generated output may expose extra atom.
1. APPROACH: controlled natural approach; camera lightly LEADs backward while distance still closes.
2. RESTRAINT: use column/linen occlusion for motivated cut; hand reaches current boundary/linen then stops; camera HOLDs.
Desired atoms: approach / boundary-hand detail / restrained side relation.

## H-S02 | 有几句想说的 -> 都变成算了
1. UNFINISHED EXPRESSION: near-static HOLD; slight inhale, eye-line and shoulder tension; no speech mouth movement.
2. WITHDRAW: cut on column/occlusion when intention changes; hand/gaze withdraw; body commits to leaving; camera YIELDs a path.
Desired atoms: almost-speaking relation / withdrawal-turn.

## H-S03 | 有几场雨停了
Actual K0: front-moving man in visibly wet post-rain corridor.
1. AFTER-RAIN WORLD: wet limestone and returning light remain readable; no active rain.
2. RAIN TRACE DETAIL: cut on footstep to low wet-stone detail; residual water only, no large splash.
3. LIGHT RETURNS: match back to person entering warmer light.
Desired atoms: wet-world / foot-wet-stone detail / warm-light return.

## H-S04 | 有几阵风过了
1. ONE GUST: one coherent sea gust moves hair < linen shirt < large linen in increasing amplitude; side-rear FOLLOW.
2. LINEN RESIDUE: use lifted linen as motivated occlusion cut; gust falls away; linen remains in delayed return swing; camera HOLD.
Desired atoms: wind-through-body / linen residue.

## H-S05 | 有多舍不得，也该放下了
1. ATTACHMENT: body already leaving while right hand still holds current linen; camera relational HOLD.
2. RELEASE: cut along arm to hand; fingers naturally loosen and fully release linen; no symbolic object.
3. WORLD OPEN: linen creates final occlusion cut; wider rear view; person continues forward; camera STOP PURSUING; final tail holds with no new event.
Desired atoms: still-holding / hand release / world-open release.

Success criteria:
- all 7 lyric lines map to at least one visible atom;
- expected usable normalized pool >=9 atoms;
- camera grammar remains motivated: LEAD -> HOLD -> YIELD -> DISCOVER/FOLLOW -> RELEASE -> STOP PURSUING;
- `TRIM BEFORE REGENERATE`.
