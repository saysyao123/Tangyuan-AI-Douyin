# T22 回归审计｜为什么第一幕T21看起来不如T18

日期：2026-10-17；反馈：用户试玩T21感觉没有明显优化，原网页结构/状态比新版本好。**该反馈成立。**

## 已验证的三个根因

### 1. T21无意替换掉原来经过多轮验证的网页壳（主要的UI回退）

旧版本真正入口：T18原`/chapter/`，源自`tools/t16/build.mjs`、`tools/t17/build.mjs`、`tools/t18/build.mjs`，提供原样的`index.html`、`style.css`、`shell.js`、`config.js`，包括：章节导航、当前目标`#objective`、任务列表`#quests`、`#focus-game`、更好的游戏视口CSS与第一幕→第二幕衔接。

T21错误：`.github/workflows/book_rpg_typepal_t21_preview.yml`只复制`web/chapter/game`进测试站点的`game/`，并用新写的`tools/t21/test_page.html`当`index.html`。新文件另加一层`iframe`和全屏入场遮罩，丢掉原来整个Shell/任务/章节/导航层。并且初版iframe路径`../game/`一度错误，后来改成`./game/`，只是修了加载，没有恢复原页面。**本来目标只需升级美术，却替换了更成熟的UI，不符合局部变更规则。**

### 2. 美术改动太少且部分低于之前质量（主要的视觉无改善）

T21`tools/t21/art_native.py`在4图中只生成**11张**原生简单像素几何图，主要替换11个非碰撞装饰的`sprite`字段。没有修改地面大面积重复铺装、光源计算、人物/商贩NPC四向动画、角色像素配色、动态环境、完整建筑地形层级与遮挡，无法实现高质量参考图的空间质感。

运行证据：`T20`真实基线`01-street-native-screen.png` vs `T21` `ACT1-street.png`。T18老`street-cottage`已经具备复杂门窗、灰旧墙肌理、暖窗与接地阴影；T21新`t21-street-house-*`屋顶外形较粗、墙体大片平色、纹理密度更低。**不能因新的RLE和11处变更就宣称美术更好。**

### 3. T21是不同的发布状态

T18原Site为独立owner-private ChatGPT Site和两幕连续`/chapter/`；T21是GitHub CDN对外公开的**合成示例剧情fixture**，与原本私有正式游戏的页面和部分文案状态不同。T21的4图SAVE12定点测试和前后路线CI技术通过，不能证明与用户原正式站点外观/体验完全一致。GitHub public副本不得注入私人原书文本。

## 修复策略：严格原页面优先，失败美术隔离

- 新`feature/t22-original-web-layout-restore-20261017`分支，绝不覆盖`main`、T18 owner-private正式 Site或旧`t21-playtest-web`对比基线。
- 构建公开T18原网站整树`web/`→`site/`，默认`/chapter/`完全保留旧`HTML/CSS/JS/config`与原生游戏逻辑/素材；不再用T21的test_page.html套iframe。
- T21新美术只在旁路`/art-review/`复制原`/chapter/`页面并替换其中`game/projects/book-pilot-cinematic`的美术数据；以保留旧壳方式对照其画面是否更差。
- CI必须字节对比`index.html`、`style.css`、`shell.js`、`config.js`，并在真实浏览器核验原导航`nav`、任务`#quests`、目标`#objective`、聚焦`#focus-game`和游戏`#screen`；截两份页面全图和原生游戏Canvas。
- 视觉不达标时默认使用T18而不允许T21发布为升级版；真正的后续任务是T18原壳上做高精度场景架构与渲染技术验证，并保持现有剧情和SAVE12。

## 状态与严格边界

T21已通过的技术: 固定TypePAL构建、4图直接恢复、若干剧情SAVE12检查点。T21正式美术审美FAIL，原UI体验回退，**不是已完成美术重制**。
T22修复工作流 `.github/workflows/book_rpg_typepal_t22_restore_ui.yml`；在CI成功并获取外部访问证据前，**不得宣称可访问的新链接已交付**。最终只将新独立预览URL当做UI回归版本，而不是用户要求的高精度完整第一幕终稿。


## 2026-10-17｜实测修复交付 T22

- 最终 T22 托管分支 `t22-restored-preview` 固定内容SHA：`d263e480be7861a2af47f184219625f548c9c662`。
- **恢复T18经典网页体验的公开试玩URL**：https://rawcdn.githack.com/saysyao123/Tangyuan-AI-Douyin/d263e480be7861a2af47f184219625f548c9c662/chapter/index.html
- **T21低细节建筑原位置对照URL**：https://rawcdn.githack.com/saysyao123/Tangyuan-AI-Douyin/d263e480be7861a2af47f184219625f548c9c662/art-review/index.html
- CI [39024912792](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39024912792)：T18四个Shell文件**逐字节一致**、原导航/当前目标/任务区/游戏聚焦仍在，重新增加更严格的**真实Type PAL `fair`场景渲染帧>0且加载遮罩消失**作为通过条件；截图 `T18-ORIGINAL-FULL-PAGE.png` 和 `T21-ART-REVIEW-FULL-PAGE.png`；同源浏览器 pageerror 为0。此前首轮QA`39024547607`虽然页面元素存在，但抓取过早出现加载/暂时无法连接画面，不能作为真实游戏可玩的证据；第二轮严格补验通过后才认为已恢复。
- 外网固定SHA文件链接成功：[39025117020](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39025117020)，验证完整章节HTML/脚本/CSS/游戏入口、任务UI、新旧街道文件差异。
- **与正式私有Site不是同域**：ChatGPT Site和GitHub CDN浏览器存储隔离，旧版本的浏览器SAVE12本地存档不会自动带到公开T22链接。用户在原站点仍可以继续用原存档；若要将旧档带到T22，需按原页面工具先导出，再到测试页面导入并读档。公开测试版是合成示例对白，不能证明私有原书具体台词一模一样。若用户要不迁移数据的原站无缝视觉升级，后续必须在获授权后将美术改造作为**同一正式Site的增量版本**部署。
- T22仅恢复原UI及默认旧美术，**并未完成目标高精细画面重制**；原目标持续，下一版本需基于保留原版网页结构进行分层高精度游戏美术施工，而不是再换掉整个网页Shell。
