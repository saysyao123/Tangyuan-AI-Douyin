# Rules｜MV Audio Timeline Gate v1.0

> Status: `ACTIVE / HARD GATE`
> Role: MV 音频时间轴唯一执行规则。解决 R1 成功但资产不可复现、WEB R2 V1/V2 假锁定的问题。
> Core: **BGM 锁定后，必须先交付并锁定 `AUDIO_TIMELINE_PACKAGE`；没有这个包，不允许进入任何依赖歌词时长/音乐卡点的下游步骤。**

---

## 1. Gate position｜HARD

新 MV Round 的顺序固定为：

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ **`AUDIO_TIMELINE_PACKAGE_LOCKED`**
→ Music/Lyric/Beat analysis
→ Director
→ First Frames
→ Dynamic
→ Dynamic QA
→ Edit
→ Subtitle
→ Final QA

说明：
- 这是 BGM 之后第一个 correctness-critical 硬节点；
- 它不是“字幕步骤”，而是整个 MV 后半段的时间真源；
- Director 可以做纯概念草案，但任何依赖“某句实际有几秒 / 哪个词在哪一刻 / 哪个峰值在哪一刻”的正式生产分配，都必须使用已锁 Package；
- 当前 WEB R2 已经完成的视觉素材不因新增此 Gate 自动作废，但 **V3 编辑必须等待此 Gate PASS**。

---

## 2. R1 validated path and its reproducibility gap

R1 最终字幕成功路径：

`锁定实际 MP3`
→ `同版本 LRC`
→ `整曲 LRC 时间 - 实际裁剪起点 01:23.800`
→ `片段内歌词时间轴`
→ `用户听感确认`
→ `lyrics_exact_v3_1.srt`

R1 成功证明了：
- 同版本 timed lyrics + 精确 clip offset 可以可靠工作；
- 视觉段落不能反推歌词时间。

但 R1 没有完整保存：
- 原始 LRC 文件；
- LRC 来源平台 / song id / stable source reference；
- transformation 记录；
- 最终 SRT 实体文件的可发现 canonical path。

因此 R1 是 `documented success`，但 timing layer 不是完整的 `reproducible success`。

未来 Golden close 必须保存 Package，而不能只在文档中写一个文件名。

---

## 3. What “accurate timeline” means

必须区分三只时钟：

### A. Lyric clock
用于：
- 每句歌词 start / end；
- repeated line occurrence；
- 字幕显示；
- 语义镜头覆盖。

### B. Music-event clock
用于：
- downbeat / strong onset；
- pickup / rest / breath；
- phrase release；
- energy peak；
- outro / tail。

### C. Visual-action clock
用于：
- 生成素材内部动作起点 / 峰值 / 落点；
- 镜头自身可用 in/out。

`AUDIO_TIMELINE_PACKAGE` 锁 A+B。
最终 Edit Map 让 A+B 与 C 协商。
字幕只服从 A；画面切点不能反向修改 A。

---

## 4. Strong timing evidence routes

至少必须有一条 Strong Route，并完成 provenance + ground-truth QA。

### Route A｜Reliable same-version LRC / enhanced LRC｜PREFERRED FAST PATH

适用：平台能提供与当前母版**同一录音版本**的 timed lyrics。

流程：
1. 核对 title / artist / release / duration / version；
2. 保存原始 LRC / source reference / platform song id（如果可得）；
3. 保留原始整曲 timestamps；
4. 根据实际音频变换到 clip timeline：

`clip_time = source_song_time - source_clip_start + render_lead_in`

默认 `render_lead_in = 0`。
若 BGM 被 time-stretch / speed-change，简单减法无效，Package 必须重建。
5. 对首句 / 中间句 / 最后句 / repeated line occurrence 做实际音频交叉检查；
6. 与 waveform/onset/breath 只做 supporting cross-check，不得用 supporting evidence 覆盖强证据冲突。

### Route B｜Trusted lyrics + forced alignment｜PREFERRED INDEPENDENT PATH

适用：歌词文本已确认，但同版本 LRC 不可得或不可信。

原则：
- **已知歌词是什么，只求“什么时候唱到”**；
- 中文优先使用 character/phoneme CTC forced alignment，不让普通 ASR 自由改写歌词；
- 保存 raw alignment / model / version / warnings / score。

当前可参考实现（实现可替换，规则不绑定具体项目）：
- Chinese trusted-lyrics CTC aligner，例如 `xingyu-lyrics-aligner`；
- 它可以对本地音频 + 已知中文歌词直接做 CTC forced alignment，并输出 `alignment.json / lyrics.lrc / report.json`。

如果 full mix 导致 alignment warning：
- 可先做 vocals separation；
- vocal stem 必须与 master 保持 1:1 时间长度/起点；
- separation 后需验证无全局时间偏移；
- 最终 timestamps 仍映射回锁定 master。

### Route C｜Official same-version timed lyric/video

适用：官方同版本 lyric video / timestamped source 可直接验证。

必须保存 stable source + original timestamps + transformation。

---

## 5. Independent cross-check｜RECOMMENDED

Strong Route 解决“真值来源”，第二路径解决“静默失败”。

优先组合：
- Route A LRC + Route B forced alignment；或
- Route B primary + independent ASR-anchor aligner。

当前可参考的 secondary tool：
- CJK-first `lyric-align`：已知歌词 + ASR word timing 做 character-level fuzzy anchor；匹配失败时可以显式标记 `unmatched`，而不是静默编一个 timestamp。

### Automatic green condition｜initial threshold

若两条独立来源都存在：
- lyric line order 完全一致；
- repeated occurrences 映射一致；
- line-start median absolute delta ≤ `0.25s`；
- 单句 start delta 通常 ≤ `0.50s`；
- 所有 > `0.50s` 的冲突必须逐句复核并解释。

这不是审美标准，是当前用于防止“看似exact、实际漂移”的工程阈值；未来可用更多样本校准。

---

## 6. Public LRC is not automatically trusted｜HARD

“搜到一份带时间戳歌词” ≠ `SAME_VERSION_LRC`。

必须先验证它与锁定 audio 的版本和实际演唱位置一致。

典型 FAIL：
- title/artist 相同但录音版本不同；
- acoustic/live/remix/short-video version；
- LRC 只有人工整秒粗标；
- 间奏长度不同导致后半段整体漂移；
- repeated chorus 被映射到错误 occurrence；
- timestamp 与 locked audio 明显冲突。

任何此类来源只能标记：
`CANDIDATE_TIMED_LYRIC / REJECTED_OR_NEEDS_VERIFICATION`

不能直接进入 Package。

---

## 7. AUDIO_TIMELINE_PACKAGE｜MANDATORY DELIVERABLE

每首 MV 必须产生一个 canonical package directory：

`<ROUND>/AUDIO_TIMELINE_PACKAGE/`

最低必需资产：

1. `audio_identity.json`
   - title / artist / exact version；
   - locked BGM path/reference；
   - source clip start/end；
   - rendered duration；
   - SHA-256；
   - speed/time-stretch state。

2. `trusted_lyrics.txt`
   - 最终准确歌词；
   - one lyric line per line；
   - repeated lines 保留真实 occurrence。

3. `alignment_raw.*`
   - 原始 LRC / alignment JSON / official timestamp evidence；
   - 不得只保留加工后的 SRT。

4. `alignment_provenance.json`
   - evidence class；
   - source/platform/tool/model/version；
   - original timestamps；
   - clip transformation formula；
   - raw evidence SHA/reference；
   - warnings / unmatched；
   - repeated-line mapping。

5. `line_timeline.csv`
   - line_id；
   - lyric；
   - start；
   - end；
   - source/evidence；
   - confidence；
   - QA status。

6. `lyrics_exact.srt`
   - 最终字幕时间资产；
   - 只从 locked line timeline 生成。

7. `anchor_words.csv`
   - 仅记录真正影响导演/卡点的词；
   - 例如“抬头 / 布谷 / 鸟儿 / 飞过树梢 / 白云 / 漂浮”；
   - 非卡拉OK项目不要求所有字都做 word timing。

8. `music_events.csv`
   - downbeat / strong onset / pickup / breath / phrase release / peak / tail；
   - 每个 event 必须标注 evidence 与用途。

9. `alignment_qa_report.md`
   - 首句 / 中间 / 最后 / repeated occurrence；
   - 每句 start/end audit；
   - 两源冲突记录；
   - unmatched / warning；
   - Ground-truth QA 总结。

10. `package_manifest.json`
   - package version；
   - 所有文件 SHA；
   - `AUDIO_TIMELINE_PACKAGE_LOCKED = YES/NO`；
   - locked timestamp。

---

## 8. Hard PASS states

只有以下全部成立，Package 才 PASS：

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = YES`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = YES`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = YES`
- `LYRIC_TIMELINE_LOCKED = YES`
- `MUSIC_EVENT_MAP_VERIFIED = YES`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`

任何一项为 NO：
`STATE = AUDIO_TIMELINE_PACKAGE_BLOCKED`

**禁止进入正式 Director timing allocation / Picture Edit / Subtitle render。**

---

## 9. Ground-truth QA vs implementation QA

### Ground-truth QA
验证：
`timing asset ↔ singer / locked audio`

这是 Package Gate 的责任。

### Subtitle implementation QA
验证：
`rendered subtitle ↔ already-locked timing asset`

这是后期字幕渲染 Gate 的责任。

二者不可互相替代。

---

## 10. Invalidation rules｜HARD

以下任一变化会自动使 Package 失效：
- locked BGM SHA 改变；
- source clip start/end 改变；
- fade 前增加/删除 lead-in silence；
- BGM speed / time-stretch 改变；
- 使用另一个录音版本；
- trusted lyric text/order 改变；
- repeated occurrence 数量改变。

失效后：
`AUDIO_TIMELINE_PACKAGE_LOCKED = NO`

所有依赖其时间的下游 Edit Map / Subtitle 必须重新生成或重新验证。

---

## 11. Anti-shortcut rules｜HARD

禁止：
- waveform valley 单独生成 exact timeline；
- BPM grid 单独生成 lyric start/end；
- 根据视频段落倒推字幕；
- 复制 `DIAGNOSTIC_ONLY` 候选并改名 `exact`；
- 只验证 SRT 被正确烧录，就声称 SRT 与人声对齐；
- 没有 raw evidence/provenance 仍设置 `LOCKED`；
- 因为自动化工具不可用而静默降低证据等级。

缺工具时必须明确：
`AUDIO_TIMELINE_PACKAGE_BLOCKED`

---

## 12. Editor entry contract｜HARD

进入剪辑前的第一条检查固定为：

`Does AUDIO_TIMELINE_PACKAGE exist and PASS against the exact current BGM SHA?`

- NO → Stop；
- YES → Load `line_timeline.csv + anchor_words.csv + music_events.csv + visual_source_map`，再创建 Edit Map。

剪辑程序/Agent 不得自己临时重新猜歌词时间。
