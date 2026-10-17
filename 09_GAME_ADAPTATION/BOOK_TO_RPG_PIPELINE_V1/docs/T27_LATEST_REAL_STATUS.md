# T27 第一幕恢复续作｜真实进度与网页交付（2026-10-18）

## 用户锁定终极目标
以用户已确认的精细等距像素雪夜木屋参考画风，统一重制第一幕 `fair → backstage → street → courtyard` 的所有场景、人物、NPC、道具与自然引导；保留 Type PAL 原游戏剧情/存档(SAVE12)/NPC事件/寻路；沿用恢复的 T22 原网页布局和 T23 自愿式提示；最终交付直接在线可玩的完整一幕，不以技术测试成功冒充美术验收成功。

## 这轮实际恢复与完成
- **首先核对上一轮卡住的位置**。先前本地 Python 拷贝 `t22_fullsite → t26/first_act_character_preview` PermissionError，但GitHub已有 T26 成功CI [39045392978](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39045392978)，不能再误称T26没通过。
- **T27新独立构建**：`feature/t27-act1-character-integration-preview-20261017`，只把经用户在T19 P1 V2认可的主角和孩子四方向站姿接入原T23网页与Type PAL native RLE，合成4方向×3帧，其他脚本和地图JSON全部保留，`main`及私有正式Site未覆盖。
- 真实浏览器4图同机位对照成功、原native`check-project`与RLE roundtrip成功，无page errors： [Actions 39047451171](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39047451171)。
- 除四图静态加载外，再在**新T27实际测试工程**运行T15事件通道：`stage → backstage`倒地角色与抬人层次，`street → courtyard → home`、药锅旁孩子、归家无黑边，均CI成功；**仍不是首次开局不依赖存档的整幕逐流程连通验收**。
- **已发布独立网页**：GitHub `t27-act1-playtest`固定SHA `9fb5986a17951b829512655f1b43fd3f69f7b7fb`；网址 `https://rawcdn.githack.com/saysyao123/Tangyuan-AI-Douyin/9fb5986a17951b829512655f1b43fd3f69f7b7fb/chapter/index.html`。外部CDN页面、游戏入口、可选引导文件、两位角色12帧RLE和SHA全都已通过 [Actions 39047706769](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39047706769)。
- 独立可打包备用：`T27_FIRST_ACT_PLAYABLE_PREVIEW.zip` 是从 T26 CI通过版原始自包含网页ZIP校验抽取，并不是新手工编造的game UI；可从本轮对话附件下载。由于GitHub网页为公开合成fixture，其浏览器原域SAVE12和ChatGPT正式私有Site存储不同域，需要导入/导出迁移存档。

## 严格验收状态
| 项目 | 结果 |
|---|---|
| T22原网页结构/T23自然可选引导 | 保持 |
| 新两主角形象/方向帧接入 | TECH_PASS |
| 四图加载、存档定向恢复、关键支线回归 | TECH_PASS |
| GitHub独立网页在线交付 | PASS |
| 角色12帧步态审美、人脸与方向一致性 | 尚未获得视觉批准 |
| 第一幕四场景高精度整体彩绘 | **NOT_PASSED**（T25程序背景曾使审美倒退，被弃用） |
| 所有既有NPC的统一精细化美术/动效 | NOT_COMPLETE |
| 从全新存档完整走完第一幕 | NOT_YET_VERIFIED on T27 |
| 用户所要求的最后最终游戏交付 | **NOT_COMPLETE** |

## 下一步不可再跑偏
1. 候选高精度雪夜传统木屋PNG(独立透明素材)已通过原生生图得到，当前在对话文件`a_detailed_isometric_3d_pixel_art_style_illustrati.png`。**图片不在GitHub正式内容目录，不能声称已接入。** 必须先与现有street/courtyard室外民居位置和透视核对，正确分层遮挡后才能进入测试版本；不能把整张海报作为底图。
2. 庙会正式戏台与摊位、后台结构与旧街小院、4图NPC动作和主角完整步态是下一真实美术核心；不要回头重复T24滤镜/T25程序砖路失败路线。
3. 只在实际游戏截图可验证环境精细度、角色足点/遮挡、真实逐幕通关后再发布为最终版。不覆盖正式Site；如需直接覆盖ChatGPT Site，另需站点编辑授权。
