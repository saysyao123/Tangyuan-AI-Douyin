# ARCHITECTURE｜Tangyuan Dola Studio

## 1. 总体结构

```text
┌──────────────────────────────────────────────┐
│                Tangyuan Dola Studio          │
├──────────────────────────────────────────────┤
│ UI / WPF                                     │
├──────────────┬──────────────┬────────────────┤
│ Account Core │ Browser Core │ Resource Core  │
├──────────────┼──────────────┼────────────────┤
│ Dola Adapter │ Capability   │ Download       │
│              │ Detector     │ Inspector      │
├──────────────┴──────────────┴────────────────┤
│ Local Automation Bridge / localhost only     │
├──────────────────────────────────────────────┤
│ Storyboard / MV Bridge                       │
└──────────────────────────────────────────────┘
```

目标：任何一层失效，都不要求推翻其他层。

---

## 2. 推荐技术栈

### Desktop
- C# / .NET 10
- WPF
- Microsoft.Web.WebView2

### Browser
P1 默认：每账号独立 User Data Folder。

```text
Profile A → UDF-A
Profile B → UDF-B
```

优点：最容易验证真正隔离。

P3/P4 后再评估：共享 Environment + WebView2 Multiple Profiles，以降低低配置电脑资源压力。

### Local Data
优先简单文件结构，不先引入数据库：

```text
data/
  app.json
  profiles/
    {profile-id}/
      profile.json
      webview2/
      downloads/
      tasks/
      logs/
```

后续数据量明显增加时再考虑 SQLite。

---

## 3. 模块职责

### 3.1 Account Core
负责：
- Profile ID；
- 昵称；
- 创建/删除；
- UDF 路径；
- 启动状态；
- 最后打开时间；
- 下载目录；
- 基础备注。

禁止：
- 保存账号密码；
- 自己实现验证码；
- 默认导出认证 Cookie。

### 3.2 Browser Core
负责：
- 创建 WebView2 Environment；
- 确保 Profile/UDF 不被重复占用；
- 导航、刷新、前进/后退；
- Dola 首页；
- DownloadStarting；
- 浏览器生命周期与崩溃恢复。

### 3.3 Dola Adapter
负责“平台相关但不属于浏览器内核”的内容：
- 当前 URL / 页面状态；
- Dola 是否加载完成；
- 当前账号是否呈现已登录状态；
- 页面公开的模型/时长信息；
- 视频任务和结果的可见状态。

Dola 页面结构变化时，优先只修改本层。

### 3.4 Capability Detector
30 秒不做布尔值硬编码，采用状态机：

```text
UNKNOWN
↓
MODEL_SUPPORTED
↓
PLATFORM_EXPOSED
↓
ACCOUNT_ALLOWED
↓
SERVER_VERIFIED
```

验证结果必须带：
- 时间；
- Profile；
- 模型；
- 页面暴露时长；
- 任务 ID（如正常页面可获得）；
- 最终视频时长；
- 结论。

### 3.5 Download Inspector
负责：
- 浏览器正常下载捕获；
- 平台自身公开/返回的下载源识别；
- 保存到对应 Profile / Project；
- 文件完整性；
- ffprobe 或等效检测；
- 缩略图/首帧；
- 可见水印检查结果记录。

不把“后处理去掉了水印”记录为原始 clean source。

### 3.6 Resource Core
统一记录：
- 图片；
- 视频；
- 来源账号；
- 来源任务；
- 创建时间；
- 时长/分辨率；
- clean-source 状态；
- MV project / shot 关联。

### 3.7 Local Automation Bridge
仅绑定：

```text
127.0.0.1
```

第一阶段只提供低风险控制：

```text
GET  /health
GET  /profiles
POST /profiles/{id}/open
POST /profiles/{id}/close
POST /profiles/{id}/navigate
```

后续任何“发送生成任务”的接口必须等 Browser / Session / Dola Adapter 均稳定后再单独设计 Gate。

---

## 4. UI 架构

```text
┌────────────────────────────────────────────────────────┐
│ Toolbar / Current Profile / Capability                 │
├───────────────┬───────────────────────┬────────────────┤
│ Account Panel │ BrowserHost           │ ResourcePanel  │
│               │                       │                │
│ A             │ Dola                  │ Videos         │
│ B             │                       │ Images         │
│ C             │                       │ Tasks          │
├───────────────┴───────────────────────┴────────────────┤
│ Status / Download Path / Logs                          │
└────────────────────────────────────────────────────────┘
```

保留原参考软件值得学习的结构：
- AccountListPanel
- BrowserHost
- ResourcePanel
- Storyboard 独立窗口/模块
- Log Viewer
- Instance Settings

---

## 5. 原参考软件能力的隔离策略

以下能力只进入 Research Adapter / Reference Map，不进入 Browser Core：
- Fingerprint 修改；
- Proxy 轮换；
- MachineGuid；
- Cookie 搬运；
- 30s request patch；
- 网络响应改写。

原因不是“这些功能不存在”，而是防止它们污染最重要的 Session / Browser / Resource 稳定层。

---

## 6. 可替换接口

必须保证后续可以把 Dola 替换为其他入口：

```text
IVideoPlatformAdapter
├─ DolaAdapter
├─ DreaminaAdapter (future)
└─ OfficialApiAdapter (future)
```

这样如果 30 秒在某个官方入口比 Dola 稳定，不需要推翻账号管理和素材层。

---

## 7. 低配置电脑策略

1. 默认一次只激活 1–2 个 BrowserHost；
2. 非活跃账号允许完全停止 WebView2；
3. Profile 数据保留，不依赖浏览器常驻；
4. 不把 Electron + bundled Chromium 作为默认路线；
5. P1 先用独立 UDF 换取隔离可靠性；
6. 隔离通过后再做共享 Environment / Multi-Profile 优化。

---

## 8. 日志原则

每个失败都要落到一个层：

```text
SESSION
BROWSER
PAGE
CAPABILITY
TASK
DOWNLOAD
MEDIA_QA
```

日志不得只写“失败”。至少包含：时间、Profile、阶段、动作、结果、错误摘要。
