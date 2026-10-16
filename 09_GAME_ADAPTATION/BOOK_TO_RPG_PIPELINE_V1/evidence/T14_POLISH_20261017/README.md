# T1.4验收与交付索引

当前私有试玩：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/pilot/

- `RELEASE.json`：正式发布、源码、下载与实测边界。
- `PAL_REFERENCE_AGGREGATE.json`：原始MKF实际解码统计，无商业图像。
- `NATIVE_ART_AUDIT.json`：最终RLE经官方解析，人物每向3帧互不相同。
- `ATTEMPT_1.json`：新美术四方向像素匹配、真实同伴绘制采样、旧结束存档接新段通过；测试路线撞NPC后的真实失败保留。
- `ATTEMPT_2.json`：新对白/青年交谈已通过，切图前对白未推进导致测试等待超时。
- `FINAL_CONTINUATION_PASS.json`：只从native合法检查点继续未过部分，小院/结局/保存重开/七步外壳通过。
- `PRIVATE_RELEASE_MATCH.json`、两份runtime清单：283个相同路径，257项逐字节相同，26项只为私有文字呈现；公共/私有54个原生内容文件机制和二进制一致。
- `FAILURES_AND_LIMITS.md`：失败原因、修正与未做范围；没有把前两次整体失败改写为PASS。
- `dialogue-framed.png`、`courtyard.png`、`shell.png`：最终素材与新UI的公共原创台词截图。原书对白仅在私有试玩中。

独立代码复核accept；用户对美术与实际书籍台词的观感待试玩反馈。全仓商业工程fixture未分发，因此不宣称全仓统一静态门通过。既有P0/T1/T11/T12套件未重复运行。
