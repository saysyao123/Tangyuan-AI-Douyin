# Dola Seedance 2.5 Workbench

这是 Tangyuan AI Douyin 仓库中的独立 Dola Seedance 2.5 实验子项目。

本目录汇总了截至 2026-08-30 的：

- Windows Electron 多账号控制平面；
- Dola 原始媒体身份捕获、Resolver、下载和文件级 QA；
- 5 秒图生视频测试记录；
- 前一次成功 clean MP4 证据与本次 Dola1 未完成测试的脱敏证据；
- 当前已确认的能力、未通过的验收项和给外部 AI 的复现问题单。

## 目录

```text
control-plane/       Electron 后台会话宿主、账号槽位、任务控制面
resolver/            Python 捕获、身份解析、候选排序、下载、FFprobe QA
prompts/             本轮测试提示词
evidence/            脱敏后的状态、结果和分析材料
```

## 当前结论

1. Dola 的用户自有登录态可以由 Electron 持久化 partition 隔离保存；账号 A/B 的登录隔离和重启保持已完成本地验收。
2. 后台控制面可以管理账号槽位、sticky job binding、耐久化捕获、健康感知轮询和任务账本；轮询目前只有模拟/编排层证据。
3. 一次较早的 5 秒请求实际产生了可下载的 1280×720、10.08 秒 MP4，并通过文件级和首/中/尾帧水印抽检；这证明过一条生成时身份捕获 → fallback candidate → clean 文件 QA 链，但不证明当前每一次请求都稳定成功。
4. 本轮 Dola1 的星河倒影图生视频请求已经提交并得到 Dola SSE 接收/额度提示，但 180 秒内没有获得 `vid`、`node_id`、`video_list` 或媒体 URL；没有 MP4，因此本轮不能判定生成完成、clean 下载成功或 5 秒时长通过。
5. 历史 AISpace 资源恢复路线曾被服务端 `country restricted` 阻断；这不是本地解析器成功或失败的证明。

## 安全边界

本公开副本不包含密码、Cookie、Token、浏览器 Profile、原始 HAR、签名 CDN URL、MP4、账号 UUID 或完整原始响应。所有真实生成和下载只能在账号所有者正常登录、账号本身拥有权限的前提下进行；不做 CAPTCHA、额度、地区或水印策略绕过。

给外部 AI 分析时，优先附加 `evidence/EXTERNAL_AI_ANALYSIS_BRIEF.md`，必要时在私下提供本地原始证据，而不要把原始抓包直接公开。
