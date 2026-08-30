# 自研消费者网关 Session Host 接入

## 结论

之前的多账号登录器位于：

```text
D:\豆包Seedance本地生成方案\consumer_gateway
```

它已经保存并管理独立账号会话，并通过本机 `127.0.0.1:19090` 提供管理 API。当前项目不重新登录、不复制 Cookie/Profile/SQLite，而是把它当作 Session Host：

```text
自研登录器账号会话
        ↓ 本机管理 API
当前项目 Account Registry
        ↓ A01/A02/A03 sticky binding
任务调度与 QA
```

## 已验证事实

在 2026-08-30 的本机检查中，旧网关 `/health` 返回正常，账号管理 API 可访问；逐个调用账号 status 接口时，当前登记的账号均返回 `logged_in=true`。旧网关默认 `max_hot_accounts=1`，因此只有一个账号会保持热浏览器，其他账号显示 `stopped` 并不代表已退出登录。

当前项目已完成一次公开状态同步，映射写入：

```text
runtime\accounts\accounts.json
```

字段为：

```text
session_host = consumer_gateway
host_account_id = 旧网关账号 ID
```

## 命令

```powershell
cd LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver
.venv\Scripts\python.exe -m app.cli consumer-gateway health
.venv\Scripts\python.exe -m app.cli consumer-gateway accounts --sync
.venv\Scripts\python.exe -m app.cli accounts --json
.venv\Scripts\python.exe -m app.cli consumer-gateway status A01
.venv\Scripts\python.exe -m app.cli consumer-gateway start A01
.venv\Scripts\python.exe -m app.cli consumer-gateway probe A01
```

`status` 会用旧网关自身的登录检查确认会话；返回 `logged_in=true` 后会把当前槽位设为 `READY`。`start` 会让旧网关按自己的账号 Profile 启动该账号，仍由旧网关负责生命周期。`probe` 是真实聊天请求验证，不等于视频生成额度验证。

## 与 Dola 的边界

旧网关的站点和生成链是豆包 `doubao.com`，不是 `dola.com`。因此：

- 它可以直接复用到我们之前的 Seedance 2.5 豆包生成、任务、AISpace 干净下载和 QA 链。
- 它不能把豆包登录态当成 Dola 登录态，也不能直接恢复 Dola 历史会话。
- 当前项目保留的 Dola 捕获/解析模块仍只服务 Dola 自己的用户会话。

这是平台边界，不是账号映射失败。

## 安全与验收

- 只读同步公开账号 ID、名称和运行状态。
- 不读取、输出或迁移 Cookie、密码、验证码、OAuth、Token、SQLite 或 Profile 文件。
- 不自动创建账号、不绕过登录/验证码/额度/地区限制。
- `logged_in=true` 只是会话验证通过；要宣布视频成功，还必须有真实任务、实际 MP4、FFprobe、哈希/完整性和首中尾帧水印 QA。
- 多账号轮询只能在用户拥有的账号和平台允许的任务范围内执行；本地日额度账本不能替代服务端额度事实。
