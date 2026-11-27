# Skill Factory V1.0.1 | 独立母 Skill

## 使用
支持 Agent Skills 的宿主：按该宿主的 Skill 安装方法导入 `skill-factory/`（保留目录结构）。不支持安装的宿主：上传本 ZIP，要求读取 `skill-factory/SKILL.md` 并执行。能读取 ZIP 不等于能运行 Python、联网或自动触发。

最短调用：**调用 Skill Factory，把这个 GitHub 项目制作成可实测的 Skill：https://github.com/owner/repo**。

没有 GitHub 链接也可输入明确需求；工厂应先筛选项目。现有 Skill 可用于审核和优化。默认不产生额外现金费用、不公开发布、不外发数据。

本地预检（从本目录）：`python scripts/selftest.py`，Python 3.10+，控制器与自测只使用标准库；不会自动安装依赖或联网。产品可能需要独立依赖。详细接口见 references/PLAYBOOK.md，锁定门槛见 references/STANDARD_V0.1.md。

输出独立子 Skill、开发工程、来源记录、实测证据、版本和未通过关卡。母 Skill 不依赖历史对话。当前为 E1 本地原型；并非已安装在任何账户，不承诺任何宿主自动触发或独立 A/B 成功。V1.0.1 修订见 CHANGELOG.md。
