# DECISIONS

## D001–D009
沿用仓库现有历史决策，不在本补丁中重写。

## D010｜建立两级验证制度
日期：2026-08-16

结论：

所有经验区分：
- PRODUCTION_VALIDATED
- PERFORMANCE_VALIDATED

原因：

Day1已证明很多规则能提升生产稳定性，但尚未证明114秒、AI Hook等一定提升抖音表现。

## D011｜Video Production Harness升级至v2.0
日期：2026-08-16

结论：

生产改为Gate流程：

TOPIC → SCRIPT → AUDIO → TRANSCRIPT/TIMELINE → DIRECTOR → ASSET → SEGMENT → QA → FULL CUT → FULL QA → PUBLISH → REVIEW。

## D012｜真实音频先于最终导演时间轴
日期：2026-08-16

原因：

Day1主体实际音频为78.799秒，后追加Hook/Outro后最终成片约114.726秒，证明文稿估算秒数不能作为正式制作基准。

## D013｜Day目录增加PRODUCTION子目录
日期：2026-08-16

目的：

把音频锁定、实际时间轴、生产日志、QA和经验从聊天中沉淀出来，不污染主Day文件。

## D014｜Day2优先效率实验
日期：2026-08-16

Day2不追求比Day1更复杂。

默认实验：
- 45–65秒
- 5–7个语义段
- 真实证据 + Remotion
- AI概念镜头0–1条
- 总生产目标≤180分钟

这只是Day2生产实验，不是长期内容时长规则。
