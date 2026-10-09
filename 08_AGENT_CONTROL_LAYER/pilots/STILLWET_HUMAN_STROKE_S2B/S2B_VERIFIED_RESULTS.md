# S2B 原生笔触机制 A/B：实际验证与复盘

日期：2026-10-09
结论：**ENGINE_PASS / PROCESS_IMPROVED / HUMAN_STROKE_NOT_YET_PASS**。

## 实际运行证据
- v1： https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37901653987 — `success`
- v2： https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37902188321 — `success`
- 上游原生引擎 `8eeb9bec3ce146bcd15c37db447665391fb95bdd`；同一画布、同一调色板、同一 `common.lua` 各自的 A/B 比较。
- A：`common.lua + uniform.lua`，更多均匀区域铺色；B：`common.lua + form_guided.lua`，形体走向、转折曲线与手动压力变化。
- 实际执行的是 Rust 物理画架 + Lua + 官方 `replay_clip`，不是 GPT 生图或数字蒙版揭示。

## 实测数据
| 组别 | 渲染时长 | 模拟手绘时间 | 原生取帧 | H.264 视频 |
|---|---:|---:|---:|---:|
| v1 / A 自动铺色 | 25.0s | 174.9min | 22 | 24s / 560×700 / 576帧 |
| v1 / B 形体导向 | 22.1s | 87.0min | 20 | 24s / 560×700 / 576帧 |
| v2 / A 优化底色 | 25.8s | 210.1min | 25 | 24s / 560×700 / 576帧 |
| v2 / B 优化底色 + 形体导向 | 23.5s | 122.1min | 22 | 24s / 560×700 / 576帧 |

所述物理模拟运行时间来自 `painting_log.txt`。录像只是以不同时间权重保留和插值已有原生时点，无新增渲染器。
特别注意：B 用时少并不意味着 B 本身质量更高，二者动作数量、覆盖率不同；必须进行视觉验收。

## 人工视觉观察
- v1 A 与 v1 B **都明显失败**：共同的第一遍铺底过于稀疏且平行，露出大片白布，形成“墙纸”/“印章”纹理。主体导向 B 可以改善个别曲线，但整体遮掩了这种改善。
- v2 A 与 v2 B **明确改善了铺底**：改为一次较完整的宽刷铺底、方向微变、湿色面融合后，背景连续、露白大幅降低。
- 用两版一致的左上方背景固定窗（20:250, 25:225 px）和启发式阈值 RGB > (155,148,135) 检测“接近浅底布的像素”：v1 约 33.22%，v2 约 0.02%。这是一个**粗略颜色代理指标**，不是真实空白像素的完美分割。
- v2 B 杯把与果体转折细节稍多，语义组织比全自动覆盖更好；但杯身过于光滑、物理体积刻画不足，柠檬阴影发绿且投影呈色块，远未达到 Stillwet 官方完整作品的审美水平。
- 仍未拥有真实画家的完整手部连续性（数十笔一气呵成、停笔观察、局部修正与落笔密度节奏）。

## 更深层的技术瓶颈：回放取帧“看似连贯”却仍可能卡顿
进一步复查原始 `crates/easel/src/frames.rs` 发现：
- recorder 按画架模拟 **hand time** 取帧，但一次 `work` 铺色可在一个 15min 时间片跨越许多录制间隔，**每次状态观察最多只产生一帧**。
- 所以 `--frames-every 45` 的 v2 B 只输出 22 个原生画面时点，而最终 24 秒 MP4 有 576 帧，视频包含大量保持时间，动态节奏不等于 576 次笔画动作。
- 下一阶段应**减少每个 work 操作中的隐藏批量动作**；拆为可追踪的多个独立 `brush:stroke`，将观察取帧间隔调整为 5~10 秒，并检查实际原生帧数而不只看 MP4 帧数。
- 如需连续笔刷运动动画（真实显示笔头位移），可能需原引擎内部更精细的回放挂钩，不能仅靠增加 FPS 或插入重复帧。

## 结论：S2C 策略
仍保留 Stillwet 物理画架；**不直接接入其它项目训练权重或 GPU 画家**。
1. 策略层采用 FRIDA 类“计划少量笔触 → 观察实际画布 → 修正”，并加 Stillwet `scratch` 试画布。
2. 画法层将 `work` 限定主要用于初始大面积铺底；分角色/形体区域规划 5–20 笔明确连续曲线路径，控制 pressure、ramps、clip 和重装颜料频率。
3. 观察层每轮保存全图、局部放大、明暗图；制定“形体完成 / 轮廓完成 / 画面材质”三个具体验收项。
4. 录像层以真实动作时点为核心验收；不能把 576 帧 MP4 等同于 576 个原生笔画状态。
5. **人类感未通过之前，不开始大幅追求美术风格和高清放大。**

## 开源来源与许可注意
- FRIDA：https://github.com/cmubig/Frida (GPL-3.0；只借鉴思想，不复制代码)
- Content Masked Loss：https://github.com/pschaldenbrand/ContentMaskedLoss
- Compositional Neural Painter：https://github.com/sjtuplayer/compositional_neural_painter
- Painterly Curved Strokes：https://github.com/Impasto-Lab/Painterly-Curved-Strokes
- Oil Paint Tuner：https://github.com/miya9756/Oil-Paint-Tuner
- BrushOS：https://github.com/Legedith/BrushOS-Robotic-painting-in-action
- 原 Stillwet：https://github.com/aliceisjustplaying/claude-paint
本轮 S2B 所有 Lua 样例均为我们自己写的演示脚本，未复制第三方绘画项目的受版权保护实现。
