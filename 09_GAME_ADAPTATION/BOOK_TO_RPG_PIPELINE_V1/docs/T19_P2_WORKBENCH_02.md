# T19 P2 工作包02：Type PAL 原生格式核验与失效场景停工

日期：2026-10-17；**P2未通过；T18正式网页未修改**。本轮实物交付为对话附件 `T19_P2_WORKPACKAGE_02_20261017.zip`。其二进制文件（PNG、GIF、RLE）尚未归档到GitHub，不可将本说明当成资源已上传或可玩样板已发布。

## 本轮新增的真实通过项

1. 已找到固定上游 `IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246` 的确切编码源码 `packages/shared/src/rle-encode.ts` 和解码真值 `packages/shared/src/rle.ts`。RLE单帧为LE尺寸+长度≤127的透明/非透明游程，sprite chunk为两字节word-offset表、偶数补齐，最后用gzip封装。这是现有Type PAL生成资产使用的结构。
2. 以用户认可的P1 V2人物四方向站姿为基础，在**原画布36×56（成人）、32×44（孩童）**下生成各12帧候选。保存严格原 `art/t14/catalog.json` 的256色调色板、透明索引255与原生 `SW/NW/NE/SE × 3` 索引顺序。仍只是候选动效，不是验收完成。
3. 实际生成 `native/t19-preview-adult.rle`（3199 B）、`native/t19-preview-child.rle`（2289 B）。Python编码→gzip解码→严格RLE逐像素和opaque mask复核成功，另以独立Node版本逐字节复刻**固定上游**的 `encodeSpriteChunk` 算法对比裸chunk：成人9640B、孩童6418B，两个完全一致。
4. 42/42项**静态结构**QA通过（尺寸、色板、透明、帧序、不同pose、头身不漂、脚底边界、gzip、SHA、Node独立编码等），证据在 `evidence/QA_REPORT.json` 和 `evidence/PINNED_CODEC_BYTE_EQUIVALENCE.json`。这不等于审美、动画、渲染或故事通过。
5. 隔离的 `preview/index.html` 可逐帧对照P2工作包01/02（文件保存在ZIP）。JS语法经Node检查，当前环境Chromium导航 `data:` / `file:` / localhost均报 `ERR_BLOCKED_BY_ADMINISTRATOR`，因此**未实际浏览器验收**。

## 未通过和明确废弃

- **P2-A旧屋场景**：尝试把已认可的概念素材分割成家具并近似T18镜头位置，实际320×200图案贴纸感强，室内地板材料回退明显。图片被放进ZIP `evidence/rejected_experiments`，明确标记 **REJECTED / NEVER_INTEGRATE**；不得以原生尺寸/图片存在宣称旧屋美术完成。
- **P2-B动画**：本轮新的髋部以下腿部像素偏移比上轮只移动鞋子多了“支撑/摆动腿”的结构，但**仍缺真实上肢反摆臂、脚底承重与角色整体动力学**；未通过动作视觉/原生运行质量门。新RLE是格式候选，绝不可替换正式角色。
- **P2-C原生游戏**：本容器没有固定Type PAL上游完整checkout及node_modules，容器无法解析GitHub域名；不存在新建引擎真实构建、原生加载演示、原生录屏或功能测试。当前原生可运行正式版仍为T18发布。
- 不更改SAVE12、projectId、两幕九图、剧情文字/任务、已有点击导航和键盘操作、私有Site权限；不借本轮把旧测试结果认作P2通过。

## 下一轮最小任务

**先解决P2-A与P2-B的审美落差，再谈P2-C。** 在已有GitHub Actions上游checkout环境中取真实 `home-room` 入场截图和现有家具锚点，**只精修一个原始高落差物件+邻接地板**并以实景反馈；人物选择一方向3帧手工定点修正，明确抬脚—承重—重心—落地—摆臂，成功才扩至四向。成功场景与动作必须分别通过320×200实际镜头/真实引擎循环，最后才开独立临时试玩，不覆盖生产。

本文件续接 `docs/T19_P2_WORKBENCH_01.md` 和 `docs/T19_NEXT_IMPLEMENTATION_STEPS.md`，作为下轮恢复入口。
