# 当前状态与唯一续作入口

更新时间：2026-10-16。历史报告按原验收范围保留，不能用本页把旧证据升级为新的通过。

- T1 完整原创短篇：已发布，真实任务、双场景、战斗、跨页存档与编辑保存重开已通过。
- T1.1：失焦输入、显示插值和轻量缓冲已发布；短时回调测试不等于引擎长期稳定证明。
- T1.2：当前建设可靠性基底；新异常/存储/发布/真实引擎活动验证待本轮 CI。未通过前不得标为已发布。
- T2 通用 IR→content22：尚未实现/验收。旧 pipeline.mjs 与轻量 HTML 只为参考测试夹具。
- EXE 后置；暂无需用户提供书籍。

试玩：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site

## 唯一正式构建路线

固定上游 IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246，Node22.19+、pnpm10.17.1、Python3/Pillow；在已安装依赖的上游 checkout 执行：

```sh
node tools/type_pal_t1_build.mjs /absolute/type-pal /absolute/output
python3 tools/release_inventory.py check /absolute/output
```

命令从本目录执行。产物用 HTTP/HTTPS 静态服务访问；不能把 file:// 双击当作运行保证。

续作先读本页→docs/T12_FOUNDATION_TASK.md→最新 RELEASE 记录→对应失败经验，按未通过项继续。P0/旧首场景冒烟不重跑。引擎/恢复改动才回归受影响的原完整故事，作者入口改动才回归编辑保存重开。
