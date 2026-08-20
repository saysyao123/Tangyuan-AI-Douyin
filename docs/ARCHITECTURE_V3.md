# Thin Skill Architecture v3.0

## Problem
旧架构已经出现典型上下文膨胀：流程、硬规则、视觉细节、Prompt、经验和项目状态交叉存在于MASTER_CONTROL、LOCKED_RULES、多个Harness与Visual System。文件越完整，运行时越容易读入无关内容，局部修改也越容易产生连锁影响。

## New Architecture
```text
SKILL.md                 # 薄Router
MANIFEST.md              # JIT加载矩阵
workflows/               # 一步一职责、Input/Output Contract
rules/                   # 唯一硬规则源
templates/               # 可复用结构/Prompt骨架
knowledge/               # 经验升级机制
tests/                   # 局部回归
00_CONTROL/CURRENT_STATE # 当前项目状态
02_DAILY/                # 每日产物/历史事实
05_IP_ASSETS/            # 设计资产与参考
```

## Dependency Direction
```text
State/Data → Workflow
Rules → Workflow
Templates → Workflow
Workflow → Deliverable
Knowledge → Rule Proposal
```

禁止反向：
- Workflow把长期规则复制回自己
- State写进Skill
- 单次Lesson直接写进Rule
- Template保存项目事实

## Module Size Rule
一个模块对应一个“可独立验收的决策”。不是按字数机械拆分，也不拆成碎片化微文件。

## Runtime Rule
默认只加载 `SKILL + MANIFEST + CURRENT_STATE + 当前模块所需文件`。完整SOP/历史Harness是Documentation/Reference，不是Runtime Context。

## Change Control
局部改动只修改对应模块；接口不变时，下游无需改动。若输入/输出Contract改变，必须更新MANIFEST与相关测试。

## Single Source
- 项目状态：`CURRENT_STATE.md`
- 项目定位/长期目标：`MASTER_CONTROL.md`
- 硬规则：`04_HARNESS/rules/*`
- 执行顺序：`04_HARNESS/workflows/*`
- 模板：`04_HARNESS/templates/*`
- 经验与实验：Daily Lessons / `03_DATA/EXPERIMENTS.md`

`LOCKED_RULES.md` 从规则正文改为规则注册表，避免复制。
