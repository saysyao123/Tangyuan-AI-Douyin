# 2026-10-09 复盘结论：S2B 艺术质量退步（勿作为新的绘画基线）

**S2B_ENGINE_PASS / S2B_ART_REGRESSION_CONFIRMED**：原生引擎与视频运行通过，但与 S2A 及原作者作品比较，S2B v2 的色面更平、陶器更像裁切剪影；不要再以“露底比例减少、笔触数量变化”为质量通过指标。

正式复盘请优先读取 [`S2B_REGRESSION_ROOT_CAUSE_20261009.md`](S2B_REGRESSION_ROOT_CAUSE_20261009.md)。后续应复用上游 94 chunk 的多轮观察、干燥、罩染、局部修改方法及其适用画材盒，而不是继续迭代本文件夹的两段 A/B 模板。**旧代码仅保留失败归因证据，不能继承为正式生产默认。**

---

# Stillwet S2B｜人类式笔触规划研究与真实画架 A/B 验证

## 当前阶段判定
已完成开源项目研究与一个 **可执行的、从同一初始画布出发** 的笔触 A/B 方案。尚未经过 GitHub Actions 真实运行验收的任何帧不得标记 PASS。

## 源头分析：S2A 的机械感究竟从哪里来
从 S2A `painting.lua` 实际统计：
- 四轮作画共 32 次 `work(` 区域填色，却只有 3 次 `brush:stroke(` 的明确路径调用；
- 12 次 `fill=true`，32 次显式固定角度 `angle=<constant>`；
- 反复在接近整幅背景的区域重涂，默认 `hand="body"` 和接近水平的角度造成连续的织物状“墙纸”视觉纹理；
- 很多中后期的“细节”本质是重新按覆盖率刷过形体，而不是建立陶杯曲面、杯口、果皮表面起伏；
- `work` 的 `clip` 并非默认总为 true；原生指南说明宽刷、罩染、干擦、阔笔默认都可能越界。S2A 最终杯身出现非意图暖色笔痕；
- `work` 本身真实使用 Stillwet 物理刷毛，也具备 passage、direction field、angle jitter、dips、curve、swell、order、clip。问题是 GPT 对其调用方式仍然过于机械，并不是引擎不支持画家笔势。

## 六个外部项目（查阅 README / 部分真实源码）的移植决定
1. **FRIDA** https://github.com/cmubig/Frida — 物理绘画反馈、视觉复查后重规划与笔触压力/长度/弯曲参数的解耦。迁移“少量动作→拍照→观察→重新规划”逻辑；**不迁移 GPL-3.0 代码**，避免依赖 GPU / 机械臂。
2. **ContentMaskedLoss** https://github.com/pschaldenbrand/ContentMaskedLoss — 语义重要区域先画；“重要特征尽早可辨识”优于均匀地减少像素误差。迁移“杯口/杯把/果体边缘先认清，再追求表面纹理”。旧 PyTorch+训练方案不直接部署。
3. **Compositional Neural Painter** https://github.com/sjtuplayer/compositional_neural_painter — 按画布当前状态动态选择下一绘画区域，防止固定格子造成的边界破碎。迁移分区规划和反污染机制；不引入 GPU 训练。
4. **Painterly Curved Strokes** https://github.com/Impasto-Lab/Painterly-Curved-Strokes — 沿轮廓/等亮度线的曲线笔触，粗到细的局部刻画。迁移曲线与结构方向；不把 PyTorch rasterizer 用来替换原生 Stillwet。
5. **Oil Paint Tuner** https://github.com/miya9756/Oil-Paint-Tuner — 方向场 / 笔触预算 / 脱离规整网格 / 按区域与结构分配笔触。迁移设计理念，不依赖已有照片像素描画，不复制该项目源码。
6. **BrushOS** https://github.com/Legedith/BrushOS-Robotic-painting-in-action — 预先规划连续曲线、按真实笔画执行、观察并修正。迁移 Tool-Act-Observe-Verify 的短循环；不移植机械臂/摄像头/密钥系统。

## S2B 的五条必须执行的新导演规则（少而有效）
- **手势目标**：每次画笔动作都先说明是“铺体积 / 塑造转面 / 沿轮廓 / 反光 / 软化边缘”中的哪一个；没有目的的笔触不进入正式日志。
- **大笔触限额**：一个区域只允许一次主铺底，后续直接进行局部渐层、轮廓与罩染，不大面积覆盖整个背景充当精修。
- **走笔符合形体**：杯身纵向随曲面轻微转折，杯沿曲线，杯把有连续曲线和压力渐变，柠檬沿其轮廓转折；桌布可有宽笔与褶皱，但不重复平行排刷。
- **保护物体**：背景和桌布修正用 `clip=true` 或指定 `clip=<region>` 的控制；罩染若没有边界确认，先在 scratch 作画。
- **画布为准**：先以 `look` 的整体图、局部图与质感模式观察，再决定后续。禁用图片替换、像素描摹或图像转画笔的替代链路。

## 隔离 A/B 对照
同一画布、同一调色板、同一初步构图及底色：
- A: `common.lua + uniform.lua`，自动填充为主的固定角度。
- B: `common.lua + form_guided.lua`，主体早认清 + 随形方向场 + 12+ 条独立连续压感笔触 + 局部修色；仍通过原生 Rust 颜料引擎作画。

原样输出同规格 PNG、原生取帧、FFmpeg MP4、视频检查和命令日志。它是 **笔触机制试验**，不是完整画师质量竞赛；不能由视频规格通过推断“人类感已经达标”。

## 待验收
1. 两组都能编译/原生执行，而不是仅生成 Lua；
2. 两组都有真实原生 `frames.tsv` 和 MP4；
3. 两组是基于同一个初始 `common.lua`，差异来自第二阶段笔触路线；
4. 重点比对杯沿、杯身弧面、杯把转折、柠檬体积、背景纹理是否还像印刷/墙纸；
5. 真人感由用户主观验收，自动检查仅检测客观协议和来源。

## 推进下一阶段 S2C 前
- 将对照结果和人工观察写成 verdict；
- 若曲线小笔仍不显著优于自动填充，则优先改变“动作语义规划”而不是盲目叠加更多笔触；
- 确认 S2B 比 A 改善后，再增加 `scratch/look --crop` 的独立自动化 Agent 契约。

开源项目只借鉴研究机制，没有复制第三方实现代码；原物理引擎仍为 Alice / claude-paint MIT 许可证。
