# D01-B｜Color Grade Plan v1

Status: `LOCKED / SUBTLE NORMALIZATION`

Goal: preserve the accepted source beauty while creating a restrained emotional progression rather than applying a uniform warm filter.

## Segment intent

- S01: slightly cooler / denser; retain shadow and pearl-lilac restraint.
- S02: neutral-soft; keep skin/water gentle and calm.
- S03: slightly clearer; let the white flower become the local visual peak.
- S04: most open; slightly lift the final highland release without turning into an exaggerated golden-sunrise look.

## Local render parameters

FFmpeg `eq` implementation on clean proxies before concat:
- S01: `contrast=1.02 / brightness=-0.012 / saturation=0.94 / gamma=0.99`
- S02: `contrast=1.00 / brightness=0.000 / saturation=0.96 / gamma=1.01`
- S03: `contrast=1.015 / brightness=0.006 / saturation=0.98 / gamma=1.015`
- S04: `contrast=1.00 / brightness=0.012 / saturation=1.00 / gamma=1.025`

No LUT, glow, sharpen halo, vignette or stylized color effect added.

Local graded pre-subtitle master:
- `D01-B_GRADE_V1_NO_SUBS.mp4`
- SHA-256: `c34b0bf2b49cdbce27651e4c7c31de55fb1bd90a36f9be5da14463cb5fcaf363`

`COLOR_GRADE_QA_PASS = YES`
