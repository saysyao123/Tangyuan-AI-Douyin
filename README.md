# Tangyuan-AI-Douyin

**项目：汤圆AI实战｜30天37粉→1000粉**

这是「汤圆AI实战」抖音账号的长期项目事实库与生产系统。

- 起始基线：2026-08-15 / 37粉
- 第一季目标：30天公开实验，37粉 → 1000粉
- 第一季主线：AI内容创作 / AI视频 / 自媒体运营
- 核心表达：真实实验 / 踩坑 → 原因 → 修正 → 可复制结论

## Runtime v3｜先读这里

新对话、Codex、Agent **不要默认全文读取整个仓库**。

```text
04_HARNESS/SKILL.md
→ 04_HARNESS/MANIFEST.md
→ 00_CONTROL/CURRENT_STATE.md
→ 只加载当前任务对应的 workflow + rules + template
```

架构说明：`docs/ARCHITECTURE_V3.md`  
迁移说明：`docs/MIGRATION_V3.md`

## 目录职责

- `00_CONTROL/`：项目合同、当前状态、决策、变更记录
- `01_TOPIC_SYSTEM/`：选题事实库
- `02_DAILY/`：每日正式档案与最终产物记录
- `03_DATA/`：真实数据与实验
- `04_HARNESS/`：v3运行时入口、Workflow、Rules、Templates、Tests；旧大Harness保留为迁移期Reference
- `05_IP_ASSETS/`：IP与视觉资产/设计参考
- `06_PRODUCTION/`：具体生产过程中的专项规格
- `06_TEMPLATES/`：项目级日常交接/文件夹模板
- `99_INBOX/`：待归档交接包
- `docs/`：架构与迁移文档

## Single Source of Truth

- 当前进度：`00_CONTROL/CURRENT_STATE.md`
- 长期项目目标/边界：`00_CONTROL/MASTER_CONTROL.md`
- 执行硬规则：`04_HARNESS/rules/*`
- 流程：`04_HARNESS/workflows/*`
- 运行加载：`04_HARNESS/MANIFEST.md`
- 实验：`03_DATA/EXPERIMENTS.md`

## Public仓库安全规则

严禁提交 API Key、Token、Cookie、登录凭证、手机号/邮箱等隐私、未脱敏后台截图、私密聊天原文或商业敏感数据。视频、音频、大体积图片原则上只保存索引，不直接批量提交。
