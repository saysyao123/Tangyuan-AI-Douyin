---
name: gpt-native-gif-video
description: Use when making a GPT-native GIF micro-animation or converting a verified GIF into a smoother 5-second video at no added cash cost. Inspect complete fixed-camera source frames, preserve variable GIF timing, interpolate with CPU optical flow, verify actual GIF/MP4 files, and report original samples, interpolated frames and holds separately. This is a specialist module under the existing Work-Fisher video route, not a general video generator.
---

# GPT 原生 GIF → 视频 v1.1.0

## 目标与边界

交付真实 GIF、5.00 秒／120 帧／24 FPS H.264 MP4、全部帧检查图和 QA。优先完整画面、固定人物、固定镜头和自然动作。不得用重复运动、滚动拼图、补间伪称原生帧、放大伪称高清。

遵守：用户当前指令 > 原项目锁定要求 > Work-Fisher 主流程 > 本专项模块。不改写 Work-Fisher 原版或历史成功资产。保持本仓库目录作为唯一正式源。

## 先检查当次能力

1. 读取 `START_WEB.md`，记录 main 当前 SHA，再以该 SHA 读取本文件、脚本和参考，避免跨提交混用。
2. 确认当次可调用的原生 GIF 生成工具、帧数上限、参考图接口及可取得的真实文件。不要靠提示词突破工具 schema。2026-11-05 此 Work 会话工具仅接受 2–16 帧；历史 30 帧样本可继续使用，不能承诺本次单次生成 30 帧。**本轮实际调用返回HTTP400：GIF output is not enabled for this request。工具参数可见不代表调用已启用；当前新GIF生成标为BLOCKED，不能声称端到端自动生成通过。**
3. 确认 Python、Pillow、NumPy、OpenCV、`ffmpeg`、`ffprobe`、libx264。优先已有环境。只有普通网页聊天而无代码/文件执行能力时，只能做生成与检查指导，不能声称脚本已执行。
4. 脚本仅后处理，不调用 GPT 生图，不含付费 API。不将 Plus 订阅等同于无限生成额度、GPU 或外部云服务。没有源文件或工具就报告具体阻塞，优先复用已有合格源 GIF。

## 执行流程

1. 继承已确认角色、镜头、时长、画幅及声音。新镜头默认单人、固定机位、一个轻动作、无声音；9:16 仅是创作目标，不把已有源图拉伸为 9:16。
2. 生成时使用 [提示词](references/PROMPTS.md)，按当次工具可支持帧数取高质量完整画面。保留已验证的 6/30 帧经验，拒绝 120 格大拼图；若是手动拼多段，先证明交界处姿态继承，不能用后期掩盖断裂。
3. 在空目录运行源检查：
   ```bash
   python scripts/gif_to_video.py --input source.gif --out inspect --inspect-only
   ```
   查看 `source_report.json`、全部 `source_frames_*.jpg`，重点看脸、手、衣物、窗框、画面边缘。数值检测是辅助，不能证明没有拼图或人物漂移。源帧有错误时停止并重生成，不硬补到 120 帧。
4. **实际完成源帧检查后**，由执行 Agent 在新的空目录运行：
   ```bash
   python scripts/gif_to_video.py --input source.gif --out result \
     --seconds 5 --fps 24 --scale 1 --source-reviewed --source-origin gpt-native
   ```
   `--source-reviewed` 是检查记录，不要求用户重复批准；未检查不得使用。来源不确定时用 `unknown`，工程 fixture 用 `synthetic-fixture`。
5. 默认保留原双向 Farneback 算法并缓存相邻帧光流。以 GIF 累计帧起始时间采样，保留变时长和最后一帧自然停留。不要自动从末帧回接首帧。`flow_flagged_source_pairs`会标记双端warp大连通分歧，强制重点复核；它只是风险提示，不能自动证明解剖正确。遮挡、手指和大动作仍可能重影；`--method blend` 仅是可检查的退路，不自动认为更优。
6. 默认全片共享 GIF 色板、无抖色，减少静态背景颜色闪动。需要 A/B 时用 `--palette per-frame`。GIF 百分之一秒时钟使用 40/50ms 混合延时，累计 5000ms；它不是恒定 24 FPS 容器。
7. 默认原尺寸；`--scale 2` 仅改变显示像素。MP4 奇数宽高在右／下补最多 1 像素，不拉伸。源透明像素按显式 `--matte '#000000'` 合成。无／零时长源默认拒绝，仅在明确恢复策略后使用 `--default-duration-ms 100` 并记录。
8. 需要现有音频时加 `--audio voice.wav`：截取／补静音至视频长度并复验 AAC；不包含 TTS、口型或字幕自动生成。默认非循环；仅检查首尾衔接后才用 `--loop`。
9. 若原片复杂动作不合格，可在用户目标允许的情况下显式选择 `--source-range 0:15` 等已查看的安全片段；必须披露选取原帧索引、原片时长与重定时倍率，保留完整原片失败证据。不得把删除动作后的片段当作原动作已修复。
10. 按 [质量门禁](references/QA.md) 回读文件并完整播放，逐帧检查实际输出。脚本只写 `TECH_PASS_VISUAL_PENDING`，永不自动签发美术通过。另写带文件 SHA、时间码和具体观察的视觉审核记录；发现问题则回退。播放器不可用时明确保留 `PLAYBACK_PENDING`，不能把解码检查等同实时观看。
11. 仅交付真实存在的 `animation.gif`、`animation.mp4`、`qa_contact_sheet.jpg`、`source_report.json`、`qa_report.json` 和视觉记录，附原生源 GIF。来源、时长、输出编码、环境和文件哈希均可查。保留所有失败边界。

## 来源统计与禁止虚报

报告按输出采样实际分列 `source_sample`、`interpolated`、`terminal_hold`，不能直接以 120−源帧数冒充准确补间计数。历史均匀 30×170ms 源按 5 秒重采样时是 **30 个源帧采样＋87 个光流补间＋3 个末尾自然停留**。后 90 个输出并非 90 个新原生画面，也不全部是光流新动作。任意变时长源可能只有少数源帧恰好落在 24 FPS 刻度上，必须以报告为准。

像素编码/量化后不保证与源 PNG 逐像素相同；源端点保留的精确性指缩放与编码前。不得因存在 120 个 GIF 图像块就声称有 120 个独立动作。

## 回归与更新

```bash
python tests/run_regression.py --out results/regression-unique
```

该命令不下载模型、不调用服务、不需要 pytest，创建 text-only fixture 后测试真实编码。测试通过只证明覆盖范围内的工程正确性，不证明真实人物美术质量或未来无限量产。

查看 [审核报告](AUDIT_REPORT.md)、[开源对照](references/OPEN_SOURCE_COMPARISON.md) 和 [历史实验](references/EXPERIMENT.md)。每次改脚本均重跑相关回归与真实样本，完成验证后再提交回同一仓库。网页端下次重新读取 main；不是内置 Skill 自动热更新。
