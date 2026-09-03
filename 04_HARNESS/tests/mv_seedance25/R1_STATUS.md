# Seedance 2.5 R1 Benchmark Status

Status: `K0_LOCKED / PROMPTS_COMPILED / DOLA_LIVE_PROBE_REQUIRED`

## Ready
- 3 real K0 benchmark assets generated and SHA-256 locked;
- K0 A/B/C benchmark QA passed;
- Production Cards bound to actual accepted K0 state;
- 12-run Legacy-vs-Lean ledger bound to exact K0 identities;
- 3 Legacy prompts + 3 Lean prompts compiled with duration placeholder;
- no mid-cell prompt mutation allowed.

## Current blocker
`DOLA_LIVE_CAPABILITY_PROBE`

Need one exact live provider binding for:
- Seedance 2.5 model label;
- Precision duration;
- K0/image input mode;
- equivalent aspect/resolution/audio settings.

## Next transition
After provider probe:
1. update `providers/dola/capability_profile.yaml`;
2. replace `{{DOLA_DURATION}}` in R1 compiled prompts;
3. fill `target_duration_s` in all 12 ledger rows;
4. change rows to `READY_TO_RUN`;
5. execute the 12 generations without prompt edits inside a cell.

No other design work is required before R1 generation.
