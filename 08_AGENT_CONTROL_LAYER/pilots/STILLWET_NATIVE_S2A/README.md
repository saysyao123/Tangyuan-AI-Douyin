# S2A｜GPT 画家 × Stillwet 原生画架｜白陶杯 + 柠檬

## 锁定目标
验证当前 ChatGPT 中的 GPT 作为真实画家，看到画布之后自主决定如何调整、调色与落笔，驱动上游原版 Rust+Lua 油画引擎；不用 GPT 图片生成功能、图片描摹、OpenCV 绘制或最终高分辨率图替换。

## 输入/执行方式
- 本轮无 OpenAI API 凭据，**不是无人值守云端 Agent**：在 ChatGPT 对话里由 GPT 人工调度多轮观察与创作。
- 第 1 轮：GPT 产生第一段可执行 Lua，交 GitHub Actions 真实画架运行。
- 随后的每一轮：实际取回原生 `canvas.png`，观察后再决定修改动作；只**追加**成功的 Lua chunk，不改变或删除已有笔触。
- 原生引擎固定于 Git commit `8eeb9bec3ce146bcd15c37db447665391fb95bdd`；`giverny` 画材箱。
- 所有指令都在 `painting.lua`；每次 GitHub commit 与 Actions run 都是可以审计的决策历史。
- 视频来自原生 `frames.tsv` 的逐笔作画取帧，经原上游 `scripts/replay_clip --reuse` 输出；不借助外部高级视频生成器。
- 画布始终以 1000 坐标单位宽、纵向 H=1250 来定义，测试题材为左前方黄柠檬、偏右的白陶杯、暖灰色桌布、橄榄灰暗背景。

## S2A 验收（分成真实的两类）
1. **引擎链路验证**：所有实际绘制与 MP4 来自原生 Stillwet Rust 模拟引擎，PNG 不是大模型生成图。
2. **观察/修正验证**：至少 4 个由 GPT 自主编写、先查看上一轮 canvas 再提交的连续创作 chunk；记录每轮画布发现、下一步目标与实际绘画结果。
3. **审美验收**：陶杯轮廓、杯把、明暗体积、椭圆杯口、柠檬的体积与桌面投影都可辨，笔触是真实的油彩模拟。
4. **视频验收**：最终回放视频时间正确、最后一帧对应原生画布，不切换 GPT 终帧。

## 当前状态
- S0 原作者样例重放：通过。
- S1 原作者完整作品重放：通过。
- S2A 第 1 次由 GPT 独立创作的真实绘制：运行中；结果须以 GitHub Actions run 与 artifact 为准。

## 上游
Alice / claude-paint: https://github.com/aliceisjustplaying/claude-paint
代码 MIT；原作和日志参照上游 CC BY 4.0 要求署名。

## 为什么不用现成 GPT 生图来做最终态
本测试唯一目标是验证 AI 控制真实画笔，任何借助生图终帧强行对齐的策略都会让结果失去验证价值。
