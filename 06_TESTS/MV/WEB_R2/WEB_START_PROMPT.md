# WEB R2｜ZERO-CONTEXT START PROMPT v1.1

把下面整段直接发给新的 ChatGPT 网页端对话：

```text
你现在要执行本仓库的 WEB R2 AI MV 网页端自动化测试。

请使用 GitHub 分支：
test/mv-web-r2
作为本轮唯一写入分支。

开始前严格按这个优先级读取：
1. 04_HARNESS/workflows/mv.md
2. 04_HARNESS/rules/mv_golden_runtime.md
3. 06_TESTS/MV/WEB_R2/CURRENT_STATE.md
4. 06_TESTS/MV/WEB_R2/AUTOMATION_MATRIX.md
5. 06_TESTS/MV/WEB_R2/WEB_R2_MASTER_PLAN.md
6. 当前 Stage 需要时，再 JIT 读取对应 rules / benchmark / Golden R1 audit 文件。

Authority hard rule：
- `workflows/mv.md` + `rules/mv_golden_runtime.md` 是运行时权威真源；
- WEB_R2_MASTER_PLAN 只是 Round summary，不能覆盖或弱化前两者；
- 若发现 Master Plan / State 与权威 Workflow/Rule 冲突，先修正文档冲突，再执行任务；
- 不要让我重新解释 R1；跨 Round 必须继承的经验应已存在 Golden Runtime，不应靠聊天记忆。

执行原则：
- 从 CURRENT_STATE 指定 Stage 开始；
- 能自己完成的搜索、读取、分析、生成、裁剪、QA、编辑都直接完成；
- 只有审美选择、外部登录/验证码、外部 Seedance 生成、确实缺失的原始文件才请求我操作；
- 每个技术 Gate 必须有真实可验证的 evidence/provenance，不能只靠一个名为 locked/exact 的文件或状态文字；
- 如果强证据缺失，状态必须 `BLOCKED`，不得为了维持 AUTO 而降低证据等级；
- 任何人物相关 Seedance 图生视频提示词第一行必须原样为：
*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。
- Seedance 原始音轨默认不是时间真源，最终BGM以锁定母版为唯一真源；
- 动态镜头不固定一镜到底或多镜，按歌词/导演任务决定；
- 精确歌词时间轴在任何 picture edit 前必须完成独立证据对齐：ASR/forced alignment、同版本可靠LRC或官方timed lyric；波形/BPM/onset只能交叉验证；
- 必须区分 `ALIGNMENT_GROUND_TRUTH_QA` 与 `SUBTITLE_IMPLEMENTATION_QA`，不得用字幕是否按SRT显示来证明SRT本身正确；
- 每完成一个Stage，更新 `AUTOMATION_MATRIX.md` 和 `CURRENT_STATE.md`；
- 每轮交付优先 ZIP，并做包内清单与完整性测试。

R1 是 Golden quality/correctness floor，但不要复刻 R1 的歌曲、人物、纸墨世界或具体镜头。

现在按 CURRENT_STATE 继续执行，不重复已完成且仍有效的上游 Stage。
```
