# CURRENT_STATUS｜Tangyuan Dola Studio

> 此文件只记录当前实际状态，不得修改 PROJECT_CHARTER 的长期目标。

## 当前日期
2026-09-10

## 当前分支
`project/dola-studio-v1`

## 当前阶段
`P1.1.1 — Runtime Stability Retest`

## 已通过 Gate

- `P0_DOC_LOCK_PASS`
- `P1_BUILD_PASS`
- `P1.1.1_REBUILD_PASS`

## 已记录失败

- `P1_RUNTIME_FAIL_001`

用户首次 Windows 真机测试发现：
1. 点击“添加账号”直接闪退；
2. 浏览器没有正确打开 Dola 页面。

该失败已单独记录于：`P1_RUNTIME_FAILURE_001.md`。

---

## P1.1.1 修复版构建证据

GitHub Actions Run：`34434105868`

最终运行时代码 Commit：`068ec037af142219d8a6de7afb6fc2626913b2c2`

后续 CI 路径优化 Commit：`fb6daea6807cc68ce9642f52d01d3f7c04c9426e`

构建步骤：
- Setup .NET 10：PASS
- Restore：PASS
- Publish single EXE：PASS
- Verify EXE：PASS
- Upload Windows EXE：PASS

Artifact：`TangyuanDolaStudio-win-x64`

Artifact ID：`10135561724`

本轮下载后的 EXE：
- 文件大小：`140906779 bytes`（约 135 MiB）
- SHA-256：`cf1bc1b516e3097cb50ccaa789c94d9da9bab879722578b30ee411b6643b7eb4`

注意：`P1.1.1_REBUILD_PASS` 只证明修复版可成功构建，不等于运行时问题已解决。

---

## 本轮已完成修复

- [x] 移除 `Microsoft.VisualBasic.Interaction.InputBox`；
- [x] 新建原生 WPF `ProfileEditorDialog`，对应参考软件 `AddInstanceDialog` 思路；
- [x] Add / Rename / Delete 增加异常保护；
- [x] 新建独立 `BrowserHostControl`，对应参考软件 `Views.BrowserHost` 模块；
- [x] WebView2 控件先加入 WPF Visual Tree，再 `EnsureCoreWebView2Async`；
- [x] CoreWebView2 初始化成功后再配置事件和执行导航；
- [x] 默认 Dola 首页从根地址改为 `https://www.dola.com/chat/`；
- [x] 老 Profile 自动迁移到 `/chat/`；
- [x] 新增全局 UI / AppDomain / Task 异常捕获；
- [x] 新增持久 `app.log`；
- [x] 新增界面“日志”按钮；
- [x] Profile JSON 改为 Semaphore + 临时文件 + 原子替换；
- [x] 旧版若留下损坏 `profiles.json`，自动备份为 `profiles.corrupt-时间戳.json` 并重建；
- [x] 每账号独立 UDF 与下载目录继续保留；
- [x] GitHub Actions 已收紧为只有源码/构建配置变化才触发，Markdown 状态更新不再重复构建。

---

## 当前第一 Gate

`P1.1.1_RUNTIME_RETEST_PASS`

### 当前唯一测试任务

```text
Launch P1.1.1 EXE
→ 点击 + 添加
→ 创建 Test-003
→ 确认不闪退
→ 选择 Dola-001
→ 打开 / 切换账号
→ 确认正确进入 Dola /chat/ 页面
→ 确认页面可交互
```

若这四步通过，再恢复：

`SESSION_AB_PASS`

即：

```text
A 正常登录
→ B 正常登录
→ 完全退出
→ 重启
→ A/B 保持各自 Session
→ 20 次切换不串号
→ A 退出不影响 B
```

在 `P1.1.1_RUNTIME_RETEST_PASS` 前，不测试 30 秒，不进入 Storyboard / Proxy / Fingerprint / MachineGuid / request patch 等后续模块。

---

## 当前风险 / 未知项

1. P1.1.1 已按参考软件结构修正并云端构建成功，但必须由用户 Windows 真机确认运行时表现；
2. Dola 登录流程在当前 WebView2 Runtime 下的第三方登录兼容性仍需实测；
3. 若 Dola 页面仍失败，必须优先读取 `%LOCALAPPDATA%\TangyuanDolaStudio\logs\app.log`，不再凭现象猜测；
4. Seedance 2.5 / 30 秒真实能力尚未进入验证；
5. Dola 原始下载与可见水印状态尚未进入验证。

## 状态更新规则

每轮开发结束必须更新：
- 当前阶段；
- 本轮 PASS / FAIL；
- 新发现；
- 下一 Gate；
- 未解决问题。

禁止仅写“已完成”。
