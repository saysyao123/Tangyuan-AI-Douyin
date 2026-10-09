# STILLWET_NATIVE_S0_STATUS — 实际验证报告（2026-10-09）

## 原始目标
验证公开原生 Rust + Lua 油画模拟与真实过程回放，不使用已有 GPT 图片贴图、不执行旧 OpenCV 笔刷显现。

## 上游与控制组
- 上游：https://github.com/aliceisjustplaying/claude-paint
- 固定版本：`8eeb9bec3ce146bcd15c37db447665391fb95bdd`
- 原始样例：`paintings/sampler/p9_study.lua`、`p9_study2.lua`、`p9_study3.lua`
- 颜料盒：`giverny`
- 执行：GitHub Actions Ubuntu 24.04 + 原始 Rust `easel` + 官方 `scripts/replay_clip --reuse`
- 复刻测试分支：`pilot/stillwet-native-20261009`

## 已通过的可复查事实
1. Rust 引擎成功编译并运行原生三阶段 Lua。
2. 原生画布 `native_finished.png` 已生成；`frames.tsv` 含原生逐笔时间轴。
3. 绘画程序实际执行 3 chunks，记录 175 分钟模拟手绘时间，生成 34 张取帧。
4. 官方重放程序输出 24.000s、24fps、576 帧、H.264 MP4，大小 500×334；画布 PNG 是 500×333，视频高度为符合编码要求补至 334。
5. 最后一帧与原生 PNG 的平均像素误差约 2.7（部分因为 H.264 和补边），没有最终切换到 GPT 图片。
6. 官方样例画面相对简单，不能视为精品质量对照；此通过结果仅证明核心工具链与物理绘画链路成立。

## 重要限制
- GPT 尚未通过实时 `paint/look` 工具参与此条实际绘画；本轮由原作者的官方 Lua 决定笔触。
- 还未获得与原始官网 2400px 作品相同的正式艺术质量；另有 S1 完整历史作品重放测试。
- 作品与日志的复用需按上游 CC BY 4.0 保留署名；代码 MIT。

## 官方署名
Original painting algorithm/sample/code by Alice and the `claude-paint` project, https://github.com/aliceisjustplaying/claude-paint.
