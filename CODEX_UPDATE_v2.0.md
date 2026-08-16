# CODEX_UPDATE_v2.0

目标仓库：

`https://github.com/saysyao123/Tangyuan-AI-Douyin`

## 任务

将本补丁包按相同相对路径合并到仓库。

## 极重要：不要无脑覆盖实时数据

当前ChatGPT无法直接读取GitHub远端HEAD。

因此以下文件必须采用：

**remote-newer-data-wins**

如果远端已经有真实的：
- 发布时间
- Post URL
- 播放
- 点赞
- 评论
- 收藏
- 分享
- 新增关注
- 粉丝数
- 完播率
- 平均观看

必须保留远端真实值，不得用本补丁中的空字段覆盖。

涉及：
- `00_CONTROL/CURRENT_STATE.md`
- `02_DAILY/DAY_01/PUBLISH.md`
- `02_DAILY/DAY_01/METRICS.md`
- `03_DATA/VIDEO_PERFORMANCE.csv`

## 新增/可直接采用的规范文件

- `04_HARNESS/AUDIO_PRODUCTION_HARNESS.md`
- `04_HARNESS/AI_VIDEO_HARNESS.md`
- `05_IP_ASSETS/PUBLISH_SYSTEM.md`
- `02_DAILY/DAY_01/PRODUCTION/*`
- `99_INBOX/DAY_02_START_PACKET.md`
- `99_INBOX/DAY_01_HANDOFF_FINAL.md`
- `REPOSITORY_UPGRADE_v2.0.md`

## 重点升级

- `00_CONTROL/LOCKED_RULES.md`
- `04_HARNESS/VIDEO_PRODUCTION_HARNESS.md`
- `05_IP_ASSETS/VISUAL_SYSTEM.md`
- `06_TEMPLATES/DAY_FOLDER_TEMPLATE.md`
- `06_TEMPLATES/DAILY_EXECUTION_START.md`

如果远端已有v1.1规则，不要删除v1.1中与v2.0不冲突的Source of Truth治理内容。

## 推荐执行流程

```bash
git pull --ff-only
git status

# 解压本patch到临时目录
# 逐文件比较，不要直接覆盖实时数据字段

git diff

# 处理CSV时：
# 如果远端Day1已有真实数据，保留真实数据，只补充新schema/状态/Notes

git add .
git diff --cached

git commit -m "docs: upgrade Day1 learnings into production harness v2"
git push

git status
```

## 合并后检查

必须确认：

- Day1状态不再是 production
- CURRENT_STATE不再写“下一步最终口播验收”
- Day1为 published_metrics_pending 或更晚状态
- 114.726s final record存在
- Production / Performance验证区分存在
- AUDIO_PRODUCTION_HARNESS存在
- AI_VIDEO_HARNESS存在
- Day1 PRODUCTION/存在
- DAY_02_START_PACKET存在
- 远端已有真实数据没有被空值覆盖

## 返回

- branch
- commit SHA
- changed files
- conflict resolution
- preserved remote metrics
- git status
