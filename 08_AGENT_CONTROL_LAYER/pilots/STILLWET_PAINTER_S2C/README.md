# Stillwet S2C｜GPT 真正分层绘画 + 原作者方法复刻

## 唯一目的
纠正 S2B「更平更像数字填色」的艺术退步。恢复原作者的**地色系 / 湿画与干燥 / 色层透明罩染 / 观察决定下一笔**方法。保留原作者 Rust+Lua 物理引擎与原生视频录制。

### 本次 S2C 的严谨含义
- 当前 GPT 在对话中编写原生 Lua，并由 GitHub Actions 在 Ubuntu 运行；逐轮取回真实画布、视觉检查后才追加下一轮。
- **不是**在线实时全自动常驻 API Agent。GitHub Actions 无须 OpenAI API Key；所有图片由原生 Stillwet 物理引擎生成。
- 原作者的笔触日志仅用于学习**操作机制**与对照；没有复制他的完整画，也不以既有生图作成品贴图。
- 独立画作：横画幅石陶罐、双柠檬与古旧桌台，有软背景和左上漫射光；原作作为方法 golden reference，不复制原画位置和形状。

### S2C 必须遵循的控制原则
1. 先观察底稿（整体/明暗/局部），再决定主体是否优先需要转面。
2. 切回原作者用的初始默认地色颜料盒（不再 `giverny`），材料可用性实际运行校验。
3. `work` 仍用于必要的宽笔和物体底层；强调其内置物理笔触，不把它一刀切禁用。
4. 透明暗部的 `pile{..., medium=0.8~0.9}` 必须先使白色底层干燥，再用软掩模和最少量低覆盖罩染，局部观察效果。切勿整只壶湿时直接刷上大量铅白混合的深灰。
5. 对果体按连续色阶与弧线敷色，尽量减少整体强混合造成的扁平化。
6. 渐变的「找回/消失」边缘先于硬 `clip=true`。只在保护确需边界的部分应用严格 clip。
7. `wait(minutes)` 要依据 `drying(x,y)` 的实际输出选择时长，而不是机械每 24 小时执行一次。
8. 视频只能来自原生 `frames.tsv`，需报告原生状态个数，不以 MP4 576 帧假装 576 次真实绘画动作。

### 计划与验收
- Round 1：铅笔构图 + 暗底背景 + 石台初稿（4 chunks）；**实际执行后观察**。
- Round 2：主体大关系；陶壶灰白体积与水果暗中亮三调；先进行连续转面，不画表面装饰。
- Round 3：根据画布需要处理混色失败、错误的实边；采集干燥状态并合理等待。
- Round 4：尝试局部薄罩染、擦改与杯口/柄部边缘；保留现场决定不做无意义新笔触的权利。
- Round 5：局部收尾及原生回放视频；最终评估「层次、体积、空间、自然笔触」是否超过 S2A/S2B。

**防提前通过**：本轮没有凭运行状态推断美学通过。任何轮次还未执行/观察都不标记 PASS；已通过的只有上一项目 S1 原作品的技术复刻。

## 核查链接
- 原项目：https://github.com/aliceisjustplaying/claude-paint
- 原生 GPT S2C 工作流：`.github/workflows/stillwet_painter_s2c.yml`
- 原创绘画源：`painting.lua`
- 上一轮退步复盘：`../STILLWET_HUMAN_STROKE_S2B/S2B_REGRESSION_ROOT_CAUSE_20261009.md`
- 原始创作过程参考：https://github.com/aliceisjustplaying/claude-paint/blob/main/archive/collection/inputs/journals/r16-c1.md
