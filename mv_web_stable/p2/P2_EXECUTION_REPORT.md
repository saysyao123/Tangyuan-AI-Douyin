# P2 实测结果 · 独立歌词镜头出片技术测试
时间：2026-10-08
GitHub successful Actions run: https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37724566599
Artifact: p2-lyric-L03-37724566599 (id: 11527580905).

## 本轮执行了什么
- 在 main 分支确认八句歌词独立镜头契约，固定全片 641 帧@30fps。
- Run 默认选中 L03「我该如何拼凑」；从全片绝对时间区间 5.75–8.00s 取片。
- 通过原 Huashu Skill 衍生 Canvas 的 render.py 实际渲染，不是用 ffmpeg 合成静态占位图。
- 安装 Chrome/FFmpeg/字体后通过所有步骤：结构校验 / 无敏感音频的 21.36s 合成参考音 / 分段出片 / 全解码 / 中点静帧 / Artifact 上传。

## 实测结果
L03 以 Python round() 的帧网格计算：start_frame=172，end_frame=240，输出 68 帧、1080×1920、30fps、H264/AAC，全部机器检查 true。
全片正确帧预算（Python round）：L01 75、L02 97、L03 68、L04 82、L05 90、L06 76、L07 74、L08 79，共 641 帧。
注意：Python round 与 JS Math.round 在 *.5 ties 情况不同，任何正式工程必须锁定同一帧量化算法。此处以 Cloud 实测 Python 结果为权威。

## 本轮不成立的事项
- L03 片段采用 **P1 旧代码风格**，只是隔离渲染的 REHEARSAL；不是重新 GPT 生图的高精度 MV。
- 8 个镜头的新 GPT 生图全为 MISSING，艺术 Gate 未通过。
- 主音轨不是原曲：本公开仓库仅用合成音频避免公开音乐源文件。
- 全片带新素材的正式动作和切镜尚未制作；不会假称 P2 已完整通过。

## 下一步
由具备 GPT 原生生图能力的 ChatGPT / Work 会话按 GPT_NATIVE_ART_BRIEF.md 先生成并锁定 L01/L04/L07/L08 新图，再补齐全八句；严格经 assets_manifest.json 的 sha256 / 像素 / 审美 Gate 才能进入 P3 动画合成。
