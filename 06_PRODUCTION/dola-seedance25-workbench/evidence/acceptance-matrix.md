# Dola Seedance 2.5 当前验收矩阵

| Gate | 状态 | 证据边界 |
|---|---|---|
| Electron health | PASS | 本地控制面 health 返回正常 |
| Independent account partitions | PASS | 用户手动登录后的 A/B partition 隔离与重启保持 |
| Account registry | PASS | 非敏感别名、slot、状态和统计 |
| Sticky job binding | PASS | job 绑定后拒绝换号 |
| Durable capture sink | PASS | 事件即时落盘 |
| Round-robin simulation | PASS | 健康感知轮询模拟通过 |
| Full CDP capability | PASS / limited | 可观察当前页面；BrowserContext 创建不支持 |
| 生成前 capture armed | PASS | 最新任务提交前已 armed |
| 最新 Dola1 任务提交 | PASS / partial | SSE 200、助手确认生成意图 |
| 最新 Dola1 provider completion | UNKNOWN | 180 秒内无完成媒体证据 |
| 最新 Dola1 media identity | FAIL | `vid/node_id/video_list` 均未找到 |
| 最新 Dola1 clean candidate | NOT RUN | 没有媒体身份和候选 |
| 最新 Dola1 MP4 download | NOT RUN | 无 MP4 |
| 最新 Dola1 FFprobe | NOT RUN | 无文件 |
| 最新 Dola1 visible watermark | UNVERIFIED | 没有视频可检查 |
| 前一次 clean MP4 chain | PASS | 另一次测试实际得到 1280×720 MP4 |
| Native 5-second output | UNVERIFIED | 已有请求参数，不等于文件时长 |
| Real multi-account generation round-robin | NOT RUN | 只有编排层模拟证据 |
| Per-account 5s capacity | UNKNOWN | 未完成逐条真实 provider 测量 |
| Historical AISpace recovery | BLOCKED | 服务端 country restriction |
