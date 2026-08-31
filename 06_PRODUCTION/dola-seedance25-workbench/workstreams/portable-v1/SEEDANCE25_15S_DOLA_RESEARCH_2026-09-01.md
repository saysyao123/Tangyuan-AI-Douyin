# Dola × Seedance 2.5｜15 秒生成研究记录

日期：2026-09-01
状态：`《五点二十》测试暂停；转入更小、更可诊断的 Seedance 2.5 参考生视频测试`

## 1. 当前实测事实

- 用户已在 Dola 中真实完成 Seedance 2.5 10 秒图生视频。
- 用户已观察到专家模式可把 30 秒需求编排为两段约 15 秒结果，但具体底层模型身份需单独确认。
- 《五点二十》S01、S02 在当前流程下曾成功；S03 在更重的多参考 + 长 Prompt 结构下被拒绝。
- 因此不能简单归因为“成年男女双人”或“公寓室内”绝对不可生成；至少已有真实反例。

## 2. 公开资料与开源项目交叉结论

### Dola 当前公开生成页

Dola 公开 AI Video Generator 页面显示：
- AI Model：Seedance 2.5 Audio
- 480p / 720p
- 时长界面：4–15 秒
- 大量官方/站内 inspiration 为 15 秒 UGC / TVC / 产品展示类任务

这说明在 Dola 的公开生成 surface 上，15 秒本身是正常支持档，而不是异常长度。

### Seedance 2.5 开源 Prompt 经验

多个近期社区 Skill/Guide 的共识：

1. **不要把图片里已经清晰可见的内容重复写成长篇人物描述。**
   图生/参考生视频 Prompt 应更多描述“变化、动作、镜头和声音”。

2. **每个参考资产只承担一个明确职责。**
   典型写法：
   `@Image1 defines identity only; do not use its background.`
   `@Image2 defines scene only; do not use its person.`

3. **参考图越多不等于越稳定。**
   社区指南给出的实际建议起点常低于模型硬上限；大参考集会增加职责冲突，尤其同一个人物在多张写实图里反复出现时。

4. **15 秒应按 3–4 个连续 Stage/Beat 写，而不是堆满导演说明。**
   每个 Beat 最好只有一个主要动作 + 一个可观察结束状态。

5. **时间段是节奏预算，不是帧级剪辑命令。**
   常见结构：0–4s / 4–9s / 9–15s，或 3–4 个 Beat。

6. **参考声明 → 一句话目标 → 分段动作 → 声音 → 连续性** 是更接近 Seedance 2.5 官方/社区范式的结构。

7. **参数应尽量在 UI / API 中设置。**
   Dola 专家模式如不能明确锁模型，可在自然语言开头要求“使用 Seedance 2.5”，但不应把整段 Prompt 写成参数说明文档。

## 3. 对《五点二十》S03失败的当前判断

更可能是以下变量之一或组合，而不是剧情本身：

- 同时上传 5–7 张写实人物/场景/故事板参考，职责重叠；
- 角色锚定图 + 首帧 + 场景图 + 四格故事板里反复出现同一人物，模型需要同时解析多个版本的脸、站位、构图；
- Prompt 过长，重复人物五官、空间规则、禁项、情绪、模型能力，降低主动作链权重；
- “故事板 grid”作为一张图片的可控性低于独立 keyframes；
- Dola Expert 是 agent surface，最终实际路由可能依据输入附件与语义自动选择生成方式，不能假设和 Dreamina/CapCut 的 reference mode 完全等价。

## 4. 下一轮不再继续《五点二十》

当前项目暂停，原因不是故事不成立，而是变量太多，不适合作为 Seedance 2.5 15 秒参考生视频的基础诊断样本。

## 5. 推荐新测试项目：单人物 + 一件道具 + 一个空间 + 3 个阶段

### 项目名：`《未寄出的明信片》`

目标：只验证 Seedance 2.5 在 Dola Expert 中的核心参考能力，不测试双人物关系。

15 秒剧情：
- Stage 1（0–5s）：一名虚构成年女性坐在雨夜咖啡馆靠窗座位，看着桌上一张空白明信片。
- Stage 2（5–10s）：她拿起笔写下一小段不可读文字，停顿，然后把笔放下。
- Stage 3（10–15s）：她把明信片翻面、放进一个浅色信封，望向雨窗，保持安静。

测试资产建议仅 3 张：
1. `@Image1`：首帧，最高优先级，定义人物 + 0 秒构图。
2. `@Image2`：角色锚定，只定义人物身份/服装，不使用背景。
3. `@Image3`：三格或四格故事板，只定义动作顺序，不使用画风。

暂时不上传单独场景母版、道具母版。

Prompt 结构：

```text
Use Seedance 2.5.

@Image1 is the first frame and defines the opening composition.
@Image2 defines only the same character's identity and clothing; ignore its background.
@Image3 defines only the action order; do not reproduce the storyboard style.

Create a 15-second 9:16 realistic cinematic clip in the same rainy café.

0–5s: ...
5–10s: ...
10–15s: ...

Sound: ...
Continuity: keep the same person, clothing, table, postcard, camera side and rainy window.
```

## 6. 推荐诊断阶梯

新项目按以下顺序，不一次把所有能力塞进去：

- Gate A：首帧 1 张 + 简短动作 Prompt → 15s
- Gate B：首帧 + 角色图 → 15s
- Gate C：首帧 + 角色图 + 故事板 → 15s
- Gate D：在 Gate C 稳定后再加入自然中文对白
- Gate E：最后才测试双人物、多参考、场景锚定和连续多段

每个 Gate 只改变一个变量。

## 7. 公开研究来源

- Dola AI Video Generator: https://www.dolai.video/
- magiccreator-ai/seedance-2-5-prompts: https://github.com/magiccreator-ai/seedance-2-5-prompts
- lukasersil/seedance-25: https://github.com/lukasersil/seedance-25
- LeonSooLab/seedance-2.5: https://github.com/LeonSooLab/seedance-2.5
- HaoXuanAce/seedance-2.5-director: https://github.com/HaoXuanAce/seedance-2.5-director
- opensource-works/awesome-seedance-prompts: https://github.com/opensource-works/awesome-seedance-prompts

> 注意：以上开源项目均为社区资料，不等同于 Dola 官方实现。Dola Expert 的真实路由和限制仍需以当前 UI 与用户账号实测为准。
