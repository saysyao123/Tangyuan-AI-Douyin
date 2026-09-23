# Stage PROJECT_AUDIO

Status: REVIEW

Current candidate: v0.2

## Purpose

Lock only the authoritative audio and timeline truth required downstream.

S1 owns:
- source media reference;
- selected audio version;
- locked start/end/duration;
- lyric/audio-event timeline;
- semantic cut-point evidence;
- Human Audio Lock.

S1 does not own:
- project aspect ratio/output format;
- Director;
- generation duration;
- shot count;
- character;
- scene;
- camera;
- motion.

Project-format metadata belongs to Runtime Project State.

## Build history

### v0.1
Representative test passed deterministic checks, but review exposed a boundary problem:
`target_aspect_ratio` was coupled into PROJECT_AUDIO using downstream evidence.

Result:
`SUPERSEDED_BEFORE_SEAL`

### v0.2
Aspect ratio removed from S1 and moved to project-level metadata.

Representative real-project test:
《爱让人脑袋空空》

Results:
- deterministic checks: PASS 6/6
- exact duration: 15.370998s
- T00–T12 timeline continuity: PASS
- Human Audio Lock: PASS
- downstream Director consumption: VERIFIED
- Fresh Judge: PENDING

Current artifacts:
- S1_STAGE_CONTRACT_v0.2.yaml
- S1_JUDGE_CONTRACT_v0.2.yaml
- S1_HANDOFF_CONTRACT_v0.2.yaml
- S1_TEST_INPUT_RUN02_v0.2.json
- validate_s1_v0.2.py
- S1_DELIVERY_RUN02_v0.2.yaml
- S1_TEST_REPORT_RUN02_v0.2.md
- S1_FRESH_REVIEW_START_PROMPT_v0.2.md
- S1_STATUS.md

Do not start S2 until S1 is SEALED.
