# REFERENCE_SOFTWARE_MAP｜豆啦啦参考软件功能镜像

> 目的：把原软件“有什么、解决什么问题、依赖什么、我们如何处理”完整记录。此文件用于防止后续因为只盯最近一个需求而遗忘原始参考对象。

## 1. 当前已识别的总体结构

参考软件静态分析显示其核心为：

```text
Windows x64
→ .NET / WPF
→ DolaMultiBrowser
→ WebView2
→ AccountInstance / BrowserHost / ResourcePanel / Storyboard / Automation
```

外部文件名与内部程序集版本可能不同，因此功能判断以实际结构和行为验证为准，不以发行文件名为唯一依据。

---

## 2. 功能镜像表

| 原软件能力 | 当前证据状态 | 真实用途 | 我们的处理 |
|---|---|---|---|
| AccountInstance | CONFIRMED | 每账号一个逻辑实例 | IMPLEMENT |
| InstanceManager | CONFIRMED | 创建/启动/停止/删除实例 | IMPLEMENT |
| BrowserHost | CONFIRMED | 承载 Dola 网页 | IMPLEMENT |
| WebView2 | CONFIRMED | 浏览器内核 | IMPLEMENT |
| 独立 UserDataFolder | CONFIRMED | Session/Cookie/Storage 隔离 | IMPLEMENT |
| AccountListPanel | CONFIRMED | 账号列表 UI | IMPLEMENT |
| Instance Settings | CONFIRMED | 单实例设置 | IMPLEMENT / SIMPLIFY |
| ResourcePanel | CONFIRMED | 视频/图片素材 | IMPLEMENT |
| VideoPreview | CONFIRMED | 预览生成结果 | IMPLEMENT |
| StoryboardWindow | CONFIRMED | 分镜/任务组织 | LATER |
| AutomationServer | CONFIRMED | 外部程序控制工作台 | IMPLEMENT LATER |
| Local API | CONFIRMED | 实例/任务控制 | IMPLEMENT SAFE SUBSET |
| Cookie Import/Export | CONFIRMED | 快速恢复/迁移 Session | RESEARCH / NOT CORE |
| Proxy config | CONFIRMED | 每实例网络出口配置 | RESEARCH / NOT CORE |
| Fingerprint Injector | CONFIRMED | UA/时区/屏幕/WebRTC 等环境修改 | RESEARCH ONLY |
| Canvas/Audio noise | CONFIRMED | 指纹差异化 | RESEARCH ONLY |
| MachineGuid modification | CONFIRMED | 修改 Windows 机器标识 | RESEARCH ONLY / DO NOT IMPLEMENT |
| Seedance 2.5 selection | CONFIRMED | 指定视频模型 | IMPLEMENT ONLY VIA AVAILABLE UI/CAPABILITY |
| 15s/30s option injection | CONFIRMED | 修改页面可见时长选项 | RESEARCH ONLY |
| duration=30 request patch | CONFIRMED | 修改生成请求参数 | RESEARCH ONLY |
| model request patch | CONFIRMED | 修改请求模型参数 | RESEARCH ONLY |
| Network interception | CONFIRMED | 读取/改写响应或请求 | SAFE OBSERVATION ONLY IF NEEDED |
| media_url/download_url parse | CONFIRMED | 找生成结果/下载源 | IMPLEMENT ONLY FOR PLATFORM-EXPOSED SOURCES |
| get_download_info style flow | CONFIRMED in related path | 找平台返回下载源 | REFERENCE / ADAPTER-SPECIFIC |
| traditional watermark removal | NOT FOUND | 图像修复/擦除水印 | DO NOT ASSUME |
| SMS receiving/captcha platform | NOT FOUND | 批量验证码 | OUT OF SCOPE |
| auto quota-rotation accounts | NOT CONFIRMED | 额度耗尽换号 | DO NOT ASSUME / OUT OF SCOPE |

---

## 3. 必须保留研究价值的设计

### 3.1 三栏工作台

```text
Account Panel | BrowserHost | ResourcePanel
```

价值：账号、平台页面、素材形成同一工作上下文，适合后续 MV。

### 3.2 Instance 独立目录
价值：
- Session 持久；
- 数据不串；
- 单账号损坏不影响其他账号；
- 便于日志和下载归档。

### 3.3 Storyboard 独立于 Browser
价值：生成工具与导演/项目层分开，后续平台变化时 MV 逻辑仍可保留。

### 3.4 AutomationServer 独立层
价值：UI 可以由用户手动操作，同时给 Codex / 脚本保留稳定控制入口，不直接依赖桌面坐标点击。

### 3.5 下载源优先于“去水印”
价值：如果平台正常返回原始 clean source，直接保存源文件比后处理更可靠。

---

## 4. 30 秒能力拆解

参考软件将“30 秒”做成一条组合链：

```text
页面/skill 配置
→ 显示 30s
→ 生成参数 duration=30
→ Seedance 2.5
→ 服务端返回
→ 视频结果解析
```

我们必须把它拆成可验证层：

```text
A. Seedance 模型理论支持 30s
B. 当前 Dola 页面是否公开 30s
C. 当前账号是否允许选择/提交 30s
D. 服务端是否真实生成约 30s 文件
```

D 才是最终 PASS。

原软件的请求 patch 用于理解链路，不直接成为我们的实现方案。

---

## 5. Download 路线拆解

参考软件值得学习的顺序：

```text
任务完成
→ 查找视频结果对象
→ 找播放源
→ 找 download/main/backup URL
→ 保存
→ 校验文件
```

我们的实现要求增加：

```text
source_type
source_url_type
profile_id
model
requested_duration
actual_duration
resolution
codec
watermark_visual_check
```

只有平台自身返回的干净源可标记 `CLEAN_SOURCE_PASS`。

---

## 6. 后续动态更新规则

每次发现原软件新功能，只能做以下动作之一：

- `CONFIRMED`：有明确静态/动态证据；
- `LIKELY`：多处证据一致但尚未完整验证；
- `UNKNOWN`：仅猜测；
- `NOT FOUND`：当前分析未发现，不等于绝对不存在。

禁止把 `LIKELY/UNKNOWN` 写成已经具备。
