# Runtime Module Tests v1.0

> 目的：修改一个模块时，先做局部回归，不必每次重跑完整视频。

## Test原则
每个 Workflow / Rule 修改都至少检查：
1. 输入Contract是否仍兼容；
2. 输出字段是否仍兼容；
3. 是否意外覆盖其他模块职责；
4. 是否新增重复规则源；
5. 是否需要更新 MANIFEST。

## Core Cases

### T01｜Script / Hook
输入：真实失败案例 + 已锁核心观点。
通过：Hook制造信息缺口但不发明新主题，正文能兑现。

### T02｜Audio ASR
输入：实际录音与略有差异的旧稿。
通过：逐字稿跟随真实音频，不自动纠正成旧稿。

### T03｜Director Material Coverage
输入：一个Director镜头引用不存在素材。
通过：状态必须停在 `MISSING/ASSUMED`，不得Lock。

### T04｜Visual Alignment
输入：黄色小框 + “37粉丝”。
通过：文字在框中上下左右视觉居中；手机端可读；不与字幕重复则保留，否则删除。

### T05｜HyperFrames
输入：错误顺序→正确顺序解释。
通过：存在Teaching Truth、Anchor/Variable/Consequence、唯一Signature Move；无Slideshow/Screensaver/Card Wall。

### T06｜Rule Promotion
输入：单条视频表现较好。
通过：只能进入Experiment，不得直接升级PERFORMANCE_VALIDATED。

新增模块至少补1个能抓住其主要失败模式的Case。
