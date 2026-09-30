# V3 evidence reproduction

The four-channel recognition is blind: neither script passes lyric text or hotwords to SenseVoice. Public summaries contain counts/hashes; raw output is temporary analysis material.

Use Python 3.12 and install `sherpa-onnx==1.13.8`, `numpy`, and `soundfile`. Obtain the official model archive described at https://k2-fsa.github.io/sherpa/onnx/sense-voice/python-api.html ; this run uses the INT8 archive `sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2`, extracted beneath `/tmp/s1c-models/`. The model SHA256 is in sensevoice_summary.json.

Place the exact source as `full.mp3` beside the two scripts (SHA256 in diagnostic_audio_meta.json), then run `python blind_sensevoice.py` and `python channel_contrast.py`. These scripts use ffmpeg. Run `python -c 'from audible_gate import regression_checks; print(regression_checks())'` for 14 gate regressions. A passing regression result does not pass the song's audible-lyric gate.

The reference map comes from the publicly displayed LINE MUSIC LRC at https://music-tw.line.me/track/7977444003 ; the page digest and ordered text hashes are retained. Consecutive combined display events remain combined. No cue time is promoted to a measured phrase end. The independently recovered old report came from Actions run 36404878024, artifact 10962021742.

Full source decode has 201.9453125 seconds; MP3 container reports 201.978776 seconds. The small remainder is codec/container timing, not a missing vocal passage. All 44 ASR windows cover the decoded duration. The 0.7673 whole-track stereo correlation does not establish absence of local phase cancellation; left/right/side tests also recovered no meaningful lyric sequence.
