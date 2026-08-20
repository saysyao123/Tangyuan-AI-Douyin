# Workflow｜Audio & Timeline v1.0

## Responsibility
把真人录音变成唯一Master Narration，并生成真实时间轴。不得根据旧稿猜录音内容。

## Input Contract
- `SCRIPT_LOCKED`
- 用户真实录音
- 允许的清洁范围

## Process
```text
Record
→ Independent ASR
→ Verbatim Transcript Confirm
→ Clean Subtitle Transcript
→ Remove invalid pauses / thinking sounds
→ Noise Cleanup
→ Loudness Normalize
→ Multi-session Tone Match
→ MASTER_NARRATION_LOCK
→ Timeline Export
```

## Rules
- ASR只听真实音频，不用旧文案反推。
- Verbatim Transcript 与 Clean Subtitle Transcript 分开。
- 可去底噪、长无意义停顿、思考音、首尾空白。
- 不改变真实音高、身份和自然声线。
- Hook / Body / Outro分开录制时，以主体为参考统一响度、动态、轻微音色差。
- AI生成视频源音轨默认删除，除非Director明确 `KEEP_SOURCE_AUDIO = TRUE`。
- `AUDIO_LOCK` 前Director只能是 `DRAFT_TIMING`。

## Output Contract
- Master Narration文件信息
- 时长 / sample rate / channels
- Verbatim Transcript
- Clean Subtitle Transcript
- 句级时间轴
- QA状态
- `STATUS = AUDIO_LOCKED`
