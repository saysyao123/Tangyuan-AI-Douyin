# Rules｜MV First-Frame Set QA v1.0

> Status: `ACTIVE / HARD FOR HG03 / D01-B HARDENING`
> Role: 防止“歌词语义正确但首帧不好看 / 整组重复 / 动态不可执行”的方案进入 HG03。
> Core: **歌词视觉命中 > 独立画面美感 > 整组差异与连续 > 动态可执行性。**

---

## 1. First-frame definition

首帧不是海报，也不是概念插画。

每张必须同时满足：
1. `LYRIC-SPECIFIC HIT`：这张图必须有属于当前歌词/Beat的不可替代视觉答案；
2. `STANDALONE BEAUTY`：单独截出来也应达到可作为电影剧照/封面候选的整体美感；
3. `0-SECOND ANCHOR`：主动作已经处于可以继续执行的初始态；
4. `EDIT VALUE`：有 clean in / clean out 与可读的动作发展空间；
5. `WORLD COHERENCE`：人物、妆造、材质、光色和空间属于同一个世界。

功能正确但视觉像说明书、劳动演示、机械任务或普通写真，不得自动 PASS。

---

## 2. Beauty Gate｜HARD

对每张首帧检查：
- 主视觉是否一眼成立；
- 构图是否有清晰层级而不是元素堆叠；
- 光线是否服务人物/事件而不是随机“漂亮光”；
- 色彩是否高级、克制、有主次；
- 人物妆造与场景是否互相强化；
- 画面是否存在一个可记忆的视觉母题；
- 是否具有电影剧照感而不是生成图展示感。

若导演只能解释“为什么语义对”，却说不出“为什么这张画面本身值得停留”，标记：
`FIRST_FRAME_BEAUTY_FAIL`。

---

## 3. Set Differentiation Gate｜HARD

整组首帧必须检查：
- 景别是否有明显变化：wide / medium / intimate / detail 等；
- 机位高度是否全部一样；
- 人物是否每张都在画面中央或都以同一方向侧背；
- 是否连续重复“人物静立 + 风吹衣摆 + 晨光远山”；
- 是否连续重复“近景脸 + 浅景深”；
- 空间开合是否存在节奏：收 / 放 / 转折 / release；
- 每张的 dominant event 是否不同。

允许统一世界，不允许统一成同一个构图模板。

若 2 张以上在缩略图级别难以区分叙事职责，先改 Director/First Frame，不进入 HG03。

---

## 4. Wardrobe / Character / World coherence

人物项目必须检查：
- 同一角色身份稳定；
- 妆容、发型、头饰、面纱/面罩政策明确；
- 服装层级与颜色连续；
- 角色造型与世界美术逻辑一致；
- 不因某一张追求“更漂亮”而突然变成另一套人物设计。

如用户给出妆容/人物参考，应提取可复用的结构性特征，再适配当前歌曲世界；不要机械复制参考场景。

---

## 5. Performability Gate｜HARD

每张必须明确：
- `PRIMARY EVENT`；
- `ACTION ENTRANCE`；
- `STATIC BASE`；
- `AVAILABLE MOTION SPACE`；
- `RESIDUE`；
- `SETTLED END POSSIBILITY`。

若首帧只是“已经完成的漂亮姿势”，后续5秒没有自然主动作入口，则不能作为正式动态首帧。

---

## 6. Actual-image authority｜HARD

HG03 通过后：

`ACCEPTED IMAGE PIXELS / K0 STATE > old prompt > old Director prose`。

动态阶段必须重新读取/观察实际通过的首帧，确认：
- 真实存在的人物；
- 真实存在的道具；
- 真实空间；
- 手的位置；
- 视线；
- 花/水/布/门/阶梯等关键对象状态。

不得在动态提示词里要求首帧不存在的关键道具或重新设计整个空间。

如果实际图片偏离原计划但用户已经接受：更新 Director state / prompt，而不是让视频模型“纠正图片”。

---

## 7. HG03 machine pre-review output

在给用户看整组前，至少记录：
- per-frame lyric role；
- beauty PASS/FAIL；
- shot scale / camera angle；
- primary visual event；
- dynamic entrance；
- set repetition risks；
- identity/world continuity risks；
- recommended KEEP / REGEN。

只有整组 machine QA PASS 后才提交：
`HG03 Visual Direction / First-frame Set Gate`。

用户仍负责最终审美权威；机器负责先拦住明显功能化、重复化、不可动态化的方案。
