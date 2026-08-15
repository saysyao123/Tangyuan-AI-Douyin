# CODEX_DEPLOY_INSTRUCTIONS

目标仓库：`https://github.com/saysyao123/saysyao123-Tangyuan-AI-Douyin`

## 目标
将本包 `Tangyuan-AI-Douyin/` 目录内部全部内容原样部署到目标GitHub Public Repository根目录。

## 原则
- 保持目录结构
- 不删除现有项目文件，除非确认只是测试残留
- 不上传Key/Token/Cookie/密码/私密账号信息
- 不上传未脱敏隐私素材
- 大型视频/音频/图片不要批量推入Git
- 不自行修改账号定位、第一季目标、已锁定规则

## 建议命令
```bash
git clone https://github.com/saysyao123/saysyao123-Tangyuan-AI-Douyin.git
cd saysyao123-Tangyuan-AI-Douyin
# 将本包 Tangyuan-AI-Douyin/ 内部全部文件复制到当前仓库根目录
git status
git add .
git diff --cached
git commit -m "chore: initialize Tangyuan AI Douyin project control system"
git push
```

## 推送前验收
必须存在：README、MASTER_CONTROL、CURRENT_STATE、TOPIC_POOL、DAY_00、DAY_01、ACCOUNT_GROWTH、KNOWLEDGE_SCRIPT_HARNESS、ACCOUNT_POSITIONING、DAILY_EXECUTION_START、99_INBOX。

## 安全扫描关键词
`sk-` / `token` / `api_key` / `apikey` / `password` / `cookie` / `authorization` / `bearer` / `secret` / `手机号` / `身份证`

命中后人工判断并删除敏感内容。

## 部署后回传
- commit SHA
- branch
- 最终文件树
- git status是否clean
- 是否发现冲突
- 是否发现敏感信息
