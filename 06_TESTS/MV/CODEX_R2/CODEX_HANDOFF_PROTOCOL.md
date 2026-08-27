# CODEX R2｜External Handoff Protocol v1.0

A handoff is used only when the current Codex environment cannot perform a required external capability. It is not permission to fake completion or bypass the Canonical Runtime.

## Allowed handoff types

- `HUMAN_GATE_REQUIRED`
- `AUTHENTICATION_REQUIRED`
- `EXTERNAL_WEB_RESEARCH_REQUIRED`
- `EXTERNAL_FIRST_FRAME_GENERATION_REQUIRED`
- `EXTERNAL_DYNAMIC_VIDEO_GENERATION_REQUIRED`
- `EXTERNAL_MEDIA_INPUT_REQUIRED`

## Required handoff package

Create one small Markdown file under:
`06_TESTS/MV/CODEX_R2/handoffs/`

Filename:
`YYYYMMDD_HHMM_<TYPE>_<SLOT>.md`

It must contain:

1. slot and current Canonical stage;
2. exact reason the local environment cannot continue;
3. what Codex already completed and validated;
4. exact user/external action required — the smallest possible action;
5. all prompts/URLs/inputs needed;
6. expected output filenames;
7. local destination folder;
8. acceptance criteria;
9. exact resume command after files/approval return;
10. explicit statement of what Codex did NOT do.

## Media workspace

Use local ignored workspace:
`06_TESTS/MV/CODEX_R2/workspace/D03-B/`

Suggested folders:
- `inbox/`
- `first_frames/`
- `dynamic_sources/`
- `audio/`
- `renders/`
- `tmp/`

Do not commit raw media from this workspace.

## First-frame handoff

If Codex has no image-generation capability:
- produce one prompt file per K0 or one clearly indexed prompt set;
- preserve character/world continuity rules;
- specify 9:16 and exact filenames;
- include machine first-frame QA checklist;
- stop before claiming HG03 is reviewable until actual images exist.

Expected returned files should use deterministic names such as:
`D03-B_K01.png`, `D03-B_K02.png`, ...

## Dynamic-video handoff

If Codex cannot call Seedance/video generation:
- output one complete copy-ready dynamic prompt per accepted K0/source role;
- include duration/aspect/reference-image mapping;
- include hard character-closure / no-unplanned-character constraints when applicable;
- include expected filenames;
- state that generated clips are RAW SOURCE and will be QA/trimmed after return.

Suggested returned names:
`D03-B_V01.mp4`, `D03-B_V02.mp4`, ...

## Authentication handoff

For login/CAPTCHA:
- never request password, cookie, token or secret text;
- ask the user only to complete the browser-side authentication step;
- do not commit browser profiles or authenticated session data;
- continue automatically after the environment becomes available.

## Human Gate handoff

When a Human Gate is reached, present only the artifacts relevant to that Gate plus the decision the user needs to make. Do not bury the user in Runtime logs.

After the user responds, preserve the user's exact decision text for the `accept-gate` command.

## Resume rule

After every external handoff, the first operation is a fresh:

```bash
python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py resume --slot D03-B
```

Never continue from a stale remembered guard/state.