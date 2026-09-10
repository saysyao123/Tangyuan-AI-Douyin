# CURRENT_STATUS｜Tangyuan Dola Studio

> 此文件只记录当前实际状态，不得修改 PROJECT_CHARTER 的长期目标。

## 当前日期
2026-09-10

## 当前分支
`project/dola-studio-v1`

## 当前阶段
`P1 — Minimal Browser + A/B Session`

## 已通过 Gate

- `P0_DOC_LOCK_PASS`
- `P1_BUILD_PASS`

### P1_BUILD_PASS 证据

- `.NET 10` WPF 工程已建立；
- Microsoft.Web.WebView2 已成功 Restore；
- GitHub Actions Run #2 已完成；
- `dotnet publish` 成功；
- 单文件 `TangyuanDolaStudio.exe` 已生成并通过存在性校验；
- Artifact：`TangyuanDolaStudio-win-x64`；
- Artifact ID：`10135143353`；
- EXE 大小：`140890395 bytes`；
- EXE SHA-256：`69647c0f083988f3c729f5ebd527e33fa8d47e116cb930900b1c44e1a87df314`。

注意：`P1_BUILD_PASS` 只证明软件成功编译并产生 EXE，不等于 `SESSION_AB_PASS`。

## 已锁定的重要结论

- [x] 参考软件先完整研究，再逐步做减法；
- [x] 项目升级为独立 `Tangyuan Dola Studio`；
- [x] WPF + WebView2 为 P1 Browser Core；
- [x] P1 每账号独立 User Data Folder；
- [x] P1 为降低低配置机器负担，先采用“一个工作台 + 多 Profile + 当前单活动 WebView2”；
- [x] 30 秒继续作为核心验证 Gate；
- [x] 30 秒采用 MODEL_SUPPORTED → PLATFORM_EXPOSED → ACCOUNT_ALLOWED → SERVER_VERIFIED；
- [x] clean download 优先验证平台本身正常返回的原始干净源；
- [x] 原软件 Fingerprint / MachineGuid / request patch 等能力保留研究映射，但不进入规避限制的正式实现；
- [x] Dola 与 MV Core 解耦，长期使用 Adapter 架构。

## 当前第一 Gate

`SESSION_AB_PASS`

## 当前唯一主任务

在 Windows 真机运行已经构建的 EXE，并完成：

```text
Launch EXE
→ Dola-001 打开
→ 用户本人正常登录账号 A
→ 切换 Dola-002
→ 用户本人正常登录账号 B
→ 完全关闭 EXE
→ 重新启动
→ 检查 A/B 是否分别保持登录
→ 连续切换 20 次
→ 检查是否串号
→ 清除/退出 A Session
→ 检查 B 是否保持不受影响
→ 输出 P1_SESSION_AB_REPORT.md
```

在 `SESSION_AB_PASS` 前，不进入 30 秒请求修改、Storyboard、复杂生成自动化、Proxy/Fingerprint/MachineGuid 等高级功能。

## P1 实现状态

- [x] 建立 `.NET 10` WPF Solution；
- [x] 引入 Microsoft.Web.WebView2；
- [x] 建立 Profile Model；
- [x] 建立 ProfileStore；
- [x] 建立 BrowserInstanceManager；
- [x] 建立 BrowserHost；
- [x] 建立 AccountListPanel；
- [x] 自动创建 `Dola-001 / Dola-002`；
- [x] 每账号独立 UDF；
- [x] 每账号独立下载目录；
- [x] GitHub Actions 单 EXE 构建；
- [x] 云端 Release Build 成功；
- [ ] EXE 在用户 Windows 真机启动验证；
- [ ] A/B 用户本人正常登录 Dola；
- [ ] 完全退出后 Session 持久化测试；
- [ ] 20 次启停/切换隔离测试；
- [ ] 破坏 A Session 不影响 B 的隔离测试；
- [ ] 输出 `P1_SESSION_AB_REPORT.md`。

## 当前风险/未知项

1. EXE 已通过编译与发布，但尚未在用户实际 Windows 环境进行 GUI / WebView2 启动验证；
2. Dola 当前登录页是否在 WebView2 中存在兼容性/第三方登录限制尚未真机验证；
3. Dola 当前页面和账号实际公开的 Seedance 2.5 时长尚未在我们自己的工作台中验证；
4. Dola 原始下载是否稳定提供无可见水印源，需要真实生成结果验证；
5. WebView2 多 Profile 的资源优化尚未实测，P1 先用独立 UDF；
6. 低配置机器上的同时常驻实例数量尚未测量。

## 状态更新规则

每轮开发结束必须更新：
- 当前阶段；
- 本轮 PASS / FAIL；
- 新发现；
- 下一 Gate；
- 未解决问题。

禁止仅写“已完成”。
