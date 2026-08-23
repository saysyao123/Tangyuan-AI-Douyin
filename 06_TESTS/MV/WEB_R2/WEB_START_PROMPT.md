# WEB R2｜ZERO-CONTEXT START PROMPT v1.2

把下面整段直接发给新的 ChatGPT 网页端对话：

```text
你现在要执行本仓库的 WEB R2 AI MV 网页端自动化测试。

唯一写入分支：
test/mv-web-r2

开始前严格按优先级读取：
1. 04_HARNESS/workflows/mv.md
2. 04_HARNESS/rules/mv_golden_runtime.md
3. 04_HARNESS/rules/mv_audio_timeline.md
4. 06_TESTS/MV/WEB_R2/CURRENT_STATE.md
5. 06_TESTS/MV/WEB_R2/AUTOMATION_MATRIX.md
6. 06_TESTS/MV/WEB_R2/WEB_R2_MASTER_PLAN.md
7. 当前Stage需要时再JIT读取其他rules/templates/benchmark/Golden audit。

Authority hard rule：
- workflow + mv_golden_runtime + mv_audio_timeline 是运行时权威；
- Master Plan只是summary，不能覆盖前者；
- 不依赖聊天记忆复用R1，跨Round正确性经验必须在Runtime Rule/Gate中存在。

执行原则：
- 从 CURRENT_STATE 指定Stage继续；
- 能自己完成的搜索、分析、裁剪、QA、编辑都直接完成；
- 技术Gate必须有可验证evidence/provenance；
- 强证据缺失就BLOCKED，不得为了维持AUTO降低证据等级；
- BGM锁定后，下一强制交付必须是完整 `AUDIO_TIMELINE_PACKAGE`；没有 `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`，不得进入正式Natural Beat timing allocation、Director timing allocation、Picture Edit或Subtitle timing/render；
- 剪辑开始时只revalidate Audio Timeline Package与当前BGM SHA，不允许剪辑模块临时重新猜时间轴；
- 必须区分歌词时钟、音乐事件时钟、视觉动作时钟；字幕只服从歌词时钟；
- 必须区分 `ALIGNMENT_GROUND_TRUTH_QA` 与 `SUBTITLE_IMPLEMENTATION_QA`；
- 任何人物相关Seedance图生视频提示词第一行必须原样为：
*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。
- Seedance源音轨默认不是时间真源；最终锁定BGM是唯一音乐真源；
- 动态镜头不固定一镜到底或多镜，按歌词/导演任务决定；
- 每完成一个Stage更新 CURRENT_STATE / AUTOMATION_MATRIX；
- 交付ZIP前做包内清单与完整性测试。

R1是Golden quality/correctness floor，但不复刻R1歌曲、人物、纸墨世界或具体镜头。

现在按 CURRENT_STATE 继续执行，不重复已完成且仍有效的上游Stage。
```
