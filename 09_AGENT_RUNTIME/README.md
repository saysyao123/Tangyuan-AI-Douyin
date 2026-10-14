# Plus-only Agent V0：只用 ChatGPT Plus，不购买其他 AI

## 什么是真的，什么尚未实现

这个目录是原仓库 `gossip_video_workflow` 的**隔离增量层**。不修改既有成片引擎。

- 智能环节：当前 ChatGPT 对话中的 GPT 负责研究、核查、撰稿、导演规划，通过连接的 GitHub 写入 episode JSON；**ChatGPT Plus 不是 API 额度**。
- 执行环节：GitHub Actions 的标准公共仓库运行器，通过原来验证过的免费 Kokoro 配音、React/GSAP、FFmpeg 和独立 STT 渲染中文视频；不需要额外 AI 会员或付费 API。
- 质量环节：生成的 MP4、SHA256、技术 QA、实际配音转写可核验。成片审美和听感为 pending 时**不得声称已全部验收**。
- 此 V0 **不能**实现跨天无人值守的 AI 研究、自动对话，也不能无成本调用 Claude Opus / Grok Bot。不能用模拟登录 Plus、盗用 session、批量账号等方法绕过产品限制。

## 操作及检测

预置任务：`09_AGENT_RUNTIME/examples/technical_smoke.json`（只用于技术样片，不是新闻）。

从仓库根目录运行：

```bash
python 09_AGENT_RUNTIME/plus_agent.py preflight --task 09_AGENT_RUNTIME/examples/technical_smoke.json
python 09_AGENT_RUNTIME/plus_agent.py inspect --task 09_AGENT_RUNTIME/examples/technical_smoke.json
# 云端 bootstrap 完成后：
gossip_video_workflow/.venv/bin/python 09_AGENT_RUNTIME/plus_agent.py render --task 09_AGENT_RUNTIME/examples/technical_smoke.json
```

网页路径：GitHub Actions → **Plus-only Agent v0 (No Paid API)** → Run workflow。首次选 `preflight`；通过后选 `render`。下载名为 `plus-only-render-<run id>` 的 artifact。只有远程实际运行成功才算云端能力验证。

正式新闻需要 GPT 实际核查来源、产生 episode JSON，并为使用的每一份素材提供 `license_evidence_url` 或 `permission_record`，在对应任务声明人工/编辑完成的来源权利审核。**网页公开可下载不等于有改编或重新发布的许可**。预检仅确认存在记录，不能自动证明真实授权。

## 状态

`preflight` → `ready_to_render`；
`render` → 原引擎执行 → `exported_awaiting_review` 或 `failed`。

没有真实 MP4/QA/哈希一致证据时不得标记“完成”。渲染所需依赖在 GitHub 云端安装，不要求用户本地电脑。Actions 运行器是短期实例；跨运行媒体缓存恢复尚未实现。

第一期目标是证明 **GPT 在本对话生成可核查输入 → 免费云端执行 → 实际结果和验收证据** 的闭环，而非虚构一个无需 API 的完整三模型自动协作系统。未来商业机会发现作为独立任务类型扩展，必须另行测试。 
