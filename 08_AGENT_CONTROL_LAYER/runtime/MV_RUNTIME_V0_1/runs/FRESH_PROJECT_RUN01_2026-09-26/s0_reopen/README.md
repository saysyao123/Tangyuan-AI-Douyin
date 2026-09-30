# S0 qualification repair, run-local

This directory belongs only to FRESH_PROJECT_RUN01_2026-09-26. The frozen shared contracts, global older-project tracker, historical ledger and song pool are unchanged. RUN_CURRENT_STATE.yaml and S0_CURRENT_STATUS.md are the active state.

`s0_gate.py` rejects page-only access, Chinese metadata without audible review, ASR-only/forced-alignment-only review, historical exclusions, supplementary-only provenance, and human rejection. Run `python -c 'from s0_gate import regression_checks; print(regression_checks())'` for 12 control cases. Passing these tests does not qualify a song.

`reference_preflight.py` is the bounded ASR support experiment. It requires Python 3.12, ffmpeg, sherpa-onnx==1.13.8, numpy, soundfile and opencc-python-reimplemented. The official SenseVoice INT8 model resides under `/tmp/s1c-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17/`, as in the V3 experiment. Its model checksum is recorded in the earlier s1c_v3_evidence/sensevoice_summary.json.

To reproduce preview inputs, open the public Bandcamp source URL listed in B/C_reference_preflight.json, parse the `data-tralbum` JSON, select the recorded track ID, and request bytes 0–1499999 from its public mp3-128 stream. Record and check the resulting hash. For B, retrieve lyric text from https://xiangxiang.bandcamp.com/track/- (same ID 985094992), rather than assuming the album JSON includes lyrics. C lyric text is in its recorded track page. In temporary local analysis only, supply `B_meta_private.json`/`C_meta_private.json` with these source fields and `lyric_text`, plus `B_reference_partial.mp3`/`C_reference_partial.mp3` to the script directory. The script decodes the first 90 seconds and checks three non-overlapping 30-second windows without giving lyrics to the recognizer. Match scoring happens after recognition; neither match count nor transcript independently passes S0.

The recorded stream hashes identify bounded reference samples, not acquired full production sources. Public outputs retain counts and hashes, not full lyric/transcript text or audio. No final segment, beat grid or full timeline is created in S0.
