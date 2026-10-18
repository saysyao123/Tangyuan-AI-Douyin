# T35｜开场与场景切换旧画面闪回已修复

2026-10-18。用户已认可 T33 室内，反馈 T34 第一幕效果还不错，要求避免开场和中途出现旧画面。21:55（Asia/Shanghai）恢复额度后继续收尾。本轮只修显示加载问题，保留 203 张已认可美术和 109 个原生工程文件，没有重做游戏。

原高清显示层首帧才懒加载，未齐时自动回退旧版；首次切到含专用人物/家具的场景会再发生。波动分层也绕过高清层。现按场景并行载图并等待 decode，与原生准备共同完成后才提交场景；预加载目标不改变当前高清状态。支持高清的场景不再自动回退，只有显式 ?art=baseline 可用于对照。波动前后景共用高清路径。

截图复核又发现原加载页会把正常等待误报连接失败，已单独修正：正常提示素材加载，15秒后可继续等待或重试，真实失败显示恢复入口。未改页面布局、操作或剧情。

Run39122828856 七项定向验证 PASS：旧版慢素材反例45帧；修复版冷启动、首次后台、波动分层、家中读档、刷新重开与失败重试均无旧图帧，采样1098+90帧。Run39133926081 只补三项加载提示检查 PASS，338 个引擎文件与前次实测逐字节一致，没有重跑先前通过的旧剧情/美术套件。最终实机截图已人工复核。初次反例判定过窄的失败与修正保留在 RELEASE，不隐藏失败。

同一试玩地址已成功更新：[第一幕](https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/) · [画面与验证](https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/review/) · [已认可室内](https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/night/)。原正式 Site/main 未动。完整网页 ZIP 已更新原文件的第4版，136291908 bytes，SHA256 d89fe80e54bfaa200b6d614a4b98c57aa673bc991ee251650544ff54e5d7beb4。发布真值见 [RELEASE.json](../evidence/T35_20261018/RELEASE.json)。

后续从当前版本继续，仅按用户实际反馈调整未通过部分；不重做已认可场景，不复制重要人物到普通 NPC，不扩后续剧情。完整第一幕、T34四景、T33室内与身份、多引擎头像通过记录继续复用。当前修复已发布，最终用户复验待反馈，不能因此宣称整个项目完成。

复建：先按 tools/t32/build.mjs 构建，再运行 `node tools/t35/patch-loading-shell.mjs /absolute/output`。最终运行分支 t35-no-flash-final，源码分支 feature/t35-no-legacy-flash-20261018；完整源码包固定在当前运行提交的 downloads/corresponding-source.zip，不用旧运行分支覆盖。已知 WebKit 隐私会话缩略图限制、未验证真实手机/Safari应用的边界保留。
