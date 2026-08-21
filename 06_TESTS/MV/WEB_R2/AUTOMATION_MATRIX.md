# WEB R2｜AUTOMATION MATRIX

> 目标：真实记录网页端自动化程度，不因最终成片完成而高估自动化。

## Overall

- Current Stage: `W01`
- Overall State: `AWAITING_AESTHETIC_GATE`
- Fully automated stages: `1`
- Human aesthetic gates encountered: `1`
- Human aesthetic gates passed: `0`
- External-required stages encountered: `0`
- Non-aesthetic manual interventions: `0`

## Stage Board

| Stage | 内容 | 预期 | 实际 | 用户操作 | 备注 |
|---|---|---|---|---|---|
| W00 | 能力基线 | AUTO | AUTO | 无 | GitHub read/write 可用；Web 可用；Files/Library 可用；Image Generation 接口存在，实际生产留 W05 验证；本地 ffmpeg/ffprobe、MoviePy、pydub、OpenCV 可用；无独立 Whisper/faster-whisper；不能控制用户本机/浏览器或 Seedance 外部站点 |
| W01 | 选歌研究 | HUMAN_GATE | HUMAN_GATE | 最终选歌 | 研究与筛选已由网页端自动完成；当前只等待用户从 3 个候选中做审美选择 |
| W02 | 音频截取 | HUMAN_GATE/PARTIAL | NOT_STARTED | 可能上传音频 + 试听确认 | |
| W03 | Beat分析 | AUTO | NOT_STARTED | 无 | |
| W04 | 导演/生产分配 | HUMAN_GATE | NOT_STARTED | 审美确认 | |
| W05 | 首帧提示词+生图 | HUMAN_GATE | NOT_STARTED | 整组审美确认 | Image Generation 实际生产能力在本 Stage 验证 |
| W06 | 动态提示词 | AUTO | NOT_STARTED | 无 | |
| W06-X | Seedance视频生成 | EXTERNAL_REQUIRED | NOT_STARTED | 外部生成+上传 | 当前能力基线未发现可直接执行 Seedance 的工具；到 W06-X 依真实执行正式记账 |
| W07 | 动态QA/返工设计 | AUTO | NOT_STARTED | 外部失败段重生成 | |
| W08 | 剪辑/字幕/Final | AUTO if inputs ready | NOT_STARTED | 看片确认 | W00 已验证本地音视频处理工具；当前无独立 Whisper/faster-whisper，字幕对齐方法到 W08 按同版本可靠 LRC/音频证据验证 |
| W09 | 复盘/锁定 | HUMAN_GATE | NOT_STARTED | 最终验收 | |

## W00 Capability Baseline Evidence

- GitHub connector: `VERIFIED` — 已从 `test/mv-web-r2` 读取指定文件，并可向同分支写回状态文件。
- Public Web research: `AVAILABLE` — 当前对话具备网页搜索/打开页面能力；W01 已进一步验证可执行实际选歌研究。
- Files / uploads / Library analysis: `AVAILABLE` — 可搜索、读取、物化会话与 Library 文件。
- Image Generation: `AVAILABLE_INTERFACE` — 当前对话暴露生图能力；是否满足本项目首帧质量线延后到 W05 实测，不在 W00 虚报通过。
- Local audio/video processing: `VERIFIED` — `ffmpeg`、`ffprobe`、MoviePy、pydub、OpenCV 可用，可进行裁剪、转码、抽帧、合成等本地处理。
- ASR / Whisper: `NOT_PRESENT_AS_DEDICATED_LOCAL_CAPABILITY` — 未检测到 `whisper` / `faster_whisper`；后续不得声称 Whisper 已运行。
- Seedance execution: `NOT_AVAILABLE_IN_CURRENT_WEB_TOOLSET` — 不假设能登录或控制外部 Seedance；正式状态在 W06-X 记录。
- User local machine/browser control: `NOT_AVAILABLE`。

## W01 Discovery Evidence

### Observation sources refreshed

1. `AI MV导演曹斌Johnny` — `ACTIVE_7D`。近期连续出现《山风山风等等我》《像我这样爱你的人》《踏马寻花向自由》《如果你也刚好抬头看树》等 AIMV / 卡拉OK内容，是当前最直接的 MV_VERTICAL_ADOPTION 观察源。
2. `丹鸾歌行` — `ACTIVE_7D`。近期主要信号为 Seedance2.5 影视叙事、动作与二创，不强行把其非歌曲型作品计入歌曲热度；用于确认当前 AI 影视动态审美仍在快速抬升。
3. `野仙仙AI` — `SPECIALIST_REFERENCE`。公开索引中最近可确认的代表 MV 仍为火星电台×窦靖童《Somewhere In Winter》，未发现最近约30天足够可靠的新歌曲采用信号，因此不用于抬高本轮候选热度。
4. `SANGR桑瑞` — `SPECIALIST_REFERENCE / WATCHLIST`。本轮公开索引未取得最近约30天足够可靠的新 AIMV 歌曲采用证据，不伪造活跃度。
5. `current music / platform diffusion check` — 酷我 2026-08-06 榜单 + 抖音普通创作者近30天扩散样本，用于补足 PLATFORM_HEAT / RECENT_SPREAD 信号；其中《山风山风等等我》榜单第1，《踏马寻花向自由》第8。

### Shortlist

#### C1｜《山风山风等等我》
- Heat: `STRONG` — 2026-08-06 酷我当前榜单第1；近期 AIMV 观察源采用；8月仍持续出现舞蹈教学、翻唱、生活内容。
- MV fit: `VERY_HIGH` — 山风、远方、山那头、自由感天然提供空间、运动、天气、景别与动作设计，不必依赖纯情绪站桩。
- Risk: 容易落入“古风女子 + 山景 + 风吹衣摆”同质化，Director 阶段必须主动 Anti-Copy。
- Representative video: https://jingxuan.douyin.com/m/video/7674486948253289782

#### C2｜《踏马寻花向自由》
- Heat: `STRONG` — 2026-08-06 酷我榜单第8；近期 AIMV 观察源连续制作；普通舞蹈/健身/生活内容仍在持续采用，且存在多版本改编。
- MV fit: `VERY_HIGH / HIGH-MOTION` — 歌词与节奏适合真正的移动、空间穿越、动作与多镜头语法，最适合本轮继续测试 Camera Repetition Gate 与更丰富运镜。
- Risk: “骑马 + 花海 + 国风侠女”已经非常容易俗套，必须保留自由/出走原理但更换表面视觉。
- Representative video: https://www.bilibili.com/list/3493080640522749?bvid=BV1Dh4y1Z7g8&oid=658319006

#### C3｜《如果你也刚好抬头看树》
- Heat: `STRONG / SUSTAINED` — 7月下旬曾出现抖音热榜信号，8月仍能看到文旅、舞蹈、普通内容持续采用；近期 AIMV 观察源也制作了对应 MV。
- MV fit: `VERY_HIGH / POETIC` — 树、叶、光、抬头、停驻、游牧感可以发展出清晰的歌词视觉事件，适合做治愈但不静态的诗意电影路线。
- Risk: 节奏与情绪比 C2 克制，更依赖导演把“光、树、空间变化”变成事件，不能只拍唯美空镜。
- Representative video/reference: http://t.cn/AXKFfKnH

## 状态枚举

- `AUTO`
- `HUMAN_GATE`
- `EXTERNAL_REQUIRED`
- `PARTIAL`
- `BLOCKED`
- `FAIL`

## Manual Intervention Log

| # | Stage | 类型 | 为什么需要用户 | 用户做了什么 | 是否未来可消除 |
|---|---|---|---|---|---|
| 1 | W01 | AESTHETIC_GATE | 3个候选均满足自动研究门槛，最终选择涉及用户对歌曲本身的审美偏好；按计划不由系统替代 | `PENDING` | 否；这是设计保留的审美 Gate，不属于自动化缺陷 |

类型只允许：
- `AESTHETIC_GATE`
- `FILE_INPUT`
- `EXTERNAL_TOOL`
- `LOGIN/CAPTCHA`
- `TECHNICAL_RESCUE`

## Final Questions

R2 结束时必须回答：
1. 网页端能否自动完成选歌研究？
2. 不靠 Codex，网页端能否自动裁剪用户上传 BGM？
3. 导演 / 首帧 / 提示词能否自动完成到只需审美 Gate？
4. Seedance 是否仍是最大人工断点？
5. 视频上传回来后，QA / 剪辑 / 字幕能否自动闭环？
6. 哪些能力应留在 Web，哪些应移交 Codex？
