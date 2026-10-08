# MV Web Stable · P0/P1

项目目标：**在浏览器中通过 GitHub Actions 触发真正可下载的 MV 视频**，再升级为逐句镜头的云端生产线。

## 当前入口

[Actions → MV Web Stable P1 Smoke](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/workflows/mv_web_stable_smoke.yml)

1. 进入上述 Actions，选 Run workflow（main）。
2. 等待任务结束；进入具体 run，从 Artifacts 下载 `mv-web-stable-p1-<run-id>`。
3. ZIP 内的 `mv_2sec_smoke.mp4` 应为 **2 秒、1080×1920、30fps、有声** 视频；`smoke_report.json` 为机器验证报告，`smoke_preview.png` 为中间帧。
4. 测试音频是合成 440Hz 音调，**不包含《若爱有尽头》原曲**，避免把可能受版权保护的音乐提交到 public 仓库。

## 真实复用、而非冒充全新引擎

- Huashu 原 Skill: `alchaincyf/huashu-art-motion`，commit `26dba25b2b495c2138848c29a2c90df356a20325`。
- GitHub 内已有真实可运行 Skill 衍生工程：`08_AGENT_CONTROL_LAYER/pilots/CODE_MOTION_MV_RUN01_2026-10-06/engine/`。
- 原工程自带 `render.py`，它驱动无头 Chromium 的 JS Canvas `renderFrame(t)` 并通过 ffmpeg 编码；P1 **真正使用这个入口**，不拿 ffmpeg 生成纯色假成片。
- 当前 P1 的 `night` 是早期代码动画烟测场景，**不是下一版最终电影插画素材**。

## 阶段边界

- **P0**：目录、Skill 和素材/状态契约、带版本的 GitHub 云端入口。
- **P1**：公开 GitHub 仓库的 GitHub Actions 输出一条自检通过且可下载的 2 秒音视频 MP4。
- **P2**：按已锁定歌词时间轴，改成每句独立 scene/shot contract，做到单句重渲与自动拼接。
- **P3**：GPT 原生生图生成新导演资产，仓库只存授权素材或加密/私有引用；拒绝把 ChatGPT Plus 生图额度误认为 Actions API 额度。
- **P4–P5**：整片、导演复审、技术/艺术双门及稳定网页工作台。

**P1 PASS 的条件是 Actions 真实 successful run + 可下载 Artifact + `smoke_report.json` 校验通过。仅提交文件不是 PASS。**

## 安全/成本

此仓库是 public；不要提交原曲、私人原始媒体、密钥或服务凭证。Workflow 仅读取代码（`contents: read`）、无需 GitHub Secrets；优先使用托管 runner。视频仅作为短暂 Artifact 保留。

## 故障诊断

- 浏览器失败：查看 `Install pinned browser renderer` 步骤；
- 字体哈希失败：检查上游固定 commit 和 SHA；
- 渲染失败：检查 `Render actual Skill Canvas engine 2 seconds` 的 console/pageerror；
- 无声、帧数不等于 60 或持续时间不符：`verify_smoke.py` 会返回非零并在报告中记录原因；
- 未出现可下载 Artifact：检查 workflow 是否被 GitHub 禁用、是否具有运行权限。

项目状态以 `project_state.json` 和 GitHub Actions 的真实 Run 记录为准，不以聊天中的“已完成”判断。
