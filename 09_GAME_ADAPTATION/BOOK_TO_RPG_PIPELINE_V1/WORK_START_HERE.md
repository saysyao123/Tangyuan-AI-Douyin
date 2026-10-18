# 当前工程续作入口

先读 docs/T35_PROGRESS.md → evidence/T35_20261018/RELEASE.json，再按需要查 T34/T33 和 T19 原目标。不要用 CURRENT_STATUS 下方历史 T22 状态代替现状。

目标：完成第一幕四景、人物/NPC的高精细整合并可在线试玩，审美和玩法未验收前不宣称整体完成。当前室内已认可、第一幕效果获正面反馈；最新一轮已修复开场和中途旧画面闪回，等待用户在同一站点复验。

锁定：保留认可的室内与四景风格、重要人物唯一身份、原剧情/地图/碰撞/操作/SAVE12；不扩写后续剧情，不重跑未变旧测试，不覆盖原正式 Site 和 GitHub main。公开工程保留合成对白，不发布私有原书。

当前源码：feature/t35-no-legacy-flash-20261018。当前运行：t35-no-flash-final。Sites、版本、部署、完整包哈希和测试真值只从 RELEASE 读取。复建先运行 tools/t32/build.mjs，再运行 tools/t35/patch-loading-shell.mjs 输出目录。

试玩：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/
