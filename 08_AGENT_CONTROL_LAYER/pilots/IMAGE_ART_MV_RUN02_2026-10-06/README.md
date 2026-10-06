# 《若爱有尽头》GPT 电影插画 MV · Run02

本轮解决 Run01 代码动画的人物、场景和光影过于简化的问题。用户已选择 A「电影插画」。使用 GPT 内置生图制作统一人物与场景，保留 Huashu Canvas 逐帧渲染器、原音频及八句歌词时间轴。

## 锁定与范围

- 音频：用户确认的 Run02《若爱有尽头》完整 21.360907 秒片段；SHA256 见 audio_meta.json。
- 八句歌词顺序、原时间轴和 ±0.25 秒既有容差不变。不是一次新的逐词听辨结果。
- 蓝夜、断红线、破碎合照、空房间、回忆停留、攥住围巾和结尾原地停留的叙事保留。
- 用移动合照纸片表达“远走”，没有把静态人物贴图平移冒充步行。
- 新增 image generation；没有调用视频生成模型。本轮为独立 pilot，不解锁正式 FRESH_PROJECT 的生产阶段。

## 美术资产

engine/assets 下包含六个 PNG：master、bridge、woman、memory、room、close。

master 是用户选定的母图；bridge 为清理人物后的背景；woman 保留真正的透明 alpha，代码按鞋底锚点恢复比例与位置；memory 为相同画风的双人合照；room 为两椅两杯的空房；close 为同一女主背面的围巾近景。

源图通过内置 image_gen 生成；提示词存于 image_prompts.json，原始图像大小和校验值存于 asset_manifest.json。生成后的源文件未做代码抠图或图像修补。Canvas 只在渲染时合成、取样和动画。

## 动画与限制

- 红线分离及末端摆动；围巾/发丝局部风动；水面反射、柳枝、薄雾与灯光循环。
- 合照按带折线的四块纸片拼合、右侧分离、回归停留；画内人物不做人体平移。
- 空房间：窗帘从上端固定点轻摆、灯光轻微变化、近杯热气；近景：松散衣料与发丝局部摆动。
- 运镜只做低幅度的平稳推进或拉远；字幕位置固定。
- 人物属于有限插画动画；没有完整的连续表演、走路或手指收紧关键帧。不能把局部图像形变宣称为模型生成的人体动作。
- imagegen 的造型、背景细节会有小幅差异；参考图维持服装、发饰、背面姿态和光色，但不是像素级角色注册。

## 复用

GitHub 保存本目录的源代码、提示词、时间轴和 QA。大体积的图像、字体、音频、成片随“若爱有尽头_GPT电影插画MV_素材交付包.zip”交付，避免在仓库重复存媒体。

下载仓库和素材包后，把包中的 engine/assets 和 engine/lib/fonts 拷贝到本目录的相应位置。运行环境为 Python 3.12、Playwright 1.51、FFmpeg。无需本地运行生成模型。

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python engine/render.py --film night --fps 30 --crf 18 --audio audio/source.mp3 --out result.mp4
python verify_export.py result.mp4 audio/source.mp3 --out technical_qa.json
python qa.py --project engine --film night --fps 15 --sub-band 0 --out qa
```

浅底无字幕的字幕区门不适用于本片纹理暗底；字幕实际布局由全片抽帧检查。音频包内文件可放在 audio/source.mp3，也可把 --audio 指向用户已有原 MP3。

## 验收

最终技术结果和独立审片意见见 RESULT.md、technical_qa.json、qa/qa.json、INDEPENDENT_REVIEW.md。美术是否满足用户审美，仍以观看成片后的用户反馈为准，不以“文件已生成”代替。
