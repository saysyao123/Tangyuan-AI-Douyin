# Rules｜MV Human Gate Contract v1.1

> Status: `ACTIVE / WEB_R3_HARDENED`
> Role: 只定义“什么时候必须停下来让用户做主观/授权判断”。技术正确性应在到达人类 Gate 前由机器 QA 完成。
> Core: **Human reviews taste and final authority; machines review implementation correctness.**

---

## 1. Why this exists

WEB R2 证明两个极端都不好：
- 人工 Gate 太少：错误时间轴、碎剪、字幕实现问题会一路污染下游；
- 人工 Gate 太多：用户被迫反复审核技术细节，流程变成来回循环。

因此未来默认只保留 5 个固定 Human Gates，并允许少量异常条件 Gate。

---

## 2. Fixed Human Gates｜DEFAULT

### HG01｜Song Aesthetic Gate

位置：Stage 1 Song Discovery。

系统先完成：
- 候选筛选；
- 版本/热度/可执行性基本核验；
- 3–5 个有明确差异的候选；
- 为每个正式候选完成 `DIRECT DOUYIN EVIDENCE PACK`；
- 每首至少 2 个近期 direct Douyin works，来自至少 2 个独立账号；
- 报告 core benchmark coverage；
- 对每条 direct work 验证 URL 的 landing work 本身，而不是依赖旧作品页/作者列表中的“相关推荐/近期作品”文本。

用户只决定：
- 这首歌是否值得做；
- 哪个候选审美最对。

### HG01 delivery separation｜HARD

`SONG_CANDIDATE_SET` 是机器内部候选预检工件，不等于用户可决策的 HG01 交付。

禁止：
- 只给“歌名 + 排名 + 机器推荐”就要求用户 A/B/C/D；
- 把 `HG01_PREFLIGHT_PREPARED` 表述为 `HG01_READY`；
- 用搜索结果中的作者旧作品页面、作者列表页面或 profile-like listing 代替具体候选歌作品直链；
- 用外部音乐平台试听链接替代 Direct Douyin Evidence；
- 因为某首歌“更适合测试技术”而覆盖用户对歌曲本身第一耳审美的 Human Gate 权限。

只有同时满足以下条件，才允许向用户提交 HG01 决策：
- `status = HG01_EVIDENCE_DELIVERY_PASS`；
- `evidence_pack_path` 已持久化；
- `all_candidates_min_direct_works_2 = true`；
- `all_candidates_independent_accounts_2plus = true`；
- `all_direct_links_landing_work_verified = true`；
- `core_account_coverage_reported = true`；
- `no_external_audio_substitution = true`；
- `user_gate_delivery_mode = DIRECT_WORKS_FIRST`。

PASS：`REFERENCE_BGM_LOCKED`。

不要让用户做人肉资料检索或版本技术校验。

---

### HG02｜BGM Excerpt Listening Gate

位置：Stage 2，实际音频截取后。

系统先完成：
- 精确版本锁定；
- 候选起止点；
- 检查前一句污染；
- 检查结尾是否截断；
- 需要时多留一句 release；
- fade 候选；
- 输出可直接试听文件。

用户只判断：
- 开头是否舒服；
- 是否进入了真正想要的段落；
- 结尾是否完整、淡出是否舒服。

PASS：`BGM_LOCKED`。

WEB R2 经验：用户最终要求“前面多 0.5s、后面多一句”，说明这一步必须在 Audio Timeline Package 之前完成；否则后续强制对齐会因为 BGM 再变而白做。

---

### HG03｜Visual Direction / First-frame Set Gate

位置：Stage 5；Director Plan 已内部锁定、完整首帧组已生成后。

系统先完成：
- Stage 3 Natural Beat；
- Stage 4 Director Concept / production allocation；
- 首帧整组生成与 set-level QA；
- 连续性、歌词命中、构图差异、动态可执行性检查。

用户主要判断：
- 世界/人物/色彩是否对；
- 歌词是否“一眼命中”；
- 整组是否够美、够统一、又不重复。

PASS：`FIRST_FRAME_SET_LOCKED`。

默认不增加一个单独的“文字版 Director Plan 人工 Gate”，避免在抽象方案和首帧之间重复审批。只有高成本/高风险项目才提前要求 Director Gate。

---

### HG04｜Picture Edit Rhythm Gate

位置：Stage 8B，`Picture + locked BGM` 预览完成、技术 QA PASS 后。

系统先完成：
- W07 Dynamic QA；
- W07.5 Atom/Arc Normalization（多镜素材时）；
- Editor Audio Gate；
- Edit Map；
- Fragmentation QA；
- WEB watermark-safe transform；
- 音频 global-lag QA。

用户只判断：
- 节奏是否舒服；
- 是否切得太碎；
- 情绪峰值/释放是否成立；
- 有没有明显导演层面的错误镜头。

PASS：`EDIT_PREVIEW_QA_PASS`。

禁止把以下基础错误交给用户发现：
- BGM错版/错位；
- 源视频音轨泄漏；
- 水印角落漏出；
- SAR/画幅错误；
- 明显拓扑风险窗未剪掉。

---

### HG05｜Final Acceptance Gate

位置：Stage 10 技术 QA PASS、Final 已渲染后。

系统先完成：
- Subtitle Runtime Gate；
- Final technical QA；
- 开头/峰值/结尾/full-watch；
- 交付包完整性；
- final identity/hash。

用户只判断：
- 成片整体是否可以接受/发布；
- 是否存在需要重新打开上游的明确创意问题。

PASS 后：`COMPLETE_LOCKED`。

---

## 3. Conditional Human Gates｜ONLY WHEN TRIGGERED

### CHG-A｜Audio Alignment Exception

仅当：
- 强证据来源冲突超阈值；
- repeated occurrence 无法自动判定；
- forced alignment 有关键 unmatched/warning；
- 机器听感证据不足。

正常 Audio Timeline Package PASS 不要求用户逐行做人肉对齐。

### CHG-B｜Dynamic Regeneration Decision

仅当 W07/W07.5 证明：
- clean duration 不足；
- 核心歌词事件没生成出来；
- 角色/拓扑错误无法靠 trim 修复；
- 没有可替代 Atom/Arc。

`TRIM_REQUIRED` 不是人工重生成 Gate；先剪可用素材。

### CHG-C｜New Subtitle Style

默认字幕基线已锁，不再每首歌做 A/B/C。

只有用户明确说“这首歌要换字幕风格”，才打开新 Style Exploration Gate。
实现 bug（padding/偏心/溢出/时间实现误差）不属于审美 Gate，由机器修复并重新 QA。

---

## 4. Gate handoff contract｜HARD

每次提交 Human Gate，必须同时提供：
1. 当前要用户判断的唯一问题；
2. 已完成的机器 QA；
3. 可直接查看/试听的 artifact；
4. 明确 PASS 标准；
5. 用户 PASS 后要锁定的 state/artifact。

HG01 额外要求：**先给 direct Douyin works，再给机器判断；机器推荐只能是辅助信息。**
HG02 额外要求：**必须给实际可试听的剪辑音频文件，不能只给时间码或文字方案。**

禁止：
- 一次让用户同时评 5 个技术问题；
- 在机器 QA 未完成时先丢给用户“帮我看看”；
- 用户已 PASS 后又因为下游实现 bug 重新打开同一个审美 Gate。

---

## 5. Nearest-cause rollback｜HARD

出现问题时只回滚到最近的根因层，不级联重做已锁上游。

| 问题 | 默认回滚位置 |
|---|---|
| 选歌不对 | Stage 1 |
| 音频段开头/结尾不舒服 | Stage 2；随后使 2A 失效 |
| BGM hash/version/clip 改变 | Stage 2A rebuild；所有 timing-dependent 下游重新验证 |
| 歌词时间轴证据错误 | Stage 2A |
| 视觉世界/首帧不对 | Stage 4/5 |
| 单条动态素材局部崩 | Stage 6/7，仅该 source |
| 多镜素材内部隐藏碎镜 | Stage 7.5，不回首帧/导演 |
| Picture Edit 太碎 | Stage 8B，优先重组 Atom/Arc；clean source 不足才回 Stage 6/7 |
| 字幕框偏心/padding 错 | Stage 9 implementation；不改 timing、不改 Picture Edit |
| 字幕跟人声时间真值错 | Stage 2A；不是 Stage 9 |
| Final codec/SAR/metadata 问题 | Stage 10；不重剪 |

原则：`Patch, Don't Cascade`。

---

## 6. Expected user interaction count

正常一首 MV 的默认人工确认次数目标：**5 次**。

1. 选歌；
2. BGM 片段；
3. 首帧整组/视觉方向；
4. Picture Edit；
5. Final。

其余阶段应自动执行或只在异常时打断。

如果正常项目频繁超过 5 次人工确认，应复盘哪个技术 Gate 没有前置或哪个规则仍依赖用户做人肉 QA。
