# MV Reference Director｜Core Song Selection Round 01

> Phase: B06 → C03
> Source: 9 个用户核心账号 + 历史 `works.csv` 89 条作品
> Rule: 所有核心账号歌曲均入池；账号角色只影响权重，不排除歌曲。

## 1. 本轮比较逻辑

综合看：

1. Core Account Repeat：跨核心账号重复是否明显；
2. Lyric / Visual Hit：歌词是否容易形成不可替代的动画视觉；
3. Animation Fit：是否适合当前原创动画人物 + 明亮治愈场景 + 奇幻物件/伙伴；
4. Motion Fit：是否能形成 5–15s 可读动态，而不是只有静态风景；
5. New-Test Value：尽量避免已经深度做过的旧项目歌曲作为首次完整 Skill 实测。

本轮不是“热度榜”，而是“最适合当前 MV Skill 第一次真实跑通”的候选。

---

# A｜Summer Love / 爱在盛夏｜综合推荐 #1

**Core evidence**：Aura + XIANGJISHI（2 个核心视觉/音乐账号）。

### Primary link｜XIANGJISHI
https://www.douyin.com/video/7673068083896814202

- captured duration: 17.467s
- caption: `与我坠入爱河吧 在这个盛夏`
- tags: 夏天 / 自由 / inmyfeeling

### Alternate link｜Aura
https://www.douyin.com/video/7673385877871136042

- captured duration: 16.734s
- caption: `与我坠入爱河吧 在这个盛夏`
- tags: 海 / 夏日 / inmyfeeling

### Why #1

- 明亮、夏日、海、心动，天然符合当前治愈动画定位；
- 两个视觉核心账号独立使用，同歌 × 场景适配信号可靠；
- 可以自然做 One Piece 式高辨识角色的轻动作/奔跑/转身/互动；
- 新海诚式天空、海面、光线、风非常容易命中；
- 17s 原 Reference 足够我们重新决定真正生成 5–15s 中哪一段，而不用照抄原时长；
- 不是之前重点制作过的旧 MV，适合第一次 Full Skill Test。

**Risk**：动作强度需要从 Reference 本身进一步确认；不能因为风景好看就退回纯静态氛围。

---

# B｜爱让人脑袋空空｜数据信号 #1 / 综合推荐 #2

**Core evidence**：乐♩青春 + Aura + Lynne小凌 + 火乐烁（≥4 个核心账号），是当前恢复窗里最强的跨核心账号重复之一。

### Primary link｜乐♩青春
https://www.douyin.com/video/7672476381650263962

- captured duration: 15.372s
- 文案：受过的伤记不住，才会一再奔赴同一份汹涌
- 账号本身兼具歌词 / 卡点 / 剪辑价值

### Alternate｜Aura
https://www.douyin.com/video/7673163298476526886

- captured duration: 15.534s
- 极端天气 / 画面氛围版本

### Alternate｜Lynne小凌
https://www.douyin.com/video/7673162974852688357

- captured duration: 16.277s
- 翻唱 / 表演版本

### Alternate｜火乐烁
https://www.douyin.com/video/7673830659274810033

- captured duration: 31.467s
- 电音版 / 音推版本

### Why #2

- 跨 4 个不同职责核心账号，证明它不仅是单账号审美偏好；
- 有歌词、场景、Cover、Remix 多种版本，可以很好测试 `SONG_FAMILY → AUDIO_VERSION LOCK` 机制；
- 人物表情和动作空间很大，非常适合高辨识动画角色；
- 动态测试价值高，能更快检验 Seedance 2.5 动作能力。

**Risk**：不同账号音频版本明显不同；必须等用户选具体视频后再锁 BGM。整体更俏皮/情绪化，治愈感没有 A 纯。

---

# C｜向山河林响｜动画冒险动态 #1 / 综合推荐 #3

**Core evidence**：火乐烁。

### Primary link｜火乐烁
https://www.douyin.com/video/7674993950716867770

- captured duration: 30.167s
- caption: `我要向山河出发 去拥抱辽阔的天下`

### Why #3

- “出发 / 山河 / 辽阔”具有非常明确的歌词视觉事件；
- 最容易融合高辨识冒险型动画人物 + 明亮天空 / 山川 / 风 / 云；
- 动作与镜头可以明显比纯治愈风景更丰富；
- 很适合测试 8–12s 或 10–15s 起势→推进→释放结构。

**Risk**：当前抓取窗只有一个核心账号信号，所以歌曲数据强度低于 A/B；但对当前目标风格的创作适配极高。

---

# Backup Pool

## 听见月亮的歌｜XIANGJISHI
https://www.douyin.com/video/7673110065674699941

`迷路的小船 终有一天会靠岸`。治愈奇幻非常强，适合加入吉卜力式原创小伙伴 / 物件，但动作可能偏轻。

## 阳光洒落｜XIANGJISHI
https://www.douyin.com/video/7673393101587707877

`阳光落在我的脸上 所有烦恼瞬间消散`。明亮治愈适配极高；适合轻动态，而不是高动作测试。

## 巴黎微光｜火乐烁
https://www.douyin.com/video/7673819402874644401

梦境城市 / 微光，适合新海诚式城市夜景，但角色动作和歌词事件需要进一步验证。

---

# Historical Regression Pool｜不作为首个全新项目优先

- `如果风会替我说话`：跨 ≥3 核心账号，但已经深度用于历史 MV 流程；适合后续 Regression。
- `我救自己于人间水火`：Aura + XIANGJISHI 双核心信号，视觉/治愈很强，但已经用于历史测试；适合回归对照。
- `我不难过`：Aura 直接作品，历史项目相关。

---

# Human Gate

用户实际打开 A / B / C。

- 若 A/B/C 有合适：选定**具体视频**，下载后发回；下一阶段锁该视频的 BGM / Lyrics / Beat / Segment / Duration。
- 若都不合适：继续 Round 02，只从完整 Core Song Pool 中再出 3 条，不退回平台随机榜单。
