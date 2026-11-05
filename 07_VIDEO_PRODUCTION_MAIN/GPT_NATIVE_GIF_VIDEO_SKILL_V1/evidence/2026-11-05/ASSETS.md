# 本轮真实素材与成片索引

原生素材来自用户已有历史ZIP；本轮未重新生成原生GIF。大型媒体保留为可读取文件，源码仓库只提交脚本、text-only fixture、结果JSON及小型关键帧证据。以下链接需要文件所有者账户访问，不承诺匿名公开。

| 文件 | 真实位置 | 状态 |
|---|---|---|
| native_source_30frames.gif | [打开/下载](https://chatgpt.com/library?file_id=libfile_2c8d3355e590819195ef7fe9d8b09290&account_id=personal) | 原始30帧/5100ms，未改写 |
| rain_window_full30_audit.mp4 | [打开/下载](https://chatgpt.com/library?file_id=libfile_a5583f348f888191926f4274ded3297e&account_id=personal) | 完整原动作后处理；技术通过，手部FLOW_REJECTED |
| rain_window_full30_audit_120f.gif | [打开/下载](https://chatgpt.com/library?file_id=libfile_baecae3917508191814a12afa9e5e5b1&account_id=personal) | 同完整动作GIF；120帧/5000ms，视觉失败保留 |
| rain_window_micro_5s.mp4 | [打开/下载](https://chatgpt.com/library?file_id=libfile_aded40a7c1b48191a6df529570b2f6ac&account_id=personal) | 原帧0–14重定时；低幅微动回退样片 |
| rain_window_micro_120f.gif | [打开/下载](https://chatgpt.com/library?file_id=libfile_796fc1e08a1481919ba6a42a8133fde8&account_id=personal) | 微动GIF；120帧/5000ms，显示2倍，非高清修复 |
| gif_video_A_B_5s.mp4 | [打开/下载](https://chatgpt.com/library?file_id=libfile_b0bff4cf2fac8191804d0a3f9f25b49e&account_id=personal) | 左旧索引版，中新版完整动作，右不同动作范围的微动回退；右侧不是同动作修复 |
| gif_video_audit_QA.json | [打开/下载](https://chatgpt.com/library?file_id=libfile_411dd2d6535c819199f99985ea712836&account_id=personal) | 测试、A/B、技术和视觉完整JSON |

## SHA256

```text
9b4c6b7d59a244071a327d760c622c91cf8e7127028acbee3bd2c4ca51df9e9b  native_source_30frames.gif
021655f59b31c909126055d8a0ce03edc7179c88ad08b1f6d899b2d77f647f2b  rain_window_full30_audit.mp4
0a65b607d1f54877b3dd46caa40e571e716cb1e8303862b1d498a79b6c9cdd3e  rain_window_full30_audit_120f.gif
20d7df156fe0aa8000d38817018d733f94b5c19f7b465de32811bb470899004c  rain_window_micro_5s.mp4
1ca0abb6d618c01734b593924cfa457d62d8c7492e3273d729a25b2518e37a3a  rain_window_micro_120f.gif
730cb7a004fc62ea104d122ff04d6072a0b828d21deed8ffadd2f013f71010e1  gif_video_A_B_5s.mp4
7369c411044fe83137f263b67d1ce7b60a188e940e2fb4910eb5c928077eeb1d  gif_video_audit_QA.json
```

源30帧144×328，完整后处理源采样30＋光流87＋末尾hold3。微动源范围0:15、2550ms→5000ms，15源采样＋98光流＋7末尾hold，288×656仅是2倍显示。原完整动作失败不因微动回退通过而自动变成通过。
