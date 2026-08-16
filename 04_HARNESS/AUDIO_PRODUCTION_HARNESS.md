# AUDIO_PRODUCTION_HARNESS v1.0

## 目标

把真人录音稳定变成唯一Master Narration，并让导演表完全基于真实音频。

## 流程

```text
Record
↓
Independent ASR
↓
Transcript Confirm
↓
Remove invalid pauses / thinking sounds
↓
Noise Cleanup
↓
Loudness Normalize
↓
Multi-session Tone Match
↓
MASTER_NARRATION_LOCK
↓
Timeline Export
```

## 1. Record

优先自然口语，不追求播音腔。

## 2. Independent ASR

ASR必须听真实音频。

禁止：
- 用原稿反推录音内容
- 看到旧文稿以后“自动纠正”用户实际说法

## 3. 两套文本

### Verbatim Transcript
记录实际说出的话。

### Clean Subtitle Transcript
为阅读清洁：
- 可去啊/嗯等思考音
- 可修正明显口语赘余
- 不得改变观点

两者必须区分。

## 4. Cleanup

可以处理：
- 底噪
- 长无意义停顿
- 思考音
- 首尾空白
- 不同录制场次响度
- 轻微动态差

不得：
- 改变真实声线
- 改人声身份
- 强修到金属/水声
- 过度压缩自然停顿

## 5. Multi-session Match

Hook / Body / Outro分别录制时：

Body作为参考。

匹配：
- Loudness
- Dynamics
- Mild tonal balance

## 6. Master Narration Rule

最终成片只有一个Master Narration。

任何AI生成视频：
`SOURCE_AUDIO = REMOVE`

除非导演表明确：
`KEEP_SOURCE_AUDIO = TRUE`

## 7. Audio Lock输出

必须记录：

- 文件名
- 时长
- sample rate
- channels
- 是否清洁
- 是否多场次
- QA状态
- 逐字稿来源
- 字幕稿来源

## 8. 时序规则

`AUDIO_LOCK` 完成前：

Director只能是 `DRAFT_TIMING`。

完成后：

Director才能进入 `FINAL_TIMING`。
