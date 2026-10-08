# Work 接力入口 · GPT 原生生图（P2 艺术资产阶段）

请在真正的 ChatGPT Work 模式中执行，已授权 GitHub 仓库 saysyao123/Tangyuan-AI-Douyin (main)。这是 P2 新素材任务，不是重做 Run01 老代码风格视频。

## 从 GitHub 读取
- mv_web_stable/project_state.json
- mv_web_stable/p2/shot_contract.json
- mv_web_stable/p2/assets_manifest.json
- mv_web_stable/p2/GPT_NATIVE_ART_BRIEF.md
- mv_web_stable/p2/P2_EXECUTION_REPORT.md
- mv_web_stable/p2/EXPLAINROO_ADOPTION.md

## 明确目标
1. 调用 **GPT 原生生图**，不是第三方模型、不是把旧资源拉伸，不通过 Explainroo 默认 OpenRouter 生图。
2. 先生成同一女性角色的统一锚图，符合电影插画 A 冷蓝/琥珀、珊瑚红围巾的审美。
3. 先做四句关键画面 L01/L04/L07/L08；对 L07、L08 尤其提供前/中/后三张相同机位关键动作帧；每张单独输出。
4. 实际落地 PNG 后，登记路径、像素宽高、sha256、生成提示词、依赖参考与审美检查。不要生成就立即登记 PASS：逐张自检和审片后再置 READY。
5. 按照 Huashu Canvas 的分层需求输出独立背景 scene、角色 pose、物件，不把动作固化成无法分层的整图。保持相机克制。
6. 只有四组锚点通过，再补其余四句 L02/L03/L05/L06；任何未完成槽位继续 MISSING。
7. 构图与角色必须服务歌词，核心事件动作峰值绑定 shot_contract 的 cue，时间峰值当前为待试听验证的导演假设。
8. 最终输出可下载图片资产包，以及更新后的 GitHub assets_manifest.json；不要宣称已经有完整 MV，直到云端实际渲染/验收。

## 先前实测可用的环节
GitHub Actions P1 云端 H264+Aac 实测通过；
P2 L03 单句隔离测试 run 37724566599 已通过（旧资产技术演练）。
正式图片生成与成片尚未完成，不能误用这些历史阶段状态。
