# Tangyuan Dola Studio

> 项目状态：FOUNDATION / P0
> 开发分支：`project/dola-studio-v1`
> 目标：参考已分析的「豆啦啦无印浏览器」产品结构，采用 clean-room 方式建立我们自己的 Dola 多账号创作工作台，并逐步验证多 Session、Seedance 2.5、30 秒能力、素材下载与 MV 工作流衔接。

## 1. 项目不是“做一个多开器”

最终目标是建立一个长期可维护的软件层：

```text
Tangyuan Dola Studio
├─ Account / Session Core
├─ WebView2 Browser Core
├─ Dola Adapter
├─ Seedance Capability Detector
├─ Video Task / Download Manager
├─ Resource Library
├─ Storyboard / MV Bridge
└─ Local Automation Bridge
```

第一阶段先验证最核心的使用闭环：

```text
创建账号实例 A/B
→ 用户本人正常登录各自 Dola 账号
→ Session 独立持久化
→ 关闭/重开不串号
→ Dola 正常生成视频
→ 探测该账号真实可用的 Seedance 时长
→ 若官方能力允许 30s，则完成真实 30s 生成
→ 捕获官方/原始下载
→ 自动归档并检测规格
```

## 2. 固定原则

1. 原参考软件的功能全部进入研究与映射，不因风险或复杂而直接忽略。
2. clean-room 重构：学习产品结构、交互和工程思想，不复制未知程序代码。
3. 先证明功能有效，再优化；不以“界面做出来”替代真实验收。
4. 多账号仅用于用户本人合法持有且有权使用的账号管理。
5. 指纹伪装、MachineGuid 修改、额度规避、强制请求解锁等能力可以分析其作用和依赖，但不进入可执行核心。
6. 30 秒是核心 Gate，不能被悄悄降级为“默认 15 秒”；但必须区分模型支持、Dola UI 支持、账号权限与服务端实际接受。
7. “无水印”优先解释为平台/账号本身返回的原始干净下载源，不以擦除、覆盖或破解水印作为默认实现。
8. 每个阶段只升级已通过实测的能力；未验证 = UNKNOWN，不得写成 PASS。

## 3. 目录说明

- `PROJECT_CHARTER.md`：最高层项目契约，定义目标、非目标、锁定规则和最终验收。
- `ARCHITECTURE.md`：整体模块、数据边界、技术栈和替换策略。
- `REFERENCE_SOFTWARE_MAP.md`：豆啦啦功能镜像表；记录“看到什么、为什么存在、我们怎么处理”。
- `ROADMAP_AND_GATES.md`：P0–P6 的逐步开发顺序和人工 Gate。
- `CURRENT_STATUS.md`：唯一当前状态文件；每轮开发结束必须更新。
- `NEW_CHAT_START_PROMPT.md`：新对话 / Codex 启动时的统一入口。
- `DECISION_LOG.md`：只记录已经锁定的重要决策，避免后续反复推翻。

## 4. 文档优先级

发生冲突时按以下顺序执行：

```text
PROJECT_CHARTER.md
↓
DECISION_LOG.md 中最新已批准决定
↓
ROADMAP_AND_GATES.md
↓
CURRENT_STATUS.md
↓
ARCHITECTURE.md
↓
REFERENCE_SOFTWARE_MAP.md
```

`CURRENT_STATUS.md` 只能说明“现在做到哪里”，不能自行改变项目目标。

## 5. 当前阶段

当前为 P0：参考软件功能镜像与项目骨架固化。

P0 完成条件：
- 原软件主要功能模块已形成映射表；
- 软件总体架构已锁定；
- P1 的实现范围与 Gate 已写清；
- 新对话启动流程可单独恢复项目上下文。

P1 将进入真正的最小可运行软件：WPF + WebView2 + A/B 独立 Session。
