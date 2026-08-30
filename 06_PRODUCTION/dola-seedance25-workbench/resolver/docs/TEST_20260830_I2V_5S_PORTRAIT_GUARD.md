# Dola Seedance 2.5｜5 秒图生视频实测记录

日期：2026-08-30
测试类型：I2V / 5s / 9:16
浏览器账号显示名：`BASELINE_ACCOUNT`
首帧：`LOCAL_USER\Downloads\ChatGPT Image 2026年8月30日 17_59_10 (1).png`

## 参数

- 模型：Seedance 2.5
- 时长：5s
- 比例：9:16
- 提示词：使用用户本轮提供的完整英文动态提示词，包含中文对白和唇形同步要求
- 捕获：提交前开启 Full CDP Network/Runtime 观察

## 验收结果

```text
ACCOUNT_REGISTRY: UNKNOWN
REAL_SESSION: PASS
CAPTURE_ARMED_BEFORE_GENERATION: PASS
GENERATION_REQUEST_CAPTURED: PASS
IDENTITY_CAPTURE: FAIL (仅捕获到会话/消息级字段，未取得可用 vid/node_id + media identity)
FOUND_CLEAN_CANDIDATE: NOT_RUN
DOWNLOAD_CLEAN_SOURCE: NOT_RUN
FFPROBE: NOT_RUN
VISIBLE_DOLA_WATERMARK: UNVERIFIED
DURATION_GATE: NOT_RUN
NATIVE_RESOLUTION: NOT_RUN
REAL_MULTI_ACCOUNT_ROUND_ROBIN: NOT_RUN
PER_ACCOUNT_5S_CAPACITY: UNKNOWN
```

## 真实证据

- `POST /chat/completion`：HTTP 200，响应类型为 SSE。
- `POST /im/chain/single`：HTTP 200，响应类型为 JSON。
- 页面随后显示 Dola 的平台拦截信息：
  “出于肖像保护考虑，未认证人脸暂不支持用 Dreamina Seedance 2.5 生成视频。你可以尝试换其它参考图或文生视频。”
- 页面没有生成视频元素，也没有本次任务的下载入口。
- 本次没有取得真实 MP4，因此没有执行下载、FFprobe、抽帧或水印判断。

## 结论

这次测试证明登录态、5 秒/9:16/2.5 参数配置、首帧上传、生成请求提交和网络捕获均可工作；失败点是 Dola 的未认证人脸保护策略，发生在视频媒体生成之前。该结果不能归因于提示词错误，也不能证明账号额度已消耗；本次账号的实际扣费/额度变化仍为 UNKNOWN。

下一次应使用不触发未认证人脸保护的首帧，或改做纯文生视频能力测试；不能通过修改提示词来绕过平台的人脸保护。
