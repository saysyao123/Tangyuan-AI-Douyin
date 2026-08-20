# Rules｜AI First Frame & Image-to-Video v1.0

## Use Gate
AI不是默认填空工具。只有 Concept / Emotion / Hook / Transition / Outro / Capability Proof 中，能显著增加表达价值时使用。真实Evidence仍由真实素材承担。

## Director Intent
生成前必须回答：
- 为什么这句需要AI？
- 真实素材是否更可信？
- AI承担事件、情绪还是空间？

答不清则不生成。

## First Frame
- 一次只生成1张独立9:16竖图、单一完整构图。
- 禁止拼图、九宫格、分镜表、多联画、海报、信息图、标题栏、时间码。
- 准确数字、账号名、DAY编号、平台UI文字后期叠加。
- 首帧必须有唯一主视觉、明确动作入口、足够动作空间、稳定闭合主体、可持续环境余韵。

Prompt基础模板：`templates/ai_first_frame_prompt.md`。

## 5s Image-to-Video
默认5秒稳定方案：
- 一个主事件
- 一个摄影机动作
- 环境余韵
- 明确结束状态

禁止让模型自由安排多个主事件。

## QA
检查身份/物体连续、无额外人物、无穿模跳变、镜头方向稳定、结束帧可剪、无水印、源音轨状态。

AI素材默认 `SOURCE_AUDIO = REMOVE`，除非Director明确保留。
