# 网页端／Work 最新启动入口 · v1.1.0

唯一正式源：`saysyao123/Tangyuan-AI-Douyin`／main／`07_VIDEO_PRODUCTION_MAIN/GPT_NATIVE_GIF_VIDEO_SKILL_V1/`。

## 可以直接发给新对话

> 请读取 https://github.com/saysyao123/Tangyuan-AI-Douyin 的 main 当前 commit SHA，再以同一 SHA 读取 `07_VIDEO_PRODUCTION_MAIN/README.md`、`07_VIDEO_PRODUCTION_MAIN/GPT_NATIVE_GIF_VIDEO_SKILL_V1/SKILL.md`、`references/PROMPTS.md`、`references/QA.md` 和 `scripts/gif_to_video.py`，按本目录最新规范执行。使用已确认人物与固定镜头，先取得GPT原生源GIF并检查全部真实源帧，再以5秒／120帧GIF为主交付，同时导出同时间轴5秒／120帧／24FPS MP4。按当次真实工具能力生成，不许凭提示词承诺 30 或 120 原生帧；不许滚动拼图、拉伸伪高清或把补间称为原生帧。尽可能由你完成生成、后处理和 QA，最后给真实文件及报告。若缺少执行能力或原生源GIF，明确说明具体阻塞，不能宣称完成；不要改用3张静态图或PNG→MP4替代正式演示。此专项不替换 Work-Fisher 总流程。

补充本次内容：例如“沿用我的雨夜窗前参考图，固定镜头、轻呼吸和一次慢眨眼；5 秒、无配音、非循环”。这是待原生复测的保守动作要求。抬手触碰另做遮挡验收。已有 GIF 时直接附源文件，避免重新生成。

## 执行 Agent 的最短操作

1. 从 GitHub 连接器或公开源读取 main SHA；随后所有文件固定到该 SHA。下载源码到当前执行环境，仓库 Markdown 不会自动安装工具。查阅 `requirements.txt`，优先现有免费环境；有已验证的锁定版本可用 `requirements-tested.txt`。
2. 用 `--inspect-only` 生成源检查页并实际查看全部帧。通过后以 `--source-reviewed` 在新空目录生产。它由执行者完成，不把剪辑工作交回用户。
3. 按 `SKILL.md` 命令导出和验证；看全部输出帧、完整播放 MP4，记录文件 SHA 与观察。没有完整观看只能保留待验收状态。
4. 首先提供原生源GIF和`animation.gif`（5秒／120帧），同时提供`animation.mp4`（同一动画的24FPS版本）、`source_report.json`、`qa_report.json`、预览与视觉记录。原生样本不随本仓库发布，历史素材位置见 `evidence/2026-11-05/ASSETS.md`，不要假定本地存在 `examples/`。

## 网页端能做什么

| 当次环境 | 可执行范围 | 不能承诺 |
|---|---|---|
| 有原生 GIF 工具、代码执行及文件能力的 Work | 生成／读取源 GIF、运行后处理、技术 QA、检查素材 | 固定额度、恒有 GPU、复杂动作无变形 |
| 有 GIF 工具和代码执行的普通网页会话 | 取决于当次能否得到 GIF 本体及 FFmpeg/OpenCV | 仅阅读 GitHub 就自动执行脚本 |
| 只能阅读／聊天 | 读取规范、审查提示词和用户提供的可见画面 | 已生成可播放成片或已完成编码测试 |

2026-11-05 本 Work 图像工具 schema 的 GIF 范围为 2–16 帧；过去 30 帧结果是历史事实，不是当前工具参数上限。本轮实际生成调用返回 `GIF output is not enabled for this request`，因此**新原生GIF生成当前BLOCKED**，不能把schema存在当成端到端通过。可复用历史合格 GIF。未新增付费 API、订阅或云 GPU。

补测不带参考图也返回同一400；尚不能确定权限／模型／执行入口中的具体原因。执行前读 [原生生成复核](references/NATIVE_GIF_RESEARCH.md)，保存完整实际请求、原始返回和源文件哈希。候选提示词未通过原生生成复验，不因文档更新而升级为已验证能力。

## 更新与安装说明

网页端不是 GitHub 自动热更新镜像。更新确认应写：“已读取 main 的 `<实际 SHA>`，所有规范及脚本来自该提交”。未经真实读取不得填 SHA。旧对话缓存不会自动被替换。

本目录保留历史名称以兼容链接。YAML 已使用标准 `name`／`description`，但目录名与 `gpt-native-gif-video` 不同，**本仓库布局不是严格可安装 Agent Skills 包**。没有在 ChatGPT 全局安装；本入口无需安装即可按文件执行。若以后明确要求安装，应由受支持的安装流程使用同一提交内容并匹配目录名，另做安装验证，不另养一套源码。

## 本轮复核后的执行边界

原生GIF生成受阻时标 `NATIVE_GIF_GENERATION_BLOCKED`。3张静态关键帧做出的眨眼视频属于 `ALTERNATIVE_DEMO_NOT_ORIGINAL_SKILL_PASS`，只能证明该眨眼效果可做，不能证明本Skill原生GIF主链跑通。不要只展示MP4而遗漏GIF主交付，也不能仅补一个实验GIF链接就宣称原流程成功。
