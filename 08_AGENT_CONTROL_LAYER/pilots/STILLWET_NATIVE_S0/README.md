# Stillwet 原生引擎试跑 S0 / S1

目标：**不采用图像擦除 / 贴图重绘**，而是真正运行原项目 `aliceisjustplaying/claude-paint` 的 Rust + Lua 油画引擎，使用其自带官方样例 `paintings/sampler/p9_study*.lua` 在干净的 Linux CI 环境生成原生油画与逐笔回放 MP4。

## 锁定基线
- 原项目固定 revision：`8eeb9bec3ce146bcd15c37db447665391fb95bdd`（2026-10-08）。
- 样例使用原作者现成的三个 Lua 阶段：`p9_study.lua`、`p9_study2.lua`、`p9_study3.lua`。
- `EASEL_BOX=giverny` 对应原工程样例说明。
- 只使用原始引擎内部的笔触、湿颜料和颜色混合能力。
- 视频来自真实 `easel run --frames-every` 的绘画帧和 `scripts/replay_clip --reuse`，无 GPT 高清图替换。
- 先完成官方样例复刻，再评估如何接入 GPT 作为 AI 画家。

## 验收
1. 远端 Rust 编译成功。
2. `easel run` 运行官方 Lua 样例且生成原生画作 PNG。
3. `frames.tsv` 存在并记录绘画时间。
4. `replay_clip` 输出 H.264 MP4，时长接近 24 秒。
5. 通过 `ffprobe` 核查真实视频规格，保留作画源程序和测试日志。

## 操作
仅操作隔离测试分支 `pilot/stillwet-native-20261009`，不修改 main 的 MV 工程。可在 GitHub Actions 中查看 `Stillwet Native Engine S0`；成功后下载 Actions artifact `stillwet-native-s0`。

## 升级到 S2 之前
先人工检查这份官方样例视频里逐笔绘画的真实性与质感。之后使用同一引擎，通过 AI 画家的 `paint/look/note/status/log` 工具接口来重创《柳树湖畔的金色暮光》的主题，不把旧 GPT 图片当作可贴图的终帧。

上游源代码 MIT License；官方绘画与其相关日志 CC BY 4.0。引用和公开展示原作者样例作品需按许可署名。项目主页：https://stillwet.art/ ，源码：https://github.com/aliceisjustplaying/claude-paint 。
