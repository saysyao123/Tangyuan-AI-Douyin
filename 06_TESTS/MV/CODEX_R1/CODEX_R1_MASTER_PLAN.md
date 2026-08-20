# CODEX R1｜MASTER PLAN v1.0

## Goal

客观测试 Codex 对人工 R1 Golden Sample 的工程复刻与自动化能力。

默认先运行 `MODE_A_ENGINEERING_REPRODUCTION`。

Codex 不以“最终有视频”为唯一成功标准，而要逐 Stage 记录：
- 是否自动完成；
- 是否需要人工；
- 是否失败重试；
- 是否达到 Golden Target；
- 自动化率。

---

# C00｜Environment Preflight

## Codex 自动执行

检查：
- Git；
- Python >= 3.10；
- ffmpeg / ffprobe；
- Whisper CLI 或 Python package；优先 `faster-whisper`，也允许 `openai-whisper`；
- Playwright；
- Chromium / Chrome；
- 网络访问；
- 当前仓库 / 分支；
- 可写输出目录。

运行：
`python 06_TESTS/MV/CODEX_R1/scripts/preflight.py`

输出：
- `outputs/reports/env_report.json`
- `outputs/logs/C00_preflight.log`

## Gate

### PASS
最低必须有：
- Python；
- ffmpeg / ffprobe；
- Git；
- 一个可用 Whisper 实现。

### PARTIAL
Playwright / 浏览器 / 网络不可用，但本地音视频工程仍可继续。

### BLOCKED
Python / ffmpeg / Whisper 均无法自动安装或使用。

Codex 允许自动安装普通依赖；涉及账户登录、验证码、安全确认时必须停下来请求用户最小操作。

---

# C01｜BGM / Datasource Reproduction

## Objective

验证 Codex 能否把“用户选中的歌”解析成可追踪的具体 BGM 实体，而不是只靠歌曲标题。

目标歌曲：
`你有没有真的爱过我｜阿图表妹`

## Preferred Path A｜Creator Center

Codex 尝试：
1. Playwright persistent profile 打开抖音创作者中心；
2. 如果未登录，只让用户完成登录 / CAPTCHA；
3. 打开选择音乐 / 热门榜；
4. 搜索或定位目标音乐；
5. 尽可能获取：
   - music_id
   - title
   - author
   - exact version
   - duration
   - share / music URL
   - account-side `使用` availability
   - captured_at

## Fallback Path B｜Public Douyin Entity

如果 Creator Center 受限：
- 使用已知 MV / 抖音分享链接；
- 使用项目已有 `R1S01_DATASOURCE` PoC / `jiji262/douyin-downloader`；
- 解析视频 metadata / music entity；
- 明确写出没有验证到的字段。

## Output

`outputs/manifests/bgm_entity.json`

Required fields:
```json
{
  "song": "你有没有真的爱过我",
  "artist": "阿图表妹",
  "music_id": null,
  "exact_version": null,
  "creator_center_available": null,
  "source_method": "...",
  "captured_at": "...",
  "confidence": "HIGH|MEDIUM|LOW",
  "missing_fields": []
}
```

## Gate

C01 可以 `PARTIAL_PASS`，因为人工 R1 已经锁定 Reference BGM。

但 Codex 最终报告必须区分：
- `REFERENCE_BGM_RESOLVED`
- `PUBLISH_BGM_RESOLVED`
- `ACCOUNT_AVAILABILITY_VERIFIED`

不得混写。

---

# C02｜Exact Audio Cut Reproduction

## Golden Truth

人工 R1 源区间：
`00:01:23.800 -> 00:02:00.600`

参考时长：
`36.80s`

Fade in：`0.25s`
Fade out：`1.20s`

## Codex 自动执行

输入优先级：
1. `inputs/audio/你有没有真的爱过我-阿图表妹.mp3`
2. Codex 从已确认同版本来源自动获取的音频

步骤：
1. ffprobe 校验文件；
2. 记录 hash / duration / codec；
3. 使用 ffmpeg 精确截取；
4. 应用 fade；
5. 输出 256 kbps MP3 或无损 WAV 工作文件；
6. 再次 ffprobe；
7. 生成 waveform / silence check 数据（可选）。

Output：
- `outputs/audio/reference_bgm.mp3`
- `outputs/manifests/audio_manifest.json`

## Gate

- duration target: `36.80s ± 0.10s`
- start/end recorded exactly
- no silent version substitution

---

# C03｜Whisper + Known-Lyric Forced Correction

## Objective

验证 Codex 能否解决人工 R1 遇到的歌词时间不准问题，并自动产出可靠 SRT。

## Codex 自动执行

1. 对 `outputs/audio/reference_bgm.mp3` 跑 Whisper；
2. 要求 word timestamps；
3. 使用 `GOLDEN_TARGET.md` 中已知歌词文本做约束；
4. 不允许 Whisper 自己改歌词文本；
5. 使用词级时间戳聚合到句级；
6. 与 Golden SRT 做误差比较；
7. 输出校正版 SRT 与 metrics。

Preferred pipeline：
`Whisper word timestamps -> known lyric text constraint -> sentence aggregation -> compare -> human spot-check if needed`

Output：
- `outputs/subtitles/lyrics_whisper_raw.json`
- `outputs/subtitles/lyrics_whisper_corrected.srt`
- `outputs/reports/subtitle_alignment_metrics.json`

## Suggested PASS Threshold

相对 Golden SRT 的句首时间：
- median absolute error <= `0.25s`
- max absolute error <= `0.60s`

如果 Whisper 明显错词但时间边界可靠，可以用已知歌词替换文本；必须保留 raw 结果供审计。

---

# C04｜Watermark-free HD Source Replacement

## Objective

人工 R1 的水印源不阻塞创意验收；Codex R1 必须验证发布级源替换能力。

## Input Options

A. 用户把 8 条无水印高清源放到：
`inputs/videos/S1.mp4 ... S8.mp4`

B. 用户提供对应分享 / 原始下载链接到：
`inputs/source_urls.json`

C. Codex 根据生成平台 / 抖音分享链接自行下载。

## Codex 自动执行

对每个 S1–S8：
- 获取无水印源；
- ffprobe；
- 确认方向 9:16；
- 优先 >= 1080×1920；若只能获得 720×1280，明确记录；
- 检测明显水印区域（能自动做则做，不能可靠做则人工抽检）；
- 保持原始5秒完整素材；
- hash + manifest。

Output：
- `outputs/sources/S1.mp4 ... S8.mp4`
- `outputs/manifests/source_manifest.json`

## Gate

- 8/8 source present
- no visible platform watermark in publish-grade path
- no accidental re-encoding before edit unless necessary

如果无法自动取得全部 8 条，状态必须 `PARTIAL/BLOCKED_SOURCE_REPLACEMENT`，不能宣称 Publish Ready。

---

# C05｜Timeline Reconstruction

## Objective

用 Codex / ffmpeg 重建人工 R1 第二轮以后已经通过的剪辑逻辑。

## Fixed Creative Order

`S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 -> S8`

## R1 Validated Edit Logic

- 尽量保留每个 5s 素材内部完整动作；
- 不采用8段机械平均截短；
- 使用 selective trim + short overlap / transition 压到 36.8s；
- 情绪流动与动作完整性优先。

### Reproduction baseline

第一版自动复刻可使用：
- 每条目标内部有效长度约 `5.00s`
- 相邻段短 overlap / dissolve 约 `0.45s`
- 7 次 overlap 总计约 `3.15s`
- 最终对齐锁定音频 `36.80s`

Codex 必须把实际采用参数写入 `timeline.json`，不能只藏在 ffmpeg 命令里。

Output：
- `outputs/manifests/timeline.json`
- `outputs/video/edit_no_subtitles.mp4`

## Gate

- final duration `36.80s ± 0.10s`
- segment order unchanged
- no source clip accidentally omitted
- audio is the locked Reference BGM

---

# C06｜Subtitle Render + Final Polish

## Inputs

- `outputs/video/edit_no_subtitles.mp4`
- `outputs/subtitles/lyrics_whisper_corrected.srt`

## Base Style

沿用人工 R1：
- 浅色中文；
- 深色半透明圆角底；
- 背景紧贴文字；
- 上下左右视觉居中；
- 底部安全区；
- 最多2行；
- 轻微淡入淡出；
- 不做复杂 KTV 字字高亮。

## Final Polish

- 不修改已锁字幕时间；
- 不重新设计剪辑；
- 尾部允许约 `0.55s` 极轻画面淡黑；
- 音频自身已有 fade 不重复破坏。

Output：
`outputs/final/CODEX_R1_FINAL.mp4`

---

# C07｜Automated QA / Golden Comparison

Codex 必须自动检查：

### Technical
- duration
- resolution
- fps
- audio presence
- audio duration
- black-frame / decode errors
- subtitle file validity

### Timeline
- S1–S8 order
- all 8 sources used
- overlap / trim recorded
- final BGM correct

### Subtitle
- exact text match
- sentence count = 9
- timing metrics vs Golden

### Source
- watermark-free status
- resolution report

### Visual human spot-check package
自动抽：
- 0.5s / middle / end contact sheet
- transition-near frames

输出：
- `outputs/reports/qa_report.json`
- `outputs/reports/contact_sheet.jpg`

---

# C08｜Final Result / Automation Score

Codex 最终必须填写：
`RESULT_REPORT_TEMPLATE.md`

并生成：
- `outputs/reports/CODEX_R1_RESULT.md`
- `outputs/reports/CODEX_R1_METRICS.json`
- `outputs/reports/FAILURE_LOG.md`

## Automation Score

分别评分：
- C00 Environment
- C01 Datasource
- C02 Audio
- C03 Whisper
- C04 HD source replacement
- C05 Edit
- C06 Subtitle / final render
- C07 QA

每项：
- `2 = fully automatic`
- `1 = automatic after one minimal human unlock/input`
- `0 = cannot complete / manual execution required`

总分：`/16`

同时记录：
- human intervention count
- human active minutes
- retries
- total elapsed time
- model / network waiting time when measurable

不要为了提高评分隐瞒人工介入。

---

# MODE B｜Fresh Creative R1

只有 MODE A 完成后再开。

MODE B 直接调用：
`04_HARNESS/workflows/mv.md`

完整走：
`选歌 -> 音频 -> Beat -> Benchmark -> 导演 -> 首帧提示词 -> 外部首帧生成 -> 动态提示词 -> 外部Seedance -> QA -> 剪辑 -> Whisper字幕 -> Final`

如果 Codex 当前不能直接调用首帧 / Seedance：
- 明确写 `EXTERNAL_GENERATION_REQUIRED`；
- 输出完整 prompt + 文件命名契约；
- 等用户把生成文件放进规定目录；
- 自动恢复下一阶段。
