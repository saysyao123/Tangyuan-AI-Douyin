# Yoinks / yt-dlp 抖音、B站、YouTube 最终下载测试结果（2026-10-27）

## 一句话最终结论

**在当前可用的 GitHub Actions 云端执行环境中，三个平台都没有下载成功。** 两个不同的公开链接 × 两种操作系统（Windows / Linux），每个平台共 4 次访问尝试，**0 个通过可播放视频文件验收**。

这代表当前“ChatGPT Plus + GitHub 云端自动下载三站视频”的技术方案**没有达到生产可用验收条件**；**不能**由此推出该工具在所有用户电脑、所有有效授权会话、所有视频上都不可用。

## 测试范围

- GitHub 仓库：`saysyao123/Tangyuan-AI-Douyin`
- 安全隔离分支：`experiment/yoinks-platform-probe-20261027`，未合并 main。
- Windows 完成运行：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/40508943332
- Linux 独立完成运行：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/40509576243
- 同期较早 Ubuntu apt-get FFmpeg 安装任务的状态与独立 Linux 任务区别对待，不冒称该安装步骤成功。
- 使用 `yt-dlp 2026.10.26`、`yt-dlp-ejs 0.8.0`、Node 22，Windows 上安装了 Yoinks 本体与 FFmpeg。
- yt-dlp + EJS + Node 的配置符合官方 YouTube 新版解析的必要条件。
- 不使用账号、Cookie、代理轮换、验证码破解或 DRM 解密；仅短片段临时测试，测试影片随即删除。
- 两个环境都基于 GitHub 云端运行器，因此结果**不能**代表家庭网络或个人本机授权浏览器。
- 只把真实取得文件、FFmpeg 可解码的测试记录认定为下载成功；元数据成功也不等于下载成功。

## 每个平台的原始链接与结果

| 平台 | 测试链接 | Windows | Linux | 实际失败环节 |
| --- | --- | --- | --- | --- |
| 抖音 | https://www.douyin.com/video/7699684520735660214 | 无视频文件 | 无视频文件 | Fresh cookies needed |
| 抖音 | https://www.douyin.com/video/7682249897617247522 | 无视频文件 | 无视频文件 | Fresh cookies needed |
| B站 | https://www.bilibili.com/video/BV13x41117TL | 无视频文件 | 无视频文件 | HTTP 412 Precondition Failed |
| B站 | https://www.bilibili.com/video/BV1AerZB6EWa/ | 无视频文件 | 无视频文件 | HTTP 412 Precondition Failed |
| YouTube | https://www.youtube.com/watch?v=aqz-KE-bpKQ | 无视频文件 | 无视频文件 | Sign in to confirm not a bot |
| YouTube | https://www.youtube.com/watch?v=YE7VzlLtp-4 | 无视频文件 | 无视频文件 | Sign in to confirm not a bot |

### 技术对照样本

Windows 使用 https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4 下载了约 3.07 秒的 MP4：

- 751584 bytes，H.264 960×540，AAC 音轨
- FFmpeg 真实解码通过
- SHA-256：`3c392ec716982d621f91db31ad6bece466f38f055d6048dfacd435591923a585`

Linux 轻量执行路径成功完成三个网站的所有元数据请求尝试，但独立控制视频的分段下载因打包的 FFmpeg 返回 `-11` 而未通过。Linux 独立对照未通过应如实说明；Windows 对照样本已确认基础工具链可正常完成视频获取与解码。

## 验收判定

- **抖音：当前云端下载不可用（0/4）。**
- **B站：当前云端下载不可用（0/4）。**
- **YouTube：当前云端下载不可用（0/4），即便补齐新版所需 EJS。**
- **Yoinks 安装/调用 yt-dlp 的技术路线可运行，但不具备突破上述平台访问策略的独立技术能力。**
- **“能下载任意三站视频”的原始目标未实现，不能升格为正式视频生产线默认素材获取引擎。**

## 继续推进的决策条件

需要证明确有可用的合法访问执行环境，例如本人有权下载的视频在正常 Windows 网络 / 已获授权的浏览器会话中，可以完成 `probe -> 真实 MP4 -> ffprobe -> 解码 -> SHA256`；只有这个最小闭环通过，才值得接入既有热点视频生产流程。不使用批量账号、验证码绕限、绕过 DRM 等手段，也不能仅凭网站收录在 yt-dlp 支持列表就判定实际下载成功。

## 实际脚本与日志

- Windows 双环境原始测试脚本：`09_VIDEO_ACQUISITION_EXPERIMENTS/final_three_sites.py`
- Linux 替代测试：`09_VIDEO_ACQUISITION_EXPERIMENTS/final_linux_quick.py`
- GitHub Actions 工作流：`.github/workflows/final_three_sites.yml`、`.github/workflows/final_linux_quick.yml`
- Windows 工作流 artifact：`final-three-sites-windows-diagnostic`
- Linux 工作流 artifact：`final-linux-quick-json`

**判定日期：2026-10-27。**
