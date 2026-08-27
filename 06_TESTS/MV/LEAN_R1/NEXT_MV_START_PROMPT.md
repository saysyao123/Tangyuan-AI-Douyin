# D03-A｜Lean R1 新 MV 启动词 v1

> 用途：下一首全新 MV 单独开新对话时，直接把下面代码块完整发给 ChatGPT。

```text
请使用已连接的 GitHub，进入仓库 `saysyao123/Tangyuan-AI-Douyin` 的 `test/mv-lean-r1` 分支。

这是「汤圆音乐映像｜30天60条」Lean Runtime R1 的第一首真实效率测试 MV。
测试合同：`06_TESTS/MV/LEAN_R1/LEAN_R1_TEST_CONTRACT.md`
目标 slot：`D03-A / Lane P`。

这是全新独立 MV：不要继承 D02-B《有几次想你了》的具体人物、海边建筑、浅色石材、白衣、纱帘、雨后世界、道具、构图或“握住→松手→世界打开”的视觉进程。只允许复用已经进入 Rule / Workflow / Knowledge 的通用能力。

【Lean 启动原则】
不要像旧 Runtime 那样一开始读取一大堆 R1/R2/R3 历史文件。
第一步只做：
1. 读取 `06_TESTS/MV/LEAN_R1/LEAN_R1_TEST_CONTRACT.md`；
2. 在 `04_HARNESS/lean_runtime_bridge/requests/` 创建一个针对 `D03-A` 的全新 immutable `RESUME` request；
3. 读取 matching response。

Lean response 应直接提供：
- Runtime mode / slot / lane / current stage；
- next_action；
- resolved_executor.executor_id；
- resolved_executor.execution_class；
- JIT reads；
- fresh next_guard。

只有 response 明确为 `ALLOCATE_NEW_SLOT / D03-A / Lane P` 时才允许初始化；如果返回 Canonical、Migration、stale、BLOCK 或其他冲突，按仓库真值解决，不得从聊天记忆绕过。

【初始化后】
使用 fresh allocation guard 完成 `INIT_SLOT`，然后只执行 HG01 所需 machine preflight。
HG01 默认仍采用 Core Benchmark Data Center 主驱动，不做全网漫游式选歌。
直接给我少量最值得听的歌曲候选 + 对应核心/补充 Benchmark 博主的实际 MV 直链，让我只做歌曲审美选择。

【Lean Runtime｜核心测试】
正常生产仍保留 5 个 Human Gates：
HG01 选歌；HG02 BGM；HG03 首帧整组；HG04 Picture Edit；HG05 Final。

但这五个 Gate 之间不应再让我看到大量纯机器 Stage 往返。
优先使用 Lean Bridge：
- `ACCEPT_GATE`：一次外部请求完成 durable gate receipt + canonical advance；
- `RUN_UNTIL_GATE_OR_BLOCK`：在机器 artifacts 已经准备好时，连续执行已有 canonical transition，直到下一 Human Gate、外部动态生成 handoff、真实 BLOCK 或 S16。

重要：宏命令只压缩 transport，不得伪造 artifact；缺 prerequisite 就 BLOCK。

【Executor First】
Runtime 告诉 WHAT，resolved executor 告诉 HOW，Rule 只定义约束。
进入每个 macro phase 后只读取 response 返回的 JIT 文件。
禁止：
- 因 Rule 提到某实现就新建工具；
- 每首歌重新安装生产模型；
- 为 D03-A 创建 slot-specific core helper；
- 为“保险”再建第二歌词时间轴；
- 新增图片/视频 backend；
- 把 D02-B 的 experiment logs 当模板复制。

【Audio Timeline】
HG02 后固定优先级：
P0 same-version timed lyric/LRC -> P1 lightweight ASR mapping -> P2 heavy forced alignment only on concrete failure。
第一条 PASS 就停止，不做多模型互证。

【Director】
JIT 使用 `04_HARNESS/knowledge/MV_DIRECTOR_LEAN_OVERLAY.md`。
保留：Director Thesis、Primary Visual Engine、视听关系、motive-first camera/subject/space、WHY CUT HERE、optional stop condition、Creative Drift QA。
它们是能力增强，不新增文字版 Director 人工 Gate。

【Dynamic / Edit】
Dynamic 仍是 RAW SOURCE，不等于成片；TRIM BEFORE REGENERATE。
Normalization 改成按需：只有多镜 atomization、WEB 清理或 proxy 真正需要时才跑完整流程。
Editor Audio Gate 只做 locked BGM identity invariant，不重做 lyric clock。
Edit Map 做好后直接渲染 Picture Preview，停在 HG04。

【Finish】
HG04 PASS 后，字幕 + Final Tech QA 应自动串行，只有真实技术 BLOCK 才打断；正常直接给 Final 候选进入 HG05。
HG05 PASS 后自动做 Release Package 到 S16。
未真实发布前禁止进入 S17、禁止写 PUBLISHED、禁止伪造发布时间。

【效率记录】
从第一条 RESUME 开始记录：
- startup calls；
- Lean Runtime 外部命令次数；
- Human Gate 次数；
- macro 压缩的 machine transitions；
- 不必要的 RESUME 是否出现；
- normalization 是否触发及原因；
- regen 次数；
- 是否创建了新 helper/model route。

目标：5 个 Human Gate不变；到 S16 的外部 controller cycles <=12；质量不低于当前已验收标准。

完成第一轮 RESUME 后，先简洁告诉我：branch/source SHA、request_id、mode、slot/lane、current stage、resolved executor、next action、当前第一个 Human Gate/唯一阻塞。若可分配，立即 INIT 并进入 HG01，不要让我重新解释项目。
```
