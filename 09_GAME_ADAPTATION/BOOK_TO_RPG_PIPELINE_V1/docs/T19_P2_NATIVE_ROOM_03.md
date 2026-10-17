# T19 P2-A 原生房间单物件试验｜Run03 技术通过，审美仍否决

日期：2026-10-17（北京时间）。当前**可执行图形生产管线已有真实引擎与浏览器证据**，并非本项目全部P2完成。

## 可复用构建与真实结果

- 独立分支：`feature/t19-p2-preview-native-20261017`；**没有合并或覆盖 main 正式运行代码，没有发布到既有 Site**。
- 原有正式基线仍是 T18 `/chapter/`，`projectId`、SAVE12、九图、剧情和寻路保持原样。
- 工作流 `.github/workflows/book_rpg_typepal_t19_preview.yml` 按固定上游 `IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246` 安装依赖，并用公开合成对白重新构建T18游戏（只为了生成本轮可运行预览，**未重跑无关旧剧情测试**）。
- `tools/t19/generate_table.py` 手工像素构造一张 80×48 indexed 256色餐桌（2碗面、木质桌腿/边框），通过 gzip RLE 生成 `noodle-table-preview.rle`，不复制仙剑商业美术。
- `tools/t19/isolated_preview.mjs` 仅克隆构建后的 `chapter/game` 成 `t19-preview` 并替换`night.noodle-table`资源字节及资源清单SHA256；其他游戏项目文件/剧情/碰撞/存档不动。
- **成功运行** [GitHub Actions Run39016679593](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39016679593)：固定引擎构建成功，T19覆盖文件合法，Chromium进入 `home-room` 原生场景并真实截图，pageerror 0。
- 下载产物：该Run的GitHub Actions artifact `type-pal-t19-p2-isolated-room`，包含 `T18.png`、`T19-preview.png`、新 indexed PNG/RLE、Manifest、隔离小游戏运行包 `t19-preview-runtime.zip`。属于公开fixture，不是私有原书正式可玩版。
- 截图对比：两者大小1280×800（320×200实际逻辑显示×4），场景均为 `home-room`，观察到的角色与实体数均为12，游戏剧情状态逐字段相同。像素差24736/1024000（2.42%），只在截图坐标x236–535,y448–599的餐桌区域（高分辨截图像素）出现；**技术隔离符合预期**。
- 首次 Run39016537264 的E2E整体结果 FAIL，是测试脚本工作目录误用了 `web/` 而非 `../web/` 寻找报告；两次原生截图此前已经完成，修正相对路径后Run39016679593完成通过。失败过程保留不抹平。

## 尚未通过的关键验收

- **美术质量：REJECTED**。真实游戏图显示新桌形体和两碗面更明确，但材质仍然过于平面、颗粒少，与同机位既有床、电视与橱柜的丰富纹理不统一。不能因为格式/构建/Chromium通过就把它列为批准的P2正式资产。下一步应以已认可V2木作真实像素表现和当前床柜纹理为参照进行精修。
- 人物行走真实承重、摆臂仍然未通过；此前候选的4向3帧RLE仅静态/格式通过，未集成。
- 当前只有**一个物件的房间渲染**；房间整体墙地、前景、家具和两主角动画仍未完成；没做全屋/全地图精修与部署。
- 源码/图片二进制保留在feature branch生成器与上述CI artifacts（30天留存）；**正式main还没有这些试验资源，不存在已发布私有Site版本。**

## 独立测试继续项

后续新增了餐桌点击交互短测（仅测试对象本次变化的opaque像素/脚边marker）。该测试在下一次CI新运行中验证，未返回结果时不得声称通过。针对桌子改材质时优先保持原 `80×48` 外轮廓、原 `meal-table` 交互ID和位置，原帧透明区域碰撞语义不动。

## 下一最小工作包

1. 只精修餐桌单件的高层次木纹、边缘厚度/背光及盆碗阴影，沿用前轮原生构建脚手架，不再重新实现格式编码。
2. 在P2隔离预览中对照T18同机位实际大小，不通过即局部返修，不上正式资产。
3. 当单件材质可与现有床/电视平衡后，再拓展墙地接口、局部灯光和两主角一步动作。人物样式、剧情/任务与 T18点击旧档维持锁定。


## Run04：餐桌真实点击交互补验（已通过）

- [Run39016997121](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39016997121) 最终成功；继承先前固定 Type PAL T18公共fixture 构建及隔离的 T19 一张餐桌资产替换。
- Chromium真实游戏目标 `home-room`，点击桌边原生脚底/标记位置 `[96,149]`（320×200逻辑像素），现有NPC/角色正常移动接近并触发剧情旧条件提示对话“先洗净”（公共fixture），`sceneId` 仍为 `home-room`。
- 浏览器 `pageerror=0`，比对 T18 与 T19 两次首屏截图的12个实体数量与剧情状态一致；验收范围不含完整新剧情、动态步态、多设备、旧档跨版本或私有原书中的完整对话。
- GitHub Actions 上传了真实的`T18.png`、`T19-preview.png`和`T19-table-interaction.png`、生成PNG/RLE以及**独立测试运行包**；证据包artifact id `12095073143`，该包已下载到本轮ChatGPT交付附件 `T19_P2_NATIVE_CLICK_PASS_20261017.zip`。
- **结果分离**：本轮单物件native渲染+剧情点击交互的*技术验收通过*；餐桌材质和全屋整体美术的*审美验收依旧明确未通过*。绝不合并替换正式Site，不把P2误标为全部完成。
