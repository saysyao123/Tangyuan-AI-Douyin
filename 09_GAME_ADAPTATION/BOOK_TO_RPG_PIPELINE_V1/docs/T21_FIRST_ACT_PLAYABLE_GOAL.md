# T21 第一幕游戏重制｜目标契约与真实交付标准

更新时间：2026-10-17。**最终目标（不是简单资产验证）：按用户已认可的高完成度参考图提升第一幕四图，交付实际网页可玩地址。**

## 原始目标

- 已固定审美锚点：用户认可的 `雪夜暖灯下的山居小屋.png` / `雪夜暖灯下的木屋日常.png`，建筑必须有完整壳体、屋顶厚度、墙/梁柱、门窗、生活物件和统一冷暖灯光；人物与空间有清晰接地和同一艺术语言。只能用原创素材，参考《仙剑98》工艺而非复制商业资源。
- 第一幕实际顺序严格为 `fair`→`backstage`→`street`→`courtyard`，角色、原有互动、剧情阶段与存档保持原真值。场景美术可重新规划，但不能凭概念图新增不在剧情中的酒馆、桥、商铺、NPC、城市名或UI。
- 目标不是单个可编码帧，而是 **四张图实际游戏内同等级审美 + 可玩事件/走路/寻路 + 可测试线上页面**。
- 保留上游固定 `IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246`、项目与SAVE12的320×200 **逻辑坐标合同**；T18公开/私有稳定版本不覆盖。允许通过独立高分辨率视觉层改善浏览器最终展示，不擅自修改底层碰撞/剧情/存档格式。

## 本轮可公开实测的T21阶段版本

- 开发分支：`feature/t21-act1-playable-rebuild-20261017`。
- 公共网页预览发布分支：`t21-playtest-web`，**独立测试版，与正式Site完全隔离**。
- 测试入口：`https://raw.githack.com/saysyao123/Tangyuan-AI-Douyin/t21-playtest-web/index.html`；这个地址是第三方用于小范围测试的GitHub源文件CDN，临时测试，不作为商业正式部署。
- CI `39022693667` 通过固定TypePAL重构、native `check-project` 与Chromium测试：四图均能从SAVE12定向恢复并渲染，合计11个原创新建筑/戏台/摊位静态素材，11个装饰性entity外观替换（fair 4、backstage 1、street 3、courtyard 3），没有更改实体ID、脚点、地图阻挡或剧本结构。测试详情见CI artifact `t21-first-act-test-game-and-qa`。
- GitHub Actions `39022936137` 对外部`raw.githack.com`地址进行了HTML、game入口与`street.json` HTTP成功验证；地址iframe相对路径后续修为`./game/`，应做更新后的二次外网回归。
- 公共测试版只使用允许公开的合成示例对白，不包含私有原书具体台词；后续私有正式部署必须单独在有授权素材的环境做同版等价验证。
- **本次技术测试通过不等于最终目标完成。** 审视真实浏览器截图后可见，当前新建建筑虽然比旧程序方盒有结构，但场景墙地、光影、纹理密度和NPC整体仍明显差于用户批准参考图，**审美正式验收FAIL/待重制**。不要把RLE/项目结构通过归入视觉通过。

## 必须改正的长期瓶颈

**根因：**在320×200逻辑画布上重复填程序砖格、每个物件靠小尺寸几何贴图，天然压低了环境精细度。把高清整屋概念图缩为320×200、或直接铺成一张非交互贴图，又会破坏遮挡、点击与寻路。

**新方案：保留原生TypePAL逻辑，独立高精度渲染层。**

1. 原`320×200`世界坐标、`(16(col-row),8(col+row))`投影、碰撞、剧情触发、队伍动作、F5/F9存档保留。
2. 在独立网页展现层绘制高分辨率(例如1280×800)建筑背景/地面/人物/前景遮挡的分层贴图，严格由原生camera和actor脚点驱动，以保留完整HUD、对白、输入和模拟；前景墙柱参与排序，不用粘平整张图充当游戏世界。
3. 先用`street`一屏做高精细真实渲染双截图：新图应能在原来真实角色和通道上与T18并置比较；而不是AI编新街地图。若画质无法达参考图，则不推广到另外三图。
4. 当前`street`原生SAVE12相机：`camera.x=480,y=112`；`stranger`原生屏幕(32,112), child(144,104), home-road(288,112)，沿着这些锚点保留现场；庙会返回点在此镜头外。
5. 之后按`fair/backstage/courtyard`的原本场景结构逐图制作、测试。每场景同时维护高精度母版、可拆分源、遮挡图/脚点、真实游戏截图，不添加故事外人物或交互。

## 最终验收（四关全部通过才写“完成”）

- **视觉：**四图在实际游戏窗口中接近获准参考图的空间感/环境材质/冷暖灯光、建筑实体感、人物自然步态；用户认可同机位截图与游玩效果。
- **真实可玩：**从`fair`开始连续到`courtyard`结束，原买物→看戏→后台→遇陌生人→邻居→归家事件完整；不卡路、不丢互动、不出现错误地图或陌生UI。
- **兼容与回滚：**SAVE12旧档、点击寻路、键盘接管、scene实体ID、可导出工程、T18回退版本不受破坏；受影响项做定向自动化+人工审美验收。
- **网页交付：**给用户真实可打开URL、版本SHA、四张真实游玩截图、测试路线、失败清单；只发布已通过版本，不拿ZIP或概念图冒充游戏网页。

## 当前实际门控

`G0(native base)=PASS`, `G1(native four-scene structural art pass)=TECH_PASS but ART_FAIL`, `G2(HD layered visuals)=NOT_STARTED`, `G3(full first-act continuous play)=NOT_YET_VERIFIED on T21`, `G4(visual user signoff and final page)=NOT_STARTED`.

后续恢复该项目要**直接处理美术落地差距**，勿再次复盘已通过RLE编码、旧存档读档阻塞、单件餐桌通路或重新生成错误酒馆城镇。


## 2026-10-17｜确切可打开的网页测试构建（仍不是美术终稿）

- 已经发布了`t21-playtest-web`独立分支。网页构建基准 commit `8a20520318681bf0626667d433e2042ed0ca06b6`。
- **公开试玩地址（固定SHA CDN）**：https://rawcdn.githack.com/saysyao123/Tangyuan-AI-Douyin/8a20520318681bf0626667d433e2042ed0ca06b6/index.html
- 源码构建与四张图实际浏览器检查：[Actions 39023002674](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39023002674) `PASS`；外部固定SHA URL 的index、`./game/`入口、旧街新资产JSON HTTP验证：[Actions 39023267364](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39023267364) `PASS`。此前用于变更中的分支CDN检查 `39023186701` 因旧缓存读取到错误iframe路径，已通过SHA固定版规避，不隐藏失败。
- QA证据为上述构建运行的`t21-first-act-test-game-and-qa` artifact，含四张来自真正Type PAL画面的`ACT1-fair/backstage/street/courtyard.png`和`T21_BROWSER_QA.json`、11个原生sprite PNG、RLE替换manifest、自包含网页ZIP；30天CI保留期。公共合成剧情，不包含私人原书对白。
- **注意：技术可以试玩 ≠ 最终项目完成。** 实际截图显示建筑纹理仍较块状、路面花纹机械重复、照明/空间与获准高细节参考差距显著，故T21高标准美术验收明确`NOT_PASSED`。它是给用户测试交互与版本连续性的首个公开技术预览，而不是已通过审美的重制正式版。真正后续必须实现高分辨率分层展现，仍不得改剧情和逻辑地图。
- 正式第一幕原入口和四场景剧情未改，`main`稳定游戏与 owner-private Site 均未更新；不得把公开CDN测试链接标为正式Site。
