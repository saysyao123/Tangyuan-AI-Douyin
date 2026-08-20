# R1S05｜Character Dynamic Prompt Prefix LOCK

User-validated hard rule for all future **character-related image-to-video dynamic prompts**.

The prompt MUST begin with the following line **verbatim, including the leading `***`**:

```text
*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。
```

## Hard requirements

1. The leading `***` is part of the prompt and must not be removed, rewritten, converted into Markdown formatting only, or omitted when copying into Seedance.
2. This line must be the **first line** of every dynamic prompt that contains a person / character reference image.
3. After this line, continue with the normal first-frame lock, fictional-character continuity, character-closure, director/camera grammar, action timing and negative constraints.
4. Avoid later wording that reclassifies the uploaded image as a real-person portrait or real-face reference.
5. This rule was re-validated in R1 after S3 / S5 / S7 originally triggered Seedance portrait-protection checks and then generated successfully after restoring the AI-fictional-character framing.
6. Non-character scenes do not require this prefix.

## Director-language follow-up

R1 also validated that 3-shot structures inside a 5-second Seedance clip can work well. Future dynamic planning should deliberately test both:
- multi-shot 2–3 node structures;
- single-shot cinematic camera moves with broader motion vocabulary (lateral reveal, crane/tilt, dolly, arc, tracking, foreground parallax, low-angle glide, rack-focus, occlusion pass, etc.).

Do not default every 5-second segment to `static character + slow push-in + robe/hair movement`.
