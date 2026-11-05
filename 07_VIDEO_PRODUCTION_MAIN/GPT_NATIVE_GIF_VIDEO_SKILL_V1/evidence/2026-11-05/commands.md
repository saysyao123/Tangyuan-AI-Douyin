# 实际执行与可复跑命令

工作目录：`/workspace/scratch/d3b00ac4fe49/repo`；源码基线SHA：`4ba129c6e178491139fb879e0dc0900e1063db1d`。

## 已运行（退出码）

- 原版：`python3 ../audit_evidence/legacy_gif_to_video.py --input ../historical_package/GPT_NATIVE_GIF_VIDEO_SKILL_V1/examples/native_source_30frames.gif --out ../audit_evidence/legacy_real --scale 1`；exit0。
- 最终回归（专项目录）：`python3 tests/run_regression.py --out /workspace/scratch/d3b00ac4fe49/audit_evidence/regression_final`；exit0，37/37；含9:16、有声AAC、完整解码、时长、disposal、透明度、负例和文档契约。
- 完整真实源：`python3 07_VIDEO_PRODUCTION_MAIN/GPT_NATIVE_GIF_VIDEO_SKILL_V1/scripts/gif_to_video.py --input ../historical_package/GPT_NATIVE_GIF_VIDEO_SKILL_V1/examples/native_source_30frames.gif --out ../audit_evidence/release_real --source-reviewed --source-origin gpt-native --scale 1`；exit0，技术PASS，视觉FLOW_REJECTED。
- 微动回退：同脚本与输入，`--source-range 0:15 --out ../audit_evidence/micro_motion --source-reviewed --source-origin gpt-native --scale 2`；exit0，技术PASS，视觉仅低幅片段PASS_WITH_LIMITATIONS。
- 基准：`python3 07_VIDEO_PRODUCTION_MAIN/GPT_NATIVE_GIF_VIDEO_SKILL_V1/tests/benchmark.py --legacy-script ../audit_evidence/legacy_gif_to_video.py --real-source ../historical_package/GPT_NATIVE_GIF_VIDEO_SKILL_V1/examples/native_source_30frames.gif --out ../audit_evidence/benchmark_final`；exit0，原版脚本可从基线提交读取。
- 真实坏120帧：实际命令、exit2与标准错误见 `rejected120_command.json`，没有编码MP4。

## FFmpeg MCI 真实对照

```bash
ffmpeg -hide_banner -loglevel error -y -ignore_loop 1 \
  -i historical_package/GPT_NATIVE_GIF_VIDEO_SKILL_V1/examples/native_source_30frames.gif \
  -vf 'setpts=PTS*5/5.1,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop_duration=1,trim=duration=5,setpts=PTS-STARTPTS' \
  -frames:v 120 -r 24 -c:v libx264 -crf 18 -pix_fmt yuv420p \
  -movflags +faststart audit_evidence/minterpolate_padded_real.mp4
```

exit0，120帧/5s。初次同命令stop_duration=0.5时虽exit0，却只有112帧/4.666667s；因此不能只看编码退出码。补尾仍有视觉软化和停留，没有同动作改善证据，不升默认。

## 实际播放与边界

Chromium134缺H264编解码支持，直接MP4浏览器播放不可用。FFmpeg解码MP4后无损VP9封装，120个YUV420p帧哈希逐个相同；浏览器实时时钟从0前进至5秒并触发ended。播放事件、等帧验证已存本目录；执行AI另实际查看全帧页及播放截图，完整30帧样片的手部仍拒绝。

这不是直接MP4浏览器播放，不将格式解码与人眼观看混为一谈。依赖中的生产脚本不需要Chromium／Playwright，播放是本轮独立审查工具。

## GitHub CI

没有触发或宣称GitHub Actions通过。回归脚本可离线本地运行，也可以被已有CI调用；本轮可核验的是提交内实际本地测试证据及媒体哈希。
