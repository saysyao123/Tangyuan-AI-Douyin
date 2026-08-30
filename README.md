# Tangyuan AI Douyin

**A reproducible, test-driven production harness for AI-assisted short-form video and music-MV workflows.**

> Status: **Early public OSS / active development**  
> Current validated runtime: **R3**, under cross-song production hardening on branch `test/mv-web-r3`.

Tangyuan AI Douyin started as a real-world short-video production experiment and has evolved into a structured runtime for turning fragile, ad-hoc AI media workflows into **stateful, auditable, reusable production systems**.

The project treats creative production more like software engineering:

`experiment -> evidence -> rule -> gate -> regression -> promotion`

Instead of keeping successful prompts as isolated notes, the repository records why a workflow works, where it fails, how it is tested, and when an experimental technique is safe to promote into the production runtime.

## Why this project exists

AI video workflows often fail for reasons that are difficult to reproduce: wrong audio versions, drifting timelines, weak shot semantics, inconsistent first frames, unstable image-to-video motion, repeated camera grammar, or local failures that trigger unnecessary full-project rewrites.

This repository addresses those problems with:

- explicit production stages and rollback boundaries;
- human decision gates and machine QA gates;
- durable project state and handoff artifacts;
- exact audio/version provenance and timeline packages;
- director and camera-language rules;
- first-frame and image-to-video control contracts;
- source normalization and editability checks;
- evidence tiers for experimental vs production-ready techniques;
- cross-song regression before promoting new rules;
- post-publish data capture for production and content evaluation.

## Current MV runtime

The active R3 workflow uses a single production path:

`Song Discovery`
→ `Douyin-first Exact BGM Version Discovery`
→ `Exact BGM Clip Lock`
→ `AUDIO_TIMELINE_PACKAGE`
→ `Natural Beat`
→ `Director Allocation`
→ `First Frames`
→ `Dynamic Source Generation`
→ `Dynamic QA`
→ `Shot Normalization`
→ `Editor Audio Revalidation`
→ `Picture Edit`
→ `Subtitle Render + QA`
→ `Final QA`
→ `Post-Publish Sync`

The runtime is intentionally split into a small authoritative workflow plus **JIT-loaded rules** so an agent does not need to load the entire project history for every task.

Key R3 entry points:

- [`04_HARNESS/workflows/mv.md`](https://github.com/saysyao123/Tangyuan-AI-Douyin/blob/test/mv-web-r3/04_HARNESS/workflows/mv.md) — authoritative MV workflow
- [`05_IP_ASSETS/MV_30D_60_OPERATING_SYSTEM.md`](https://github.com/saysyao123/Tangyuan-AI-Douyin/blob/test/mv-web-r3/05_IP_ASSETS/MV_30D_60_OPERATING_SYSTEM.md) — 30-day / 60-MV operating system
- [`05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`](https://github.com/saysyao123/Tangyuan-AI-Douyin/blob/test/mv-web-r3/05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md) — zero-context agent restart entry point
- [`04_HARNESS/rules/ai_video.md`](https://github.com/saysyao123/Tangyuan-AI-Douyin/blob/test/mv-web-r3/04_HARNESS/rules/ai_video.md) — first-frame and image-to-video production contract

## What is reusable

The repository is not a collection of one-off MV prompts. Reusable components include:

### 1. Audio truth layer
- exact source/version identification;
- locked BGM provenance;
- forced-alignment-ready timeline package;
- line, anchor-word and music-event timing;
- downstream invalidation rules when audio changes.

### 2. Director runtime
- lyric-specific visual hit checks;
- Natural Beat allocation;
- `HOLD / BRIDGE / HIT / PEAK / RELEASE` edit roles;
- camera-subject relationship design;
- camera repetition gates;
- separation of conceptual beats, source segments and final edit fragments.

### 3. First-frame + I2V runtime
- 0-second dynamic-anchor first frames;
- full-set first-frame QA;
- accepted K0 pixel authority;
- first-frame character closure;
- bounded 5-second motion contracts;
- `STATIC BASE -> ONE EVENT -> RESIDUE -> CLEAN ENDPOINT` generation logic;
- local regeneration instead of cascade regeneration.

### 4. Evidence and regression model
New techniques are not promoted because they worked once. The project distinguishes:

- `EXPERIMENTAL / POSITIVE EVIDENCE`
- `PRODUCTION-READY EXPERIMENTAL`
- `CROSS-SONG HARDENED`
- authoritative production rules

This makes failures and improvements traceable across songs and production rounds.

## 30D / 60-MV production experiment

The current public-production experiment tests whether the validated R3 workflow can scale to roughly **60 controlled MV publication samples in 30 days** without collapsing visual quality or production consistency.

The workload is separated into three lanes:

- **P — Primary / Trend:** highest-quality baseline;
- **S — Stable / Fast:** lower-complexity, repeatable production;
- **R — R&D:** one major experimental variable per MV.

The goal is not to claim 60 viral videos. The goal is to create enough controlled production and publishing evidence to measure which workflows, camera grammars, visual motifs and production rules actually repeat.

## Repository structure

```text
00_CONTROL/       project control, master state, handoff
01_TOPIC_SYSTEM/  topic / candidate systems
02_DAILY/         daily production archives
03_DATA/          experiment and performance data
04_HARNESS/       authoritative workflows, rules, knowledge, QA
05_IP_ASSETS/     account and production operating systems
06_PRODUCTION/    production artifacts
06_TEMPLATES/     reusable templates
99_INBOX/         incoming handoff / staging
```

Experimental branches may additionally contain test receipts and regression artifacts under `06_TESTS/`.

## Dola Seedance 2.5 experimental workbench

The repository also contains a separately scoped Dola Seedance 2.5 workbench under
[`06_PRODUCTION/dola-seedance25-workbench/`](06_PRODUCTION/dola-seedance25-workbench/).
It includes the Windows multi-account control plane, the media-identity resolver,
sanitized test evidence, and an external-AI analysis brief. It is experimental:
real Dola generation, clean-source delivery, native 5-second output, and real
multi-account capacity remain evidence-gated and must not be inferred from
configuration or assistant acknowledgement alone.

## Quick start for an agent-assisted MV run

1. Clone the repository.
2. Check out `test/mv-web-r3` while R3 is being promoted to main.
3. Start from `05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`.
4. Load only the authoritative runtime files listed there.
5. Respect Human Gates; do not skip directly to image/video generation.
6. Save durable artifacts and update project state at the end of each stage.
7. Treat experimental knowledge as candidates until cross-song validation promotes it.

## How Codex fits this project

The next maintenance phase is focused on using Codex for OSS engineering work around the creative runtime, including:

- PR and rule-change impact analysis;
- workflow/state consistency checks;
- regression detection across authoritative rules;
- structured evals for prompt/runtime changes;
- stale-document and broken-reference detection;
- issue triage and reproduction-plan generation;
- release notes and promotion receipts;
- GitHub Actions that validate runtime invariants before merge.

See [`ROADMAP.md`](ROADMAP.md) for the planned maintenance automation work.

## Contributing

Contributions are welcome, especially around reproducibility, QA, evaluation design, state validation, camera/motion regression testing, documentation and maintenance tooling.

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a PR.

## Safety and repository hygiene

Do not commit:

- API keys, tokens, cookies, passwords or login sessions;
- private account data or unredacted analytics screenshots;
- personal chat exports;
- copyrighted audio/video binaries unless redistribution rights are clear;
- large generated-media batches that belong in external storage.

The repository should contain rules, provenance, indexes, tests, receipts and reproducible metadata rather than private credentials or unnecessary media blobs.

## Project maturity

This is a **new public open-source project** and does not yet claim broad adoption, package downloads, stars or ecosystem dominance. Its current value is the depth of a real production runtime being hardened through repeated use, explicit failure analysis and cross-song regression.

The objective of opening and documenting the project is to make those methods reusable by other creators, maintainers and agentic production systems instead of keeping them as private prompt history.

## License

This project is licensed under the [MIT License](LICENSE).

---

## 中文简介

Tangyuan AI Douyin 是一个正在真实生产中验证的 **AI 短视频 / 音乐 MV 生产 Harness**。项目核心不是保存“某一条好用的提示词”，而是把 AI 内容生产拆成可恢复状态、人工 Gate、机器 QA、时间轴真值、导演规则、首帧规则、动态生成合同、素材标准化、剪辑验收和跨歌曲回归。

当前 R3 运行时正在 `test/mv-web-r3` 分支持续实战验证；新的经验只有经过实际素材和跨歌曲复验后，才会晋升为正式生产规则。
