# 来源与许可

本目录的渲染工程借鉴并改写自 op7418/guizang-product-video-skill 的起步工程与已交付的中文新闻集锦工程。保留原作者 Copyright © 2026 op7418。此目录中派生/新增的工作流工程代码按 GNU AGPL-3.0 发布，完整条款见 LICENSE；不改变仓库其他目录原有的MIT许可。

上游基准版本：

- https://github.com/op7418/guizang-product-video-skill — c2ce3491f71bc127fdec3dc468714df469a967c8
- https://github.com/op7418/guizang-social-card-skill — cf4b810fac1c73fb65a2bb31d8c9278d82cbc4c5
- https://github.com/op7418/Humanizer-zh — f4518a8eab97b8bfebc66a89d34320a89bef6930

新环境如需加载上述技能，读取固定版本的SKILL.md及其实际引用文件，不将本目录当上游技能本身。源码不要写入上游技能目录。这里归档的是用户的独立工作流，并未创建或修改个人技能。

免费配音使用 hexgrad/Kokoro-82M-v1.1-zh；代码 https://github.com/hexgrad/kokoro ，中文发音 https://github.com/hexgrad/misaki 。模型与库按其各自Apache-2.0许可使用，不提交模型权重。默认声线zf_001，不声称真人，也不克隆新闻当事人。

字体使用 notofonts/noto-cjk 的 Noto Sans CJK SC，SIL Open Font License；下载使用官方仓库。运行器提取成片字体，仅随交付保留适用字体许可。第三方公开素材 URL 是溯源，不代表获得无限制再分发许可；原影片不提交 Git。

自检片的视频由FFmpeg testsrc2程序生成，音乐为本工作流代码原创稀疏器乐，不使用外部歌曲样本。自检内容不含真实新闻或虚构当事人，不拿自检片当成用户要求的热点集锦。
