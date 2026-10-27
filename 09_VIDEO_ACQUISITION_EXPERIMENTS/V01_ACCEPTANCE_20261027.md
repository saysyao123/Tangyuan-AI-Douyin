# Video Acquisition V0.1 — 实测验收记录（2026-10-27）

## 原始目标

把视频网页 URL 转换为可用素材文件，目标平台抖音、B站、YouTube、红果相关网站；在现有视频制作流水线之前增加独立下载与质量验证组件。仅 GPT Plus/现有 GitHub；不重构已确认的配音与剪辑流程。

## 实际交付

- 获取器：09_VIDEO_ACQUISITION_EXPERIMENTS/acquire.py
- 离线单元测试：09_VIDEO_ACQUISITION_EXPERIMENTS/test_acquire.py（9 项）
- 外网平台测试：09_VIDEO_ACQUISITION_EXPERIMENTS/run_ci.py
- 自动化工作流：.github/workflows/video_acquisition_v01.yml
- 使用说明与接入契约：09_VIDEO_ACQUISITION_EXPERIMENTS/README.md
- 独立实验分支：experiment/yoinks-platform-probe-20261027（未合并 main）

## 最后完成的生产性测试

2026-10-27 GitHub Actions 运行 40462330106，状态 success。

https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/40462330106

测试 yt-dlp 2026.10.26，FFmpeg/FFprobe 校验。由同一获取器实际输出文件后做元数据、码流、播放解码、大小和哈希验证。第三方视频不会上传 GitHub；只保存 JSON 证据。

| 平台 | URL 类型 | 实际结果 | 下一步 |
|---|---|---|---|
| 抖音 | douyin.com/video | 解析被拒绝：SESSION_NEEDED | 在获授权本地访问环境验证，不做挑战绕过 |
| B站 | bilibili.com/video | 解析被拒绝：HTTP_412 | 判断本地正常网络/有权会话是否不同 |
| YouTube | youtube.com/watch | 解析被拒绝：SESSION_NEEDED（机器人检测） | 在有正常授权访问的环境再次验证 |
| 红果相关网页 | hongguoduanju.com/player | VERIFIED_CLIP_TEMPORARY；3.08s、147469 B、360×640、H.264 + AAC，解码成功 | 还需查验网站归属、可用权利、不同样本和完整剧集 |
| 独立 CC0 控制样本 | MDN flower.mp4 | FILE_VERIFIED；5.055s、1128375 B、960×540、H.264 + AAC，解码成功 | 已验证正式完整文件下载路径 |

控制样本（MDN/CC0）的 SHA-256:
0cd83d944a6ca7822b4a8306cecc60a36e859b041f6702c6a1ad9ead78924451

红果相关网站的 3 秒内部测试片段 SHA-256:
c5cd3600d3bed01a2f808cabea04d9e23438b03a1646d7baf68e12da98c5a178

9 项离线测试 PASS：错误识别、来源 URL 敏感参数去除、平台归类、完整下载的权利确认门槛、CI 禁用本机浏览器 Cookie 等。

对照样本初始选择 W3C Sintel 触发 403 / Cloudflare，已切换到 MDN CC0 公共视频。前一轮 40461976743 失败不应算作工具通过；40462183624 短片段对照通过，40462330106 完整文件对照通过。

## 验收判断

1. 可在在线执行环境实际调用 yt-dlp、保存视频文件、进行 FFprobe/FFmpeg 真实解码、形成有哈希的 JSON 资产记录 —— **已验证**。
2. 同一环境内红果相关网站公开网页片段 —— **已验证一个样本**。该域名不能自动视为已核实红果 App 官方来源。
3. 抖音/B站/YouTube 的素材实际下载 —— **未通过**，当前云端环境被访问条件拦截。
4. 原 gossip_video_workflow 的文件导入格式 —— **已核对**，本轮提供接入契约，但没有把真实下载文件输入完整视频渲染，不得宣称集成测试通过。
5. 完整版权/授权核实、任意红果整集/1080P、批量下载成功率 —— **均未验证**。
6. 主分支原工作流、Work-Fisher 主方案 —— **未改动**。

## 验收后规划

- 第一优先：选用具备合法下载/使用权的抖音、B站、YouTube 样本在用户正常的本地网络中试跑 probe -> full，验证是否是数据中心网络限制。
- 第二优先：拿已明确授权的真实视频文件做一轮原热点生产线资产导入与 QA，不改变原流程内部模块。
- 第三优先：积累可复现成功与失败样本，再决定有没有必要加其它视频源适配器。

实现约束：无隐藏登录、无批量账号、无验证码绕过、无 DRM 解密、无默认持续轮询和无人授权的批量下载。
