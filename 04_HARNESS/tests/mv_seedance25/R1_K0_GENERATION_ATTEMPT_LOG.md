# Seedance 2.5 R1 K0 Generation Attempt Log

Status: `INPUTS_STILL_BLOCKED`
Date: 2026-09-03
Branch: `experiment/mv-seedance25-lean-compiler-v1`

## Purpose
Track K0-generation attempts without treating failed or malformed outputs as benchmark inputs.

## Acceptance authority
The benchmark requires three **standalone 9:16 K0 image files** matching `R1_K0_GENERATION_BRIEF.md`.

A contact sheet, benchmark infographic, collage, documentation panel, or composite image is **not** a valid K0 asset even if it contains visually useful sub-images.

## Attempts

### Attempt 01
Result: `REJECTED_AS_INPUT`
Failure type: `COMPOSITE_DOCUMENT_INSTEAD_OF_STANDALONE_K0`
Reason: output packaged A/B/C as a benchmark/documentation sheet rather than three independent 9:16 images.

### Attempt 02
Result: `REJECTED_AS_INPUT`
Failure type: `COMPOSITE_DOCUMENT_INSTEAD_OF_STANDALONE_K0`
Reason: output again rendered a benchmark dashboard rather than a standalone K0.

### Attempt 03
Result: `REJECTED_AS_INPUT`
Failure type: `COMPOSITE_DOCUMENT_INSTEAD_OF_STANDALONE_K0`
Reason: even after explicitly targeting K0-A only, output remained a multi-panel benchmark document and changed the intended wardrobe/world.

## Locked conclusion
- Do not register any of these attempts in `R1_INPUT_MANIFEST.yaml`.
- Do not compute benchmark asset IDs/SHA values from the composite sheets.
- `R1_INPUT_MANIFEST.yaml` remains `BLOCKED_ON_REAL_K0`.
- Exact standalone K0 bytes remain required before any R1 generation.

## Next allowed action
Generate K0-A, K0-B and K0-C as separate image-only outputs using a generation surface/context that reliably honors the standalone-image contract. After each image exists, register its durable identity and bind the same bytes to both Legacy and Lean variants.
