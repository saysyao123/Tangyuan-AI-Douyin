# Dola Desktop → Resolver 后台接入

日期：2026-08-30

## 结论

已把 Dola 自研桌面登录器作为本地会话宿主接入 Resolver。后台通过
`%LOCALAPPDATA%\SeedanceDesktopStudio\control.json` 发现 loopback 控制端点，使用其短期
本地控制令牌调用账号列表和激活接口。

不迁移、不读取、不落盘以下数据：

- Google/Dola 密码
- Cookie、access token、refresh token
- TOTP、验证码、Passkey
- Chromium Profile 数据库

## 当前实际映射

| 后台账户 | Slot | 宿主 | Dola Desktop 账号 |
| --- | --- | --- | --- |
| D01 | DS01 | `dola_desktop_studio` | Dola A |
| D02 | DS02 | `dola_desktop_studio` | Dola B |
| D03 | DS03 | `dola_desktop_studio` | Dola C（历史第三账号新槽位） |

宿主返回的 UUID 只作为本机绑定键保存到 `runtime/accounts/dola_accounts.json`，不作为登录
凭据使用。

## 验收

```text
DOLA_DESKTOP_HEALTH: PASS
DOLA_DESKTOP_ACCOUNT_DISCOVERY: PASS (Dola A, Dola B, Dola C)
BACKEND_REGISTRY_SYNC: PASS (D01, D02, D03)
ACCOUNT_ACTIVATE_D01: PASS
ACCOUNT_ACTIVATE_D02: PASS
ACCOUNT_ACTIVATE_D03: AVAILABLE_AFTER_LOGIN
COMPUTER_USE_REQUIRED_FOR_ABOVE: NO
AUTHENTICATION_STATUS: BOOLEAN_ENDPOINT_AVAILABLE (live result may be unknown)
DOLA_GENERATION_SUBMISSION: BLOCKED_BY_D2_GATE
```

在用户明确确认两个 Dola 槽位均已登录后，后台记录为：

```text
D01 / Dola A / DS01: READY / user_confirmed
D02 / Dola B / DS02: READY / user_confirmed
D03 / Dola C / DS03: NEEDS_LOGIN / new_isolated_slot
```

随后对 D01、D02 各执行一次后台激活，均返回 `200`，且宿主返回的 partition 与绑定关系
一致。再次执行 `accounts --check-session --sync` 时，探测结果虽为 `unknown`，但不会覆盖
用户确认的 READY 状态。

`NEEDS_LOGIN` 是故意的 fail-closed 状态：当前登录器的 `/v1/accounts` 只返回账号元数据，
没有返回真实页面登录状态。不能把 partition 存在误判为已登录。之后可以在登录器中增加
只返回布尔值的 session health endpoint，再由后台把已验证账号置为 `READY`。

若账号所有者已确认登录成功，可运行 `dola-desktop confirm-login D01/D02`。后台会将
`readiness_basis` 标成 `user_confirmed`，并保留这一事实来源；这不等于 Dola 服务端额度或
生成能力已验证。

## 日常命令

```powershell
cd LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver
.venv\Scripts\python.exe -m app.cli dola-desktop health
.venv\Scripts\python.exe -m app.cli dola-desktop accounts
.venv\Scripts\python.exe -m app.cli dola-desktop accounts --sync
.venv\Scripts\python.exe -m app.cli dola-desktop activate D01
.venv\Scripts\python.exe -m app.cli dola-desktop activate D02
```

激活调用只通知桌面宿主切换对应的已登录 partition，不需要 Codex 操作鼠标。生成任务仍需
Dola Provider 的真实 baseline 生命周期验证；额度、权限、账号或地区限制必须原样记录并
停止，不自动换号规避。
