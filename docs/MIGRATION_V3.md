# Migration Guide｜v2 Harness → v3 Thin Skill

## Migration Strategy
采用渐进式迁移，不删除旧Harness，先切断默认运行依赖。

## Runtime入口变化
旧：`MASTER_CONTROL → 各大HARNESS全文`  
新：`SKILL → MANIFEST → 当前Workflow + Rules + Template`

## Legacy Files
现有 `04_HARNESS/*_HARNESS.md` 与 `05_IP_ASSETS/VISUAL_SYSTEM.md` 继续保留，用于：
- 历史追溯
- 未迁移细节查询
- 设计参考
- 回归核对

它们**不再是默认Runtime入口**。若与新 `rules/*` 冲突，以新规则文件为准。

## Migrated Authority
- `KNOWLEDGE_SCRIPT_HARNESS` → `workflows/script.md`
- `TOPIC_SELECTION_HARNESS` → `workflows/topic.md`
- `AUDIO_PRODUCTION_HARNESS` → `workflows/audio.md` + `rules/production_core.md`
- `VIDEO_PRODUCTION_HARNESS` → `workflows/director.md` + `workflows/production.md`
- `AI_VIDEO_HARNESS` → `rules/ai_video.md`
- `HYPERFRAMES_EXPLANATION_HARNESS` → `rules/hyperframes.md` + scene template
- `LOCKED_RULES`正文 → `rules/account_truth.md` / `production_core.md` / `visual_core.md`

## What Is Intentionally Not Migrated Yet
以下细节先留作Reference，不进入默认上下文：
- HyperFrames完整Blueprint清单
- 详细Asset Registry字段
- 大量视觉配色/美术解释
- 历史案例长说明
- 旧版本演进记录

后续只有当某类细节在多个任务中稳定复用时，才提炼成小规则或模板。

## Cleanup Trigger
满足以下条件后才物理归档/删除Legacy大文件：
1. 新架构连续跨至少3条视频运行稳定；
2. 所有需要的历史细节已有明确去向；
3. Runtime tests无回归；
4. 人工确认不再需要旧入口兼容。
