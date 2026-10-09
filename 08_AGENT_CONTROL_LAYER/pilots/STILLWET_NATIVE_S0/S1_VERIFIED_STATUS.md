# STILLWET_NATIVE_S1_STATUS — 官方完整绘画记录原生重放成功

日期：2026-10-09
状态：`VERIFIED_NATIVE_GALLERY_REPLAY`

## 本轮做了什么
- 源项目：Alice's `claude-paint` (https://github.com/aliceisjustplaying/claude-paint)
- 固定 revision：`8eeb9bec3ce146bcd15c37db447665391fb95bdd`
- 绘画原作：`Stoneware Jug with Two Lemons and a Knife` （Round 16，原作者/AI 画家 Claude Opus 5.5）
- 官方历史源码：`archive/collection/studios/paint-studio-3be9e8/paintings/lua/painting.lua`
- GitHub Actions 运行：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37887747535
- 实现：编译原始 Rust `easel`，原样重放官方 Lua；使用官方 `scripts/replay_clip --reuse` 合成视频。

## 核验结果
- GitHub Actions 结论：`success`
- 原始绘画 chunk：94/94 执行成功
- 原生画布：700×560 PNG
- 真实物理绘画取帧：229 帧
- 绘画模拟手绘时间：701.3 分钟
- 重放实际计算耗时：185.2 秒（日志记录）
- MP4：32 秒、H.264、24 FPS、768 帧、700×560
- 末尾视频帧与原生 PNG 的平均像素差距约 1.52/255（正常有损压缩），不存在参考高清图换源。
- 生成：`original_still_life_32s.mp4`、`original_finished_700.png`、`contact_sheet.jpg`、`original_94_chunk_painting.lua`、`frames.tsv`、`video_specs.json` 和日志。

## 该结果证明与没有证明的事项
**已证明：** 用官方引擎从保存的 94 段绘画指令中重新实际绘制复杂静物；保留对湿油彩、画笔与颜料叠层的原生模拟；成功逐阶段录制为短视频。

**尚未证明：** GPT 能在本工作流中独立实时调用 `paint/look` 创作出与作者同等精致的全新油画。这需要下一阶段的画家 Agent 接入与真实质量验收。

此轮先采用 700px 宽的预览重放以压缩计算成本。官网原作品通常使用 2400px 画架画布，不能把 700px 版本当成最高分辨率基线。

## 原始作品与许可
原作页面：https://stillwet.art/p/r16-c1.html
上游代码 MIT；绘画、日志与作品依上游 CC BY 4.0 署名。
