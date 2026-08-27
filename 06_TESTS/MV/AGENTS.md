# AGENTS.md — MV-specific Codex R2 instructions

Scope: `06_TESTS/MV/**` on the Codex R2 branch.

## Codex R2 target

- Test branch: `test/mv-codex-r2`
- Test slot: `D03-B`
- Expected lane: `S`
- Program: `30D_60`
- Canonical program root: `06_TESTS/MV/WEB_R3/30D_60`
- Finish boundary for this test: `S16_RELEASE_PACKAGE_READY`

`D03-A` is inherited from the Lean R1 branch and is not the Codex R2 target. Always pass the explicit slot `D03-B` to Codex-side Runtime commands so another active slot cannot be selected accidentally.

## No second MV state machine

Do not recreate the old CODEX_R1 `C00 -> C08` state chain. Codex R2 uses only the Canonical S00-S18 registry. CODEX_R2 files track test metrics and handoffs, not production state.

## User-visible production phases

Canonical evidence remains fine-grained, but Codex should operate in coarse phases:

1. Resume / allocate / HG01 song selection.
2. HG01 accepted -> exact BGM discovery -> HG02.
3. HG02 accepted -> Audio Timeline -> Natural Beat -> Director -> first-frame package -> HG03.
4. HG03 accepted -> dynamic prompts -> external video generation handoff when required.
5. Dynamic sources returned -> source QA -> conditional normalization -> edit -> picture preview -> HG04.
6. HG04 accepted -> subtitle implementation -> final render/technical QA -> HG05.
7. HG05 accepted -> Release Package -> S16.

Do not expose every machine transition as a separate user interaction when `run-until` can safely compress already-valid transitions.

## Audio Timeline

Use the priority route already promoted into Lean R1:
`P0 same-version timed lyric/LRC -> P1 lightweight ASR mapping -> P2 heavy forced alignment only after a concrete failure`.

Stop at the first route that passes. Do not run multiple alignment stacks for reassurance. Do not install a production model per slot. P1 reusable tool: `04_HARNESS/tools/mv_audio_timeline/lightweight_align.py`.

## Director layer

Use `04_HARNESS/knowledge/MV_DIRECTOR_LEAN_OVERLAY.md` JIT. Preserve:
- Director Thesis;
- Primary Visual Engine;
- audiovisual relationship;
- motive-first camera / subject / space;
- WHY CUT HERE;
- optional-element trigger/function/range/stop condition;
- Creative Drift QA.

These are creative capabilities, not a new Human Gate.

## First frames and dynamic sources

- First frames are performable K0 anchors, not merely pretty stills.
- Accepted pixels outrank superseded prose.
- Dynamic video is RAW SOURCE, not automatically the final 5 seconds.
- TRIM BEFORE REGENERATE.
- If a source contains useful internal multi-shot atoms, atomize only when it materially improves the edit.
- Normalization is conditional: run full normalization only for multi-shot atomization, Web-source cleaning, proxy/codec requirements, or another explicit edit prerequisite.

## Edit and final

- The locked BGM identity/timeline is invariant at editor entry; never create a second lyric clock.
- Every meaningful cut should have a readable WHY CUT HERE.
- Edit Map -> render preview -> HG04.
- After HG04 PASS, subtitle implementation and Final Tech QA should normally run as one machine phase until a real block or HG05.
- After HG05 PASS, build Release Package and stop at S16 unless the user supplies real-world publication confirmation.
- Never write PUBLISHED or invent publish time before real publication evidence.

## External handoff

When Codex lacks an external capability, follow `06_TESTS/MV/CODEX_R2/CODEX_HANDOFF_PROTOCOL.md`. Handoff packages must contain exact prompts/inputs, expected filenames, destination folder, acceptance criteria, and the exact resume command.

## Codex R2 measurement

Maintain the final metrics requested by `CODEX_TEST_MATRIX.md`: Human Gate count, Codex operator invocations, external handoffs, unnecessary resumes, dependency installs, core helper creation, normalization trigger reason, regen count, commits, and final stage reached.