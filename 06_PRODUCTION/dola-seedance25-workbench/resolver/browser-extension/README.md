# Dola P1 Browser Capture

1. 在 `LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver` 启动：

   ```powershell
   python -m app.cli capture-server
   ```

2. 在 Chrome/Edge 的扩展管理页面打开开发者模式，加载本目录。
3. 使用本人已登录的 Dola，打开本人已完成的视频对话并刷新。
4. 查看 `captures/` 是否出现 `dola_chain_*.json` 与对应的 resolve report。

如需自动请求已捕获的 fallback_api、下载 clean candidate 并运行 ffprobe：

```powershell
python -m app.cli capture-server --auto-download
```

扩展仅捕获 HTTPS `dola.com`（含子域名）的精确 `/im/chain/single` 响应，并只向 `127.0.0.1:8765` 发送响应体。它不读取密码、验证码、Cookie 或浏览器存储。原始响应 JSON 为 P0 解码所需的本地敏感捕获数据，报告与日志会脱敏，勿上传到 GitHub 或第三方。
