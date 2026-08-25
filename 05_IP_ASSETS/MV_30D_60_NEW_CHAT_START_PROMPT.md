# 汤圆音乐映像｜30D/60 下一首 MV 新对话启动词 v1

> 用途：每一首新 MV 单独开新 ChatGPT 对话。新对话从 GitHub 读取正式 Runtime / Account OS / Knowledge，不继承上一首歌的具体创意残留，也不要求用户重讲 R1/R2/R3。

```text
请使用已连接的 GitHub，读取 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-web-r3` 分支。

这是「汤圆音乐映像｜30天60条音乐MV」的新一首独立生产实例。
不要让我重新解释 R1 / R2 / R3，也不要把上一首《如果风会替我说话》的具体人物、雨夜、面纱、冰块、镜头构图或视觉主题自动继承到这一首。

开始前按以下权威顺序读取：

A. 账号与30D/60生产系统
1. `05_IP_ASSETS/ACCOUNT_POSITIONING.md`
2. `05_IP_ASSETS/PUBLISH_SYSTEM.md`
3. `05_IP_ASSETS/MV_30D_60_OPERATING_SYSTEM.md`
4. `05_IP_ASSETS/MV_30D_60_TRACKER.csv`

B. MV正式生产 Runtime
5. `04_HARNESS/workflows/mv.md`
6. `04_HARNESS/rules/mv_golden_runtime.md`
7. `04_HARNESS/rules/mv_bgm_discovery.md`
8. `04_HARNESS/rules/mv_audio_timeline.md`
9. 当前 Stage 需要时 JIT 读取：
   - `04_HARNESS/rules/mv_human_gates.md`
   - `04_HARNESS/rules/mv_editing.md`
   - `04_HARNESS/rules/mv_source_normalization.md`
   - `04_HARNESS/rules/mv_web_source_roughcut.md`
   - `04_HARNESS/rules/mv_subtitle.md`
   - `04_HARNESS/rules/ai_video.md`

C. R3 中已验证但仍属 Knowledge / Candidate 的经验，仅在相关 Stage JIT 读取，不要当成当前歌曲的固定创意模板：
10. `04_HARNESS/knowledge/MV_DYNAMIC_GENERATION_R3_LESSONS.md`
11. `04_HARNESS/knowledge/MV_CAMERA_LIBRARY_CANDIDATES.md`

执行原则：
- 账号前台身份固定为「汤圆音乐映像」；普通 MV 的账号包装、标题、封面、默认标签不主动强调 AI；
- 后台仍完整使用 AI 生产系统；
- 当前30天目标约60条 / 平均2条每天；
- 内容分为 P Primary/Trend、S Stable/Fast、R Camera/Director R&D 三类；
- 不允许每一条都复制 R3 的高研发成本；稳定生产优先复用已验证 correctness；R&D 镜头实验只放入 Lane R 或明确指定的单变量测试；
- 正常固定人工 Gate 仍只有 5 个：HG01选歌、HG02 BGM试听、HG03首帧整组、HG04粗剪节奏、HG05最终验收；但在30D/60体系中优先采用批量 Gate；
- BGM 默认 Douyin-native exact asset first；
- BGM 锁定后必须先完成 AUDIO_TIMELINE_PACKAGE，再进入任何依赖时间的导演工作；
- 每句歌词先找“不可替代视觉答案”；歌词视觉命中 > 轻叙事连续 > 炫技镜头；
- 环境必须参与叙事，避免整组都退化为人物近景写真；
- 动态素材是 RAW SOURCE，不等于最终5秒成片；TRIM BEFORE REGENERATE；
- WEB正式 Picture Edit 前必须通过 Source Rough-Cut Gate，继承 R2 已验证统一水印安全裁切基线；
- 字幕直接继承已锁 R2 baseline，除非用户明确要求重新设计；
- 局部问题 Patch, Don't Cascade；
- 上一首歌的成功构图、角色、色调、道具不得自动复用；只复用规则、QA、Camera候选语法和生产经验。

如果用户没有指定下一首歌：
- 从当前 Music Radar / Data Center / Song Queue 开始；
- 给出第一批适合未来30D/60节奏的候选歌曲；
- 优先做 HG01 Song Aesthetic，不要直接跳到首帧。

如果用户已经指定歌曲：
- 为该歌曲建立新的独立 MV slot / project state；
- 从 HG01 / exact Douyin evidence 开始，不要直接继承上一首的 BGM 或视觉。

每完成一个 Stage：
- 生成 durable artifact / receipt；
- 更新该新 MV 的独立 CURRENT_STATE / tracker slot；
- Gate PASS 后再前进。

上一首《如果风会替我说话》已经单独进入 R3-D2 发布数据观察，不要在本对话重新打开其制作流程。

现在先读取上述文件，告诉我：
1. 当前30D/60系统状态；
2. 本次新MV应该占用哪个 slot / lane；
3. 当前第一个人工 Gate 是什么；
然后立即开始该 Gate，不要让我重复项目背景。
```
