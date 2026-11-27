# SF-P002｜VoiceScript 中文知识口播改写

2026-11-27 正式立项，工厂稳定版本 V1.0.1。当前候选 V0.1.1，E1 作者同会话试运行，不代表独立宿主或商业验收。唯一功能：已有中文原稿→自然、准确、可直接朗读的普通话单人口播。默认不增事实、不查证、不生产标题、选题、配音或视频。无需核心第三方 API/服务器；宿主模型额度仍适用。

## 三源固定版本

| 项目 | commit | 许可证 | 提炼能力 |
|---|---|---|---|
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh/tree/f4518a8eab97b8bfebc66a89d34320a89bef6930) | f4518a8eab97b8bfebc66a89d34320a89bef6930 | MIT | 语义保护与编辑判断 |
| [humanizer-zh-speech](https://github.com/KyrieHuang/humanizer-zh-speech/tree/4009329e733de802a363c6222efd105c9f32e0f8) | 4009329e733de802a363c6222efd105c9f32e0f8 | MIT | 口播语域、意群与节奏，台湾语料不直接迁移 |
| [Podcastfy](https://github.com/souzatharsis/podcastfy/tree/053b54a0917e35edb2808049499292361ccaae7b) | 053b54a0917e35edb2808049499292361ccaae7b | Apache-2.0 | 听众视角、内容连贯，不引入完整程序/API |

内部方法：04_HARNESS/KNOWLEDGE_SCRIPT_HARNESS.md（commit 363cf6d3447b4e12eb93b119c0fc5b4a56ed635c）。顶层许可证已查；未作完整商业分发权利审计，未打包上游语料或程序。

## 版本与测试

- V0.1.0：先固定10个原创开发任务，再产出文本；字面必要断言 10/10，作者语义复核发现适用群体、计划状态和限时估算问题。
- V0.1.1：修改相应规则，局部修复3个稿件，保留其余7个，文本回归断言 10/10；结构检查 8/8，ZIP 独立解压、YAML、发布包范围检查通过。非独立模型重新运行；未验证真实朗读时长。不得将字面通过率视为任务质量或能力增量通过率。
- 尚未运行独立 A/B/C/D、封存、三次重复、消融、真人盲听、目标宿主、SkillPay 支付；未发布。

## 交付资产（会话文件，未公开上传）

- VoiceScript_V0.1.1_Trial.zip；SHA-256 396f22c18c310423f459b6b46cd004c88397092371e6c2651b316803e2af0956。
- VoiceScript_SF-P002_Development.zip；SHA-256 0ec3f43b7095a4deca830b6f6b9d75a1c75d5df0284c12a1e6ef79b79286a806。包含开发任务、原始文本、检查程序、版本修复记录和独立评测手册。

## 工厂反馈候选

三源互补、固定 commit、来源矩阵、冲突仲裁及消融应成为候选工厂规范；知识型 Skill 需要独立模型运行及评委，字面程序检查不能替代语义和听觉验证。先验证 VoiceScript 效果，再决定是否修改母工厂；稳定版本不变。
