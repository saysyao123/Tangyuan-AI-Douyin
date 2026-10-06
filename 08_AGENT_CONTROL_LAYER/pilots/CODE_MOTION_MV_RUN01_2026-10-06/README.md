# 《若爱有尽头》代码动画 MV 实验 Run01

## 目标与边界

把既有的歌词时间轴接入 huashu-art-motion 帧引擎，制作一条 21.36 秒、9:16 的音乐视频，验证无需视频生成模型的制作路径。此目录是独立能力实验，正式 Fresh Project 的选歌、S1 封存和 S2 阻断状态均不改变。

音频复用 `MV_RUNTIME_V0_1/stages/01_PROJECT_AUDIO/S1_DELIVERY_RUN02_FINAL.yaml` 中用户已确认使用的完整片段，不复用已否决的《告别》，也不把《一个人在家》的测试来源升级为制作选歌。

## 当前视觉决定

用户已从同构图三方向中选择 **A 蓝夜剪影**。备选 B 灰墨薄雾、C 暖色纸景是本实验的配色和材质候选，不能代表已复刻水墨或剪纸的全部传统技法。

八句歌词使用统一的月光、桥、红线、照片与剪影角色。动作包括红线分开、回环、照片碎片拼合、空座与杯中蒸汽、人物步行远去、照片停留和收紧红线。镜头采用单方向推近，环境动作由枝叶、水面和颗粒承担。

## 真实复用的模块

- 上游项目：`alchaincyf/huashu-art-motion`，commit `26dba25b2b495c2138848c29a2c90df356a20325`，MIT，许可保存在 `HUASHU_LICENSE.txt`。
- 使用其 `engine.js`、场景装载器、`util.js`、`motion.js`、crossfade 转场、`render.py` 和 `qa.py`。
- 本实验新增 `scenes/mv.js`、段落表、歌词叠层、音频元数据及实验记录。
- 帧引擎仅改为 1080×1920；渲染器增加可选 Chromium 路径、FFmpeg 返回码检查、faststart，取消会截掉尾部 B 帧的 -shortest，并用 medium 编码预设。
- 中文字由代码与内置字体绘制，字体许可见 `engine/lib/fonts/`；字体二进制通过固定上游 commit 和 SHA256 恢复，不重复提交到仓库。
- 没有调用视频生成模型，也没有调用图片生成模型。

## 时间轴与精度

`timeline.json` 是本轮输入。其八句边界源于旧项目对原视频字幕的视觉检查，容差约 ±0.25 秒；没有重新生成词级 ASR，也不宣称音画逐词达到单帧精度。

新下载的 MP3 解码时长为 21.362358 秒，与原交接中的 21.360907 秒相差约 1.45 毫秒。容器时长 21.394286 秒包含 MP3 帧封装差异。视频按 30fps 取 641 帧，名义时长 21.366667 秒。

## 复现

依赖 Python、Playwright Chromium、FFmpeg、numpy、Pillow。此云端测试使用 Python 3.12、Playwright 1.51.0。

```bash
python -m pip install playwright==1.51.0 numpy pillow
python -m playwright install chromium --only-shell
python bootstrap_fonts.py
python engine/render.py --film night --fps 30 --audio /path/to/confirmed_audio.mp3 --out mv.mp4 --crf 18
python qa.py --project engine --film night --fps 15 --sub-band 0 --out qa
```

音频来自用户已提供的片段，仓库只保留文件哈希、来源身份和时间轴；复现者自行提供同一音频。导出视频与包含音频的测试包单独交付。

`qa.py` 的诊断阈值不是自动封存门。底部歌词属于成片叠层，额外通过整片抽帧检查；深色纹理背景不适用上游浅底无字幕的 `subzone_gate.py`。

## 验收

最终依据 `RESULT.md`、`technical_qa.json`、`qa/` 和独立审片记录。渲染完成不代表审美已被用户接受，也不证明当前正式 S0/S1 自动选歌链已跑通。
