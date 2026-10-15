# Work-Fisher Skill V1 — 主视频生成方案

**政策**：2026-10-15 起设为仓库视频生成项目的默认核心 Skill。**先使用原版验证，后按结果调整**，不在基线测试前重构提示词规则。

## 直接入口
- [START_WEB.md](START_WEB.md)：给 GPT 网页端 / Work / Codex 的新对话入口
- [WORKFLOW.md](WORKFLOW.md)：执行阶段与审批边界
- [QA.md](QA.md)：真实结果及验证级别
- [state/PROJECT_STATE_TEMPLATE.json](state/PROJECT_STATE_TEMPLATE.json)：每个书籍/视频单独建立状态，不继承示例角色
- [original/korean-thriller-asset-to-video/SKILL.md](original/korean-thriller-asset-to-video/SKILL.md)：原版核心 Skill
- [original/korean-thriller-asset-to-video/references/video-contract.md](original/korean-thriller-asset-to-video/references/video-contract.md)：原版视频格式、语音与机位规范
- [original/comfyui/【Work-Fisher】AI短剧制作全流程.json](original/comfyui/【Work-Fisher】AI短剧制作全流程.json)：原始 ComfyUI 工作流
- [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md)：原版文件清单及来源、完整度状态

## 阶段工作法
| 阶段 | 交付 | 过门条件 |
|---|---|---|
| 0 剧本拆解 | 原著/用户素材、选段、人物与事件顺序 | 不擅自改写事实剧情 |
| 1 角色提示词 | 逐角色中文生图词 | **用户明确确认整批角色** |
| 2 场景与道具提示词 | 无人场景和必要独立道具 | **用户明确确认整批场景** |
| 3 资产检视 | 实际生成图片、ID映射、冲突说明 | **收到并实际检查可用参考图** |
| 4 视频提示词 | 15秒、3–4镜头、1–2个A/B机位、固定五字段 | 对照原文和参考图结构核验 |
| 5 视频生成 | 真正的视频文件/模型设置/失败记录 | 不存在即不可称已出片 |
| 6 后期与验收 | 实际MP4、音轨、剪辑、质检证据 | 经实际播放/规格检查；效果基于人眼验收 |

原版 Skill 实际只定义了「角色→场景→参考图→视频提示词」三阶段；阶段 0、5、6 为本仓库围绕**真正成片**增加的外围流程，不擅自写回原版文件。

## 命名规范
角色 `C01`，角色衣着版本 `C01-V01`，场景 `E01`，关键道具 `P01`，Speaker `S1`。每个项目的资产、版本、状态独立；任何镜头不得借用另一作品的图像或角色状态。

## 禁止虚报
- 自定义 Skill 并非在 ChatGPT 已注册安装的系统工具；GitHub 文件是执行规范。
- 历史 ComfyUI 预览不是本项目的生成成功证据。
- 离线 QA、JSON 已上传不代表实际渲染通过。
- 公开仓库不得保存未授权的整本书、受限原著素材或私人账号信息。

