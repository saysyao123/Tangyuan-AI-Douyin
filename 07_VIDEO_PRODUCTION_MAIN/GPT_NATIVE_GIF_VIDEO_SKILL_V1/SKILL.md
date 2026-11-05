---
name: gpt-native-gif-video
summary: 以 GPT 原生 GIF 为基础，制作稳定、可核验的 5 秒 / 120 帧 / 24 FPS 竖屏 MP4，并形成可复用的动画视频工作流。适用于情绪微电影、动态 MV、低幅度角色演出和 RPG 剧情特写；不替代 Work-Fisher 的创作总流程。
description: Use when the user asks to make a GPT-native GIF animation or convert a verified GPT GIF into a smoother short-form video. Generate coherent source frames, inspect every frame, interpolate to a CFR video, reject scrolling/sliced grids, report provenance honestly, and deliver actual verified GIF/MP4 files. Do not claim upsampled optical-flow frames were generated natively.
---

# GPT 原生 GIF → 可交付视频 Skill v1.0

## 触发条件
- 用户要求「用 GPT 生成 GIF 动画」、「把 GIF 做成 5 秒视频」、「改善 GPT GIF 卡顿」、「用 GPT Plus 不增加付费制作微动态短片」。
- 如果用户要求多镜头短剧/小说影视化，先按仓库 `07_VIDEO_PRODUCTION_MAIN/README.md` 所规定的 Work-Fisher 主导演流程；仅在需要生成简单动效镜头时调用本 Skill。
- 用户明确要求动态 MV、既有视频的局部返工时，优先遵守原项目已批准要求，不强制改为本 Skill。

## 目标 / 定义
- 基线交付 **5.00 秒、120 帧、24 FPS MP4**，附独立 GIF 与 QA 报告；实际时长、fps、帧数均须从最终文件回读。
- 原生 GIF 是源动作帧；高帧率版本通常含光流补间。**禁止**把插值后的 120 帧称为「120 帧 GPT 原生生成」。
- GIF 封装的每帧时长以 10ms 为单位：120 帧 / 5 秒平均 41.667ms，采用均匀分配 40ms、50ms 使总时长精确 5000ms；MP4 是 24 FPS 恒定帧率。
- 不增加现金订阅，不需要使用付费生成 API。脚本使用 Pillow、NumPy、OpenCV 和系统 FFmpeg；运行环境可用时由 Agent 执行，不要求用户购买服务。

## 锁定优先级
用户当前明确指令 > 已批准的既有视频项目硬规则 > 现有 Work-Fisher 主视频流程 > 本专项 Skill > 临时实验建议。

## 执行步骤（不得跳步）
1. **任务契约**：确定镜头数量、时长、画幅、动作幅度、参考形象；默认 5s、9:16、固定机位、仅 1–2 个轻动作、不配乐。原有项目有锁定素材则直接继承。
2. **原生生成**：调用 GPT 原生 GIF 能力，优先 **24–30 张**有实质差异的连续源画面；对于 5 秒镜头可让源动画总时长约 5s，而不是 1s 片段重复 5 次。优先人物/构图稳定性，不为追求 120 原生帧牺牲单帧分辨率。使用 `references/PROMPTS.md` 模板。
3. **源 GIF 检查**：从真正的 .gif 文件解码每一帧，确认所有帧为完整独立画面、尺寸一致；检查不存在大网格滚动、裁剪错位、人物分裂、长时间静帧或不合逻辑的回环。不合格则重做原生 GIF，绝不直接插帧补救。
4. **统一时长并补间**：源 GIF 已通过后，用 `scripts/gif_to_video.py` 将 24–30 源画面按时间轴映射到 120 个输出画面，使用双向 Farneback 光流近似补间。低幅度动作才适用；复杂手部/遮挡可能重影，必须肉眼审查。
5. **导出**：编码 `GIF89a` + `MP4 H.264 yuv420p`。GIF 不强制无缝循环；有完整起止动作时默认单次播放。MP4 的 5s/24FPS 是成片技术验收基准。不得拉伸视频伪称原生高清。
6. **输出回读与 QA**：严格核对 GIF 实际帧数/时长/尺寸、MP4 帧数/时长/fps；查看 16 格关键帧图与整段 MP4。禁止出现画面滚动、黑边、拼图切断、镜头意外抖动。报告中注明真实原生帧数与补间帧数、放大仅为显示尺寸而非细节修复。
7. **交付**：仅在文件真实存在且通过格式 QA 后给下载链接；视觉 QA 未经审核只能标「技术验收通过、视觉验收待人工」，不声称成片完全无瑕疵。应附 `qa_report.json`。

## 一键执行
```bash
python scripts/gif_to_video.py \
  --input /path/to/native_source.gif \
  --out /path/to/results \
  --seconds 5 --fps 24 --scale 2
```
依赖：`pip install -r requirements.txt`，且系统可运行 `ffmpeg` / `ffprobe`。

## 必看参考
- `START_WEB.md`：ChatGPT 网页端或 Work 无上下文调用入口
- `references/PROMPTS.md`：GPT 原生 GIF 生图约束
- `references/QA.md`：文件级、画面级验收与失败回退
- `references/EXPERIMENT.md`：雨夜窗前已测试结果与已知限制

## 禁止事项
- 不再将 10×12 大拼图未经验证地分割成 120 帧，已有滚动错位失败案例。
- 不用重复帧「凑到」120；允许自然静止但不得靠大量重复帧假造流畅。
- 绝不把 288×656 画面用放大操作表述成原生 1080×1920 清晰度。
- 不让增帧覆盖用户已经认可的角色、服装、构图和动作设计。
- 不保证 GPT 生图工具能够在未来所有会话、账户和模式中稳定调用；以当次实际工具和文件核验为准。