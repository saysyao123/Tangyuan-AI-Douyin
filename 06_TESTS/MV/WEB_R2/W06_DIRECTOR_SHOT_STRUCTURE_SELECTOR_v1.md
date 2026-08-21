# WEB R2｜W06 Director Shot-Structure Selector v1

> 状态：`EXPERIMENTAL / NOT PROMOTED`。本文件来自 S1 / S2 Seedance 2 mini 实测，只记录当前 R2 的导演判断模型；未经过更多镜头类别验证前，不写入 `04_HARNESS/rules/ai_video.md` 的硬规则。

## 1. Why this exists

S1 与 S2 的对比证明：

- `一镜到底` 不是问题本身；
- `多镜` 也不是默认答案；
- 真正需要提升的是 **5 秒生产单元的导演结构选择能力**：先判断歌词任务、首帧潜力、视觉进程与模型负荷，再决定 `1镜 / 2–3镜 / 3–5镜`；
- 运镜是每个 Shot 内的摄影机控制，不是把整条 5 秒强行做成一个运镜术语展示。

核心修正：

`结构先于运镜，歌词任务先于结构，运镜服务视觉进程。`

---

## 2. Generated Evidence

### S1 v1 — FAIL

- 5.09s / 720×1280 / 24fps；
- fixed extreme-wide one-take；
- 巨树、弧墙、光束和人物比例几乎不变；
- 人物动作不足以构成持续视觉进程；
- 动态负担被转移到纱/衣料；
- 模型生成脱离人物的独立白纱，产生 topology failure；
- 结论：**“一镜到底 + 弱视觉进程”失败，不等于一镜到底失败。**

### S2 v1 — PASS / POSITIVE EVIDENCE

User-returned raw clip:
- 5.04s / 720×1280 / 24fps；
- single continuous Arc / orbit-like move；
- 人物从偏侧关系逐步过渡到更正的四分之三关系；
- 前景粗壮树干、人物、远处弧墙形成持续 parallax；
- 人物动作只保留伸手 / 抬头 / 凝望，模型负荷低；
- 摄影机运动本身持续改变人物与空间关系，因此 5 秒内始终有视觉进程；
- 单镜没有呆板感，反而保留了完整动作与柔和流动感；
- user judgement：S2 效果不错，环绕运镜感觉成立，应记录。

S2 的关键成功因素不是“环绕”这个词，而是：

`强首帧深度 + 一个连续人物动作 + 明显前中后景 + 可读视差 + 单一摄影机运动 + 明确更漂亮的终点角度`。

---

## 3. Director Decision Order

每个 5 秒动态段在写提示词前，按以下顺序判断：

### Step A｜Lyric Task

先回答：这句歌词在 5 秒里要让观众 **看到什么变化**？

只能选 1 个 Primary Task：
- `EMOTION_HOLD`：一个情绪持续存在；
- `DISCOVERY`：从未知到看见 / 从遮挡到揭示；
- `GESTURE`：一个完整身体或手部动作；
- `SPACE_REVEAL`：人物与巨大空间关系变化；
- `MOTION_PEAK`：歌词能量峰值 / 飞 / 跑 / 舞 / 爆发；
- `DETAIL_SHIFT`：眼睛、手、面纱、物件等注意力转移；
- `RELEASE`：尾部放松 / 漂浮 / 停留；
- `SEMANTIC_SEQUENCE`：一句歌词内部存在两个或更多明确语义阶段。

如果 Primary Task 说不清，禁止进入 Shot 设计。

### Step B｜First-frame Performance Potential

检查首帧本身：
- 是否有明显前 / 中 / 后景？
- 是否有适合形成视差的前景实体？
- 人物姿态是否已经提供动作入口？
- 构图从某个方向移动后是否会变得更漂亮？
- 是否有足够动作空间？
- 面纱、手、鸟、树枝等 fragile anchors 是否适合连续运动？

### Step C｜Choose Shot Count

不是机械配额，按导演任务选择。

#### 1 Shot / One Take

优先条件：
- 歌词是一个连续情绪 / 一个完整动作；
- 首帧本身已经漂亮且有空间深度；
- 一次摄影机移动能产生持续视觉进程；
- 动作无需语义跳跃；
- 连续性本身比切镜更舒服。

推荐任务：`EMOTION_HOLD / GESTURE / SPACE_REVEAL / RELEASE`。

S2 为当前 Positive Sample。

**One-take Gate：**
如果摄影机移动 5 秒后，主体大小、角度、前景遮挡、背景关系、光影或动作状态中没有至少 2 项发生清晰变化，则一镜到底风险高，应考虑切镜。

#### 2–3 Shots

优先条件：
- 有一个主事件，但需要 `建立 → 核心事件 → 余韵`；
- 需要从人物到细节 / 从细节回人物；
- 歌词存在一次明显转折；
- 单镜无法同时给出情绪与信息。

推荐任务：`DISCOVERY / DETAIL_SHIFT / moderate SEMANTIC_SEQUENCE`。

#### 3–5 Shots

优先条件：
- 歌词密度高；
- 明显卡点 / 拟声词 / 动作峰值；
- 需要多景别、多角度共同制造能量；
- 一条视频本身承担高潮或强 Hook；
- 单镜虽然可生成，但不足以达到 MV 所需视觉密度。

推荐任务：`MOTION_PEAK / dense SEMANTIC_SEQUENCE / strong Hook`。

**警告：** 3–5镜不是“更电影”的同义词。若每镜都只有 0.5–0.8 秒且没有清晰视觉任务，会变成随机剪辑。

---

## 4. Per-shot Camera Contract

无论 1 镜还是 5 镜，每个 Shot 内只定义一个主要 Camera Contract：

`景别 + 角度 + 起点 + 摄影机运动 + 速度 + 主体关系 + 终点`

例如 S2：

`中景 / 偏低角度 → 人物左前方 → 小角度 Arc → 稳定匀速 → 摄影机绕人物产生树干/人物/弧墙视差 → 结束在更漂亮的四分之三侧面。`

禁止：
- 同一个 Shot 同时要求 orbit + push + crane + handheld；
- 用“电影感运镜、动态镜头、史诗运镜”代替物理路径；
- 运镜没有明确终点；
- 运镜与人物动作抢同一个视觉重心。

---

## 5. Camera / Performance Load Budget

每个 Shot 默认只分配：

- `1 Primary Camera Move`
- `1 Primary Subject Action`
- `1 Secondary Physical Motion`

例如 S2：
- Camera：Arc；
- Subject：伸手 / 抬头；
- Secondary：发丝 / 面纱小幅风动。

避免同时要求：
- 大幅人物动作；
- 大幅布料；
- 飞鸟；
- 强光变化；
- 复杂焦点变化；
- 复杂摄影机运动。

Seedance 不是不能做，而是同一 5 秒同时竞争的任务越多，主体 / 面纱 / 拓扑越容易崩。

---

## 6. Lyric-to-Camera Matching｜Experimental

不是固定配方，只用于导演初筛。

| 歌词任务 | 优先考虑 | 谨慎使用 |
|---|---|---|
| 抬头 / 发现 | Tilt Up / Arc reveal / Push from wide to medium | static without event |
| 翩翩 / 优雅流动 | Arc / lateral Track / gentle Orbit | aggressive whip / shake |
| 呼喊 / 拟声词 | 2–3 shot reaction / Snap pan / cut to detail | 5s slow orbit only |
| 飞过 / 冲出 / 高潮 | 3–5 shots / low-angle track / pedestal/crane / fast follow | locked long hold |
| 看见鸟 / 细节发现 | rack focus / reveal / tilt / insert cut | large 360 orbit |
| 巨大空间 / 人很小 | Pull-back / Crane / static with strong subject action | repeated slow push |
| 漂浮 / 释放 | long one-take / small lateral drift / locked hold | fast cuts |

---

## 7. Beauty / Comfort Gate

在最终提示词交付前，导演必须自问：

1. 这 5 秒最值得保留的一张“动态中的封面帧”预计在哪里？
2. 摄影机为什么从这里移动到那里？
3. 如果不切镜，这 5 秒是否始终有视觉进程？
4. 如果切镜，每一次 Cut 是否都带来新的信息 / 情绪 / 视角？
5. 人物动作是否比歌词更抢戏？
6. 环境动态是否只是在“乱动”？
7. 面纱 / 衣摆是否被当作主事件过度使用？
8. 最后一镜有没有一个舒服、可剪的结束状态？

任何一个 Shot 仅仅为了“增加镜头数”存在，则删除。

---

## 8. Current R2 Testing Consequence

- 不再要求 S1 v2 的 4 镜结构代表所有片段；
- S2 单镜 Arc 已作为 Positive Sample 记录；
- 后续 S2–S9 应逐段重新做 Shot-count decision，而不是统一 1 镜或统一 3–5 镜；
- 当前需要继续测试的是“导演结构选择器”是否能让每段歌词得到更合适、更美、更舒服的 5 秒视觉；
- 本文件仍为实验层，至少需更多 `one-take pass + multi-shot pass + failure` 证据后再讨论固化。
