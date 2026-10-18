# 当前工程续作入口

先读 docs/T36_PROGRESS.md → evidence/T36_20261018/RELEASE.json，再按需要查 T35/T34/T33 与 T19 原目标。不要把 CURRENT_STATUS 下方历史阶段当现状。

目标：在现有真实 Type PAL 工程上完成高精细美术、人物/NPC与可玩的在线游戏；审美和玩法未验收前不宣称整体完成。用户已认可室内、对第一幕正面反馈，T35修复旧图闪回；2026-10-18 22:27明确授权现有第二幕按相同标准优化，T36本轮已上线，等待用户复验。

本轮第二幕覆盖雪夜街道、便利店、意识空间、雪院及专属司机/店主/受伤动作；家中和第一幕保持。锁定原剧情/地图/碰撞/脚点/寻路/操作/SAVE12，重要人物唯一身份；不扩写不存在的后续章节、不重复未变旧测试、不覆盖原正式Site或GitHub main。公开工程用合成对白，不发布私有原书文本。

当前源码 feature/t36-second-act-style-20261018；最终运行 t36-night-candidate@4abf3c935fb7efa67b9ad32bc907d374062a2c38。Site/版本/部署、包哈希及测试真值从 RELEASE 读取。复建先 tools/t32/build.mjs，再 tools/t35/patch-loading-shell.mjs。仅当提交标记 [snow-only] 时，T36工作流只跑雪院影响范围；其他改动默认四景受影响测试，须按真实改动选择范围，不能漏验。

第二幕：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/night/
第二幕对照：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/review/act2.html
连续试玩：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/
