# T34 当前续作｜按已认可室内统一四景

2026-10-18。用户于 17:56（Asia/Shanghai）明确认可 T33 室内“已经OK，效果挺好”，要求其他场景沿用同一风格和设计思路。该认可只覆盖室内；本轮四景更新的最终审美尚待用户验收，项目最终完成仍为 FALSE。

## 本轮锁定

承接 WORK_START_HERE、T19 V2、T22 网页和 Type PAL 固定上游 f98d0ddd89ebdee7b04502ee35de26ee82c6d246。先完成 fair→backstage→street→courtyard，不扩写后续剧情。保留原地图、碰撞、人物脚点、剧情、键盘/点击寻路、SAVE12；保留已认可室内及重要人物独立身份；不覆盖 main 或原正式 Site。

## 新环境

三种朴素旧租屋、三类不同摊位、重绘戏台、完整灰泥/木护墙后台、自然地面、低院墙、树、路牌、路灯、药炉、冬菜、柴堆与箱罐，共 20 张环境图；另有六相位身体火焰及六相位火球，共 32 张新图。材质统一为旧木、灰泥、灰砖、灰瓦、自然积雪与柔和灯光。后台墙体/木地板包住原有随从与抬人路线。

四景仅显示缩放为 0.8，街院上移取景、后台适度上移；点击共用严格逆变换。原生 camera、col/row、运动和存档真值保持。T33 home-room 的显示变换、房间模块、家具和纹理保持；原 171 张栅格字节保持。

首轮实机发现院墙偏高挡人、道具图集切片混入邻近墙柱、药炉仍绑定旧图，均已修正。舞台火焰按原“红色里透蓝光”细化，保留原生 48×64 / 32×36 范围、六帧各 100ms 和飞行路线。没有把人物遮住的高墙或技术通过版直接交付。

## 证据与发布

来源 c4756cd70b4f1ca657be30a14486813951be6b75；运行 e3de3a907e6cb6b1be93887524c14ee76081310d。分支 feature/t34-world-style-20261018 / t34-world-candidate。Run39119246651 共 13 项四景检查与 2 项后台检查 PASS、零 pageerror。109 个原生文件与固定基线一致，171 张原有素材保持，338 个部署 game 文件与实测一致。详见 evidence/T34_20261018/RELEASE.json 和在线 review/QA.json。复用已通过的完整第一幕及未变的头像/独立人物/室内测试，本轮只运行变更影响到的四景视野、点击、交互、演出、后台动作与存读档。对实际截图进行审查后发布。

试玩：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/

四景对照：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/review/

已认可室内：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/night/

同一 owner-private 隔离站点。后续先读本页和 RELEASE，再按用户反馈修未通过部分。不要重建游戏、重复未变旧测试，或把新四景内部审查等同用户认可。未验证真实手机或 Safari 应用；WebKit 隐私会话缩略图限制保留。公共源代码继续使用合成对白。

## 本轮实际发布真值

- 同一 Site 源提交：d97f8c4896e1b0ecc691f68c446e8e9ade26a6a1
- 版本：appgprj_6ad427757a608191a95a42cc68b1f19b~appgver_d6f9594bcb9481919e568ffbb4101fbd
- 部署：appgdep_6ad4a1a8e280819192b922b66c25f13e，succeeded
- 940 项运行清单、帮助/对照页相对链接及本地下载哈希检查通过。
- 完整网页 ZIP：130069294 bytes，SHA256 27859cb2d3f3c5e514f0549f7dfb441172f38a6db070d32fc207c19b1e44a105。
- 图像生成方式、提示与原始输出记录见 [T34_ART_BRIEF.md](../art/t32/T34_ART_BRIEF.md) 和 T34_ASSET_PROVENANCE.json；实际素材在对应源码包。
