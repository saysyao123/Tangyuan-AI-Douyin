# AI Digital Asset Factory：统一执行入口

适用于 ChatGPT 网页端、Codex、Work。三种入口是同一个项目的执行环境，使用同一仓库、同一目录、同一状态。

- 仓库：`saysyao123/Tangyuan-AI-Douyin`
- 分支：`main`
- 唯一项目根目录：`10_DIGITAL_ASSET_FACTORY/`
- 项目标识：`AI_DIGITAL_ASSET_FACTORY`

## 每轮必须读取

1. [PROJECT_CONTRACT.md](PROJECT_CONTRACT.md)：当前目标、分工和商业验收规则。
2. [PROJECT_STATE.json](PROJECT_STATE.json)：唯一当前状态、已验事实、阻塞和下一任务。
3. [AGENTS.md](AGENTS.md)：所有执行环境共用的读写与交接规则。
4. [ASSET_REGISTRY.md](ASSET_REGISTRY.md)：真实资产、版本、哈希和私人交付说明。
5. [PROJECT_EXECUTION_PLAN.md](PROJECT_EXECUTION_PLAN.md)：完整路线、候选顺序、试销实验、收款模型和停止条件。
6. [EXECUTION_CHECKLIST.md](EXECUTION_CHECKLIST.md)：按顺序的人机分工、完成节点与进度快照。
7. 仅按当前任务读取关联证据：
   - [完整方案补充证据](research/CYCLE08_PLAN_EVIDENCE.md)
   - [历史目标与分工核对](research/CYCLE07_HISTORY_AND_ROLE_AUDIT.md)
   - [平台规则复核](research/CYCLE06_PLATFORM_RULES_AUDIT.md)
   - [7个AI变现公共仓库与1个设计项目](research/CYCLE06_OPEN_SOURCE_REVIEW.md)
   - [设计质量门槛](DESIGN_QUALITY_GATE.md)
   - [决策日志](DECISIONS.md)

[PROJECT_MASTER_PLAN_V1.md](PROJECT_MASTER_PLAN_V1.md)保留为历史总控和索引，不再把其中不同日期的“当前下一步”当作并列指令。Cycle04/05、旧Work启动文件、旧操作卡和私人ZIP内文案均是相应日期快照。当前状态以 `PROJECT_STATE.json` 为准，当前规则以 `PROJECT_CONTRACT.md` 为准；用户当轮明确指令优先，并须记录变更。

## 当前最重要的事实

截至2026-10-28，尚未证实一条满足全部条件的盈利渠道。完整中英文PPTX已私人交付，但平台AI准入、买家授权、本人结算与自然订单仍未全部通过。不能因已有成品或账号注册而跳过市场验证。

当前核验顺序：先查MotionElements与现有英文PPT的适配及本人收款，同时补一个国内候选；这是核验优先级，不是已通过上架。公开单席位许可在一名使用者为自己/雇主制作报告的范围有依据；实际商品审核、最终收款与自然需求仍未知。Payoneer可能有固定/年费，不能默认免费开户即可无成本收款。完整安排见项目执行方案。

历史纠偏继续保留：原创力普通非独家及人民币结算有官方依据，但AI收费准入没有找到明确许可；买家使用授权另有待确认条款。因此从“国内第一测试候选”降为“待规则确认候选”，不要求用户盲目上传。MotionElements的AI及非独家公共规则较清楚，最终提现与自然订单仍未知。

## 通用续作指令

> 继续同一个 AI Digital Asset Factory 项目。读取 `saysyao123/Tangyuan-AI-Douyin` 的 `main` 分支 `10_DIGITAL_ASSET_FACTORY/START_HERE.md`，按其顺序读取当前合同、状态、执行规则和资产登记。先报告状态 revision 与唯一下一任务，然后直接完成当前环境能独立完成的工作。不要另建网页端/Codex/Work项目，不从头制作已有商品，不恢复历史已否决路线。完成后以最新GitHub内容和SHA为依据更新同一状态与证据。完整待售商品留在私人附件中。

无法读取仓库时，明确标记“未同步”，可准备增量补丁；不得声称已检查最新状态或把本地副本称作新的权威项目。
