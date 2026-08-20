# Workflow｜Topic Selection v1.0

## Responsibility
只负责从候选池选出当天唯一主选题，不负责写Hook、脚本或导演表。

## Input Contract
- 当前账号/第一季目标（需要时加载）
- 历史真实项目池
- 用户问题池
- 24小时热点池（如有）
- 当前可用真实证据
- 当天生产预算

## Process
1. 去除已做过且无新信息差的题。
2. 真实性 Gate。
3. IP匹配 Gate。
4. 观众价值 Gate。
5. 关注理由 Gate。
6. 证据可得性 Gate。
7. 生产可行性 Gate。
8. 选出唯一主选题，并写明为什么现在做。

建议评分：真实性20、受众痛点20、IP匹配15、关注转化20、证据10、故事性10、生产可行性5。

## Output Contract
必须只输出：
- `TOPIC_ID`
- `TOPIC`
- `WHY_NOW`
- `AUDIENCE_PROBLEM`
- `EVIDENCE_AVAILABLE`
- `CORE_PROMISE`
- `PRODUCTION_RISK`
- `STATUS = TOPIC_LOCKED`

## Gate
- 不因“热点”自动覆盖更强真实题。
- 制作中途不换题，除非出现明显高价值新证据。
- 未锁选题，不进入 Script Workflow。
