# 前一次成功 clean 文件证据（脱敏摘要）

这是另一条较早的用户自有账号生成测试，不是本轮星河倒影任务。

## 结果

```text
CAPTURE_ARMED_BEFORE_GENERATION: PASS
POST_COMPLETION_CHAIN_REFRESH: PASS
VID_FOUND: YES (redacted)
FALLBACK_API_FOUND: YES (redacted)
KEY_SEED_FOUND: YES (value redacted)
VIDEO_LIST_FOUND: YES
FOUND_CLEAN_CANDIDATE: YES
DOWNLOAD: PASS
FFPROBE: PASS
VISIBLE_DOLA_WATERMARK: NO observed in first/middle/last frame sampling
```

## 文件级事实

```text
container: MP4
video: H.264, 1280x720, 24 fps
duration: 10.080 seconds
format bitrate: approximately 5.78 Mbps
reencoded: NO
```

## 重要限制

- UI/任务参数曾请求 5 秒，但实际文件是 10.08 秒；后续验收必须以 FFprobe 为准；
- clean candidate 来自生成完成后捕获到的 fallback API 路由，不代表 AISpace 当前可用；
- 本轮保存了完成后的 chain、Resolver 输入、下载文件和 QA 结果，但实时 SSE 原始归档不完整；
- `unwatermarked` 等字段只是线索，clean 结论来自实际下载文件和代表帧抽检；
- 这条成功不能外推到本轮未拿到媒体身份的星河倒影请求。
