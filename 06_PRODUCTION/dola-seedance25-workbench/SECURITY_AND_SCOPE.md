# 公开导出范围与安全说明

## 已排除

- Google/Dola 密码、Cookie、access token、refresh token、TOTP、Passkey；
- Chromium/Electron Profile、IndexedDB、Local Storage 数据库；
- 原始 HAR、完整 SSE/Network response body、带签名参数的 CDN URL；
- 生成 MP4、图片附件原文件、截图中的账号信息；
- 实际 Dola 账号 UUID、会话 ID、个人昵称和本机绝对路径；
- 小柴多开器的 `app.asar`、二进制、反编译源码和第三方资源。

## 保留内容

- 我们自研的控制平面和 Resolver 源码；
- 不含真实凭据的 fixture、单元测试和接口路径；
- 经过脱敏的字段存在性、HTTP 状态、任务状态、时长/分辨率/码率等结果；
- 可供外部 AI 复现思路的时间线和问题假设。

## 解释规则

`PASS` 只表示对应证据层通过。登录态、页面参数、接口 200、助手“已开始生成”的文案都不等于生成完成。只有真实 MP4 + FFprobe + 完整性校验 + 代表帧检查，才能把媒体交付标记为 PASS。
