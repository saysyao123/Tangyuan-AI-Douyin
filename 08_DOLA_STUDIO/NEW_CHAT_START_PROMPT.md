# NEW_CHAT_START_PROMPT｜Tangyuan Dola Studio

将下面整段复制到新的 ChatGPT / Codex 会话中使用。

---

请使用已连接的 GitHub，读取仓库：

`saysyao123/Tangyuan-AI-Douyin`

分支：

`project/dola-studio-v1`

这是「Tangyuan Dola Studio」长期项目的新会话继续执行。

首先严格按顺序读取：

1. `08_DOLA_STUDIO/PROJECT_CHARTER.md`
2. `08_DOLA_STUDIO/DECISION_LOG.md`
3. `08_DOLA_STUDIO/ROADMAP_AND_GATES.md`
4. `08_DOLA_STUDIO/CURRENT_STATUS.md`
5. `08_DOLA_STUDIO/ARCHITECTURE.md`
6. `08_DOLA_STUDIO/REFERENCE_SOFTWARE_MAP.md`
7. 当前阶段对应的 Implementation Guide（P1 时读取 `P1_IMPLEMENTATION_GUIDE.md`）

读取后不要让我重新解释历史。

## 原始目标

参考已分析的「豆啦啦无印浏览器」产品结构和工作流，采用 clean-room 方式建立我们自己的 Dola / Seedance 视频创作工作台。

长期核心目标必须保持：

```text
多个自有 Dola 账号独立 Session
→ 稳定正常登录
→ Dola / Seedance 能力识别
→ Seedance 2.5 30 秒真实能力验证
→ 正常生成
→ 原始/官方下载源优先
→ 媒体规格检测
→ Resource Library
→ Storyboard / MV Pipeline
```

## 绝对不要跑偏

1. 不要把项目降级成只有一个普通 WebView2 浏览器。
2. 不要因为 30 秒当前测试失败，就把 30 秒目标从项目中删除；应记录真实状态并继续保留后续验证路径。
3. 不要把“页面显示 30s”当成 `30S_PASS`；必须用真实生成文件验证。
4. 不要把“界面完成”当成核心功能完成。
5. 不要跳过当前 Gate 去堆后续功能。
6. 不要因为原软件某个功能暂不实现，就从 `REFERENCE_SOFTWARE_MAP.md` 删除；先研究，后做减法。
7. 不允许 CURRENT_STATUS 自行覆盖 PROJECT_CHARTER 和已锁定 Decision。

## 当前边界

多账号用于用户本人合法持有账号的 Session 管理。

原参考软件中的以下能力继续保留研究价值，但不要实现成平台限制规避工具：
- Fingerprint spoofing；
- MachineGuid modification；
- Cookie 搬运用于绕过身份验证；
- 多账号额度轮换；
- 强制 request patch 解锁未授权 30 秒；
- 破解或擦除平台水印。

对于 30 秒，采用：

```text
MODEL_SUPPORTED
→ PLATFORM_EXPOSED
→ ACCOUNT_ALLOWED
→ SERVER_VERIFIED
```

对于无水印，优先验证平台本身正常返回的 `CLEAN_SOURCE`。

## 执行规则

1. 读取 `CURRENT_STATUS.md` 后，先明确当前阶段和当前第一 Gate。
2. 若当前阶段信息足够，直接继续执行，不要重复问已经在文档里的决定。
3. 每次只解决当前 Gate 所需问题；出现失败时先定位层级：

```text
SESSION / BROWSER / PAGE / CAPABILITY / TASK / DOWNLOAD / MEDIA_QA
```

4. 一次失败后优先单变量修正，不要整体推翻。
5. 只有实测通过才能把 Gate 写为 PASS。
6. 每轮结束更新 `CURRENT_STATUS.md`；重要、长期有效的新决定才写入 `DECISION_LOG.md`。
7. 如果新要求与现有锁定规则冲突，先明确指出冲突，再决定是局部修正、增加约束、替换旧规则还是升级项目目标。

## 当前阶段执行

以 `CURRENT_STATUS.md` 为准。

如果仍为 P0，则先复核文档完整性并完成 `P0_DOC_LOCK`。

如果 P0 已 PASS，则严格按 `P1_IMPLEMENTATION_GUIDE.md` 开始：

```text
Solution
→ Profile Model
→ ProfileStore
→ BrowserInstanceManager
→ WebView2 BrowserHost
→ AccountListPanel
→ A/B 人工正常登录
→ Restart persistence
→ 20-switch isolation test
→ destructive isolation test
→ P1 report
```

只有通过 `SESSION_AB_PASS` 才进入 P2。

---

开始执行时先用简短内容确认：
- 原始目标；
- 当前阶段；
- 当前第一 Gate；
- 本轮实际交付；
- 当前假设。

然后直接开始，不要让我重新解释本项目历史。
