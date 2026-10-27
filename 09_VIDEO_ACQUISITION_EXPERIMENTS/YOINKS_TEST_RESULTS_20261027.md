# Yoinks / yt-dlp 四平台联网实测报告 — 2026-10-27

## 范围与保护条件

- 执行位置：GitHub Actions 的独立实验分支 `experiment/yoinks-platform-probe-20261027`，未修改 `main`
- 成功运行：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/40459243816
- yt-dlp 版本：2026.10.26；FFmpeg 版本：6.1.1-3ubuntu5
- 样本：每站一个**公开的、真实的视频或剧集播放页**；仅普通无账号、无 Cookie、无 DRM 绕过的访问
- 测试步骤：解析 metadata -> 若成功，尝试下载最多前三秒的媒体 -> FFprobe 识别视频/音频轨 -> FFmpeg 解码前一秒
- 为避免传播他人版权素材，本轮没有上传媒体文件，下载测试完即删除。报告和 CI 日志保留。
- 结果不构成平台覆盖率或下载成功率估计，不意味着网页视频获得商用许可。

## 运行结果

| 平台 | 样本 | 元信息解析 | 视频下载 | 视频解码 | 证据 |
|---|---|---|---|---|---|
| 抖音 | https://www.douyin.com/video/7682249897617247522 | ❌ | 未尝试 | 未尝试 | `Fresh cookies (not necessarily logged in) are needed` |
| B站 | https://www.bilibili.com/video/BV1AerZB6EWa/ | ❌ | 未尝试 | 未尝试 | HTTP 412 Precondition Failed |
| YouTube | https://www.youtube.com/watch?v=YE7VzlLtp-4 | ❌ | 未尝试 | 未尝试 | Sign in to confirm you're not a bot |
| 红果短剧 | https://hongguoduanju.com/player/7690961604636052505 | ✅ | ✅ | ✅ | 3.08 秒 MP4，FFmpeg 解码通过 |

### 红果成功样本的客观参数

- 标题：军需处长的账本 第1集 | 全集在线免费观看 | 红果短剧 (1)
- 提取器：`HTML5MediaEmbed`；format_count：1
- 测试文件：`video.mp4`，147469 bytes，3.080000 seconds
- 视频：H.264 / 360×640
- 音频：AAC
- `ffprobe` 检测到视频流和音频流；`ffmpeg -t 1 -f null -` 返回 0
- 未测试整集、付费集、其他剧集或更高清晰度。只证明此公开播放页的短片段可获取和解码。

## 失败分类

1. 抖音：运行环境未具备目标站要求的新鲜会话 Cookie，因此未获得元数据。需在用户授权的本地登录浏览器环境另行验证，不应采用批量账号或验证码绕过。
2. B站：从 GitHub 托管运行器访问样本时收到 412，无法区分具体站点策略或云端出口因素。
3. YouTube：云端连接触发网站机器人检测。不能推断用户本机正常会话也失败。
4. 红果：网页嵌入的公开视频轨成功下载；这不意味着所有剧集或 DRM / 受限媒体可以获取。

## 测试局限、验收

- 本轮 4 个样本的完成情况：**1 个成功下载及解码；3 个因访问限制无法进入下载环节。**
- yt-dlp 提供底层解析下载，Yoinks 只提供交互式外壳；本轮实际执行的是 yt-dlp 命令行而非 Yoinks 的 TUI。
- 已验收：孤立分支、真实 URL、元数据阶段、下载阶段、媒体探测和解码阶段、GitHub Actions 真实日志、结果 JSON。
- 未验收：抖音/B站/YouTube 在有效授权的本地网络与会话下下载；红果整集/高清下载；自动无损接入已有视频生产线；商用版权许可。
- 下一步应单独验证合法本地浏览器会话与平台允许的下载方式，尤其针对云端 412 / 人机校验，不把外部站点访问限制说成下载器功能缺陷。

## 文件与追溯

- 实际测试脚本：`09_VIDEO_ACQUISITION_EXPERIMENTS/yoinks_platform_probe.py`
- GitHub Actions 工作流：`.github/workflows/yoinks_platform_probe.yml`
- 结构化结果：成功运行的 artifacts 中 `yoinks-platform-probe-20261027/results.json`
- 首次运行因 Ubuntu Runner 未预装 FFmpeg 而提前失败，随后修正工作流完成正式测试，首次环境错误**未被计入四平台结果**。
