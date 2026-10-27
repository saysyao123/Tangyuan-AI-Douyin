# 真实视频获取引擎 V0.1（独立实验）

## 目标与边界

- 视频 URL -> 平台元数据 -> 实际媒体下载 -> FFprobe + FFmpeg 解码验证 -> JSON 资产记录。
- 核心依赖 yt-dlp 和 FFmpeg，Yoinks 是友好的终端界面，并不包含额外的通用解锁引擎。
- 不尝试绕过账号验证、验证码、地理和 DRM 授权；尊重下载与使用条款。
- 媒体版权 / 再发布许可要另外审核；工具只验证技术，不授予商用权利。
- hongguoduanju.com 的素材可以单独解析，但该网站与红果官方 App 的归属关系未在此验证。
- 保留旧的热点视频与 Work-Fisher 生产线。这个分支不修改主流程。
- 测试中的第三方媒体不进入公共 GitHub，CI 只上传 JSON。

## 环境

- Python >= 3.10
- pip install -U yt-dlp
- ffmpeg 和 ffprobe 放在 PATH
- 所有软件本身免费，不需要增加 AI 订阅

## 运行（命令在仓库根目录）

### 探测，不下载

    python 09_VIDEO_ACQUISITION_EXPERIMENTS/acquire.py --mode probe --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

返回 METADATA_ONLY 只表示获取了元数据，绝不算完成下载。

### 三秒临时内部测试：验证后删除视频，保留 JSON

    python 09_VIDEO_ACQUISITION_EXPERIMENTS/acquire.py --mode clip --rights-basis internal_evaluation --url "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"

### 正式下载：仅自己拥有或获得相应许可的视频

    python 09_VIDEO_ACQUISITION_EXPERIMENTS/acquire.py --mode full --rights-basis licensed --url "https://YOUR_AUTHORIZED_SOURCE/video.mp4" --output-dir acquired-assets

### 可选：使用本人本机已经授权的浏览器会话进行探测

    python 09_VIDEO_ACQUISITION_EXPERIMENTS/acquire.py --mode probe --browser edge --url "https://www.bilibili.com/video/BV..."

此模式只能在本地显式启用，不会在 GitHub CI 读取、导出或上传 Cookie。本人会话也不保证目标平台允许下载。不要向聊天助手发送账号密码、Cookie 文件或验证码。

## 输出格式与验收逻辑

每次在输出目录下生成一个隔离子目录，其中有 asset_manifest.json。

- METADATA_ONLY：只有页面元数据，无法进入剪辑
- ACCESS_BLOCKED_OR_EXTRACTION_FAILED：获取元数据时被站点限制或解析失败
- DOWNLOAD_FAILED：解析成功但文件未下载到
- MEDIA_QA_FAILED：拿到文件但媒体探测或解码失败
- VERIFIED_CLIP_TEMPORARY：短片段解码通过，视频随后删除；只作技术测试
- FILE_VERIFIED：完整下载成功，并且 FFprobe / FFmpeg 解码通过（可以进入素材审核）

FILE_VERIFIED 时 JSON 的 media 字段包含本地文件绝对路径、真实 SHA-256、文件大小、时长、分辨率、视频编码和音频编码。ready_for_editor_review = true 不是版权/事实/审美通过。

## 与现有视频制作流程对接（明确未自动打通）

原有 gossip_video_workflow/run.py 通过 episode.json 的 assets[name].file 读取本地影片路径（相对 episode JSON 所在位置），并能通过 assets[name].sha256 验证文件一致性。例如以下配置仅示范字段，不是已生成的素材：

    "assets": {
      "authorized_source.mp4": {
        "file": "../path-to-existing-authorized-file.mp4",
        "sha256": "从本次资产 manifest 获取的真实 SHA-256"
      }
    }

只有先取得真实 FILE_VERIFIED，且具备必要的使用权利，才能将其置入生产工程，指定实际剪辑 start/end/crop，随后仍按原有 QA 完成事实、画面与版权审核。不能凭这份 README 假装原始视频已经进入成片。

GitHub Actions 运行器是临时环境，JSON 中记录的临时 local_file 路径无法跨会话恢复原视频。此实验不上传第三方视频文件；需要在最终素材所在环境真实获取或由内容权利人交付文件。

## GitHub 自动化测试

工作流：.github/workflows/video_acquisition_v01.yml

- 离线测试：异常分类、URL 敏感参数清理、平台匹配、版权确认门槛和 CI 中禁用浏览器 Cookie。
- 联网测试：抖音、B站、YouTube 元数据诊断；红果相关网页三秒临时片段；独立 CC0 公共控制视频。
- 每个平台返回具体 status + error_code；不能从“域名支持”推断实际成功率。
- 如发生 HTTP 412 / 403 / SESSION_NEEDED，记录证据，不做无限重试、验证码或账号限制绕过。
