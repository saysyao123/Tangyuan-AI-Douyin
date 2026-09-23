# Fresh Judge Blind Baseline Run01 — Independent Scoring Report

**Repository:** `saysyao123/Tangyuan-AI-Douyin`  
**Branch:** `main`  
**Scoring context:** new / independent  
**Date:** 2026-09-23  
**Prediction file:** `BLIND_PREDICTIONS_RUN01.jsonl`  
**Status file:** `BLIND_RUN01_STATUS.md`  
**Answer key:** `CONTRASTIVE_ANSWER_KEY_v0.1.jsonl`  
**Judge contract:** `MOTION_JUDGE_CONTRACT_v0.1.yaml`  
**Fixture set:** `CONTRASTIVE_FIXTURES_v0.1.jsonl`

## 1. Preconditions

- Status confirmed: **PREDICTIONS_FROZEN**
- Status file declares: **Cases: 40**
- Prediction file independently counted: **40 JSONL records**
- Frozen prediction file was **not modified**
- Answer key was read only after confirming the frozen status
- Scoring used only the five files authorized for this scoring context

## 2. Executive result

- **Correct cases:** 40 / 40
- **Overall accuracy:** **100.0%**
- **Incorrect cases:** 0
- **Route mismatches:** 0
- **Misclassified case_ids:** **None**

The frozen Run01 predictions exactly match the Answer Key for all 40 cases, including deterministic routes.

## 3. Four-label confusion matrix

Rows are Answer Key labels; columns are frozen predictions.

| Actual \ Predicted | TRUE | FALSE | INSUFFICIENT_EVIDENCE | NOT_APPLICABLE | Total |
|---|---:|---:|---:|---:|---:|
| TRUE | 20 | 0 | 0 | 0 | 20 |
| FALSE | 0 | 20 | 0 | 0 | 20 |
| INSUFFICIENT_EVIDENCE | 0 | 0 | 0 | 0 | 0 |
| NOT_APPLICABLE | 0 | 0 | 0 | 0 | 0 |
| **Total** | **20** | **20** | **0** | **0** | **40** |

Interpretation: TRUE and FALSE are perfectly separated in this fixture set. However, this Run contains no Answer Key examples whose expected label is `INSUFFICIENT_EVIDENCE` or `NOT_APPLICABLE`, so those two allowed answer modes are **not regression-tested by Run01**.

## 4. Accuracy by criterion

| Criterion | Cases | Correct | Accuracy |
|---|---:|---:|---:|
| J01_required_action_coverage | 6 | 6 | 100.0% |
| J02_grounded_displacement | 8 | 8 | 100.0% |
| J03_no_unsupported_translation | 4 | 4 | 100.0% |
| J04_camera_intent_defined | 4 | 4 | 100.0% |
| J05_end_state_defined | 6 | 6 | 100.0% |
| J06_reference_capability_valid | 4 | 4 | 100.0% |
| J07_evidence_sufficient | 2 | 2 | 100.0% |
| J08_inertia_and_settle | 4 | 4 | 100.0% |
| J09_prompt_density_reasonable | 2 | 2 | 100.0% |
| **Overall** | **40** | **40** | **100.0%** |

## 5. Case-by-case scoring

| case_id | Criterion | Expected | Predicted | Expected route | Predicted route | Result |
|---|---|---|---|---|---|---|
| MG001_A | J02 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG001_B | J02 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG002_A | J03 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG002_B | J03 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG003_A | J02 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG003_B | J02 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG004_A | J02 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG004_B | J02 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG005_A | J01 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG005_B | J01 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG006_A | J01 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG006_B | J01 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG007_A | J04 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG007_B | J04 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG008_A | J04 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG008_B | J04 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG009_A | J05 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG009_B | J05 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG010_A | J05 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG010_B | J05 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG011_A | J06 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG011_B | J06 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG012_A | J06 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG012_B | J06 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG013_A | J08 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG013_B | J08 | FALSE | FALSE | PASS | PASS | CORRECT |
| MG014_A | J08 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG014_B | J08 | FALSE | FALSE | PASS | PASS | CORRECT |
| MG015_A | J09 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG015_B | J09 | FALSE | FALSE | PASS | PASS | CORRECT |
| MG016_A | J03 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG016_B | J03 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG017_A | J02 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG017_B | J02 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG018_A | J07 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG018_B | J07 | FALSE | FALSE | ESCALATE | ESCALATE | CORRECT |
| MG019_A | J05 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG019_B | J05 | FALSE | FALSE | REVISE | REVISE | CORRECT |
| MG020_A | J01 | TRUE | TRUE | PASS | PASS | CORRECT |
| MG020_B | J01 | FALSE | FALSE | REVISE | REVISE | CORRECT |

## 6. Misclassified cases

**None.**

There are therefore no observed false positives, false negatives, route-selection errors, criterion-local errors, or critical/non-critical routing errors in Run01.

## 7. Error-type analysis

Because the observed error count is zero, Run01 does not expose an empirical judge failure mode. In particular:

- no missing-required-action false pass was observed;
- no grounded-displacement false pass was observed;
- no unsupported-translation false pass was observed;
- no camera-intent classification error was observed;
- no end-state classification error was observed;
- no invalid reference-capability dependency was incorrectly accepted;
- the J07 missing-evidence case correctly routed to `ESCALATE`;
- non-critical J08/J09 FALSE results correctly retained `PASS` routes.

## 8. Systematic-bias assessment

### Observed judge bias
No label-direction bias is visible **within the scored outcomes**: all 20 TRUE and all 20 FALSE cases were classified correctly.

### Evaluation-design confound
There is, however, a material fixture-structure confound:

- all 20 `case_a` examples have expected label **TRUE**;
- all 20 `case_b` examples have expected label **FALSE**.

Therefore a trivial positional heuristic — “A => TRUE, B => FALSE” — would also score **40/40**. Run01's 100% accuracy is real against the current Answer Key, but by itself it does **not prove** that the judge learned/applied J01-J09 rather than exploiting pair position or correlated surface cues.

A second coverage gap is that the Answer Key contains **zero expected `INSUFFICIENT_EVIDENCE` cases and zero expected `NOT_APPLICABLE` cases**, despite both being allowed by the contract.

These are limitations of the current regression fixture, not evidence that `MOTION_JUDGE v0.1` contract text is wrong.

## 9. Recommendation

### Decision: **扩充 fixture 后再判断**

Do **not** modify the contract yet: Run01 produced no contract-level contradiction or criterion failure.

Before treating this result as sufficient evidence for promotion into the next general regression stage, expand the fixture suite to remove the current confounds. At minimum:

1. Randomize/reverse pair polarity so some `case_a` are FALSE and some `case_b` are TRUE.
2. Include standalone cases without A/B pairing.
3. Add expected `INSUFFICIENT_EVIDENCE` and `NOT_APPLICABLE` cases where contract semantics genuinely require them.
4. Add harder near-boundary negatives where lexical cues are weaker and only the physical/contract logic separates TRUE from FALSE.
5. Preserve criterion balance, especially adding more J07 and J09 coverage.
6. Run the expanded suite in a fresh stateless scoring context before contract changes.

### Promotion interpretation

- **Current Answer Key performance:** PASS (40/40)
- **Contract modification required now:** NO
- **Regression evidence sufficient for robust activation:** NOT YET
- **Next action:** expand/deconfound fixtures, then rerun blind regression.

## 10. Integrity note

`BLIND_PREDICTIONS_RUN01.jsonl` was treated as frozen input and was not modified or regenerated during scoring.
