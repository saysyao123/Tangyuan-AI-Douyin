# WEB R3｜Picture Edit v1 EDL

Status: `PICTURE EDIT V1 READY / HG04 PENDING`
Song: `如果风会替我说话`
Locked BGM: `如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`
Target: first 24.32s picture-rhythm candidate, no subtitles / no final packaging.

## 1. Edit policy

- `SOURCE != FINAL SHOT`: 5s generated clips are reservoirs, not mandatory 5s blocks.
- use the latest user/Doubao-rewritten S02/S06 outputs as the primary replacements;
- use previously accepted best sources for the remaining segments;
- source audio is removed; locked BGM is the only production audio;
- trim around physically loud / semantically weak generated regions instead of forcing them to read;
- preserve long continuous camera arcs where they are emotionally strong, especially S08;
- exploit S04 foreground occlusion as a motivated editorial cut point rather than asking the model to recover the same scene after heavy cover.

## 2. Source mapping used in Picture Edit v1

- S01 = `3S1.mp4`
- S02 = latest Doubao rewrite output `AI动画人物雨夜窗边视频生成(1).mp4` (rain-window)
- S03 = `3S3.mp4`
- S04 = `3S4(1).mp4`
- S05 = `3S5(1).mp4`
- S06 = latest Doubao rewrite output `AI动画人物雨夜窗边视频生成 (2)(1).mp4` (ice foreground)
- S07 = `3S7.mp4`
- S08 = `3S8.mp4`

## 3. Timeline / trim decisions

| Final timeline | Lyric | Source trim | Final duration | Reason |
|---|---|---|---:|---|
| 0.00–3.00 | 如果风会替我说话 | S01 `0.15–3.15` | 3.00s | keep immediate eye/wind hook; avoid wasting tail |
| 3.00–6.00 | 如果雨会替我回答 | latest S02 `2.00–5.00` | 3.00s | skip the earliest / loudest rain-tube growth; retain calmer rain-window/reflection state |
| 6.00–8.00 | 如果我还会想起他 | S03 `0.60–2.60` | 2.00s | strongest absence / warm-empty-space reveal window |
| 8.00–12.00 | 如果还能一起回家 | S04 `0.20–4.20` | 4.00s | preserve corridor reveal; end near strong foreground occlusion so the cut becomes motivated |
| 12.00–15.00 | 如果梦能模糊真假 | S05 `0.30–3.30` | 3.00s | stable dry-mirror geometry; clean ambiguity without unnecessary fluid event |
| 15.00–18.00 | 如果痛能随之融化 | latest S06 `2.00–5.00` | 3.00s | de-emphasize questionable droplet phase; prioritize wet-ice -> rack-focus -> eyes emotional read |
| 18.00–20.00 | 如果我们还是傻瓜 | S07 `0.80–2.80` | 2.00s | strongest two-object metaphor / focus behavior |
| 20.00–24.32 | 如果爱不只是童话 | S08 `0.40–4.72` | 4.32s | preserve world-opening crane/retreat and allow BGM tail to breathe |

## 4. HG04 review priorities

Human review should ignore subtitles / final packaging and judge only:
1. picture rhythm against the locked BGM;
2. lyric-to-visual fit;
3. whether S02/S06 remaining liquid artifacts are sufficiently de-emphasized at real playback speed;
4. whether S04 -> S05 cut reads as an intentional foreground-occlusion transition;
5. whether shot-scale rhythm breathes naturally across close / medium / wide / object / release shots;
6. whether S08 should remain as long and continuous as possible;
7. whether any shot should move its in/out point by a few frames without regenerating source.

## 5. Current decision boundary

Do not regenerate before HG04 unless a source remains visibly unusable after trim.

If HG04 fails for rhythm:
- patch edit points first;
- do not modify generation prompts by default.

If HG04 passes:
- lock Picture Edit;
- proceed to subtitle integration / final polish / HG05 path.

`PICTURE_EDIT_V1_READY = YES`
`HG04_PASS = NO / PENDING HUMAN REVIEW`
