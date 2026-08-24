# WEB R3｜HG01 Evidence Delivery Contract v1

> Status: `ACTIVE / R3 CORRECTION`
> Purpose: 修正 R3-A3 首轮交付中“趋势证据成立，但没有把可直接查看的抖音作品作为用户决策材料”的问题。
> Core: **HG01 是选歌审美 Gate，必须让用户直接看到/听到支撑候选的抖音作品，而不是只给外部试听或文字结论。**

---

## 1. Evidence tiers

### Tier A｜CORE BENCHMARK DIRECT DOUYIN EVIDENCE
来自用户指定核心 Benchmark 账号的具体抖音作品：
- 必须有 account name；
- 具体 post/video；
- publish time；
- direct Douyin/Douyin精选 work URL；
- song family / identifiable audio version；
- 用户应能直接点击进入作品查看/试听。

Tier A 是“这首歌确实在我们核心观察账号中出现”的最高优先级证据。

### Tier B｜SUPPLEMENTAL CREATOR DIRECT DOUYIN EVIDENCE
来自补充音乐账号、歌手本人、官方卫视/节目、音乐解析账号等具体抖音作品。

必须同样提供 direct work URL。

Tier B 可以证明抖音近期传播，但不能冒充“用户核心 Benchmark 账号重复”。

### Tier C｜PLATFORM / SEARCH CORROBORATION
包括：
- 汽水音乐列表；
- 搜索索引；
- 榜单；
- 媒体/曲谱等外围信号。

Tier C 只能作为 corroboration，不单独进入 HG01 决策包。

---

## 2. Hard delivery rule for HG01

每首进入 HG01 的 SONG_FAMILY 必须提供一个 `DIRECT DOUYIN EVIDENCE PACK`，至少包含：

1. 2 个可直接打开的近期抖音作品链接；
2. 至少来自 2 个独立账号；
3. 每条标 account / date / duration / evidence tier；
4. 说明这些链接是：
   - 用户核心 Benchmark；还是
   - supplemental/official evidence；
5. 能识别时标注具体 AUDIO_VERSION；
6. 如果 direct video 无法检索，不得用外部平台试听链接替代并假装等价。

推荐质量：
- `>=1 Tier A + >=1 Tier B`；或
- 当 Tier A 因公开索引不可得时，`>=3 Tier B`，但候选必须标记 `EXTERNAL_RADAR_CANDIDATE / CORE_ACCOUNT_UNCONFIRMED`。

---

## 3. Core-account uncertainty rule

公开搜索无法索引用户指定账号近7天作品时：

`NOT INDEXED != NOT POSTED`

必须记录：
`CORE_ACCOUNT_INDEX_STATUS = UNKNOWN / INDEX_PENDING`

禁止：
- 把“搜不到”记成0；
- 声称该账号没有使用该歌曲；
- 把补充账号的证据描述成“来自用户提供账号”。

---

## 4. HG01 decision packet format

每首候选必须按以下结构交付：

### SONG_FAMILY
- Radar class：EARLY_RISE / CONFIRMED / REVIVAL / OVERHEATED
- 为什么入选：一句话
- Core benchmark evidence coverage：`CONFIRMED / PARTIAL / UNCONFIRMED`

### Direct Douyin works
1. `[账号｜发布时间｜时长｜Tier A/B]` direct work URL
2. `[账号｜发布时间｜时长｜Tier A/B]` direct work URL
3. optional

### What user should judge
- 这首歌第一耳是否值得做；
- 当前抖音实际使用的版本/段落是否好听；
- 同类作品目前视觉是什么状态；
- 我们是否有明显可提升空间。

只有这个 evidence pack 完成后，才允许 `HG01_READY = YES`。

---

## 5. Correction to previous R3-A3 delivery

首轮 A3 shortlist 的趋势判断使用了：
- 用户提供账号用于角色/Benchmark 分类；
- supplemental public creators；
- official/program creators；
- platform corroboration。

但由于用户核心账号（如火乐乐、泡泡与茶、乐丨青春等）的完整近7天作品未被公开搜索稳定索引，首轮 shortlist **不能表述为“这些歌已在用户核心账号中重复验证”**。

正确状态应是：
- SONG trend signal：部分已验证；
- core-account repeat：多数仍 `PARTIAL / UNCONFIRMED`；
- HG01 direct evidence delivery：需要重新包装。

因此首轮 `READY FOR HG01` 状态撤回，进入：
`A3_DIRECT_DOUYIN_EVIDENCE_REPACK`。

---

## 6. Why inability to provide a direct link does NOT mean no Douyin video exists

抖音主页/作品的公开 Web 索引并不完整；搜索引擎常只能抓到部分 Douyin精选页面或作者页中的近期作品列表。

因此：
- 有 direct link → 可以作为强作品证据；
- 没有 direct link → 只能说明当前检索路径没有拿到，不能推断作品不存在。

用户若提供具体账号主页/作品分享链接，可以升级该账号的 Tier A evidence coverage。

---

## 7. Gate

Before HG01:
- `DIRECT_DOUYIN_EVIDENCE_PACK_READY = YES`
- `CORE_ACCOUNT_COVERAGE_REPORTED = YES`
- `NO_EXTERNAL_AUDIO_LINK_SUBSTITUTION = YES`

Only then:
`HG01_READY = YES`
