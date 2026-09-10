# CURRENT_STATUS｜Tangyuan Dola Studio

> 此文件只记录当前实际状态，不得修改 PROJECT_CHARTER 的长期目标。

## 当前日期
2026-09-10

## 当前分支
`project/dola-studio-v1`

## 当前阶段
`P1 — Minimal Browser + A/B Session`

## 已通过 Gate

`P0_DOC_LOCK_PASS`

P0 已完成并复核：
- [x] `README.md`
- [x] `PROJECT_CHARTER.md`
- [x] `ARCHITECTURE.md`
- [x] `REFERENCE_SOFTWARE_MAP.md`
- [x] `ROADMAP_AND_GATES.md`
- [x] `CURRENT_STATUS.md`
- [x] `DECISION_LOG.md`
- [x] `P1_IMPLEMENTATION_GUIDE.md`
- [x] `NEW_CHAT_START_PROMPT.md`

文档已确认位于 GitHub 分支 `project/dola-studio-v1` 的 `08_DOLA_STUDIO/` 目录。

## 已锁定的重要结论

- [x] 参考软件先完整研究，再逐步做减法；
- [x] 项目升级为独立 `Tangyuan Dola Studio`；
- [x] WPF + WebView2 为 P1 Browser Core；
- [x] P1 每账号独立 User Data Folder；
- [x] 30 秒继续作为核心验证 Gate；
- [x] 30 秒采用 MODEL_SUPPORTED → PLATFORM_EXPOSED → ACCOUNT_ALLOWED → SERVER_VERIFIED；
- [x] clean download 优先验证平台本身正常返回的原始干净源；
- [x] 原软件 Fingerprint / MachineGuid / request patch 等能力保留研究映射，但不进入规避限制的正式实现；
- [x] Dola 与 MV Core 解耦，长期使用 Adapter 架构。

## 当前第一 Gate

`SESSION_AB_PASS`

## 当前唯一主任务

严格按 `P1_IMPLEMENTATION_GUIDE.md` 建立最小可运行程序：

```text
Solution / WPF App
→ Profile Model
→ ProfileStore
→ BrowserInstanceManager
→ WebView2 BrowserHost
→ AccountListPanel
→ A/B independent UDF
→ user manual Dola login
→ full app restart
→ 20-switch isolation test
→ destructive isolation test
→ P1 report
```

在 `SESSION_AB_PASS` 前，不进入 30 秒请求修改、Storyboard、复杂生成自动化、Proxy/Fingerprint/MachineGuid 等高级功能。

## P1 尚未完成

- [ ] 建立 `.NET 10` WPF Solution；
- [ ] 引入 Microsoft.Web.WebView2；
- [ ] 建立 Profile Model；
- [ ] 建立 ProfileStore；
- [ ] 建立 BrowserInstanceManager；
- [ ] 建立 BrowserHost；
- [ ] 建立 AccountListPanel；
- [ ] 创建 A/B 独立 UDF；
- [ ] A/B 用户本人正常登录 Dola；
- [ ] 完全退出后 Session 持久化测试；
- [ ] 20 次启停/切换隔离测试；
- [ ] 破坏 A Session 不影响 B 的隔离测试；
- [ ] 输出 `P1_SESSION_AB_REPORT.md`。

## 当前风险/未知项

1. Dola 当前页面和账号实际公开的 Seedance 2.5 时长尚未在我们自己的工作台中验证；
2. 参考软件的 30 秒链包含页面/请求修改，但这不等同于当前账号官方允许 30 秒；
3. Dola 原始下载是否稳定提供无可见水印源，需要真实生成结果验证；
4. WebView2 多 Profile 的资源优化尚未实测，P1 先用独立 UDF；
5. 低配置机器上的同时常驻实例数量尚未测量。

## 状态更新规则

每轮开发结束必须更新：
- 当前阶段；
- 本轮 PASS / FAIL；
- 新发现；
- 下一 Gate；
- 未解决问题。

禁止仅写“已完成”。
