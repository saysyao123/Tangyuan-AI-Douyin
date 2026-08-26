# CODEX_DEPLOY_INSTRUCTIONS

目标仓库：`https://github.com/saysyao123/Tangyuan-AI-Douyin`

> Status: historical bootstrap / maintenance reference.  
> The repository is already initialized and public; this file is retained for deployment and repository-hygiene guidance, not as the current production runtime entry point.

## 当前推荐入口

- 默认仓库入口：`README.md`
- 当前 R3 MV 生产 Runtime：`test/mv-web-r3`
- 新 MV 零上下文入口：`05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`（R3 branch）
- 权威 MV workflow：`04_HARNESS/workflows/mv.md`（R3 branch）

## 部署 / 同步原则

- 保持目录结构；
- 不删除现有项目文件，除非确认只是测试残留或已有迁移计划；
- 不上传 Key / Token / Cookie / 密码 / Session / 登录凭证；
- 不上传未脱敏隐私素材；
- 大型视频、音频、图片原则上只保存索引、hash、时间轴、QA 与 provenance，不直接批量推入 Git；
- 不自行修改已锁定的账号定位、Gate、Runtime authority 或生产规则；
- 实验性规则必须先保留为 experiment / knowledge，再通过证据和回归晋升。

## 建议 Git 流程

```bash
git clone https://github.com/saysyao123/Tangyuan-AI-Douyin.git
cd Tangyuan-AI-Douyin

git status
git switch -c <focused-branch>
# make focused changes
git add .
git diff --cached
git commit -m "<type>: <focused change>"
git push -u origin <focused-branch>
```

优先通过小范围 PR 合并，不把不相关的 runtime / docs / experiment 修改堆在同一个提交中。

## 推送前安全扫描

至少检查：

`sk-` / `token` / `api_key` / `apikey` / `password` / `cookie` / `authorization` / `bearer` / `secret` / `sessionid` / `手机号` / `身份证`

命中后必须人工判断；敏感信息禁止提交。

## OSS 维护要求

- authoritative rule 变更说明受影响 Stage；
- 实验结果保留 evidence / receipt；
- 局部失败优先 local patch，不无原因 cascade rewrite；
- 规则晋升前检查 regression；
- README / ROADMAP / CONTRIBUTING 与实际 Runtime 保持一致。
