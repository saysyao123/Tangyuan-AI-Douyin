# CURRENT_STATUS｜Tangyuan Dola Studio

> 此文件只记录当前实际状态，不得修改 PROJECT_CHARTER 的长期目标。

## 当前日期
2026-09-10

## 当前分支
`project/dola-studio-v1`

## 当前阶段
`P0 — Reference + Project Lock`

## 当前结论

### 已完成
- [x] 参考软件已完成第一轮静态结构拆解；
- [x] 确认 WPF / WebView2 / AccountInstance / BrowserHost / ResourcePanel / Storyboard / AutomationServer 等结构；
- [x] 确认存在独立 Session / UDF 思路；
- [x] 确认存在 Cookie Import/Export、Proxy、Fingerprint、MachineGuid 等高级模块；
- [x] 确认参考软件存在 Seedance 2.5 / 15s/30s 页面与请求处理相关逻辑；
- [x] 确认其下载链会解析多种视频/下载 URL 字段；
- [x] 已建立本项目独立 GitHub 分支；
- [x] 已建立项目文档目录。

### 尚未完成
- [ ] P0 文档最终复核；
- [ ] P1 WPF 工程；
- [ ] WebView2 BrowserHost；
- [ ] A/B Profile 创建；
- [ ] A/B Session 实机登录测试；
- [ ] 30 秒账号真实能力测试；
- [ ] 下载与媒体 QA；
- [ ] Codex localhost bridge；
- [ ] Storyboard / MV bridge。

## 当前第一 Gate
`P0_DOC_LOCK`

完成标准：
- README / PROJECT_CHARTER / ARCHITECTURE / REFERENCE_SOFTWARE_MAP / ROADMAP_AND_GATES / CURRENT_STATUS / NEW_CHAT_START_PROMPT / DECISION_LOG / P1_IMPLEMENTATION_GUIDE 全部存在；
- 文档之间目标无冲突；
- 30 秒目标明确保留；
- 原软件高级能力仍在研究表，但未错误写成必须实现。

## P0 通过后的唯一下一动作
进入 `P1 — Minimal Browser + A/B Session`。

优先顺序：

```text
Solution / Project
→ Profile model
→ Profile storage
→ WebView2 BrowserHost
→ Account list
→ Start/Stop
→ A/B independent UDF
→ user manual login
→ restart persistence
→ 20-switch isolation test
```

在 `SESSION_AB_PASS` 前，不进入 30 秒自动化、Storyboard、资源批量分发或复杂页面注入。

## 当前风险/未知项

1. Dola 当前页面和账号实际公开的 Seedance 2.5 时长尚未在我们自己的工作台中验证；
2. 参考软件的 30 秒链包含页面/请求修改，但这不等同于当前账号官方允许 30 秒；
3. Dola 原始下载是否稳定提供无可见水印源，需要真实生成结果验证；
4. WebView2 多 Profile 的资源优化尚未实测，P1 先用独立 UDF；
5. 低配机器上的同时常驻实例数量尚未测量。

## 状态更新规则

每轮开发结束必须更新：
- 当前阶段；
- 本轮 PASS / FAIL；
- 新发现；
- 下一 Gate；
- 未解决问题。

禁止仅写“已完成”。
