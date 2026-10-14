# 本轮完整试片记录

本目录只保存配置、来源、适配补丁和验收证据。最终MP4、逐句音频和可恢复工程已随本轮交付ZIP提供；不把二进制源片和模型放入Git。

复用原gossip_video_workflow时，复制为独立云端工程，应用baseline_adapter.patch，将av==15.1.0加入requirements.txt，运行已有bootstrap.sh，再用episode_retrieve_originals.json与--stt导出。原基线及Actions配置未覆盖；本次在Work云端实际导出，未声称触发了新的GitHub Actions运行。

# 热点真实视频试片｜2026-10-14

本包是完整中文实片工程，沿用 gossip_video_workflow 的 React/GSAP 渲染、纸白/安全橙、逐句 Kokoro 中文女声与原创 BGM 侧链压低。没有公开发布。

## 看成片

观看“绕月资料公开_1080x1920_中文试片.mp4”。720P版本用于快速预览。质量结论和仍待用户判断的听感/观众吸引力见 QA报告.md。

## 恢复工程

Linux云端安装：bash engine/bootstrap.sh

使用已锁定逐句音频和已取得真实片段重导：engine/.venv/bin/python engine/run.py --episode episode.json --stt

原始源视频恢复配置：episode_retrieve_originals.json，指向官方公开HTTPS文件；素材访问和使用条件必须按本次来源清单重新核对。本包只保存用到的源片段，避免让用户下载两GB完整直播。sources.json保留原视频区间和所用片段哈希；evidence/raw-downloads.json保留完整原视频SHA256。

engine是已验证原引擎的独立副本，增加首尾镜头可用动态媒体的适配，并使临时帧清理失败立即报错。baseline_adapter.patch列出全部差异；原仓库基线未覆盖。新增av==15.1.0，修复faster-whisper与av19音频文件读取不兼容。

## 素材与使用范围

本轮是非商业、信息介绍用途的私下试片；NASA媒体指引允许相应使用，保留明确影像来源，不含NASA对GPT文案的审定或代言。NASA/CSA联名标注图按非商业个人信息使用范围记录。以后用于广告、商业代言、产品包装或其他超出本轮用途的发布，不应把本次依据视为全面商业授权。人物及实物标识均来自任务实拍，未借用于代言。

使用规则：
- https://www.nasa.gov/nasa-brand-center/images-and-media/
- https://www.asc-csa.gc.ca/eng/terms.asp

四无婚礼暂缓：已读媒体页，但未取得复用授权；没有使用他人婚礼画面或课程录屏替代本次素材。

新话题依据：10月7日官方资料公开、10月9日Wired与10月11日The Verge报道。未获得中文平台热榜排名/播放量，也未证明与四无婚礼同量级热度。

评论依据：十月Reddit转发页未返回可引用评论；另读四月同任务评论，包括用户希望观看“舱内到窗外”的第一人称视频。其日期保留为四月，没有冒充十月评论，更没有把评论推测写成事实。

课程学习边界：复用此前三课画面分析，补核第1课关键画面、第2课20:00至20:50音频。关键音频确认了AI润色后继续人工编辑的动作。未宣称72分钟完整转写已经完成。
