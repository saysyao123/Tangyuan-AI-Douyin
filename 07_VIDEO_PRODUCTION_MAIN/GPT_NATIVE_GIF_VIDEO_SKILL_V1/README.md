# GPT Native GIF-to-Video Skill v1.1.0

零新增现金费用的低幅动画专项模块：由当次可用GPT原生GIF工具生成／读取完整源画面，CPU光流后处理，以 **5秒／120帧GIF为主交付**，同时提供同一动画的5秒／120帧／24FPS MP4及原生源GIF。保留原Work-Fisher主路由。

- [网页端／Work入口](START_WEB.md) · [执行规范](SKILL.md)
- [审核与真实证据](AUDIT_REPORT.md) · [开源对照](references/OPEN_SOURCE_COMPARISON.md) · [质量门禁](references/QA.md)
- [变更记录](CHANGELOG.md) · [原审核任务书](WORK_AUDIT_START.md)

## 执行

```bash
python scripts/gif_to_video.py --input source.gif --out inspect --inspect-only
# 实际查看全部源帧检查页后，使用新的空目录：
python scripts/gif_to_video.py --input source.gif --out result \
  --seconds 5 --fps 24 --scale 1 --source-reviewed --source-origin gpt-native
python tests/run_regression.py --out results/regression-unique
```

运行依赖为 `requirements.txt` ＋系统 `ffmpeg`／`ffprobe`（libx264）；已实测精确版本见 `requirements-tested.txt`。回归使用标准库unittest，无需pytest，无模型下载或服务调用。源码只负责后处理，不自动调用GPT生成。

## 本版修复重点

真实GIF累计时长采样、光流缓存、共享色板、disposal／透明度重建验证、源滚动负例、完整MP4解码与CFR时间戳检查、真实来源计数、奇数尺寸补边和可选已有音轨封装。默认不放大、不循环；输出名改为 `animation.gif`／`animation.mp4`，避免非5秒参数仍写死5秒文件名。

文件格式正确≠人物动作合格。脚本永远保留视觉待验收；每个实际样片另做完整播放和逐帧记录。30原生帧的本次采样是30源采样＋87光流＋3自然停留，不能笼统宣传“120原生帧”或“90个新动作”。

历史原生素材、成片的真实位置与SHA见 [素材索引](evidence/2026-11-05/ASSETS.md)。仓库保持源码／text-only fixture，未打包人物GIF二进制；找不到历史文件时如实标PENDING_REAL_ASSET，不能从fixture推断人物通过。

这是可按文件执行的仓库规范；尚未安装为ChatGPT全局Skill，原目录命名与严格安装包要求的name不一致。网页端下次应重新读取main当前SHA，不承诺自动更新聊天缓存。

## 原流程与替代实验的边界

正式路线：参考图 → GPT原生源GIF → 全帧检查 → 补间 → 5秒／120帧GIF＋同时间轴24FPS MP4。原生源帧数不必是120；历史30帧源经验保留。

2026-11-05的咖啡馆眨眼样片实际使用3张新生成PNG及7个复用的时间位置，最终还直接由PNG输入模块函数编码MP4。该样片应归类为眨眼效果实验，不能认定原Skill演示通过。眼睛效果与5秒／120帧参数可分别记录，但不能替代原生GIF来源和主交付检查。

正式演示不以静态关键帧替代原生GIF；接口受阻保留 `NATIVE_GIF_GENERATION_BLOCKED`。替代实验标 `ALTERNATIVE_DEMO_NOT_ORIGINAL_SKILL_PASS`，不更改主流程或历史成功资产。
