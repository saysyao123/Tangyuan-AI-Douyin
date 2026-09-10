# PROJECT_CHARTER｜Tangyuan Dola Studio

## 一、原始目标

建立一套长期可维护的 Dola / Seedance 视频创作工作台，重点解决：

1. 多个自有 Dola 账号的独立 Session 管理；
2. 稳定打开 Dola 并长期保持登录；
3. 识别当前账号真实可用的 Seedance 模型与时长能力；
4. 对 Seedance 2.5 的 30 秒能力做正式、可复现的真实性验证；
5. 对生成结果进行下载、归档、规格检测和可见水印检查；
6. 后续接入 Storyboard / MV Pipeline，成为汤圆 MV 生产基础设施。

项目参考「豆啦啦无印浏览器」的产品结构、模块划分与工作流，但采用 clean-room 重构。

---

## 二、最终交付物

最终软件至少包含：

### A. Account / Session
- 创建、重命名、删除账号实例；
- 每账号独立浏览器 Session；
- 登录状态持久化；
- 防止 Profile 串号；
- 独立下载目录和日志；
- 可见的登录/运行状态。

### B. Browser
- Windows 桌面 GUI；
- WebView2 浏览器宿主；
- 正常导航、刷新、前进/后退；
- Dola 首页快捷入口；
- 单实例和多实例生命周期管理。

### C. Seedance Capability
- 识别模型信息；
- 识别页面/账号公开的 5s / 10s / 15s / 30s 能力；
- 将“模型理论能力”和“当前账号实际能力”分开显示；
- 30 秒必须通过真实任务 + 文件规格确认，不以按钮显示为 PASS。

### D. Video / Download
- 记录任务状态；
- 捕获正常浏览器下载；
- 优先识别平台自身暴露的原始下载源；
- 自动归档到对应账号/项目目录；
- ffprobe 或等效方式读取时长、分辨率、编码、文件大小；
- 进行可见水印检查并记录结果。

### E. Resource / MV Bridge
- 视频和图片素材列表；
- 视频预览；
- 项目/镜头关联；
- 后续接 Storyboard 和 MV Pipeline。

### F. Local Control Bridge
- 只监听 localhost；
- 健康检查、实例枚举、打开/关闭、导航等基础操作；
- 后续供 Codex / 本地工作流调用。

---

## 三、明确不等同于项目成功的结果

以下不能单独算完成：

- 做出一个像原软件的 UI；
- 能同时打开两个网页；
- 页面出现“30s”文字；
- 一次生成返回成功提示；
- 下载到一个 MP4；
- 某个脚本在一次测试中工作。

必须通过定义的 Gate 和重复测试。

---

## 四、锁定规则

### 4.1 原软件研究规则

原软件中发现的模块全部记录，包括：
- AccountInstance / InstanceManager；
- BrowserHost / WebView2；
- ResourcePanel；
- Storyboard；
- Local Automation Server；
- Cookie Import / Export；
- Proxy；
- Fingerprint Injector；
- MachineGuid 相关逻辑；
- Seedance 2.5 / 30s 页面和请求处理；
- Video URL / Download Source 解析。

“记录/研究”不等于“实现”。

### 4.2 安全与平台边界

可实现：
- 自有账号的独立 Session；
- 正常手动登录；
- 正常 WebView2 Profile；
- 平台公开功能的辅助操作；
- 当前账号能力检测；
- 正常下载和本地素材处理。

只做结构研究、不实现为规避工具：
- 设备/浏览器指纹伪装；
- MachineGuid 修改；
- 用 Cookie 搬运绕过登录或身份验证；
- 用多个账号规避额度/频控；
- 强制修改请求以解锁未授权 30 秒能力；
- 破解、擦除或覆盖平台水印。

### 4.3 30 秒硬规则

30 秒是核心目标，不允许后续默默删除。

必须区分四个状态：

```text
MODEL_SUPPORTED
PLATFORM_EXPOSED
ACCOUNT_ALLOWED
SERVER_VERIFIED
```

只有 `SERVER_VERIFIED`，且实际下载文件时长达到验收阈值，才能标记 `30S_PASS`。

### 4.4 版本与变更

- 新要求只能作为局部修正、新增约束、替换旧规则或目标升级之一记录；
- 任何会改变原始目标的修改，必须更新本文件或 DECISION_LOG；
- CURRENT_STATUS 不得覆盖本文件。

---

## 五、最终验收标准

### Session
- A/B 两账号分别正常登录；
- 完全关闭软件后重新打开，仍保持各自 Session；
- 连续切换/启动/停止至少 20 次不串号；
- 清除 A Session 不影响 B。

### 30 秒
- 当前账号公开能力可被检测；
- 若账号被官方允许 30 秒：至少 3 个不同任务成功；
- 每个最终文件实际时长建议 >= 29 秒；
- 记录模型、时间、文件规格和失败原因。

### Download
- 下载来源可追踪；
- 文件完整可播放；
- 能读取时长、分辨率、编码、大小；
- 若官方/原始下载本身无可见水印，记录 `CLEAN_SOURCE_PASS`；
- 若只有带水印版本，记录事实，不通过后处理伪装成“原始无水印”。

### Stability
- 异常关闭后不损坏其他账号；
- Profile 被占用时能明确报错；
- 日志可以解释失败发生在哪一层。

---

## 六、最终项目成功定义

项目成功不是复制“豆啦啦”本身，而是证明我们拥有一套自己的、长期可维护的：

```text
多账号 Session
+ Dola Browser
+ Seedance Capability
+ 30s Verified Path
+ Clean Download Path
+ Resource Management
+ MV Integration
```

并且每一层都能被单独测试、替换和维护。
