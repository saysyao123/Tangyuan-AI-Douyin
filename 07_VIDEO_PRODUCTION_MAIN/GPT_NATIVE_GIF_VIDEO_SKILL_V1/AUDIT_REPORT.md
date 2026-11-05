# Work 深度审核 · GPT Native GIF-to-Video v1.1.0

日期：2026-11-05。基线 main：`4ba129c6e178491139fb879e0dc0900e1063db1d`。唯一正式源码仍在本目录；Work-Fisher默认主流程及历史成片未改动。

本报告覆盖实际源码修复、可复现工程回归、取回的真实30帧源及开源对照。本次仅将通过验证的工程修复纳入正式源码；完整抬手样片不签发视觉通过，当前新GIF生成实际受阻。下面分别列出已通过及未通过项目。

## 核心缺陷与处理

| 严重度／旧问题 | 原因及证据 | 实际处理 | 验证方式 |
|---|---|---|---|
| 高：变速动作时序错误 | load_gif读取duration，render_frames却均匀按索引0…29取样 | 按累计duration的帧起始时间映射到CFR刻度；保留末帧自然hold | [100,700,200]ms fixture，旧版120刻度有71个落错源区间；新版0 |
| 高：来源计数不成立 | 旧版120−30即填90；旧索引模式只有首尾2端点精确落点 | 逐输出帧记录源索引／alpha／类别 | 30×170ms本次为30源采样、87光流、3末尾hold；不称120原生 |
| 高：技术通过检查不足 | 未验视频时长／codec／解码帧数／时间戳；assert可被-O关掉 | 显式失败异常、ffprobe、全部CFR时间戳、FFmpeg完整音视频解码 | 5秒120帧24/1H264/yuv420p；破损MP4负例 |
| 高：源坏帧无执行闸门 | 数值只警告，不拒绝整图滚动／全静止；没有全帧审核步骤 | 已知风险启发式拒绝＋执行者实际源审核；全部源页 | 合成滚动／错片负例、历史坏120帧源；不能证明全世界的错片都可自动识别 |
| 中：透明度行为不明确 | 直接转RGB丢弃alpha语义；disposal无测试 | 顺序seek逻辑画布重建后显式matte合成；记录disposal／local rectangles | disposal2/3局部patch逐像素断言、透明源fixture |
| 中：GIF色闪 | 每帧独立median-cut色板重新分配静态颜色 | 全片共享色板默认，保留per-frame A/B选项 | 固定背景时序MAE约0.885→0；不宣称恢复真实细节 |
| 中：重复算光流 | 同一源帧对在每个输出t重估双向流 | 每对缓存，保留原Farneback与warp | 236→58调用，同t87组像素差0；最终三次小图CPU中位数约3.84倍加速 |
| 中：偶数编码与依赖缺口 | yuv420p奇数宽高失败；未预检ffprobe，依赖无上界 | 右／下补最多1像素，检查ffmpeg/ffprobe；记录已测版本 | 91×161→92×162；真实9:16 fixture；Linux/Python3.12已跑 |
| 中：旧结果可能冒充新结果 | 输出路径可复用；非5s参数仍写死5s文件名 | 新空输出目录，通用animation文件名、运行SHA与文件SHA | 旧目录负例，不自动覆盖历史资产 |
| 中：生成与后处理边界模糊 | Python不调用GPT；网页读Markdown不是工具安装 | 拆清能力检查／原生生成／文件处理／视觉验收 | 当前schema列2–16帧；实调用12帧GIF返回HTTP400未启用，标BLOCKED；历史30帧仍可后处理 |
| 中：安装与更新误解 | YAML多summary；历史目录名不匹配name | 最小标准frontmatter；保留目录并披露严格安装差距；同SHA读取 | 文档契约测试；未全局安装，不承诺热更新 |
| 范围扩展：音轨接口 | 旧版-an，无已有音轨接入 | --audio WAV，AAC截补至视频长度并回读 | 1秒合成tone补至5秒；不等同配音听感／口型／字幕通过 |

## 第一性原理与取舍

保留固定人物、固定镜头、完整帧、禁止滚动拼图和原生／补间区分。原生信息量决定细节上限；插帧只估计时间过渡，不能补回错误结构。默认不放大，2倍仅作显示版本。原30帧144×328不是9:16，不进行拉伸裁切。历史“30＋90”更精确地分列为30＋87＋3，不用改像素凑120个独立动作。

先修时序、证明缓存不改变同t像素，再引入共享色板这一可量化改进。没有证明更优的神经插帧不替换默认。完整方案和维护／许可见 [开源对照](references/OPEN_SOURCE_COMPARISON.md)。

## 安装、自动化与边界

- AI可独立读取版本、检查已有素材、运行CPU后处理、回归、编码、输出回读和记录、提交已验证改动。
- AI原生生成取决于当次真实工具与额度；本轮取回历史合格源回归，没有重新生成30帧。不增加付费模型API或云GPU。
- 普通网页端需要可执行代码和取得源GIF本体；只有聊天／搜索无法运行Python。下一次必须重新读取main同一SHA，不会替换旧聊天缓存。
- 当前repo目录兼容历史链接，frontmatter字段规范，但目录不匹配name，因此不宣称严格安装包或ChatGPT全局安装。
- 人物一致性、手指自然程度、跨段连续性仍需真实样片视觉检查；fixture不能替代人物验收。
- 用户原则上无需剪辑；仅当实际服务要求登录授权、文件仅在用户端或最终审美取舍时参与。已存在可读素材不重复要求上传。

## 本次运行结果

**验收范围：工程修复通过，保守微动后处理通过；整套全自动新生成＋完整抬手动作尚未通过。** 不以fixture、降低动作或参数合格冒称原手部问题解决。

| 项目 | 实际结果 | 证据 |
|---|---|---|
| 离线回归 | 37/37，0失败、0错误、0跳过；测试exit0；集成fixture产线exit0 | [test_summary.json](evidence/2026-11-05/test_summary.json)、[完整测试日志](evidence/2026-11-05/tests.log) |
| 源GIF | 真实历史样本144×328、30帧、5100ms，SHA256 9b4c6b7d…51df9e9b | [真实源及所有成片位置](evidence/2026-11-05/ASSETS.md) |
| 完整30帧后处理 | GIF120帧/5000ms；MP4实际120解码帧、24/1、5.000s、H264/yuv420p、完整解码通过；视觉FLOW_REJECTED | [技术QA](evidence/2026-11-05/full30_qa_report.json)、[手部失败关键帧](evidence/2026-11-05/hand_ghost_failure.jpg) |
| 真实坏120帧源 | 进程exit2，GLOBAL_DRIFT_OR_SCROLL，未生成MP4 | [命令/退出码](evidence/2026-11-05/rejected120_command.json)、[QA](evidence/2026-11-05/rejected120_qa_report.json) |
| 保守微动回退 | 原源0–14帧/2550ms重定时至5s，15源采样＋98光流＋7末尾停留；288×656仅为2倍显示；技术通过、低幅动作视觉通过（有范围限制） | [技术QA](evidence/2026-11-05/micro_qa_report.json)、[视觉记录](evidence/2026-11-05/visual_review.json) |
| 全片观看 | 全部源/输出帧检查；浏览器对同一解码内容完整播放至5s ended；对应120个YUV420p帧哈希逐帧一致 | [完整片播放](evidence/2026-11-05/full30_playback.json)、[微动播放](evidence/2026-11-05/micro_playback.json)、[等帧验证](evidence/2026-11-05/micro_playback_equivalence.json) |
| 播放限制 | 本机Chromium无H264 codec，直接MP4浏览器播放不可用。实际看的是lossless VP9派生；MP4自身由FFmpeg完整解码验证。没有将派生播放写成直接MP4播放 | [完整片等帧说明](evidence/2026-11-05/full30_playback_equivalence.json) |
| A/B效率/颜色 | 最终3次中位数旧2.562s、新0.667s，约3.84倍；同t像素误差0；色板固定背景时序MAE0.885→0；变时长落错区间71→0 | [benchmark.json](evidence/2026-11-05/benchmark.json) |
| 独立使用检查 | 在最小任务上下文实际使用规范完成导出，并独立发现2.75s手部重影；其当时运行版本与后续版本区分，媒体哈希相同 | [使用记录](evidence/2026-11-05/independent_forward_run.md)、[独立视觉记录](evidence/2026-11-05/independent_forward_review.md) |
| 新原生生成实测 | 尝试12帧/400ms低幅眨眼，HTTP400：GIF output is not enabled for this request。没有实际新源GIF；BLOCKED | [视觉/能力记录](evidence/2026-11-05/visual_review.json) |
| 神经/替代补间 | RIFE、FILM未运行推理；MCI实跑首次112帧，补尾后120帧，未证明更优；DIS及加权splat样本实验仍有鬼影/孔洞，未纳入默认 | [开源对照](references/OPEN_SOURCE_COMPARISON.md)、[拒绝的候选图](evidence/2026-11-05/rejected_flow_candidates.jpg)、[MCI图](evidence/2026-11-05/minterpolate_comparison.jpg) |

默认原光流算法被保留，未把实验候选写进正式后端。新增分歧风险规则能定位源16→17帧的已知失败；不代表所有手部问题都能自动检测。原片65–67帧（约2.708–2.792s）明显半透明双轮廓，81–83帧指尖偏软；仍须更密、更合理的原生动作或通过同源A/B的更强补间。

## 实际命令与重跑

本轮执行Python3.12.14、Pillow13.0.0、NumPy2.3.5、OpenCV5.0.0、FFmpeg6.1.1，无新增付费服务。运行命令及退出码详见 [commands.md](evidence/2026-11-05/commands.md)。关键复跑：

```bash
cd 07_VIDEO_PRODUCTION_MAIN/GPT_NATIVE_GIF_VIDEO_SKILL_V1
python tests/run_regression.py --out results/new-run
python scripts/gif_to_video.py --input /path/native_source_30frames.gif --out inspect --inspect-only
# 仅实际查看源帧后运行，均使用新的空目录：
python scripts/gif_to_video.py --input /path/native_source_30frames.gif --out full30 \
  --source-reviewed --source-origin gpt-native
python scripts/gif_to_video.py --input /path/native_source_30frames.gif --out micro \
  --source-range 0:15 --scale 2 --source-reviewed --source-origin gpt-native
```

所有正式变更限定本专项目录及父README。完整文件清单见 [FILE_CHANGES.md](FILE_CHANGES.md)。通过独立分支/PR同步；最终main SHA应由GitHub提交元数据及交付回复核验，避免在提交自身内容内伪造自引用SHA。没有运行GitHub Actions，不把本地37项测试写成CI通过。

## 下一轮可验证提升

1. 先恢复当次可用原生GIF工具，再实际测试12–16帧生成的完整帧与分辨率；不能沿用本轮失败调用当成功证据。
2. 针对原手部片段收集同源真值/更密动作，测试遮挡友好的学习型插帧；仅在可用免费环境与同源结果胜出后考虑升级默认。
3. 高原生细节、其它风格、9:16真实素材、多镜头姿态继承及自然配音/字幕/口型，需要各自真实样片；本轮仅测封装音轨扩展，不签发这些质量结论。
