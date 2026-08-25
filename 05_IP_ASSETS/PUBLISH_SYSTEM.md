# PUBLISH_SYSTEM v3.1｜Music-MV Sprint

> Current season: `30D / ~60 MUSIC MV`
> Previous DAY-series `37→1000` publish package is historical and no longer the current front-facing default.
> Front-facing brand: **汤圆音乐映像**.
> Hardened after D01-A / D01-B: packaging components are now explicitly separated to prevent title/cover drift.

## 1. Default packaging identity

Current first baseline:
`MUSIC_FIRST`

Order:
1. exact song identity;
2. one restrained emotional reason to stay;
3. healing / atmosphere / cinematic visual category;
4. production technology stays backstage by default.

Hard front-facing rule for ordinary MV posts:
- do not lead with `AI生成`;
- do not use `AI视觉 / AIGC` as default tags;
- do not make the cover a creator-process experiment;
- do not make technical production identity compete with song/emotion identity.

Exception:
Only posts whose actual subject is behind-the-scenes creation / workflow / technical review may explicitly mention AI.

## 2. Packaging component contract｜HARD

Do not mix these three fields:

### A. Internal project title
Used only for repository / production management.
May contain slot, lane, test variant or descriptive suffix.
It is **not automatically public copy**.

### B. Douyin caption / post copy
This is the normal public text block for the current sprint.
For the first baseline block, use:

`歌曲名。`
`一句克制的具体情绪。`
`一句当前MV的视觉/情绪解释。`（可选但推荐）

Then hashtags.

Do **not** automatically invent a separate public `歌曲名｜情绪标题` if the platform post already uses the above caption structure.

The earlier generic `歌曲名｜一句具体情绪/视觉理由` format may still be used only when:
- a platform explicitly exposes a separate title field; or
- a future controlled packaging experiment defines it as the variable.

During the current first ~10 post MUSIC_FIRST baseline, Douyin should preserve the D01-A-style caption family rather than alternating between unrelated title systems.

### C. Cover text
Default one main line only:
`exact song name`

No emotion subtitle by default.
No AI / DAY / 30天60条 / hashtag / decorative English.

These three layers must be stored separately in every `PUBLISH_PACKAGE`.

## 3. Cover｜ACCOUNT-LEVEL FAMILY

Default:
- choose the strongest still frame from the actual accepted MV;
- one main line: exact song name;
- no secondary line unless a future controlled cover experiment explicitly enables it;
- no DAY number as primary hierarchy;
- no `37→1000` line;
- no `AI生成` / `AI视觉` label by default;
- no long explanatory paragraph;
- no decorative English by default.

### Consistency rule
Consecutive normal MV posts should look like one account family even when the scene/world changes.

Keep consistent:
- song-name-only hierarchy;
- restrained typography;
- cinematic still as the dominant visual;
- clean placement away from eyes/face and bottom lyric-safe area;
- no promotional poster clutter.

Allow song-specific variation in:
- frame choice;
- text position (upper / side / negative-space area);
- scale within a restrained range;
- portrait vs landscape emphasis.

Do not force identical coordinates if the composition changes, but do not redesign the entire graphic language each post.

Cover-frame preference is song-specific:
- human-gaze Hook when thumbnail stop power matters;
- world-opening / landscape frame when profile visual variety needs breathing room.

## 4. Douyin caption baseline

Recommended 2–3 short lines:
1. exact song identity;
2. one emotional statement;
3. one sentence describing this MV's visual interpretation.

Example family:
`如果风会替我说话。`
`有些没说出口的话，就让风替我说吧。`
`风替她开口，雨替她回答，天亮以后，就继续往前走。`

Do not beg for follows.
Do not claim virality / guaranteed healing.
Do not explain AI production unless the post itself is a creation-process post.

Avoid:
- generic production-method language first;
- keyword stuffing;
- repeated identical emotion templates across 60 videos;
- switching between caption family and a new decorative “title” system without recording a controlled experiment.

## 5. Hashtags

Default structure:
1. exact song/search identity;
2. music-category tag;
3. visual/emotion category;
4. one precise song- or mood-relevant tag.

Typical baseline:
`#歌曲名 #音乐推荐 #治愈系 #氛围感 #音乐MV`

Default forbidden front-facing production tags during this sprint:
- `#AI视觉`
- `#AI生成`
- `#AIGC`

These may only be used on explicit behind-the-scenes / production-process content.

Do not waste most tag slots on self-created brand tags during the calibration month.

## 6. Pinned comment / comment entry

Default low-friction prompt tied to the actual lyric or emotion.

Examples:
- `这段里你最喜欢哪一句？`
- `如果风能替你说一句话，你最想说什么？`

Do not use generic `求关注 / 求点赞` as default CTA.
Do not turn the pinned comment into a technical-production explanation.

## 7. Controlled packaging tests

Do not randomly change title/cover identity every post.

Baseline block:
- first 10 real MV posts: primarily `MUSIC_FIRST`;
- same account cover family: cinematic still + song name only;
- same Douyin caption family: song identity -> restrained emotion -> visual interpretation;
- later selected posts may use `EMOTION_FIRST` on different videos;
- never duplicate-post the same finished MV solely to A/B packaging.

If a post intentionally changes cover hierarchy / caption structure / title format, record the changed variable in Tracker/Publish Package.

Packaging conclusions are `PERFORMANCE` hypotheses and require repeated real-data validation.

## 8. Publishing cadence

Current target average: ~2 posts/day.

Use two separated posting windows initially; exact timestamps must be recorded.
Do not assume a universal best time before the account itself has enough evidence.

After the first 7–10 days, compare window performance and adjust as an experiment rather than a permanent rule.

Do not post the two daily videos back-to-back.

## 9. Performance review

Record at:
- 1h;
- 3h;
- 24h.

When visible:
- views;
- likes;
- comments;
- favorites;
- shares;
- profile visits;
- new follows;
- followers before/after;
- completion rate;
- average watch time.

Primary growth normalization:
`follows_per_1000_views = new_follows / views * 1000`.

Also track:
- like rate;
- favorite rate;
- comment rate;
- share rate;
- completion / duration relationship.

Do not promote a performance rule from one post.

## 10. Production lanes

Reference:
`05_IP_ASSETS/MV_30D_60_OPERATING_SYSTEM.md`

- P: Primary / Trend MV
- S: Stable / Fast MV
- R: Director / Camera R&D MV

Packaging should record the lane so production complexity can be separated from performance.

## 11. Publish package required fields｜HARD

Every ready-to-publish MV package should separately store:
- `internal_project_title`;
- `douyin_caption`;
- `hashtags`;
- `pinned_comment`;
- `cover_frame_source`;
- `cover_text`;
- `cover_family = SONG_NAME_ONLY_CINEMATIC_STILL` unless testing another variable;
- `packaging = MUSIC_FIRST / EMOTION_FIRST / named experiment`;
- audio attachment/sync note where relevant.

Do not leave the package with a single ambiguous `title` field that can mean several different public surfaces.

## 12. Post-Publish Sync｜HARD

When the user confirms a post is actually live, production state must be synchronized immediately.

Update:
1. slot `CURRENT_STATE` -> `PUBLISHED / DATA_COLLECTION_ACTIVE`;
2. `MV_30D_60_TRACKER.csv` status -> `PUBLISHED`;
3. exact actual publish timestamp if known;
4. if timestamp is unknown, store `timestamp_pending_backfill` rather than guessing;
5. first observed metric may be written as an observation note but must not be mislabeled as the 1h/3h/24h checkpoint unless the elapsed time is known.

Published performance does not automatically reopen production.
Single-post low views are data, not a production failure verdict.
