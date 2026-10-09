# Stillwet S2C｜2026-10-09 最终原生绘画实测与失败归因

**最终判定：技术链路通过，艺术表现未通过（`NATIVE_PASS_ART_FAIL`）。不得用 S2C 替换官方 S1 作为质量基线。**

## 明确范围
- GPT 在当前对话中阅读前轮实际画布后，逐轮编写真实 Lua；云端 GitHub Actions 运行原作者固定版本 Rust `easel`。`scripts/replay_clip` 的默认 hand time ^0.6 时间压缩规则被本地重编码脚本复现，用于编码从云端取得的真实 `frames.tsv` + PNG。**没有**使用 AI 生图终帧、旧版 OpenCV 假笔触或末尾高清图替换。
- 上游固定 `8eeb9bec3ce146bcd15c37db447665391fb95bdd`；采用原始默认颜料盒，允许 raw umber、bone black、green earth、lead white 等，而非 S2A/S2B 使用的 `giverny`。
- 用户之前生成的柳树湖畔油画没有被这条静物实验用作终帧；仍以原官方静物的物理绘画方法为验收对象。
- 本轮是**人工调度的 GPT 画家闭环**（有模型决策，但无无人值守 OpenAI API 自动调用），与作者官方 painter harness 持续交互模式仍然不同。

## 四轮 GitHub 云端实际执行（都 success）
- 第一阶段（4 chunks）：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37907548045
- 第二阶段（8 chunks）：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37908076556
- 第三阶段（12 chunks）：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37908565360
- 第四阶段（15 chunks）：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37908985220
- 一个 FFmpeg apt 软件源超时的环境失败：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37907075157；后续取消云端依赖，物理渲染与视频编码解耦，该故障没有涉及任何绘画指令。

## 各轮真实画布视觉结果
1. **R1（4 chunks，27原生时点）**：暖灰背景和石台不再机械横向填满，地色系正确，主体刻意未完成。
2. **R2（8 chunks，48原生时点）**：对白陶罐使用高覆盖率深褐透明罩染导致深色岛状黑斑。最关键的根因证据：画布在等待 4 模拟绘画日后 `drying(365,424)` 仍是 `setting`，水果 `tacky`，盲目按固定天数罩染不成立。
3. **R3（12 chunks，65原生时点）**：不规则黑斑被分区重画遮住，但因为大量铅白进入修复混色，陶罐又几乎成了白色剪影；接触阴影像独立的不规则块。
4. **R4（15 chunks，78原生时点）**：再等待至第 26 模拟日局部颜料真正 dry，然后使用 8 次有压力变化的真实 filbert 手控长笔薄罩染。陶罐右侧出现阴影，但明显成为竖条带，依然没有自然明暗转折；没有达到原作质感。

每轮云端 Rust 物理绘制成功；每轮原生取帧均重新编码为**24秒 / 24FPS / 700×560 / H.264 MP4**。视频最后一帧与原生 PNG 的平均 RGB 绝对差：R1 1.38，R2 1.58，R3 1.54，R4 1.59（/255）。差距来自 H.264 有损压缩，无末段替换参考高清图。

## 对比原版的真正失效点
**S1**（原作者已完成的 `Stoneware Jug with Two Lemons and a Knife`，94 chunks、229 原生时点）仍明显优于这幅作品，不是因为画笔算法不同，而是因为 **画家控制循环** 不同：
- 我们在 Github Actions 里离线重放 **4/8/12/15 chunks**，每次待生成整张后才观察一次；官方原作连续完成更多小段、多种放大检查、湿干试验、调色、减法修正，并且有完整 journal 和 scratch 能力。
- 虽然 R3/R4 在同等物理引擎中试过 `piles` 梯度和独立手控 `:stroke`，仍无法替代真正的局部明暗规划与在画布上观察、微调的闭环。
- 原作者的画家日志明确提示：若白色基底未干，铅白吞噬阴影；即便干燥，也应小片测试混色和 glaze 强度。我们没有在正式落笔前先做 scratch，也没有有效的灰度/局部放大质量检查，因此 R2/R3 重复了原作者已经记录过的失败。
- 背景/果体/接触阴影缺乏真实光照体积；几何 mask 与单次剪影叠加让画面较为平面。V4 的竖条受单次连续操作位置过于规则和 lack of blend 的影响；物理模拟真实性不等于人类作画审美。

## 本轮学到的可迁移结论
1. 不可以凭“等待 N 模拟日”就假设漆层已经 dry；必须调用 `drying(x,y)` 多点探针，并判定局部条件达到后才能正式罩染。
2. `work` 不是要淘汰的工具；原版也大量使用它，但应避免在看图之前连续执行十几行全区铺色/罩染。
3. `medium=0.88` 是物理颜料参数，不保证自动形成漂亮透明渐层；透明度与负载、笔刷、已有色层、状态一起决定视觉效果。
4. 具有连贯几何路径的 `:stroke` 也不必然像真正人画；没有手动调色、值域过渡和局部检测就会产生条纹。
5. 录像 576 帧并非 576 个真实绘画时刻。最后一轮只有 78 个取帧条目（相同 hand_time 合并后 67 个不同时间点）；下一阶段录制需增加内部每笔状态 hooks，不能仅提高 MP4 FPS。

## 明确停止线与下一步 S2D（尚未执行）
**立即停止以旧 S2C 模板为基础无脑叠加更多镜头、细节或伪高清。**
下一步搭建真正「原生 live easel 画家」：
1. 云端持久化画家会话，使用 `easel open / do / look / note`（或官方 harness 工具层），支持 `scratch: true`；非每轮将完整 Lua 重放一遍才拿到一张整体 PNG。
2. 一次 GPT 只画 1–3 个小操作，每次前后用 `look` 观察整体 + crop + value + squint；重要的透明深色混合一律先在 scratch 再进主画布。
3. 建立 7 阶明度调色带和“光源/体积/受光/背光/反光”检查清单；让颜色质量先过关，后续再做边缘处理和材质点睛。
4. 运行时间和 API 成本可衡量：若希望完全无需用户逐轮干预，需允许 Work 云端执行或提供合规的 OpenAI API 接入；当前手动对话式流程不应该冒称全自动。
5. 真正能让陶罐转面、柠檬立体、背景有空气感并接近官方原作之后，才尝试柳树湖畔构图与抖音9:16视频。

## 文件
- `painting.lua`：15 chunks 的原创实际作画决策，无参考图片像素采样。
- `.github/workflows/stillwet_painter_s2c.yml`：GitHub Actions 真正 Rust 原生执行 + 保存 PNG、帧图和 `frames.tsv`。
- 回放脚本：从 `frames.tsv` 依据原官方 replay_clip 的 `hand_secs^0.6` 时间缩放规则、每个状态最多停留12秒、最后固定留3秒编码为 24秒视频。源帧未改动，视频编码在 ChatGPT 工作容器完成。
- 画布、过程图、4个视频、完整帧、QA 与中文说明随本轮压缩包交付。

原始作者及许可证：Alice / claude-paint, https://github.com/aliceisjustplaying/claude-paint 。代码 MIT；原作者绘画/日志 CC BY 4.0。
