# AI_VIDEO_HARNESS v1.0

> 用于“首帧图 → 5秒图生视频”类素材。

## 原则

AI不是默认填空工具。

只在：
- Concept / Emotion
- Capability Proof
- Hook / Transition / Outro

显著增加表达价值时使用。

真实证据仍由真实素材承担。

## Stage 1｜Director Intent

先回答：

- 这句旁白为什么需要AI？
- 一张真实截图能否更可信？
- AI要表达的是事件、情绪还是空间？

回答不了，不生成。

## Stage 2｜First Frame

一次只生成一个场景。

Prompt开头必须明确：

> 只生成1张独立9:16竖版图片，单一完整构图。

默认禁止：
- 拼图
- 九宫格
- 分镜表
- 多联画
- 海报
- 信息图
- 标题栏
- 时间码
- 可读平台数据

AI不负责准确生成：
- 37
- 1000
- DAY XX
- 账号名
- 精确平台UI文字

后期叠加。

## Stage 3｜First Frame QA

检查：
- 主视觉是否唯一
- 后续动作入口是否明确
- 空间是否足够
- 人物/物体是否闭合稳定
- 是否真的适合动
- 是否存在多余文字/UI

通过后再生成视频。

## Stage 4｜5s Image-to-Video

默认5秒。

只写：
- 一个主事件
- 一个摄影机动作
- 环境余韵
- 明确结束状态

禁止让模型自由安排多事件。

## Stage 5｜AI Video QA

检查：
- 身份/物体连续
- 无额外人物
- 无明显穿模
- 无不可解释跳变
- 镜头方向稳定
- 结束帧可剪
- 无第三方水印
- 原始音轨状态

## Stage 6｜Audio Strip

AI素材即使文件名带 clean，也必须实际Probe。

若存在源音轨：
默认删除。

## 输出状态

- DRAFT
- QA_PASS
- APPROVED
- SUPERSEDED
- USED_IN_FINAL
