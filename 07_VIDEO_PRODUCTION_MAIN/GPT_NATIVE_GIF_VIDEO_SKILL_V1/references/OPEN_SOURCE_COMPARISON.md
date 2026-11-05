# 开源技术对照 · 2026-11-05

评判依据：完整动作与人物稳定、遮挡、部署条件、真实运行成本及可重复性；不按 star 数决定默认。维护状态为本次 GitHub 元数据快照，不等于质量保证。原始摘要见 `../evidence/2026-11-05/upstream_snapshot.json`。

| 项目／一手来源 | 许可与维护快照 | 质量与负担 | 网页端／Work 和零新增费用 | 本轮证据与选择 |
|---|---|---|---|---|
| [OpenCV](https://github.com/opencv/opencv)、[Farneback 文档](https://docs.opencv.org/4.x/dc/d6b/group__video__track.html) | Apache-2.0；未归档，2026-11-04 有推送 | 稠密光流；CPU 小图可运行；近似双向反向 warp 不解决全部遮挡，±24px 裁剪不适合大运动 | 本 Work 实跑；无权重、无付费服务；普通网页须有代码执行与依赖 | 保留原算法默认；缓存58次光流替代236次，同t像素差0；修正时间轴 |
| [FFmpeg minterpolate](https://ffmpeg.org/ffmpeg-filters.html#minterpolate)、[源码](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_minterpolate.c) | 核心 LGPL-2.1+；本环境启用 libx264 的构建为 GPL；未归档、持续推送 | 块运动补偿可选 aobmc/bidir/vsbmc；CPU可跑，仍可能块状失真；尾部需显式处理 look-ahead | 本 Work 已有FFmpeg；不要求付费GPU；普通网页无系统执行则不可直接调用 | 真实30帧源实跑：首次112帧/4.666667s，延长末尾再trim可到120/5s，但带更多尾帧停留；没有优于原算法的证据，不升默认 |
| [Practical-RIFE](https://github.com/hzwer/Practical-RIFE) | MIT（README明确所列模型同许可）；未归档，2026-08-27推送 | 学习型插帧，对复杂遮挡有研究价值；模型／PyTorch负担高；源码支持CUDA或CPU，不能据此宣称本环境性能 | 免费开源不等于现成免费云推理；README要求Python≤3.11、额外模型下载。本次是Python3.12，无3.11、无已配置GPU或权重 | 实际查README和推理源；**未运行模型推理**。保留候选，不引入依赖或付费服务 |
| [FILM](https://github.com/google-research/frame-interpolation)、[论文](https://arxiv.org/abs/2202.04901) | Apache-2.0；GitHub归档，最后推送2024-08-10 | 大位移插帧研究；TensorFlow2 SavedModel；官方安装示例Python3.9/CUDA11.2，重于小图Farneback | 可开源本地部署；仓库Colab／外部Demo链接不是本系统拥有的免费额度；本次无所需权重环境 | **未运行模型推理**；维护／部署成本使其不适合作为本轮默认替换 |
| [Pillow](https://github.com/python-pillow/Pillow)、[GIF文档](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif)、[LICENSE](https://github.com/python-pillow/Pillow/blob/main/LICENSE) | 当前LICENSE称MIT-CMU；GitHub自动识别NOASSERTION，不能照抄为“无许可”；未归档，2026-11-05推送 | 成熟GIF seek重建、disposal、透明度、局部帧；每帧量化可能闪色，save_all会合并同像素帧 | 轻量CPU，本Work实跑；无服务费 | disposal2/3及透明度像素断言通过；全片共享色板；公共块写入接口保留真实hold，避免偷偷合帧或改像素凑数 |
| [Gifsicle](https://github.com/kohler/gifsicle)、[COPYING](https://github.com/kohler/gifsicle/blob/master/COPYING) | GPL-2.0；未归档，2026-10-15推送 | 擅长GIF优化／unoptimize，不能补出真实人体运动；额外可执行依赖 | 本地免费，网页仍需运行环境 | 代码／用途对照，**未运行**；现有Pillow经测试已能重建，暂不增加必要依赖 |
| [Agent Skills](https://github.com/agentskills/agentskills)、[规范](https://agentskills.io/specification) | 仓库Apache-2.0；未归档，2026-11-04推送 | 精简frontmatter＋按需脚本／参考；规范要求目录名匹配name；Markdown不等于工具注册 | 读取即可作为任务规范；安装／全局触发依赖实际宿主 | 删除非标准summary；原目录保留兼容。明确仓库布局不是严格安装包，未宣称ChatGPT全局安装或自动热更新 |

## 已采纳与保留

- 采纳真实累计时间映射、GIF逻辑画布解码、稳定共享色板、逐对光流缓存、CFR时间戳及全媒体解码检查、资源边界和失败状态、来源分类。
- 保留V1原光流参数以保护成功画面；缓存前后逐对同一t的87组对照最大像素差0。时间映射属于明确bug修复，因此最终视频节奏与旧版索引重采样不同。
- 暂不把神经插帧、超分、复杂遮挡、商业生成额度引入正式依赖；没有已运行的同源A/B不能宣称效果更优。
- 上述源码仅作技术对照，本模块没有复制第三方大型模型代码或打包其二进制。实际依赖分发需保留相应许可，本次只调用已安装组件。

## 第一性原理结论

帧率不能创造缺失的主体结构和原生细节。约144×328的30帧样本，最有价值的改进是保持真实动作时间、避免重复估计引入不确定性、避免GIF色板额外闪动、拒绝错误源，并证明实际文件能解码。将其放大到1080×1920或切成120原生格不能提高原生信息量。
