# ROADMAP_AND_GATES｜Tangyuan Dola Studio

> 原则：每一阶段只有通过 Gate 才进入下一阶段。未通过时做单变量修正，不允许跳级堆功能。

## P0｜Reference + Project Lock

目标：把参考软件、项目目标、边界和开发顺序固化。

交付：
- 项目宪章；
- 架构；
- 原软件功能镜像；
- Roadmap；
- Current Status；
- New Chat Start Prompt；
- Decision Log。

Gate P0：
- [ ] 文档全部存在；
- [ ] 30 秒仍被列为核心验证目标；
- [ ] 原软件功能没有因“暂不实现”而从研究表消失；
- [ ] 新对话可通过启动文件恢复目标和当前阶段。

---

## P1｜Minimal Browser + A/B Session

目标：做出第一个可运行桌面程序，只证明多账号 Session。

实现：
- .NET 10 WPF 工程；
- WebView2；
- Account Panel；
- Add/Delete/Rename Profile；
- 每 Profile 独立 UDF；
- BrowserHost；
- Dola 首页；
- Start/Stop；
- Profile 独立 download/log path。

不在 P1 做：
- Storyboard；
- 自动提交视频；
- 指纹；
- MachineGuid；
- 30s patch；
- Cookie Import；
- 多账号任务轮换。

Gate P1：
1. 建立 A/B 两个 Profile；
2. 用户分别正常登录自己的 Dola；
3. 完全退出应用；
4. 重开后 A 仍为 A、B 仍为 B；
5. A/B 启停与切换 20 次；
6. 清除 A 浏览数据后 B 不受影响；
7. 不出现 UDF 锁死或无解释崩溃。

通过标准：`SESSION_AB_PASS`。

---

## P2｜Reference-like UI + Resource Shell

目标：在 P1 稳定核心上还原参考软件有价值的三栏工作台。

实现：

```text
AccountListPanel | BrowserHost | ResourcePanel
```

增加：
- 顶部状态；
- Current Profile；
- Download directory；
- Resource cards；
- VideoPreview；
- Log Viewer；
- Instance Settings；
- Working Directory。

Gate P2：
- UI 不影响 P1 Session 稳定性；
- Profile 切换后 Resource / Download 上下文同步；
- 任何 Profile 操作都能在日志追踪。

通过标准：`WORKBENCH_UI_PASS`。

---

## P3｜Dola Adapter + Capability Detector

目标：不修改平台能力，先准确读出“这个账号现在到底能做什么”。

实现：
- 页面 Ready 状态；
- 登录状态；
- 当前模型可见状态；
- 页面公开时长；
- 5/10/15/30 capability record；
- UNKNOWN / MODEL_SUPPORTED / PLATFORM_EXPOSED / ACCOUNT_ALLOWED / SERVER_VERIFIED 状态机。

30 秒测试协议：
1. 选择当前账号正常公开的 Seedance 2.5；
2. 记录 UI 是否出现 30s；
3. 若出现且允许正常提交，则创建真实任务；
4. 正常等待结果；
5. 下载结果；
6. 检测实际时长；
7. 使用至少 3 个不同任务重复。

Gate P3：
- 探测结果不能靠硬编码；
- 不能把“页面有 30”直接当 PASS；
- 真实文件 >= 29s 且 3 次测试满足要求才记录 `30S_PASS`；
- 若当前账号没有 30s，必须记录 `30S_NOT_AVAILABLE_CURRENT_PATH`，不得伪装成功。

---

## P4｜Download + Media QA

目标：把生成结果稳定变成可管理素材。

实现：
- WebView2 DownloadStarting；
- 正常下载归档；
- 平台自身暴露的原始下载信息识别；
- download/main/backup source 模型；
- ffprobe 检测；
- 首帧/缩略图；
- 可见水印 QA；
- ResourcePanel 正式接入。

Gate P4：
- 连续至少 5 个视频下载成功；
- 文件与来源 Profile 不串；
- 视频均可播放；
- 时长/分辨率/编码可读取；
- clean source 只在证据成立时标记。

通过标准：`DOWNLOAD_MEDIA_PASS`。

---

## P5｜Local Automation Bridge

目标：给 Codex / 本地脚本稳定入口，但保持浏览器操作可见、可控。

第一版：

```text
GET  /health
GET  /profiles
POST /profiles/{id}/open
POST /profiles/{id}/close
POST /profiles/{id}/navigate
```

要求：
- localhost only；
- 明确日志；
- 不提供批量账号注册/验证功能；
- 不依赖屏幕坐标自动化。

后续只有在用户明确选择且现有 Gate 全部 PASS 时，才评估任务辅助接口。

Gate P5：
- Codex 能查询并打开指定 Profile；
- API 操作和手动操作结果一致；
- 不影响 Session；
- 外部网络不能直接访问服务。

通过标准：`LOCAL_BRIDGE_PASS`。

---

## P6｜Storyboard + MV Integration

目标：正式服务汤圆 MV Pipeline。

实现：
- Project；
- Shot；
- Prompt；
- First-frame asset；
- Generated video；
- Profile / Platform source；
- QA result；
- Export to MV production folder。

不把 Dola 绑死为唯一后端：

```text
IVideoPlatformAdapter
├─ Dola
├─ Other official web entry
└─ Official API / future adapter
```

Gate P6：
- 一个实际 MV 片段能从 Shot → Dola/Seedance → Download → Resource → MV 素材目录完整走通；
- 软件层故障不改变 MV 导演规则；
- 替换视频平台 Adapter 不需要重写 Account/Resource/MV Core。

通过标准：`MV_BRIDGE_PASS`。

---

# 全项目禁止跳过的 Gates

```text
P0 Project Lock
↓
P1 SESSION_AB_PASS
↓
P2 WORKBENCH_UI_PASS
↓
P3 30S capability conclusion
↓
P4 DOWNLOAD_MEDIA_PASS
↓
P5 LOCAL_BRIDGE_PASS
↓
P6 MV_BRIDGE_PASS
```

P3 的结论可以是 `30S_PASS` 或“当前路径不可用”的真实结论；不能因为 30 秒失败就伪造通过，也不能因为失败就删除 30 秒目标。

---

# 失败处理规则

遇到失败：
1. 定位层：SESSION / BROWSER / PAGE / CAPABILITY / TASK / DOWNLOAD / MEDIA_QA；
2. 保存日志和最小复现；
3. 一次只改变一个主要变量；
4. 重测当前 Gate；
5. 只有重复有效的修复才能进入 Decision Log；
6. 不因单次失败整体重构。
