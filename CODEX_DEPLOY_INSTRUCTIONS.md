# CODEX / Agent Runtime Instructions v3.0

目标仓库：`saysyao123/Tangyuan-AI-Douyin`

## 不要这样启动
不要一上来全文读取整个Repo、全部Harness、全部Daily、全部IP Visual文档。这样会造成上下文膨胀和规则冲突。

## 正确启动
```text
1. 读取 04_HARNESS/SKILL.md
2. 读取 04_HARNESS/MANIFEST.md
3. 读取 00_CONTROL/CURRENT_STATE.md
4. 判断当前任务
5. 按 MANIFEST 只读取对应 workflow + rules + template
6. 完成当前模块并通过Gate后，再加载下一模块
```

## Change Discipline
- Workflow只写流程和Input/Output Contract。
- Rule只写长期可验收约束。
- Template只写复用骨架，不保存项目状态。
- 单次经验进入Daily Lessons / Experiments，不直接塞进Skill。
- 修改局部模块时，不重写无关模块。
- Contract改变时同步更新MANIFEST与Tests。

## Git Safety
- 不自行修改账号定位、第一季目标、已锁定规则。
- 不提交Key/Token/Cookie/密码/私密账号信息。
- 不上传未脱敏隐私素材。
- 大型视频/音频/图片不要批量推入Git。
- 提交前检查diff，只提交本任务相关路径。

## Architecture References
- `docs/ARCHITECTURE_V3.md`
- `docs/MIGRATION_V3.md`

## Legacy
旧 `04_HARNESS/*_HARNESS.md` 是迁移期参考，不属于默认运行上下文。只有缺少细节、追溯来源或回归测试时按需读取。
