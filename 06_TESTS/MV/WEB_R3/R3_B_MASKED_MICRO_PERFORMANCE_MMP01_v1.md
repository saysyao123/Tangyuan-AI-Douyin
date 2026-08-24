# WEB R3｜Masked Micro-Performance Layer MMP-01 v1

Status: `R3-B TEST LAYER / READY`
Song: `如果风会替我说话`
Upstream: `R3_B_VISUAL_DIRECTION_LOCK_v1.md`

## 1. Purpose

验证在“下半脸始终被面纱完整覆盖”的人物约束下，能否通过微表演提升真实感、辨识度与情绪可信度，降低 generic AI beauty 感。

核心不是夸张表情，而是：

`eye movement -> eyelid -> brow tension -> breath/veil physics -> hand interaction -> residual release`

各动作之间默认保留约 `0.1–0.3s` 的自然错峰，不同时启动全部动作。

## 2. Hard continuity

- 同一位虚构年轻成年东方女性；
- 不复刻任何真实明星身份/骨相；
- 仅继承已锁眼区设计原则：修长东方杏眼、干净上眼睑结构、自然外眼角延伸、明确眉眼深度、湿润 catchlight；
- 烟炭黑半透明面纱始终完整覆盖鼻口及下半脸；
- 不使用暴露嘴唇/嘴角/下巴的表演语法；
- 头部默认低运动，眼球先于头部；
- 不连续眨眼、不频繁扫视、不卡通式“瞪眼+皱眉+撅嘴”；
- 无台词，仅轻微自然呼吸；
- 面纱必须有真实布料受力、贴合、回弹、透光，不是平面贴图。

## 3. State library

### M0｜Neutral Hold
- 头部稳定；
- 双眼自然睁开；
- 视线稳定；
- 眉间放松；
- 面纱自然垂落，仅有呼吸级微动。

用途：动作起点 / 结尾 residual baseline。

### M1｜Eye-first Shift
- 眼球先向目标方向移动；
- 头保持原角度；
- 视线停住，不来回扫；
- 眉毛基本不动。

用途：牵挂 / 回忆 / 察觉 / 偷看远处。

### M2｜Slow Blink Reset
- 一次自然偏慢眨眼；
- 上眼睑先落再开；
- 睁眼后视线重新稳定；
- 禁止连续眨眼。

用途：状态切换、内心转折。

### M3｜Contained Ache
动作顺序：
1. 内眉轻提；
2. 眉心轻微向中央收；
3. 下眼睑轻度绷紧；
4. 视线仍保持稳定。

效果：委屈/压住/未说出口，但不哭、不深皱眉。

### M4｜Veil Contact
- 一只手从画面边缘自然进入；
- 先接触面纱，再经布料轻触脸侧；
- 接触后有短暂停顿；
- 眼神不追手。

用途：将面纱升级成表演介质。

### M5｜Veil Tension Peak
- 手指通过面纱轻压/轻牵脸侧；
- 布料局部拉紧、产生真实折皱与贴合；
- 脸侧轮廓只发生轻微受力变化；
- 人物主动表情幅度保持小；
- 主要高潮来自真实物理受力。

用途：唯一明显物理表演峰值。

### M6｜Elastic Release
- 手逐步减力；
- 面纱与脸侧轮廓自然回弹；
- 眉眼张力逐渐减弱；
- 保留约 0.2s 情绪残留，不瞬间中性。

### M7｜Close / Reopen / Look Beyond
- 一次短暂闭眼；
- 睁眼后视线转向斜上或远处；
- 头仍基本不动；
- 眉心放松；
- 面纱保持轻微余动。

用途：释然 / release / ending。

## 4. Assignment in this MV

| Segment | Lyric | MMP use | Purpose |
|---|---|---|---|
| S01 | 如果风会替我说话 | `M0 -> M1` | HOOK 中让“风先动、眼后回应” |
| S02 | 如果雨会替我回答 | `M1 + optional M2` | 让真实眼睛与雨中倒影形成回应 |
| S03 | 如果我还会想起他 | `M1 -> M2` | 只用视线确认缺席，不出现第二真人 |
| S04 | 如果还能一起回家 | light M1 only | 主任务由空间/门槛承担，不抢戏 |
| S05 | 如果梦能模糊真假 | M0 / reflection-driven | 主任务由真假重影承担，表情克制 |
| S06 | 如果痛能随之融化 | `M3 -> M4 -> M5 -> M6` | 本轮核心微表演压力测试 |
| S07 | 如果我们还是傻瓜 | M0 + softened gaze | 温柔而不笑，避免俗套情侣表演 |
| S08 | 如果爱不只是童话 | `M6 -> M7` | 从残余张力到稳定远望，完成 release |

## 5. Test hypothesis

`MMP01_HYPOTHESIS`:
在面纱完整遮挡下，微表演如果以眼球/眼睑/眉区的错峰变化与真实面纱物理受力为主，可以明显降低 AI 模板脸感，同时保持角色稳定与治愈气质。

## 6. Pass / fail criteria

### PASS
- 眼神变化自然，不像关键帧硬切；
- 头部稳定，眼球先动成立；
- 眉眼张力细微但可读；
- 面纱受力符合布料物理；
- 不露下半脸；
- 人物 identity 不漂移；
- 表演增强情绪而不是抢歌词；
- 生成后仍有 clean in/out 可供剪辑。

### FAIL / regenerate
- 眼神跳变/抽搐；
- 眉眼同时夸张启动；
- 面纱穿脸/消失/透明到露出口鼻；
- 手部拓扑错误；
- 手一出现即造成换脸；
- 面纱被牵动但脸部没有对应真实受力；
- 角色变成商业美容广告式表演；
- 微表演让画面失去治愈与克制。

## 7. Promotion policy

MMP-01 当前只属于 R3-B 测试层。
只有经过：
`first-frame suitability -> dynamic sample -> user review -> repeatable success`
后，才考虑晋升到 `04_HARNESS/rules/ai_video.md` 或独立人物表演规则。
