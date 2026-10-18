# T36｜第二幕按已认可风格优化并发布

2026-10-18。22:27（Asia/Shanghai）用户要求第二幕按当前标准优化；23:06追问是否卡住时，第二幕本轮优化已发布，余下交接归档随后完成。原目标仍是高精细、可玩、可在线测试的实际游戏，不能以技术绿灯或概念素材替代画面验收。

本轮覆盖现有 night-road、night-shop-room、mind-tree、snow-yard；已认可 home-room 及第一幕保持。新增42张lossless栅格：便利店/货车/雪人与足迹、店内墙与陈列、意识树与抽取物件、专属司机/店主/头像和主角受伤姿态，以及司机四向三阶段步态。203张已认可图片、109个原生工程文件、家中显示模块保持。没有改剧情、地图、碰撞、物品/货币、SAVE12或写新章节。

首轮实机四景状态/点击八项通过，但司机原始 visitor 是静态 layout，新动作一直取同一帧，断言失败。改为显示元数据读取已有移动步相，未更改原生运动。人工另发现事故演员被下方对白遮住、旧方块标记和墙外重复柜；均已显示层修正。Run39137781144 十三项第二幕受影响检查 PASS、零pageerror，实际货车/白火/司机离场、店主购买与头像、一次原生抽取、两雪人和存档重开均验证。原完整第二幕12项机制检查复用 Run38977914977，没有再跑七抽全流程或其他未变旧套件。

完整通过后仍从实际截图发现小雪人下半身被前墙遮住，最终只缩小 snow-yard 墙（112→84），Run39138209265 仅补四项院内显示、点击、雪人和存档检查 PASS。最终截图确认两个雪人与孩子脚部清楚，未把首轮技术通过版直接当最终交付。

当前已成功发布：
- [第二幕新开局](https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/night/)，从家中按右侧目标推进。
- [第二幕实机对照](https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/review/act2.html)，含四景前后、真实人物演出与最终雪院录像。
- [从第一幕连续游玩](https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/)。

完整网页包已更新同一文件第5版，包含两幕，161875419 bytes，SHA256 650ef1bbf44079b2ac7e16d495cb92944ab23455a12165f6a24496297b39b337。380个游戏文件与最终CI逐字节一致，1013项运行清单、相对链接和本地下载哈希通过。实际发布/源码/运行提交/版本/部署真值见 [RELEASE.json](../evidence/T36_20261018/RELEASE.json)。

源码 feature/t36-second-act-style-20261018；最终运行 t36-night-candidate@4abf3c935fb7efa67b9ad32bc907d374062a2c38。复建仍先 tools/t32/build.mjs，再 tools/t35/patch-loading-shell.mjs。新 night-world.ts 只做显示，所有场景共用 T35 素材解码提交门槛。司机/店主以原实体ID分别绑定，不在普通NPC中复用重要人物。美术来源见 [T36_ART_BRIEF.md](T36_ART_BRIEF.md) 与 art/t32/T36_ASSET_PROVENANCE.json。

后续先收用户实际反馈，再只修改未通过部分；不重做已认可家中/第一幕，不扩写未授权后续章，不重跑未变旧测试，不覆盖原正式Site/main。第二幕最终审美与玩法复验待用户反馈，整体项目完成仍为 FALSE。当前只在CI Chromium验证，真实手机/Safari应用、WebKit隐私会话缩略图限制等边界保留。
