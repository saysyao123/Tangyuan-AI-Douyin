# LEAN_R1｜下一首真实 MV 测试卡

Status: `READY_TO_START`
Branch: `test/mv-lean-r1`
Planned slot: `D03-A`
Lane: `P / Primary-Trend`

## 1. Test purpose

This MV is a real production asset and simultaneously the Lean Runtime validation run.

Primary experiment variable: **process efficiency**, not new creative novelty.

We must prove:
- same five Human Gates;
- same canonical correctness / rollback / publish boundary;
- materially fewer controller round-trips and startup reads;
- no visual-quality regression;
- no per-song tool/model invention.

## 2. Creative isolation

This must be a completely new MV.

Do not inherit D02-B specifics:
- no automatic male-lead requirement;
- no coastal pale-stone architecture unless the new song independently demands it;
- no white-linen continuity;
- no forced wind/curtain/rain-afterglow engine;
- no reuse of D02-B framing, props or emotional arc.

Only reusable promoted knowledge may carry over:
1. lyric visual hit > light narrative > camera trick;
2. Director Thesis;
3. Primary Visual Engine;
4. explicit audiovisual relationship;
5. motive-first camera/subject/space;
6. WHY CUT HERE;
7. optional-element stop condition;
8. Creative Drift QA;
9. TRIM BEFORE REGENERATE;
10. accepted actual K0 pixels outrank superseded prose.

## 3. Lean execution target

User-visible normal decision points remain exactly:
- HG01 song;
- HG02 BGM excerpt;
- HG03 first-frame set / visual direction;
- HG04 picture edit;
- HG05 final.

Machine stages should be grouped:

`Audio Timeline -> Natural Beat -> Director`

`Dynamic QA -> conditional normalization -> Edit Map`

`Subtitle -> Final Tech QA`

Use `RUN_UNTIL_GATE_OR_BLOCK` after the corresponding artifacts are prepared. Use `ACCEPT_GATE` for each accepted Human Gate.

## 4. Audio route

After HG02:
- P0 same-version timed lyric/LRC first;
- P1 lightweight ASR mapping if P0 is unavailable/ambiguous;
- P2 heavy forced alignment only on concrete P1 failure;
- stop at first PASS;
- one lyric audit, not repeated evidence hunting.

## 5. Normalization route

Do not automatically pay the full normalization cost.

- clean single-shot source -> direct edit eligibility;
- multi-shot source -> atomize/Shot Library;
- WEB corner-mark / unsafe source -> clean proxy / rough-cut gate;
- source audio removed from formal picture edit.

## 6. PASS metrics

By S16:
- fixed Human Gates = 5;
- startup before actionable Runtime state <= 3 reads/calls;
- Lean controller command cycles target <= 12 excluding external image/video generation waits;
- no slot-specific core helper;
- no per-song model install;
- no default second alignment model;
- all canonical transition/Human Gate evidence valid;
- HG04/HG05 quality no worse than D02-B/R3 baseline.

## 7. Starting condition

D02-B is reserved in Lean Tracker as `RELEASE_READY` to prevent accidental reallocation. D03-A is the intended new slot. The first Lean RESUME must explicitly request D03-A and must return `ALLOCATE_NEW_SLOT` before initialization.
