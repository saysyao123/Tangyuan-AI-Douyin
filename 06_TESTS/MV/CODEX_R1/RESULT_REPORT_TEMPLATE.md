# CODEX R1｜RESULT REPORT TEMPLATE

# 1. Executive Result

- MODE:
- Final State: `PASS | PARTIAL | BLOCKED`
- Automation Score: `__/16`
- Final video path:
- Final subtitle path:
- Publish ready: `YES | NO`
- Total elapsed time:
- Human active minutes:
- Human interventions:
- Retry count:

# 2. Stage Score

| Stage | Scope | Score 0/1/2 | Result | Human unlock | Retries | Key output |
|---|---|---:|---|---:|---:|---|
| C00 | Environment |  |  |  |  |  |
| C01 | Datasource |  |  |  |  |  |
| C02 | Audio |  |  |  |  |  |
| C03 | Whisper |  |  |  |  |  |
| C04 | HD source replacement |  |  |  |  |  |
| C05 | Edit reconstruction |  |  |  |  |  |
| C06 | Subtitle/final render |  |  |  |  |  |
| C07 | QA |  |  |  |  |  |

Scoring:
- `2`: fully automatic
- `1`: automatic after one minimal human unlock/input
- `0`: cannot complete / manual execution required

# 3. Golden Comparison

## Audio
- source version match:
- source start:
- source end:
- duration:
- fade:
- PASS/FAIL:

## Timeline
- S1-S8 order preserved:
- final duration:
- overlap/trim manifest complete:
- PASS/FAIL:

## Subtitle
- lyric text exact:
- line count:
- median start-time absolute error:
- max start-time absolute error:
- human spot-check:
- PASS/FAIL:

## Sources
- 8/8 present:
- watermark-free count:
- native resolutions:
- publish-grade status:

# 4. Human Intervention Log

| # | Stage | Why Codex stopped | User action | Minutes | Could this be automated later? |
|---|---|---|---|---:|---|

# 5. Failure / Retry Summary

| # | Stage | Failure | Root cause | Retry | Fix | Final state |
|---|---|---|---|---|---|---|

# 6. What Codex Did Better Than Manual R1

- 

# 7. What Codex Could Not Match

- 

# 8. Automation Candidates to Promote

Only list items backed by this real run.

- 

# 9. Keep as Experiment

- 

# 10. Recommendation

Choose one:
- `READY_FOR_MODE_B_FRESH_R1`
- `REPEAT_MODE_A_AFTER_FIXES`
- `BLOCKED_BY_ENVIRONMENT`
- `BLOCKED_BY_EXTERNAL_SERVICE`

Explain why.
