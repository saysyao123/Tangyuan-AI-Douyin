# Dola Expert Mode Findings v0.1

> Status: `EXPERIMENTAL PROVIDER ANALYSIS`
> Date: 2026-09-03
> Purpose: explain why benign MV prompts can be refused in Dola Expert Mode even when the underlying Seedance video route is available.

## 1. Working hypothesis

Treat Dola as two different provider surfaces rather than one:

1. `DOLA_EXPERT_AGENT`
   - chat/expert agent interprets the request;
   - may rewrite, refuse, or decide whether to invoke a video skill before the actual video job is submitted;
   - the natural-language refusal itself is therefore not sufficient evidence that Seedance 2.5 rejected the video job.

2. `DOLA_DIRECT_VIDEO`
   - dedicated video-generation surface;
   - model, duration and aspect ratio are real UI parameters;
   - prompt and reference images are submitted to the video generation path directly.

The current R1 A/C failures occurred on `DOLA_EXPERT_AGENT`; B succeeded. This is evidence of surface-level variability, not yet evidence of Seedance 2.5 model-level rejection.

## 2. Open-source evidence

Primary reference: `Shaun520/quota-flow` (MIT, public, actively updated in Aug-Sep 2026).

Its Dola WebView implementation documents the direct path as:

`open Dola -> video generation -> select model/duration/ratio -> upload references -> append prompt -> generate -> collect mp4`

Observed capabilities in that implementation:
- `Dreamina Seedance 2.5` is an allowed Dola model;
- duration choices are `5s / 10s`;
- aspect ratios include `9:16`;
- up to 10 reference images;
- modes include `multi_ref` and `text2video`;
- model/duration/ratio are UI parameters, not content that must be embedded into the generation prompt.

Recent repository commits also show active adaptation to Dola's real DOM:
- Radix menu selection required real input events;
- multi-image upload was changed to Dola's official file input;
- Dola output can be HEVC and may need local playback conversion.

This makes the repository useful evidence for *surface behavior*. We should not copy its multi-account/quota-pooling or cookie automation architecture into this MV Harness.

## 3. Content-block evidence

The same project detects a Dola block by scanning visible page text for terms such as content review, cannot generate, copyright, portrait, sensitive, risk, refusal, etc. Its dispatcher treats a content-policy block as unrelated to account switching.

Therefore a `BLOCKED` result should be logged as a content/surface event, not automatically retried through another account.

## 4. Dola policy context

Dola publicly states that it uses automated moderation plus human review and may evaluate signals including keywords and images. Its published Community Guidelines focus on harmful/illegal/sexual/violent and rights-sensitive content; ordinary adult hand-to-face movement or water-hand interaction is not explicitly listed as a prohibited category.

Thus the A/C explanations returned by Expert Mode (for example treating benign hand-face interaction or water in a hand as inherently disallowed) should be treated as possible false-positive classification or agent interpretation until tested on a direct video surface.

This is not a reason to bypass genuine safety controls. The correct response is to isolate the surface and simplify benign production language, while preserving the actual creative intent.

## 5. Harness change

Provider result must record:

```yaml
provider: dola
surface: EXPERT_AGENT | DIRECT_VIDEO
stage_reached: AGENT_INTERPRETATION | VIDEO_JOB_SUBMITTED | VIDEO_RENDERING | VIDEO_OUTPUT
status: PASS | BLOCKED | FAILED
blocked_text: null
```

Key distinction:
- refusal before `VIDEO_JOB_SUBMITTED` = Expert Agent / orchestration result;
- block after a real video job is submitted = video provider/model moderation result.

Do not merge these two failure classes.

## 6. Prompt strategy for Expert Mode

Expert Mode should receive a short execution wrapper plus a compact Seedance production prompt.

Avoid making the Expert Agent reason over a long policy-like prompt containing many repeated phrases such as `face`, `touch`, `skin`, `liquid`, `contact`, `hard constraint`, `do not`, etc. Those phrases may be legitimate production descriptions but can unnecessarily increase semantic ambiguity before the video tool is even called.

Recommended structure:

1. task header: use Seedance 2.5, reference image, 5s, 9:16;
2. one-sentence director goal;
3. 3-stage positive action progression;
4. one camera instruction;
5. 2-3 continuity constraints;
6. audio intent only if needed.

Do not add text claiming that a real-person reference is fictional. Provenance statements must stay factual.

## 7. Next diagnostic test

Before comparing Legacy vs Lean at the Seedance level, first run an `EXPERT_AGENT_COMPATIBILITY` mini-test:

- B is current positive control (already generated);
- rewrite A without physical face contact: hand moves through a near-face arc while gaze/head respond;
- rewrite C so water is released from a small neutral vessel into the basin, preserving the same gravity/impact/ripple physics objective;
- keep K0, Seedance 2.5, 5s, 9:16 and single-shot structure constant;
- record whether Expert Mode actually reaches video generation.

If these pass, the issue is likely the Expert Agent semantic layer. If the direct Dola video surface accepts the original A/C while Expert Mode rejects them, the separation is confirmed.

## 8. Low-confidence sources not promoted

A separate public `dola-seedance-adapter` repository hardcodes an unknown IP endpoint, 30-second requests and up to 30 images. Those claims conflict with the actively maintained Dola WebView evidence above and are not treated as provider truth.

Rule: prefer observed Dola UI behavior and repeated independent evidence over an unofficial adapter's constants.
