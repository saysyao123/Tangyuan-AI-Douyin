# Dola Multi-Account 5s Clean Video Production Workbench 验收记录

日期：2026-08-30

## 结论摘要

本轮完成了 P2.1 Durable Capture、P3.1 Account Registry，以及可验收的单 Worker 健康感知轮询、Job sticky binding、任务恢复、账本和 5 秒文件级 QA Gate。

代码层与本地编排层通过；真实多账号 Dola 生成和“每个账号 5 秒能做几条”尚不能 PASS。当前 Codex 内置浏览器只暴露一个已登录页面，Full CDP 的 `Target.getBrowserContexts` 与 `Target.createBrowserContext` 均返回不支持，无法在一个 Browser Process 中创建独立账号 Context。

## 验收矩阵

```text
ACCOUNT_REGISTRY: PASS
SESSION_SLOT_UNIQUENESS: PASS
DURABLE_CAPTURE_SINK: PASS
ROUND_ROBIN_SIMULATION: PASS
HEALTH_AWARE_SKIP: PASS
STICKY_BINDING: PASS
JOB_RESUME: PASS
5S_DURATION_GATE: PASS
MINIMUM_RESOLUTION_GATE: PASS
SIGNED_DATA_REDACTION: PASS
FULL_CDP_AVAILABLE: PASS
FULL_CDP_BROWSER_CONTEXT: NOT_AVAILABLE
REAL_MULTI_ACCOUNT_DOLA_SESSIONS: NOT_RUN
REAL_ROUND_ROBIN_GENERATION: NOT_RUN
PER_ACCOUNT_5S_CAPACITY: UNKNOWN
DOLA_2_5_5S_OPTION_VISIBLE: PASS
DOLA_CURRENT_ACCOUNT_QUOTA_VISIBLE: NO
```

## 已实现文件

- `app/production/account_registry.py`：`runtime/accounts/accounts.json`，账号只含非敏感标识、状态、Slot 和统计字段。
- `app/production/models.py`：Account/Job 模型、状态转移和 sticky binding。
- `app/production/scheduler.py`：只从 READY 账号中轮询；NEEDS_LOGIN、ERROR、COOLDOWN 不会被硬分配。
- `app/production/ledger.py`：事件立即 `flush + fsync`；总账本只保存脱敏 URL 和字段存在性，不保存签名串、key_seed 值或 Cookie。
- `app/production/job_store.py`、`queue.py`：Job 持久化、Prompt Hash、恢复入口和 JSONL 队列。
- `app/qa/production_gate.py`：4.0–6.5 秒、最低 1280×720、人工无水印确认门禁。
- `app/production/capacity.py`：只报告观察到的本地/服务端字段；服务端未验证时 `capacity_known=false`、`max_jobs=null`。

## 本地轮询证据

三槽位模拟：

```text
A01 READY       → Job001
A02 NEEDS_LOGIN → skipped
A03 READY       → Job002
A01 READY       → Job003
A03 READY       → Job004
A01 READY       → Job005
```

测试覆盖了 `A01 → A02 → A03 → A01`、跳过未就绪账号、Job 绑定后拒绝换号、空 READY 池 fail-closed，以及事件即时落盘。

## 当前真实会话证据

只读打开 Dola 首页后，页面显示账号按钮 `BASELINE_ACCOUNT`，Full CDP capability 可取得，说明当前内置浏览器有一个可用登录页面。

进入 Dola「AI 创作 → 视频 → 模型 2.5」后，5s 选项可见并已设置在测试表单中；页面没有显示可直接审计的剩余生成次数。测试提示词已经填入，但没有点击提交。

随后探测：

```text
Target.getBrowserContexts     → Error: This method is not supported through raw CDP
Target.createBrowserContext   → Error: This method is not supported through raw CDP
```

因此当前不能证明：

```text
A01 / S01 → 独立 Dola 登录态
A02 / S02 → 独立 Dola 登录态
A03 / S03 → 独立 Dola 登录态
```

三个账号需要分别人工登录到可用的独立浏览器会话，或未来 Full CDP 开放 BrowserContext 后再做实机轮询验收。普通多 Tab 不等于 Session 隔离，本报告不把它算作 PASS。

## 5 秒与容量结论

此前生成证据中有一条文件级时长约 10.08 秒；按照本轮门禁，它不能算 5 秒素材 PASS。后续每条视频必须以下载文件 FFprobe 为准：4.0–6.5 秒才进入 QA，其余记录 `FAIL_DURATION`。

“每个账号 2.5 视频 5 秒可以做几个”不能从本地 `local_remaining` 推导。当前 Doubao Harness 只读状态显示 `account-04` READY、`local_remaining=10`，并且 5 秒/10 jobs preflight 通过，但 provider quota 仍是 `unverified`；`default` preflight 被 account_not_ready 与 quota_error 拦截，`account-02/03` 被 account_not_ready 拦截。这些只是另一套 Doubao Harness 的观测，不是 Dola 多账号登录证明，也不是可承诺的 Dola 服务端生成次数。正式容量测试必须在每个目标账号会话可用后，逐条记录服务端实际成功/失败、每条成本、5 秒 FFprobe 和 clean 下载 QA；遇到 quota/rate-limit/account restriction 必须停止并记录，不能自动换号规避限制。

## 运行检查

```text
.venv\Scripts\python.exe -m pytest
44 passed

.venv\Scripts\python.exe -m compileall -q app tests
PASS
```

真实生成尚未在本轮提交，因为当前只有一个可见 Dola 登录会话，且生成提交是用户确认的外部动作。下一步需要先把至少两个独立 Dola Session Slot 人工登录并显式标记 READY，再逐条执行 5 秒测试。
