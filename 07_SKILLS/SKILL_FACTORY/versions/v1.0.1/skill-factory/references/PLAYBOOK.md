# 工厂操作手册 V1.0.1

## 证据与决策
G0 需求和技术来源：项目 URL、版本、许可证、实际源码路径、依赖、最小链路、风险。G1 工程：结构检查与接口实现。G2 真实用例：开发与封存分开；先固定验收规则，后写/优化产品。G3 演进：版本快照、同条件回归和回滚。G4 宿主/支付：独立真实运行、平台审核、费用和授权。G5 市场：真实非关联客户付费、退款及到账。E0/E1/E2/E3/E4 含义见原标准。V1 CLI 只实现 E0/E1、候选打包、同用例本地回归比较；G0 人工/Agent 研读、G2 独立模型对照和 G4/G5 仍需实际环境与证据。

## 本地接口
`init SPEC NEW_PROJECT` 创建 `manifest.json`, `skill/<slug>/`, `evals/`, `evidence/`, `listing/`，不覆盖已有项目。manifest 中 entrypoint 是 skill 目录相对路径。适配器 CLI：`python entrypoint request.json result.json workdir`；输入 JSON，输出 JSON，0 为成功，非零为有结构的失败。产物写到 workdir；不得覆盖原始输入。项目根为工作目录。产品必须在 README/runbook 给出具体调用方式。

`evals/cases.json` 包含 cases 数组：每个 case 有唯一 id、request、exit_code、expect（结果 JSON 精确键值）、critical（默认 true）、可选 oracle 对象。若配置 oracle，独立于适配器的 `evals/oracle.py` 接收 request、result、workdir、oracle JSON；0 代表断言全通过。oracle 需验证真实文件内容而非信任适配器输出。测试脚本和 oracle 只由已审查的可信代码提供。工具不是沙箱，运行权限与 Python 进程相同；拒绝不可信代码和敏感输入，使用宿主提供的隔离环境。运行时不自动下载、安装或访问网络；脚本的真实行为需事先审查。`--trusted-local` 是显式确认而非安全认证。

`check ROOT` 返回 E0；`evaluate ROOT --repeat 3 --trusted-local` 生成独立运行目录、日志、产物哈希和 JSON 报告；失败返回非零。`package ROOT OUT.zip` 在证据未过期、至少3个用例、通过率>=90%、无关键失败时打包本地候选，仅包含产品目录；不含 evals 或私有数据。`compare OLD.json NEW.json` 比较同产品、同测试及 oracle 哈希、运行条件下的通过率和回归；不自动修改文件。Agent 应保留旧快照以手动恢复。

## 独立 A/B 测试模板（未自动化）
固定宿主/模型/版本/预算/工具权限/同一输入；A 不加载 Skill、B 加载 Skill，C 原工具作为参考。隔离上下文，随机排序成果，独立评委核对文件/操作而非文档；记录各组原始输出、客观断言、时间、人工介入、实际费用。开发集>=10、封存集>=5、关键场景重复>=3；按基线阈值判断。没有独立运行不填造结果。原标准门槛不因 V1 工厂功能不足而降低。

## 商业化停止条件
任何未核实许可证、危险脚本、数据外发、隐性费用、宿主能力缺失、支付准入/退款/结算未知均阻断实际发布。仅制作候选包不构成商业验证。

## V1.0.1 证据增强
测试数据置于 evals/ 或 input_assets/；manifest、这些目录中的普通文件及产品文件均纳入一致性核对。禁止测试中修改这些内容。旧报告须重测。外部系统、依赖版本、环境变量及目录外部输入仍需单独记录；哈希不是签名或防篡改证明。无 oracle 的本地候选只检查结果字段，不能替代产品客观验收。
