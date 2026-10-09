# S2A_Result — GPT 自主画家 × Stillwet 原生真实画架（2026-10-09）

状态：**技术闭环 PASS；艺术品质 NOT YET PASS**。

## 执行方式
- GPT 在 ChatGPT 对话中看到**上一轮实际生成的 Stillwet 画布**，按观察情况编写新的 Lua 作画 chunk；接入 GitHub Actions 的原版 `easel` Rust 引擎执行。无 OpenAI API Key，因此这次属于“手动调度的 GPT 绘画 Agent 闭环”，**不等于无人值守的云端 AI Agent**。
- 只保留 GPT 原始作画 Lua 和物理颜料画架；**没有**调用 GPT 图片生成、参考图逐像素描摹或将最终 PNG 替换到视频尾帧。
- 固定原项目源码：https://github.com/aliceisjustplaying/claude-paint ，提交 `8eeb9bec3ce146bcd15c37db447665391fb95bdd`；`giverny` 颜料盒。
- 题材：白陶杯 + 柠檬 + 桌布，画布宽高比 4:5。

## 完成的四轮独立决策（每轮观察前一轮画布）
1. **Chunk 1**：线稿、配色、大色块铺色。首次执行因错用颜料盒里不存在的 `raw umber` 和 `bone black` 失败，按报错换用该盒实际有的颜料后成功；画布偏紫，器物轮廓初成。
2. **Chunk 2**：观察到背景偏紫、杯身笔触太碎、柠檬平面化；重配背景与桌面色、补杯口和杯身明暗、柠檬体积；运行成功。
3. **Chunk 3**：观察到投影偏紫、背景发黄、柠檬层次不够；补涂墙面、阴影、杯底、果体；运行成功。
4. **Chunk 4**：观察到背景太绿且密、桌布空、杯身侧面平；加薄罩染、桌布层次、陶杯侧面和柠檬局部笔触；运行成功。

## 真实运行证据
- 第 1 轮成功：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37892579839
- 第 2 轮成功：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37892969561
- 第 3 轮成功：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37893494104
- 第 4 轮成功：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37894442380

第 4 轮原生渲染日志：
- 4/4 chunk executed OK
- 83 native painting snapshots in `frames.tsv`
- 1223.1 minutes of simulated hand time
- 65.3 seconds to render completed native painting at 600 px
- H.264 MP4: 600×750 / 24 FPS / 24 s / 576 frames
- 视频最后一帧与原生渲染 PNG 平均绝对像素差约 1.85/255，是视频压缩带来的常见误差，**不是末尾切高清原图**。

## 客观审美复盘
这轮成功验证 GPT 主导真油画引擎作画并通过画布反馈修改，但距离官网精品还明显有差距：
- 颜料调色不够稳定，色相在两轮间出现较大变化；
- 最后罩染背景时一些暖色笔触越过边界落到杯子上；
- 背景刷痕太规律；桌布缺乏真实细腻的结构；
- 陶杯尚缺真实物体复杂的光影过渡和杯沿结构，柠檬层次初具但不够精致。

## 下一阶段应优先做
- 真实运行 `scratch` 测试调色配方、工具 / 掩模边缘，避免盲画污染完成区域。
- 增加杯口、柄部、果体的原生 `look --crop` 观察。
- 减少单次覆盖面积，每次修正先保护已完成区域，优先修体积与光影而不是全图加纹理。
- 继续保留所有真实 Chunk + 原生引擎完整回放证据。
- 只有在这一层作品质量稳定后，再决定是否接入 OpenAI API 做自动无人值守；不尝试违规登录自动化或绕过限制。

原始作者 Alice / claude-paint，代码 MIT；原上游作品与日志 CC BY 4.0。
