# P1_RUNTIME_FAILURE_001｜首次 Windows 真机失败复盘

日期：2026-09-10

## 用户实测现象

1. 点击“添加账号”时程序直接闪退；
2. 使用已有实例打开浏览器时，没有正确打开 Dola 页面。

结论：`SESSION_AB_PASS = FAIL / BLOCKED`。不得进入 30 秒 Gate。

---

## 与参考软件的结构偏差

### 偏差 A｜实例创建 UI 过度简化
参考软件静态分析确认存在独立：
- `AddInstanceDialog`
- `InstanceSettingsDialog`
- `InstanceManager`

P1.0 为快速验证曾使用 `Microsoft.VisualBasic.Interaction.InputBox`，且 `AddProfile_Click` 没有自己的异常保护。这与参考软件的稳定实例生命周期结构偏差过大。

### 偏差 B｜BrowserHost 生命周期被塞进 MainWindow
参考软件存在独立 `DolaMultiBrowser.Views.BrowserHost`，并围绕 WebView2、userDataFolder、实例状态做独立管理。

P1.0 的做法是：

```text
MainWindow
→ new WebView2()
→ EnsureCoreWebView2Async(environment)
→ 再加入 BrowserHost Grid
→ 再导航
```

这使 WebView2 初始化、WPF 可视树、Profile 切换、销毁与导航耦合在主窗口中。

### 偏差 C｜依赖 Dola 根地址重定向
P1.0 默认入口：
`https://www.dola.com/`

当前 Dola 根地址实际进入 `/chat/`。P1.1 直接使用：
`https://www.dola.com/chat/`

避免把首次导航稳定性依赖在站点重定向上。

### 偏差 D｜无可诊断日志
参考软件存在日志/状态相关模块；P1.0 在 UI 事件发生未捕获异常时可能只表现为闪退，无法定位用户机器环境问题。

### 偏差 E｜Profile 保存过于直接
P1.0 直接覆盖 `profiles.json`。P1.1 改为 Semaphore + 临时文件 + 原子替换，降低快速操作或异常退出导致配置损坏的可能。

---

## P1.1 修复

- [x] 移除 `Interaction.InputBox`；
- [x] 新建原生 WPF `ProfileEditorDialog`；
- [x] Add / Rename / Delete 均增加异常处理；
- [x] 新建独立 `Controls/BrowserHostControl`；
- [x] WebView2 先进入 WPF Visual Tree，再显式初始化；
- [x] 初始化完成后配置 CoreWebView2，再导航；
- [x] 默认 Dola URL 改为 `https://www.dola.com/chat/`；
- [x] 老 Profile URL 自动迁移到 `/chat/`；
- [x] 新增全局 Dispatcher / AppDomain / Task 异常日志；
- [x] 日志位置：`%LOCALAPPDATA%\TangyuanDolaStudio\logs\app.log`；
- [x] 新增 UI“日志”按钮；
- [x] Profile 保存改成原子写入；
- [x] GitHub Actions 最新修复版构建通过。

---

## P1.1 重新测试顺序

只做最小复测：

```text
1. 启动 EXE
2. 点击 + 添加
3. 输入 Test-003 并保存
4. 确认程序不退出且实例出现
5. 选择 Dola-001 → 打开 / 切换账号
6. 确认地址栏最终为 dola.com/chat/... 或合法 Dola 页面
7. 确认 Dola 页面可交互
8. 再进入 A/B 登录测试
```

若任一步失败：
- 点击“日志”；
- 发送 `app.log` 最后异常段或截图；
- 不继续后续 Gate。

---

## PASS 条件

`P1.1_RUNTIME_RETEST_PASS` 需要同时满足：
- 添加账号不闪退；
- 新实例被持久保存；
- Dola 页面正确加载；
- WebView2 不白屏/崩溃；
- 才恢复执行 `SESSION_AB_PASS`。
