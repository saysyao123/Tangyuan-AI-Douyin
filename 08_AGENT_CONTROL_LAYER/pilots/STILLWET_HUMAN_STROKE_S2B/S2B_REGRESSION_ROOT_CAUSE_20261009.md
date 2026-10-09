# S2B REGRESSION｜为什么“人类笔触优化”反而比上一版差

时间：2026-10-09
权威结果：`S2B_ART_REGRESSION_CONFIRMED`。保留 S2B 作实验对照，不把它作为下一轮画质基线。恢复 **上游官方 94-chunk 绘画过程** 作为主流程/质感基线；S2A 只作 GPT 创作的中间参照。
保留物理原生引擎，不改视频为图片渐显。

## 1. 三条对照结果（视觉）
1. **S1 / Stillwet 原作《Stoneware Jug with Two Lemons and a Knife》**：深浅有空间关系，暖灰墙面有空气感，器物不靠白色平块描轮廓，而靠陶器薄罩染、湿干混合、近实远虚及细节逐渐塑造。
2. **S2A / GPT四轮**：虽色彩污染、重复横纹严重，但笔触可见，暖冷有局部变化，绘画过程的局部动势仍较强。
3. **S2B / 双段 A/B**：背景更均匀，图像更干净；但陶杯薄如平面剪影，果体像被轮廓裁切的色块，光影不够连续，负空间更显空白。属于审美退化，不可因“露底像素下降”宣告更好。
三者题材、构图/画布长宽比不同，不能用单一指标定量排序；但主观对照可支持 S2B 在层次和视觉兴趣上退步。

## 2. 上游真实过程与我们的数字差异
- 上游完整Lua：`archive/collection/studios/paint-studio-3be9e8/paintings/lua/painting.lua`，**94 successful chunks**，53 个模拟绘画日，229 个原生画布取帧。保留日记：`archive/collection/inputs/journals/r16-c1.md`。
- 上游源码表达（注意以下是**Lua代码调用点**，不是实际物理落笔数量）：33 `work`、50 `blend`、72 `:stroke`、22 `wait`。
- 以绘画块粗分，上游初稿 chunk 1–17：13 work、11 blend、0 明确 stroke；形体 18–38：10 work、11 blend、2 stroke；罩染 39–60：6 work、9 blend、36 stroke；精修 61–94：4 work、19 blend、34 stroke。**随进度从大体积到手工塑形**。很多 `work()` 自身执行几十上百次真实刷毛运动，因此不能用“work 很多”推断“没有真实笔触”。
- S2A：4 chunks，3次局部反馈，原生83时点；调色/遮盖失控但确有阶段性修正。
- S2B v2 guided：只有 2 chunks、22 原生取帧、`wait()` = 0，12 次 `work`、2次 `blend` 和 6 个显式 `:stroke` Lua 调用点。即使 H264 MP4 576 帧，仍不等于发生过576次绘画状态记录。

## 3. 与原项目相比的六大偏差，按严重度排序

### 根因 A：创作活动被我们缩短成两个分段，失去「作品由实际判断持续成长」
官方日记：重画墙面、湿画时反复调颜料、因整个物体 blend 失去明暗而重做，观察阴影“太冷太深”和轮廓“被切直”，反复等待干燥、试透明罩染、调整果体接触阴影，最后按审美决定停手。
我们 S2B 的第二块在第一次看到中间画布之前就写完，没有临场反馈，**这不是原作者意义上的 painter loop**。
**修正：**重启多轮 `paint → look[whole,crop,value,squint,relief,palette] → note → scratch → paint`。每轮按当前缺陷自主决定下一笔，不能按预设“第 N 步加曲线”行事。

### 根因 B：误解 `work` 是机械填色器
上游 `notes/easel_guide.md` 明确：`work` 是以原生画笔进行连续实笔，支持 `piles`渐变、`scale_at`、`angle`函数、`edge`选择、压力、补色、随机性。上游画家不仅允许它，还在初稿使用很多次。
**修正：**恢复以 `work` 进行必要的大色块/转面、以 `brush:stroke` 做关键细笔，再由局部混色结合二者的阶段化策略。两者不是非此即彼。

### 根因 C：铺底“填满 + 混平”被当成高质量
S2B v2 为降低“墙纸纹”对所有背景增加 `fill=true`，再整面 `blend()`。消除露白属实，但牺牲笔触厚薄、背景价值变化，产生壁纸一样均匀的灰蓝大片。上游既保留可见底色，也会在需要时交叉 blend：目的是控制空气与距离，而不是追求像素100%不露布。
**修正：**撤销“浅色像素比例→质量提升”的优化判据。用静物视觉层次、明暗及局部笔触组织来验收。

### 根因 D：过度硬剪 `clip=true` 的几何剪影
上游笔记：`clip=true` 精准停止每一根刷毛在 mask 边缘，产生刚性的数字轮廓；`edge=found/firm/soft/lost`与局部越界可以帮助有控制地建立丢失与找回的边缘。
我们大面积 `clip=true`＋规则 poly/ellipse＋均匀白色填充，整张图像卡通贴纸。
**修正：**修切轮廓边界时用局部保护；主体内部使用软转面；背景用 `edge`的层次，不把每一笔剪成形状蒙版。

### 根因 E：颜色盒错误，不具备上游 Chardin 风格的泥土色系
上游 r16 真实作品配方大量使用 `raw umber`、`bone black`、`green earth`等中性地色，能够自然产生陶器白光和暖灰墙。
我们始终采用 `--@ box giverny`（`lead white/cobalt blue/viridian/cadmium yellow/... `但无原作者配方的地色管），只能用浓蓝+红+黄勉强调灰，易出现紫色和蓝绿色，颜色被迫漂移。
**修正：**下轮锁定可提供上游相同地色管的合法画材盒，并先在 palette / scratch 检查颜色；禁止把当前 `giverny` 的混色问题伪装成 GPT 画笔规划问题。

### 根因 F：颜料干燥与罩染真正缺席
原作者 22次 `wait()`，多轮测试得知白色氧化铅在湿混时会吞噬暗色，因此经过等待干燥的半透明无白色罩染塑形；另外对果体靠暗部→中间调→亮部的成组笔触取代全体 blend。
我们 S2B `wait=0`，只用湿油彩铺底＋少量亮部曲线，失去了颜料分层和透光感。
**修正：**在暗白交界优先测 `drying(x,y)`，等待“dry/setting”条件之后局部薄罩染与干擦，收尾由画面需要决定。

## 4. 重启的正确验收方案
**基线选择**：以 Stillwet r16 本物理引擎 + 官方日志/日记/艺术品质为 golden reference；不沿用 S2B v2 `common.lua` 的整面填充作为新默认。保留老文件作 FAIL witness。
**同题控制**：在相同 1000×800 的宽画幅、相同画材盒、陶壶-双柠檬-小刀等相似复杂度下，让 GPT *独立* 根据文字 brief 创作，不照搬原作者 94-chunk Lua；原作只用于 **方法基线**，不是直接复制结果。
**技术步骤**：
1) 原样复刻 original run 再次检查 palette / crop / gallery，不改物理引擎；
2) 研究 original 在早期/中期/晚期工作方法；生成 GPT 全局构图和基准灰度、光线计划；
3) 以真实画布每回合观察并记录动机，先铺体积，建立暗中明，不能仅走轮廓；
4) 真实测试 `scratch` 的调色与小区域试笔，之后正式画布使用同方案；
5) 让干燥与透明罩染遵守物理状态，以人工审美评价作停止标准；
6) 原生短视频从真实帧日志生成，帧状态数量/创作轮数皆作为独立佐证，不能拿 MP4 FPS 代替笔画数量。
**质量门槛**：空间明暗 > 形体可信 > 材料触感 > 边缘控制 > 视频流畅。若不满足，不推进高清/9:16成片与自动Agent。

## 5. 公开原作链接
- 原作者 repo: https://github.com/aliceisjustplaying/claude-paint
- 原作品: https://stillwet.art/p/r16-c1.html
- 原作 Lua: https://github.com/aliceisjustplaying/claude-paint/blob/main/archive/collection/studios/paint-studio-3be9e8/paintings/lua/painting.lua
- 原作日记: https://github.com/aliceisjustplaying/claude-paint/blob/main/archive/collection/inputs/journals/r16-c1.md
- 工具手册: https://github.com/aliceisjustplaying/claude-paint/blob/main/notes/easel_guide.md
- S2B 初轮通过，但艺术结果不及上游: https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37901653987
- S2B 修改铺底通过，但艺术进一步扁平化: https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37902188321

结论：原项目成功的核心是 **会观察材料、判断转面、知道什么时候继续画/等待/停手**。我们先前把它错误地简化成更密集/更连贯的可见笔触。恢复原项目的真实创作循环后才能谈“人类式笔触”与审美升级。
