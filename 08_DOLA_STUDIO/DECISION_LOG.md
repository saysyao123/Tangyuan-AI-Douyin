# DECISION_LOG｜Tangyuan Dola Studio

> 只记录已经锁定、会影响后续方向的重要决定。临时想法不要写入本文件。

## D-001｜项目升级为独立软件项目

**状态：LOCKED**

不再把目标定义为“做一个 Dola 多开登录器”。

正式目标：`Tangyuan Dola Studio`，包含 Session、Browser、Capability、Download、Resource、Storyboard/MV Bridge。

---

## D-002｜参考软件先完整研究，再逐步做减法

**状态：LOCKED**

原软件发现的功能不得因为当前暂不实现就从研究范围删除。

采用：

```text
完整镜像研究
→ 判断真实价值
→ 建立我们自己的实现
→ 实测
→ 再做减法/替换
```

而不是一开始凭主观判断大量删功能。

---

## D-003｜Clean-room 重构

**状态：LOCKED**

参考原软件的：
- UI 布局；
- 模块边界；
- 产品工作流；
- 数据组织思想；
- 已发现的能力链。

不直接复制未知闭源程序的实现代码。

---

## D-004｜P1 Browser Core 使用 WPF + WebView2

**状态：LOCKED**

第一版：
- .NET 10；
- WPF；
- Microsoft.Web.WebView2；
- 每账号独立 User Data Folder。

先换取隔离可靠性，后续再考虑共享 Environment + Multiple Profiles 优化资源。

---

## D-005｜30 秒保持核心 Gate

**状态：LOCKED**

不能因为实现复杂或当前入口失败，就把项目目标悄悄改为只支持 15 秒。

30 秒必须按四层验证：

```text
MODEL_SUPPORTED
PLATFORM_EXPOSED
ACCOUNT_ALLOWED
SERVER_VERIFIED
```

真实文件验证才是最终结论。

---

## D-006｜不把参考软件的 30s Request Patch 直接实现为解锁功能

**状态：LOCKED**

参考软件中发现的 UI/请求修改逻辑保留在研究映射中，用于理解产品工作原理和诊断链路。

我们的正式产品先采用 capability detection 和当前账号真实可用能力；不通过强制改写请求来伪造 `30S_PASS`。

---

## D-007｜无水印目标解释为 Clean Source 优先

**状态：LOCKED**

正式目标：优先获得平台本身正常暴露/返回的原始干净下载源。

如果源文件本身有可见水印，记录事实；不把后处理擦除后的结果冒充为原始无水印下载。

---

## D-008｜多账号的用途是 Session 管理，不是额度轮换

**状态：LOCKED**

多账号核心价值：
- 独立登录；
- 项目隔离；
- 不同自有账号统一工作台；
- 对应素材归档。

不以账号池自动轮换来规避平台限额或频控作为项目目标。

---

## D-009｜Automation Bridge 后置

**状态：LOCKED**

在 `SESSION_AB_PASS` 前不做复杂自动化。

Local API 先只提供 health / list / open / close / navigate，并且仅 localhost。

---

## D-010｜MV Pipeline 与 Dola 解耦

**状态：LOCKED**

Dola 是当前重要 Adapter，不是整个系统唯一后端。

长期保持：

```text
IVideoPlatformAdapter
→ Dola
→ other official web entry
→ official API / future provider
```

避免未来 Dola 页面变化导致 MV 系统整体重写。
