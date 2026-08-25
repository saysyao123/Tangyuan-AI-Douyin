# 汤圆音乐映像｜30天60条｜D01-B HG01 Candidate Evidence Pack v1

Status: `HG01_READY / USER_AESTHETIC_SELECTION_REQUIRED`
Slot: `D01-B`
Lane: `S / Stable-Fast`
Previous-song exclusion: `如果风会替我说话 = EXCLUDED`

## Scope

本文件只负责 HG01 Song Aesthetic Gate：让用户从已经完成基础证据、版本一致性与 Lane-S 可执行性检查的候选中选择一个 `SONG_FAMILY`。

当前 Gate 不锁 BGM 截取、不做歌词时间轴、不做导演方案、不生成首帧，也不继承上一首《如果风会替我说话》的具体人物、场景、道具、色调或构图。

## Machine QA completed

- Tracker first available slot verified: `D01-B`.
- Tracker lane verified: `S`.
- Lane-S production target retained: short stable production, low physical-interaction risk, proven camera grammar.
- Previous accepted song `如果风会替我说话` removed from candidate pool.
- Current Music Radar was checked; fresh Radar-only songs without a complete >=2-account direct-work evidence pack are not promoted into HG01 merely for freshness.
- All four candidates below have >=2 direct Douyin works from >=2 independent core benchmark accounts.
- Work durations are persisted in `database/works.csv`.
- Exact production `AUDIO_VERSION` is intentionally NOT locked here; that begins only after HG01 PASS.

---

## Candidate A｜Summer Love 爱在盛夏

- Data-center grade: `CONFIRMED_REPEAT`
- Core benchmark coverage: `CONFIRMED / 2 independent core accounts`
- Observed audio consistency: `HIGH` — both works point to the same 三棱镜 original-sound family.
- Lane-S fit: `HIGH`
- Why it is here: bright emotional direction, short-form excerpt already proven in two core accounts, low physical-risk production potential, and strong visual separation from the previous song.
- Main risk: late-August seasonal shelf life; common summer/sea imagery can become generic, so if selected the later visual direction must deliberately avoid benchmark-copying.

Direct Douyin works:
1. Aura｜2026-08-13 17:00:00｜16.734s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7673385877871136042
2. XIANGJISHI｜2026-08-12 17:03:01｜17.467s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7673068083896814202

## Candidate B｜我救自己于人间水火

- Data-center grade: `CONFIRMED_REPEAT`
- Core benchmark coverage: `CONFIRMED / 2 independent core accounts`
- Observed audio consistency: `LOW/MEDIUM` — same SONG_FAMILY, but the observed posts expose account-specific original sounds; B0 must re-lock exact production audio if selected.
- Lane-S fit: `HIGH`
- Why it is here: self-rescue/healing semantics fit the account promise and can be expressed with stable, low-interaction visual beats rather than complex choreography.
- Main risk: do not let the visual treatment become heavy, tragic or abstract to the point that the lyric hook is weakened.

Direct Douyin works:
1. Aura｜2026-08-13 18:25:19｜15.967s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7673460363010018611
2. XIANGJISHI｜2026-08-13 17:15:23｜15.967s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7673442358406957285

## Candidate C｜若爱有尽头

- Data-center grade: `CONFIRMED_REPEAT`
- Core benchmark coverage: `CONFIRMED / 2 independent core accounts`
- Observed audio consistency: `HIGH` — both works expose the same named track family and artist pair.
- Lane-S fit: `MEDIUM/HIGH`
- Why it is here: hook is direct and emotionally legible; existing core-account usage proves short-form music-video compatibility.
- Main risk: generic melancholy-MV grammar. If selected, later creative direction must not fall back to the previous song's rain/night/veil/longing visual residue.

Direct Douyin works:
1. XIANGJISHI｜2026-08-14 17:43:48｜21.400s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7673820758652768945
2. 乐 ♩青春｜2026-08-11 23:07:14｜20.968s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7672790854586937178

## Candidate D｜杀破狼

- Data-center grade: `CONFIRMED_REPEAT`
- D02 assessment: `CLASSIC REVIVAL / HIGH RECOGNITION`
- Core benchmark coverage: `CONFIRMED / 2 independent core accounts`
- Observed audio consistency: `MEDIUM/HIGH` — both point to 萧泽x.z original-sound family, with R&B / cover labeling differences.
- Lane-S fit: `MEDIUM`
- Why it is here: gives HG01 a genuinely different recognition/energy option rather than four similar soft-healing songs.
- Main risk: can easily drift into high-cost ancient/fantasy/epic spectacle; if selected under Lane S, production must remain restrained and stable instead of becoming a Lane-R experiment.

Direct Douyin works:
1. XIANGJISHI｜2026-08-14 20:03:41｜20.934s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7673856812899138149
2. 乐 ♩青春｜2026-08-14 00:02:20｜13.073s｜Tier A Core Benchmark
   - https://www.douyin.com/video/7673547221526478026

---

## Fresh Radar screening note

`雨后轻风有香` and `甲乙丙丁` remain valid current Radar observations, but this D01-B HG01 pack does not promote them yet because the current repository snapshot does not preserve a complete >=2-independent-account direct-work evidence pack for each candidate under the active HG01 Evidence Delivery Contract.

This is an evidence-quality decision, not a claim that those songs are not trending.

## User decision required｜HG01

Choose exactly one SONG_FAMILY from A/B/C/D based on:
1. first-ear appeal;
2. whether the observed short-form treatment feels worth making now;
3. whether our account has obvious room to improve the visual presentation;
4. whether it feels right for this independent D01-B / Lane-S MV.

Recommended Lane-S order from production-system perspective:
`A Summer Love 爱在盛夏` → `B 我救自己于人间水火` → `C 若爱有尽头` → `D 杀破狼`.

HG01 PASS condition:
`USER_EXPLICITLY_SELECTS_ONE_SONG_FAMILY = YES`

After PASS:
1. lock `SONG_FAMILY` into D01-B;
2. enter exact `AUDIO_VERSION / Douyin asset` discovery;
3. prepare HG02 BGM excerpt listening;
4. only after HG02 PASS build the trusted Audio Timeline;
5. no visual generation before the audio gates are complete.
