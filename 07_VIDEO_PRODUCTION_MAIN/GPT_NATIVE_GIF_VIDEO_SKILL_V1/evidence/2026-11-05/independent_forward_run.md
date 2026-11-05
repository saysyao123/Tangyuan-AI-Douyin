# 本地正向使用记录

已真实生成5秒GIF与MP4，并完成技术回读与全部帧静态检查。**技术通过；视觉因抬手重影标记FLOW_REJECTED，完整播放仍为PLAYBACK_PENDING。** 本记录不把文件生成等同于成片验收完成。

## 实际输入、版本和能力

输入：`native_source_30frames.gif`，144×328，30帧，每帧170ms，总时长5100ms，GIF89a，无透明像素，原源循环标记0。输出保留原尺寸；既未拉伸到9:16，也未放大。

本地main与HEAD均为 `4ba129c6e178491139fb879e0dc0900e1063db1d`。任务要求按工作区当前文件执行，工作区原先已有v1.1.0未提交变更；没有声称该工作区内容属于main提交。遵守本地操作限制，未查询远端main，因此该SHA仅是本地main，不证明远端最新。

实际执行脚本SHA256：`52dbc92ee99a3e4de77cb242864fb0c4be32bf9b42b3ce6356ebdad019792d37`。执行期间主线程更新了检查页来源，后观察到脚本SHA为 `fa0062ab03161d8a491e5a8281bb51e8314eade8d6451652b7c970502caf79ce`。已保存两份副本；重建的实际执行副本经过全文件SHA校验，与生产报告完全相符。该操作仅在输出目录进行。

已有环境：Python3.12.14、Pillow13.0.0、NumPy2.3.5、OpenCV5.0.0、FFmpeg/ffprobe6.1.1与libx264。无安装、无API、无付费服务、无生成调用、无推送。本次工具schema支持2–16帧GIF，不将历史30帧资产当作当前可单次生成30帧的证明；`gpt-native`为沿用历史素材来源声明。

## 命令

完整实际命令与执行结果保存在 `commands.log`。核心顺序为：

```bash
python /workspace/scratch/d3b00ac4fe49/repo/07_VIDEO_PRODUCTION_MAIN/GPT_NATIVE_GIF_VIDEO_SKILL_V1/scripts/gif_to_video.py --input /workspace/scratch/d3b00ac4fe49/historical_package/GPT_NATIVE_GIF_VIDEO_SKILL_V1/examples/native_source_30frames.gif --out /workspace/scratch/d3b00ac4fe49/forward_use_result/inspect --inspect-only
```

实际看完全部30帧源检查页后：

```bash
python /workspace/scratch/d3b00ac4fe49/repo/07_VIDEO_PRODUCTION_MAIN/GPT_NATIVE_GIF_VIDEO_SKILL_V1/scripts/gif_to_video.py --input /workspace/scratch/d3b00ac4fe49/historical_package/GPT_NATIVE_GIF_VIDEO_SKILL_V1/examples/native_source_30frames.gif --out /workspace/scratch/d3b00ac4fe49/forward_use_result/result --seconds 5 --fps 24 --scale 1 --source-reviewed --source-origin gpt-native
python /workspace/scratch/d3b00ac4fe49/forward_use_result/readback_check.py
```

以上均exit0。首次inspect/result/decoded_review均不存在，不存在旧成片冒充本次结果。脚本内部耗时约1.77秒。所有编码器、探测和回读子命令见JSON。

## 技术QA

| 项目 | 实测结果 |
|---|---|
| GIF | GIF89a；120图像块；144×328；5000ms；100×40ms＋20×50ms；disposal1；无透明；无循环扩展 |
| MP4 | H.264 High；yuv420p；144×328；SAR1:1；120帧；5.000000秒；r/avg均24/1；无音轨 |
| 时间戳 | 全部120个MP4帧按n/24核对通过 |
| 完整解码 | FFmpeg严格错误模式通过，stderr为空；Pillow回读全部GIF帧通过 |
| faststart | moov在偏移32，mdat在偏移2164，顺序正确 |
| 来源计数 | 30 source_sample＋87 interpolated＋3 terminal_hold |
| 光流 | 默认双向Farneback；相邻29对缓存；共58次计算 |
| 比例与缩放 | scale1；无拉伸；偶数宽高不需右/下补边 |
| 技术脚本状态 | TECH_PASS_VISUAL_PENDING |
| 独立视觉状态 | FLOW_REJECTED；PLAYBACK_PENDING |

输出GIF的117、118、119帧与前一帧逐像素重复，属于自然末尾停留。MP4采用有损编码，这些停留帧解码后未保持逐像素相同；不据此虚报新的动作。

## 文件

| 文件 | 大小 | SHA256 |
|---|---:|---|
| result/animation.gif | 3,709,590字节 | `0a65b607d1f54877b3dd46caa40e571e716cb1e8303862b1d498a79b6c9cdd3e` |
| result/animation.mp4 | 109,869字节 | `021655f59b31c909126055d8a0ce03edc7179c88ad08b1f6d899b2d77f647f2b` |
| result/qa_contact_sheet.jpg | 149,029字节 | `c98de25aa3003134e70d5efe078749e251998e250d9220202e1edd15240c12c7` |
| native_source_30frames.gif | 900,262字节 | `9b4c6b7d59a244071a327d760c622c91cf8e7127028acbee3bd2c4ca51df9e9b` |

`result/source_report.json`和`result/qa_report.json`为脚本原样报告；`readback_report.json`为独立真实文件回读报告；`VISUAL_REVIEW.md`含全部已观察时间码、失败证据和播放边界；`execution_provenance.json`含环境、版本和快照哈希；`decoded_review/`含真实GIF、真实MP4各120帧检查页及动作细节图；`used_source_snapshot/`含规范和源码副本。

## 操作障碍与验收

1. 本地main内容与工作区修改不一致，且脚本在生产后发生并发更新；已明确区别，并以实际执行时记录的脚本哈希锁定证据。
2. 最初版本检查页来自编码前像素；已另行完整解码真实GIF/MP4并生成、查看全部页，弥补这一检查漏洞。
3. 实际看到输出66帧（2.750s）手部半透明双轮廓，65–67帧相关问题见细节图；技术数值没有检测出这个美术错误。未擅自把失败样本判为视觉通过。
4. 此执行Agent未取得实时播放画面和起止证据；播放检查尚未完成。

本次完成了真实转换、规格验证、源帧和输出帧检查与失败记录。最终视觉通过未达到；算法或源动作仍需改进，后续变更须新样本复验。本Agent没有修改仓库。没有改脚本，因此本任务没有重跑全量工程回归；此一正向样本也不能证明全量工程边界或未来生产效果。
