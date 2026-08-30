# P0 验收记录（2026-08-30）

## 结果

P0：**PASS**。项目、代码、模拟响应、隔离环境、单元测试和 CLI 验收均已完成。

## P0 顺序核对

| 顺序 | 项目 | 状态 | 证据 |
|---|---|---|---|
| P0-1 | Python 项目骨架与依赖 | PASS | `pyproject.toml`、`app/`、`tests/`、`fixtures/` |
| P0-2 | 递归 JSON walker | PASS | `app/discovery/router_data.py`，支持嵌套 JSON 字符串 |
| P0-3 | `MediaCandidate` / `ResolveResult` | PASS | `app/models.py` |
| P0-4 | main_url 等直出字段解析 | PASS | `app/resolver/candidates.py` |
| P0-5 | Base64 / Base64URL / `$ @ #` 解码 | PASS | `app/resolver/url_decoder.py` |
| P0-6 | qAAB AES-CBC 解码 | PASS | `app/resolver/qaab.py` 与测试夹具 |
| P0-7 | fallback_api 参数构造与解析 | PASS | `app/resolver/fallback_api.py` |
| P0-8 | 清洁源排序 | PASS | 无水印负证据优先于更高码率/分辨率 |
| P0-9 | 流式下载 | PASS | `.part`、Content-Length、原子改名；不重新编码 |
| P0-10 | MP4 ftyp 校验 | PASS | `app/download/validator.py` |
| P0-11 | ffprobe QA | PASS | 已实测两条现有 15 秒视频 |
| P0-12 | CLI | PASS | `resolve`、`download`、`inspect` |
| P0-13 | fixtures + tests | PASS | `8 passed` |
| P0-14 | README | PASS | `README.md` |

## 实测结果

```text
.venv\Scripts\python.exe -m pytest
8 passed in 1.95s
```

模拟响应的 `resolve` 结果：4 个候选、2 个明确无水印候选，选中 1920×1080、H.264、原始标记候选；报告中的 URL 查询串已脱敏。

真实现有文件的 `inspect` 结果：

- segment 01：720×1280，HEVC，15.092971 秒，4,008,404 bytes
- segment 02：720×1280，HEVC，15.092971 秒，4,678,183 bytes

这两条是已有带水印预览文件的技术检查结果，不是无水印源验收结果。

## 安全边界

本 P0 工具不会抽取 Cookie、不会读取浏览器 Profile、不会绕过登录/验证码/配额、不会伪造签名、不会处理 403 绕过。真实网络 fallback 请求必须由调用者显式加 `--fetch-fallback`，默认关闭。

P1 浏览器 Network/XHR 捕获尚未实现；当前模块只提供明确失败的占位，以防止把“未捕获到响应”误报为“已拿到原始源”。
