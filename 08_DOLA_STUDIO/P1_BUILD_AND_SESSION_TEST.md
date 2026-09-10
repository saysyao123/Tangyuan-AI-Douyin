# P1_BUILD_AND_SESSION_TEST｜Tangyuan Dola Studio

## 1. 当前构建结论

状态：`P1_BUILD_PASS`

GitHub Actions：Run #2

构建目标：
- Windows x64
- .NET 10 WPF
- Self-contained
- Single-file EXE
- Microsoft.Web.WebView2

产物：
- `TangyuanDolaStudio.exe`
- Size: `140890395 bytes`
- SHA-256: `69647c0f083988f3c729f5ebd527e33fa8d47e116cb930900b1c44e1a87df314`

首次构建 Run #1 失败原因：`ProfileStore.cs` 缺少 `System.IO` 引用。
修复后 Run #2：Restore / Publish / Verify / Artifact Upload 全部通过。

---

## 2. EXE 首次启动预期

首次启动时应出现：

- 左侧：`Dola-001`、`Dola-002`；
- 中间：Dola Browser 占位区；
- 右侧：当前实例和 Seedance 能力占位状态；
- 顶部：下载目录、Dola 首页；
- 底部：WebView2 状态。

本地数据目录：

```text
%LOCALAPPDATA%\TangyuanDolaStudio\
├─ profiles.json
└─ profiles\
   ├─ <profile-a-id>\
   │  ├─ webview2\
   │  └─ downloads\
   └─ <profile-b-id>\
      ├─ webview2\
      └─ downloads\
```

---

## 3. TEST-01｜启动 Gate

操作：
1. 双击 `TangyuanDolaStudio.exe`；
2. 确认主窗口正常出现；
3. 选择 `Dola-001`；
4. 点击“打开 / 切换账号”；
5. 确认 Dola 页面能够显示。

PASS：
- 软件不闪退；
- WebView2 正常启动；
- Dola 页面正常加载。

FAIL 时必须记录：
- Windows 提示；
- 软件弹窗；
- 页面截图；
- 是否安装 Edge / WebView2 Runtime。

---

## 4. TEST-02｜A/B 独立登录

操作：
1. 打开 `Dola-001`；
2. 用户本人正常登录账号 A；
3. 确认登录完成；
4. 切换到 `Dola-002`；
5. 用户本人正常登录账号 B；
6. 再切回 `Dola-001`。

PASS：
- Dola-001 仍是 A；
- Dola-002 仍是 B；
- 切换过程中不继承另一个账号的 Session。

注意：
- 不导入 Cookie；
- 不复制登录数据；
- 不使用自动登录。

---

## 5. TEST-03｜完全重启持久化

操作：
1. A/B 均完成登录；
2. 完全关闭 Tangyuan Dola Studio；
3. 确认程序窗口完全退出；
4. 再次双击 EXE；
5. 打开 Dola-001；
6. 打开 Dola-002。

PASS：
- A/B 各自仍保持原登录身份；
- 不需要重新登录；
- 不串号。

---

## 6. TEST-04｜20 次切换

按以下顺序重复 20 次：

```text
A → B → A → B ...
```

每次记录：
- 当前 Profile；
- Dola 当前账号；
- 是否异常退出；
- 是否重新登录；
- 是否出现账号串号。

PASS：20 次全部正确。

---

## 7. TEST-05｜破坏性隔离

目标：证明 A 的 Session 改变不会污染 B。

建议第一轮使用低风险方式：
1. 在 Dola-001 中正常退出账号 A；
2. 停止当前浏览器；
3. 打开 Dola-002；
4. 检查 B。

PASS：
- B 仍然正常保持登录；
- B 的 Session 不受 A 退出影响。

然后重新登录 A。

---

## 8. SESSION_AB_PASS

只有以下全部通过才允许升级：

- [ ] TEST-01 启动 PASS
- [ ] TEST-02 A/B 登录隔离 PASS
- [ ] TEST-03 重启持久化 PASS
- [ ] TEST-04 20 次切换 PASS
- [ ] TEST-05 破坏性隔离 PASS

全部通过后：

`SESSION_AB_PASS`

下一阶段才进入：

```text
Dola Adapter
→ Seedance Capability Detector
→ Seedance 2.5
→ 30s Capability Gate
```

30 秒不能因为当前 P1 已成功构建而被视为已验证。
