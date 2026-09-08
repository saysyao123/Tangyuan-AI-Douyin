# MULTIMODAL_REFERENCE_HARNESS v1.0

> 用于 Seedance 2.5 / 同类多模态视频模型的参考素材组织、上传顺序、职责绑定、时间轴调用与 QA。

## 状态

- 结构：LOCKED FOR CURRENT TEST。
- 当前 15.57s 测试：8 张图片 + 1 条 Temporal Depth + 1 条 BGM。
- 生成效果尚待首轮完整 Seedance 2.5 成片 QA；效果参数可继续迭代，但**素材职责与上传顺序先固定**。

## 核心原则

1. **One Asset = One Primary Role**：一个参考素材只承担一个主要职责。
2. **先绑定，再写时间轴**：先明确 WHO / WHERE / HOW MOVE / WHEN / END LOOK，再写动态提示词。
3. **角色与场景解耦**：角色图不负责换场景；场景图不负责改脸。
4. **Depth 只负责动作层**：不继承原真人身份、服装、背景、滤镜。
5. **BGM 是唯一节奏基准**：动作卡点、镜头转换、高潮和最终停帧都对齐 Master Audio。
6. **不强制九宫格**：能拆成独立参考图时，优先独立图片，降低 grid crossover。
7. **不堆无意义参考**：只上传确实会在 Timeline 被调用的素材。
8. **禁止过度禁止项**：优先写清正向职责、优先级和时间轴；禁止项只保留关键失败模式。

## 默认参考层

### A｜Character Identity

默认 3–5 张，当前测试锁定 5 张：

- 正面全身
- 3/4 全身
- 背面 / 3/4 全身
- 正面脸部近景
- 侧脸 / 3/4 脸部近景

只负责：

- facial identity
- hairstyle
- makeup
- body proportions
- costume
- accessories

### B｜Scene Lock

默认 2 张：

- Scene Master Wide
- Performance Area Mid / Full Shot

只负责：

- architecture
- room layout
- windows / screens
- lighting direction
- color atmosphere
- performance zone

### C｜Storyboard / Atmosphere

按需要 1–4 张，不强制九宫格。

当前测试只保留：

- Final Silhouette / Sunset Atmosphere

仅在 Timeline 明确调用时生效。

### D｜Motion

默认：

- `Temporal Depth` = 正式动作参考
- `Raw Depth` = 细节 A/B / QA，不默认上传

只负责：

- body movement
- gesture sequence
- arm trajectory
- torso / shoulder rotation
- center of gravity
- timing
- acceleration / deceleration

### E｜Audio

默认只使用一个 Master BGM。

负责：

- beat
- action accents
- shot transitions
- emotional progression
- final pose timing

## 固定上传顺序

上传必须逐项核对编号，不建议一次性多选导致自动重排。

```text
1. Character Identity images
2. Scene Lock images
3. Storyboard / Atmosphere images
4. Temporal Depth video
5. Master BGM
6. Index Audit
7. Paste Prompt
8. Generate
```

当前测试映射：

```text
@Image1 = 女主全身正面
@Image2 = 女主全身 3/4
@Image3 = 女主背面 / 3/4
@Image4 = 女主正面脸部近景
@Image5 = 女主侧脸近景
@Image6 = 古风雅室大全景
@Image7 = 古风雅室表演区域
@Image8 = 夕照剪影 / 氛围参考
@Video1 = Depth Anything V2 Temporal Depth
@Audio1 = Master BGM
```

上传完成后，必须先做 Index Audit，确认 Prompt 里的编号与 UI 实际编号一致，再点击生成。

## Prompt 固定骨架

动态提示词默认按以下顺序：

```text
1. Task
2. Reference Binding
3. Character Isolation
4. Visual Direction
5. Reference Timeline
6. Motion Priority
7. Motion Physics
8. Camera Discipline
9. Overall Requirements
```

### Reference Binding 必须回答

- 哪些图定义人物？
- 哪些图定义场景？
- 哪张图只控制特殊镜头 / 剪影？
- 哪条视频只控制动作？
- 哪条音频是唯一节奏基准？

### Character Isolation

单女主项目默认写明：

- 全片只有一个主角；
- Character Identity references 具有最高人物身份优先级；
- Scene / Atmosphere references 不得重新定义人物脸型和服装。

多角色项目必须为每个角色分配独立引用区间，禁止 crossover。

## Motion Priority

不要让 Depth 在每个镜头拥有同样控制权。

每个 Timeline 段至少标注一个 Motion Priority：

- `NONE`：空镜 / 纯场景
- `LOW`：近景表情、静态造型
- `MEDIUM`：轻动作、过渡
- `HIGH`：舞蹈起势 / 主要动作
- `VERY HIGH`：核心舞段 / 收尾动作

原则：

- Dance = HIGH / VERY HIGH
- Beauty Close-up = LOW–MEDIUM
- Scene Establishing = LOW
- Silhouette Transition = MEDIUM
- Silhouette Closing with choreography = VERY HIGH

## Timeline 规则

每个时间段必须写：

- Time Range
- Narrative / Visual Function
- Primary References
- Motion Priority
- Shot Size / Camera
- Main Action
- Transition / Ending State

不要只写“漂亮地跳舞”“电影感运镜”。

## 动作物理硬规则

人物位移必须可读：

```text
抬脚 → 落脚 → 蹬地 → 重心转移 → 加速 / 减速
```

禁止无足部逻辑的地面滑行 / 漂移。

当 Depth 本身没有完整脚部信息时：

- 不擅自创造大幅横向跑动；
- 优先稳定站位；
- 用转髋、转肩、躯干和重心变化完成动作。

二级物理：

```text
body
→ hair / sleeve / ribbon
→ inertia
→ overshoot
→ rebound
→ decay
```

不同材质不得同步机械摆动。

## 当前视觉测试预设（非通用硬规则）

当前这一轮采用：

- Character：冒险少年动画式、强轮廓、动态可读的人物设计语言；
- Background：明亮、通透、天空与光线层次丰富的动画电影背景；
- Objects / Creatures：手作感、温柔奇想、轻巧有生命力的设计语言；
- 全部保持原创，不直接复制现有角色或具体镜头。

未来换项目时只替换 Style Preset，不改变本 Harness 的角色 / 场景 / Motion / Audio 职责结构。

## Baseline 生成规则

首轮生成必须保持“干净基线”：

- 上传顺序固定；
- 不临时增加新参考；
- 不在生成前反复改 Prompt；
- 不同时测试多个变量；
- 先得到一条完整结果，再做 QA。

## QA Gate

生成后至少检查：

### 1. Identity Lock
- 是否始终同一张脸
- 发型 / 服装 / 体型是否稳定

### 2. Scene Lock
- 是否始终同一空间
- 月窗 / 灯笼 / 地面 / 光向是否连续

### 3. Reference Crossover
- 场景图是否污染人物
- 剪影图是否重塑人物身份
- Character 图是否把环境拉回人物参考图背景

### 4. Depth Obedience
- 手势顺序是否命中
- 肩线 / 躯干 / 重心是否跟随
- 高优先级舞段是否明显优于纯 Prompt 自由舞蹈

### 5. Audio Sync
- 动作峰值是否踩点
- 转场是否贴合 BGM
- 最终 Pose 是否落在正确结尾

### 6. Physics
- 无滑行 / 漂移
- 无四肢异常
- 头发 / 袖子 / 飘带存在合理惯性

### 7. Ending
- 必须回到主角
- Ending Pose 清晰可剪
- 不用空镜或配角收尾

## 迭代规则

一次只改一个主要变量：

```text
A. Reference Mapping
B. Timeline
C. Motion Priority
D. Camera
E. Style
F. Depth Segment
G. Audio Alignment
```

禁止一条结果不好就同时换角色图、场景图、Depth、BGM 和 Prompt。

只有连续测试证明某项规律稳定有效，才升级为长期 LOCKED_RULE。
