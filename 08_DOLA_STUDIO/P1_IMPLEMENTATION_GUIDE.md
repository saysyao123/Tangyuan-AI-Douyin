# P1_IMPLEMENTATION_GUIDE｜Minimal Browser + A/B Session

> 本文件只指导 P1。目标不是做完整 Dola Studio，而是用最小实现证明 A/B 两个自有 Dola Session 可以长期独立、稳定、不串号。

## 1. P1 唯一目标

```text
A Profile 正常登录 Dola
B Profile 正常登录 Dola
→ 完全退出应用
→ 重新打开
→ A 仍然是 A
→ B 仍然是 B
→ 20 次切换/启停不串号
```

在此 Gate 通过前，不加入 30s patch、Storyboard、复杂自动化或高级身份功能。

---

## 2. 建议工程结构

```text
src/
  Tangyuan.DolaStudio.sln
  Tangyuan.DolaStudio.App/
    App.xaml
    MainWindow.xaml
    MainWindow.xaml.cs

    Models/
      AccountProfile.cs
      ProfileRuntimeState.cs

    Services/
      ProfileStore.cs
      BrowserInstanceManager.cs
      AppPathService.cs
      LogService.cs

    Views/
      AccountListPanel.xaml
      BrowserHost.xaml
      InstanceSettingsDialog.xaml

    ViewModels/
      MainViewModel.cs
      AccountListViewModel.cs
      BrowserHostViewModel.cs

data/
logs/
tests/
```

P1 不追求完美 MVVM；但 Browser、Profile storage、UI 不能全部写进 MainWindow code-behind。

---

## 3. Step 1｜创建 Solution

要求：
- .NET 10；
- WPF；
- x64；
- 引入 `Microsoft.Web.WebView2`；
- Debug 默认使用项目本地 data 路径；
- 不把运行时 Session 文件提交 Git。

验收：空应用能运行。

---

## 4. Step 2｜建立 Profile Model

最低字段：

```text
Id
DisplayName
HomeUrl
UserDataFolder
DownloadFolder
CreatedAt
LastOpenedAt
Enabled
```

不存：
- password；
- sms code；
- auth token；
- 手工导出的 Cookie。

验收：可以创建 A/B 两条 profile.json。

---

## 5. Step 3｜ProfileStore

职责：
- 加载 profiles；
- 新建；
- 重命名；
- 删除；
- 检查目录；
- 原子写入 JSON；
- 数据损坏时保留可诊断错误。

建议目录：

```text
%LOCALAPPDATA%/TangyuanDolaStudio/
  profiles/{id}/
    profile.json
    webview2/
    downloads/
    logs/
```

开发模式可允许配置 portable data root。

---

## 6. Step 4｜BrowserInstanceManager

每个 Profile 对应一个运行实例状态：

```text
Stopped
Starting
Running
Stopping
Error
```

要求：
- 同一 Profile 不能重复启动两个使用同一 UDF 的实例；
- 停止后正确释放 WebView2；
- 异常退出后下次能重新打开；
- 错误写日志。

---

## 7. Step 5｜BrowserHost

创建 WebView2 时明确绑定当前 Profile 的独立 User Data Folder。

P1 浏览器功能只做：
- Navigate；
- Back；
- Forward；
- Refresh；
- Home；
- Current URL；
- DownloadStarting 基础日志。

首页默认 Dola 官方网页。

验收：A/B 分别打开后浏览数据独立。

---

## 8. Step 6｜AccountListPanel

每个账号卡显示：

```text
DisplayName
Stopped / Running
LastOpenedAt
[Open]
[Stop]
[Settings]
```

不要在 P1 伪造“已登录”状态；如果尚未建立可靠页面判断，只显示浏览器运行状态。

---

## 9. Step 7｜第一次 A/B 人工登录

测试过程必须人工可见：

1. Open A；
2. 用户本人正常登录 Dola A；
3. 关闭 A；
4. Open B；
5. 用户本人正常登录 Dola B；
6. 关闭整个应用；
7. 重新打开。

记录：
- 是否保持 Session；
- 是否要求重新 OAuth；
- LocalStorage/Cookie 是否仍有效；
- 是否出现页面异常。

---

## 10. Step 8｜隔离测试

执行：

```text
A open
B open
A stop
A open
B stop
B open
...
```

至少累计 20 次启停/切换。

检查：
- A 不变成 B；
- B 不变成 A；
- 下载路径不串；
- UDF 不串；
- 日志 profile_id 正确。

---

## 11. Step 9｜破坏性隔离测试

只对测试 Profile：

- 清除 A 的 WebView2 browsing data / 删除 A 测试 Session；
- 再打开 B。

期望：B 完全不受影响。

如果 B 也掉登录，P1 FAIL，必须先修架构。

---

## 12. Step 10｜P1 报告

生成 `tests/P1_SESSION_AB_REPORT.md`，至少包含：

```text
Build / commit
Windows version
WebView2 runtime
Profile A result
Profile B result
Restart result
20-switch result
Isolation destruction test
Known issues
PASS / FAIL
```

只有全部关键测试通过，才允许把 CURRENT_STATUS 改为：

```text
SESSION_AB_PASS
Current Stage: P2
```

---

## 13. P1 不允许的“顺手增加”

为了防止跑偏，遇到以下需求先记录到 backlog，不直接实现：

- 30 秒按钮注入；
- request patch；
- Proxy；
- Fingerprint；
- MachineGuid；
- CK import/export；
- 自动生成任务；
- Storyboard；
- 多账号并行批任务；
- MV 导演 UI。

这些并非永久删除，而是必须等待 Session Core 被证明稳定。

---

## 14. P1 验收口令

只有满足全部核心条件后才能写：

`SESSION_AB_PASS`

否则必须写：

`SESSION_AB_FAIL: <原因>`

禁止用“基本可以”“应该没问题”替代测试结论。
