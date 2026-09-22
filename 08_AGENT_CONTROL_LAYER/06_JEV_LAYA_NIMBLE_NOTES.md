# 06 — Jev / Laya / Nimble Research Notes

> Purpose: preserve the architectural conclusions that led to the Agent Control Layer. This is not a claim that any external model is currently required in production.

## 1. Jev

### Useful concept
Jev/System-One reframes model work as narrow probabilistic decisions rather than open-ended generation.

Useful primitives:
- Choice
- Score
- Noul / proposition-like judgment

Architectural lessons:
- code should own workflow;
- uncertainty should route;
- narrow decisions are easier to validate;
- output space should be bounded.

Important limitation for our video use:
- the decision layer is not itself a replacement for video perception;
- wrong upstream evidence can still lead to confidently wrong decisions.

Adoption:
- borrow the decision architecture first;
- do not require Jev as a dependency.

References:
- https://typesafe.ai/
- https://github.com/typesafe-ai/skills
- https://github.com/typesafe-ai/system-one-adapter-python

## 2. Laya

### What it demonstrates
A small encoder-based model can become a useful specialized workflow Judge after domain training.

The main value is not zero-shot intelligence. It is:
- specialization;
- consistency;
- stateless execution;
- calibration as an explicit objective;
- cheap repeated inference.

Important conclusion:
The published specialized checkpoint performs far better than the base zero-shot checkpoints on its trained decision domains. Therefore Laya is best understood as a **Judge training platform / compiled Judge**, not an out-of-the-box universal reviewer.

Risks for our use:
- current Chinese/video-production domain is unvalidated;
- calibration must be redone on held-out project data;
- no direct visual/video perception;
- training labels must include real/human ground truth rather than only GPT labels.

Adoption:
- do not deploy now;
- collect Stage Judge data first;
- later train one narrow stable Gate if evidence supports it.

Reference:
- https://github.com/NandhaKishorM/laya

## 3. Nimble

### What it demonstrates
A general generative LLM (Qwen3.5-9B) can be adapted into a strong typed decision model.

Key methods worth copying even without its model:
- bounded candidates;
- candidate scoring rather than open essay generation;
- independent fields;
- small context;
- explicit no-match / unknown options;
- contrastive/counterfactual data pairs;
- versioned scoring prompt;
- regression testing.

The part we cannot directly reproduce in normal ChatGPT:
- direct access to internal candidate-token logits.

But most workflow benefits can still be approximated by:
- strict structured outputs;
- fresh context;
- atomic questions;
- deterministic routing outside the model;
- contrastive regression tests.

Adoption:
- use Nimble as the main reference for GPT-Nimble Judge v0.1;
- do not deploy Qwen/Nimble until the GPT approach has been tested.

Reference:
- https://github.com/bespokelabsai/nimble

## 4. Current backend strategy

```text
New / complex / low-frequency judgment
        -> GPT-5.6 Fresh Judge

Deterministic fact
        -> Code / State

Mature / repetitive / high-volume judgment
        -> future Laya/Nimble candidate

Creative or diagnostic work
        -> GPT-5.6 Executor / Diagnostic
```

## 5. What should reduce hallucination

The architecture primarily targets:
- state hallucination;
- process drift;
- forgotten locked rules;
- self-review bias;
- false stage completion;
- uncontrolled context inheritance.

It does **not** automatically solve:
- visual perception errors;
- wrong ASR;
- incorrect upstream evidence;
- subjective aesthetic disagreement.

## 6. Research question to keep open

After the GPT Fresh Judge pilot, compare:

```text
GPT Fresh Judge
vs
Laya-style trained Judge
vs
Nimble/Qwen-style trained Judge
```

using exactly the same contracts and held-out regression suite.

Do not compare them using different tasks or different labels.
