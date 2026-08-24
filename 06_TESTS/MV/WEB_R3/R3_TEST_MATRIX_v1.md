# WEB R3｜TEST MATRIX v1

> Rule: 每个 micro-round 只验证一个主问题；PASS 才继续。任何一轮都允许停下来复盘，不提前执行后续轮。

| Micro-round | 唯一核心问题 | 本轮产物 | Human Gate | PASS 后 |
|---|---|---|---|---|
| **R3-A1 Account Registry** | 我们监测谁才有意义？ | benchmark registry + account role/weight | 无 | A2 |
| **R3-A2 7-Day Music Radar** | 哪些歌跨账号重复且正在起势？ | raw 7d observations + normalized SONG_FAMILY/AUDIO_VERSION + repeat/recency metrics | 无 | A3 |
| **R3-A3 Shortlist Validation** | Radar 能否给出真正值得做的3–5首，而不是单账号主观推荐？ | EARLY_RISE / CONFIRMED / OVERHEATED shortlist | **HG01** | 锁1首歌 |
| **R3-B0 BGM + Timeline Lock** | 选中的歌能否锁定舒服且完整的音频段？ | BGM + Audio Timeline Package | **HG02** | B1 |
| **R3-B1 Static Healing Visual** | 我们能否明显提高治愈感/画质，而不先承担动态风险？ | 3个代表Beat的首帧小样 | **Visual Mini Gate 1** | B2 |
| **R3-B2 Dynamic Healing Visual** | B1视觉在5s动态中还能保住质感与稳定性吗？ | 2–3条代表动态 + Atom/Arc QA | **Visual Mini Gate 2** | C |
| **R3-C Full MV Integration** | 新选歌+新视觉能否一次跑进R2生产链？ | 完整MV | R2固定HG03/HG04/HG05 | D |
| **R3-D1 Packaging Benchmark** | 哪种标题/简介/标签表达与音推定位最匹配？ | MUSIC_FIRST / EMOTION_FIRST packaging candidates | 无/发布前一次选择 | D2 |
| **R3-D2 Live Data Feedback** | 发布后哪些包装/歌/视觉信号值得保留？ | post data review + promotion decision | 数据复盘 | R3 close |

## Variable isolation

### A-series
只测试：Music Intelligence。
禁止测试新视觉。

### B-series
只测试：Healing Visual。
歌曲/BGM/Timeline 已锁；剪辑/字幕使用 R2 baseline。

### C
只测试 integration，禁止同时发明新字幕、新剪辑语法、新时间轴方案。

### D-series
只测试 Publish Packaging / data loop，不因为一条数据不好回头重写 R2 production runtime。

## Temporary R3-only extra human gates

R3-B1/B2 的两个 Mini Gate 是研发期临时 Gate。
一旦 Healing Visual System 被验证并晋升，未来正式日常生产取消这两个额外 Gate，恢复正常 5-Human-Gate 模型。

## Stop rule

任何 micro-round FAIL：
- 保留证据；
- 只修改当前变量；
- 不自动进入下一轮；
- 不重开 R2 frozen baseline。
