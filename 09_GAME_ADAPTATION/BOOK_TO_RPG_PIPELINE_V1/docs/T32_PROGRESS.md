# T32 第一幕美术整合｜唯一续作状态

原始目标：T22 完整页面上，第一幕 fair→backstage→street→courtyard、高精细环境与全部人物/NPC、自然步态、实际完整试玩、隔离在线交付。

基线：T31 开发分支 745968a827848948403f0cbf5255d765ea3cff9d；运行 T30 固定 146298ede54a65025ab7a794b49ab53c4bf3ae92；原 Site 不覆盖；main 不合并。

本轮已制作：T31 512×360 雪屋纳入 art/t32；GPT 原创戏台/摊位/后台/院墙/冬树/药炉；三种高清地表；原生画布高分辨率绘制和脚点深度排序。沿用原实体显隐、地图/故事/碰撞/输入/SAVE12，不重新生成剧情。

验收：本地编译和 TypeScript 定向检查进行中；四图实际浏览器、动作、完整新开局、在线 HTTP 尚待 CI。ART/USER 仍 PENDING，禁止以技术结果代替美术验收。

当前环境没有 Sites 要求的 control-browser 能力，按该技能要求不启动本地预览、不自行安装浏览器。采用交接授权的 GitHub Actions 执行现有真实 Chromium 测试并取回截图人工审查。

唯一施工入口：tools/t32/build.mjs；.github/workflows/book_rpg_t32_art_integration.yml。
