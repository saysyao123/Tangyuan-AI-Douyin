# Run03：动态导演评估与人物动作实验

本目录是《若爱有尽头》电影插画 A 的动态实验。原完整 MV 仍见兄弟目录 `IMAGE_ART_MV_RUN02_2026-10-06`。这里没有替换完整片，也没有更改正式流程的批准状态。

- `DIRECTOR_DYNAMIC_PLAN.md`：在原八句、21.36 秒时间轴上的动作升级计划。
- `DYNAMIC_PROMPTS_DRAFT.md`：K0/K1/K2 动态提示词草案，未声称视频模型生成成功。
- `CAPABILITY_ASSESSMENT.md`：本项目可追求的 2.5D 动画目标和实际证据边界。
- `probe_contract.json`：5.11 秒试片范围与真实图集规格。
- `gesture_atlas_prompt.txt`：本轮唯一新 imagegen 素材的实际生成提示词。
- `INDEPENDENT_REVIEW.md`：修订成片的独立审片；初版报告保留在 `reviews/`。
- `verification/`：技术导出与动感 QA；技术通过不代表人物动作达到正式制作质量。
- `assets_manifest.json`：媒体素材字节校验。PNG、WOFF、MP4 随素材交付包提供，不写入 Git。

## 复现试片

安装 Python 依赖、ffmpeg 与 Playwright Chromium。将媒体交付包的 `engine/` 合并到本目录对应路径，将 `audio/motion_probe_audio.wav` 作为原曲末段音源。字体及许可随包提供；`bootstrap_fonts.py` 是另一个字体恢复途径。

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
python3 engine/render.py --film night --fps 30 --crf 18 --audio audio/motion_probe_audio.wav --out probe.mp4
python3 verify_export.py probe.mp4 audio/motion_probe_audio.wav --out export_verification.json
python3 qa.py --project engine --film night --fps 15 --sub-band 0 --out qa_probe
```

字幕由原时间轴偏移 16.25 秒得到。`--sub-band 0` 关闭几何字幕带探测，本轮字幕安全区由实际成片目视复核；不能把 QA 空列表当作字幕位置检测的证据。

153 个视频显示帧来自八个角色姿态及环境合成；不是自然的 30fps 人物动画。缺失的手臂过渡姿态和接触重影仍需通过资产补画与动画修订解决。
