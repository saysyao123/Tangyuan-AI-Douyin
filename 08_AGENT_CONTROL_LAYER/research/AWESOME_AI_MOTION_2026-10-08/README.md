# Awesome AI Motion 深度学习档案

本档案把 [guanmo-ai/awesome-ai-motion](https://github.com/guanmo-ai/awesome-ai-motion) 的固定版本整理为可追踪的学习资料，重点服务 Tangyuan-AI-Douyin 的角色动作、镜头和音画同步问题。研究日期：2026-10-08（UTC）；上游提交：`e8df52d548fa6f15acc39098e6a0bf3df1651309`。

**已覆盖全部 581 条目录记录、1,943 个跟踪文件、128 段内联指令／任务描述及 90 条资源关联。** 每条案例都有来源、资料状态、学习问题和建议检验。全部 581 张封面缩略图已查看。39 个关联仓库检查了 README，14 个关键源码／导演文档作了重点深读。

**本轮尚未逐部看完 581 个视频、听完全部音轨，亦未独立重建外部工程。** 完整提示词缺失、页面取回与媒体失效均留在状态表中；全目录覆盖不等于全片复现完成。

项目的核心是“可信目录 + 静态画廊 + 维护工具”，不是一套能统一重建所有案例的视频引擎。对本项目最有价值的是：音画共享主时钟；世界到画面的变换只做一次；先检查关键动作与接触，再加纹理、转场和镜头；短样通过后再投入全片渲染。

**网页端使用：** 上传 [WEB_MV_EXPERIENCE_HANDOFF.md](WEB_MV_EXPERIENCE_HANDOFF.md)，同时提供本轮音频和角色素材，再粘贴其中的启动消息。文件包含精简经验、能力验证、短样验收和后续记录方式。

## 阅读入口

| 内容 | 文件 |
|---|---|
| 架构、数据与维护机制 | [01_PROJECT_ARCHITECTURE.md](01_PROJECT_ARCHITECTURE.md) |
| 所有文件的覆盖方式与模块分析 | [02_FULL_FILE_REVIEW.md](02_FULL_FILE_REVIEW.md) · [FILE_INVENTORY.jsonl](FILE_INVENTORY.jsonl) |
| 七类作品的学习方法 | [03_CATEGORY_LESSONS.md](03_CATEGORY_LESSONS.md) |
| 具体引擎和源码机制 | [04_ENGINE_DEEP_DIVE.md](04_ENGINE_DEEP_DIVE.md) |
| 如何用于汤圆项目 | [05_TANGYUAN_ADOPTION.md](05_TANGYUAN_ADOPTION.md) |
| 检查结果与未完成范围 | [06_TEST_AND_COVERAGE.md](06_TEST_AND_COVERAGE.md) |
| 39 个关联仓库逐项技术笔记 | [07_RESOURCE_LESSONS.md](07_RESOURCE_LESSONS.md) |
| 全部外链与许可条件 | [RESOURCE_REVIEW.md](RESOURCE_REVIEW.md) · [RESOURCE_STUDY_INDEX.jsonl](RESOURCE_STUDY_INDEX.jsonl) |
| 指令的组织方式与缺失项 | [PROMPT_STUDY.md](PROMPT_STUDY.md) · [PROMPT_STUDY_INDEX.jsonl](PROMPT_STUDY_INDEX.jsonl) |
| 581 条案例机器索引 | [CASE_STUDY_INDEX.jsonl](CASE_STUDY_INDEX.jsonl) |
| 冻结版本和状态 | [SOURCE_SNAPSHOT.json](SOURCE_SNAPSHOT.json) · [RESEARCH_STATUS.json](RESEARCH_STATUS.json) |
| 可重复覆盖验证 | [verify_research.py](verify_research.py) · [evidence/ARCHIVE_VERIFICATION.json](evidence/ARCHIVE_VERIFICATION.json) |

## 逐项阅读

| 分类 | 条目 | 笔记 |
|---|---:|---|
| 产品宣传 | 110 | [逐项记录](cases/01.md) |
| 叙事短片 | 96 | [逐项记录](cases/02.md) |
| 3D 与交互 | 113 | [逐项记录](cases/03.md) |
| 短动效 | 74 | [逐项记录](cases/04.md) |
| 知识讲解 | 97 | [逐项记录](cases/05.md) |
| 像素与角色 | 39 | [逐项记录](cases/06.md) |
| 音乐与歌词 | 52 | [逐项记录](cases/07.md) |

类别编号由目录首次出现顺序生成，以最终类别标题和统计为准。案例中的“学习问题／建议检验”属于从主题和可得指令提炼的研究假设；没有源码或运行结果时，不猜测作者实现。作者成本、模型名与制作时间按来源声明处理，不当作本次测量。

## 归档边界与署名

只添加研究文件，不改变已经锁定的音频、镜头规则、生产技能或交付状态。学习假设按本仓库 `experiment → receipt → review → regression → promotion` 的路径验证后才有资格进入生产。

上游自编分类、标题、简介和实现说明来自上述固定版本，遵循其 [MIT 许可](https://github.com/guanmo-ai/awesome-ai-motion/blob/e8df52d548fa6f15acc39098e6a0bf3df1651309/LICENSE)；许可文本与本次整理的署名见 [NOTICE.md](NOTICE.md)。作者视频、音轨、封面、长提示词及外部仓库源码没有镜像到本档案。第三方内容仍以原作者和独立许可为准。
