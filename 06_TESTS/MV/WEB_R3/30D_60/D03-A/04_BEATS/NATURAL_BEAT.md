# D03-A｜Natural Beat v1

Status: `READY_FOR_S04 / AUDIO_TIMELINE_DERIVED`

Authority: `03_AUDIO_TIMELINE/line_timeline.csv` + locked 31.921625s BGM.  This document groups the exact lyric clock into semantic/emotional units only; it does **not** introduce visual design or a second timing source.

## Global emotional contour

`清醒地知道会痛 → 再次受伤 → 从专一跌入失控 → 承诺消散 → 痴迷加重 → 关系真相刺入 → 盛夏反转成寒冬 → 旧的自己被亲手送走`

- Hook zone: `0.841–4.983s` — 自嘲式清醒 + “脑袋空空”的标题记忆点。
- First escalation: `4.983–8.686s` — 情绪从麻木转为真实受伤，并开始逃离/赶路。
- Emotional rise: `8.686–15.631s` — 从“情有独钟”一路走到眼泪和承诺消失。
- Peak pressure: `15.631–23.436s` — 主体失控，而对方已经转向另一段关系。
- Metaphoric turn: `23.436–27.078s` — 外在仍是盛夏，内在已经寒冬，是全段最清晰的冷热反差。
- Final release / identity loss: `27.078–31.921625s` — “当初真的自己”被葬送，29.780s 后进入音乐尾部余韵。

## Natural Beats

| Beat | Time | Canonical lyric lines | Semantic job | Emotion / energy | Edit role |
|---|---:|---|---|---|---|
| NB01 | 0.841–4.983 | L01–L02 | 明知会痛却再次陷进去；标题句把这种反复浓缩成“脑袋空空” | 克制、自嘲、轻微失神；开场迅速建立人物状态 | HOOK |
| NB02 | 4.983–8.686 | L03–L04 | “忘了痛”的代价兑现：伤口重新被打开，随后只剩匆匆离开 | 痛感突然实体化，能量向前冲 | HIT / BRIDGE |
| NB03 | 8.686–12.348 | L05–L06 | 从最初的唯一选择，坠落到最后无法压住的情绪 | 由温热记忆转向失守 | RISE |
| NB04 | 12.348–15.631 | L07 | 承诺不再有实体，关系第一次出现真正的不可追回 | 拉长、抽空、失去抓手 | RELEASE-1 |
| NB05 | 15.631–19.753 | L08–L09 | 主体的依恋进一步升级成失控，结果不是靠近而是更沉重 | 全段主观情绪峰值之一 | PEAK-A |
| NB06 | 19.753–23.436 | L10–L11 | 关系真相落地：对方关闭与“我”的连接，却在另一边保持亲密 | 刺痛由内耗转为明确事实 | PEAK-B / REVEAL |
| NB07 | 23.436–27.078 | L12–L13 | 时间和季节没有变，人的内部温度却完全反转 | 能量短暂收住，形成最强对照句 | CONTRAST / HOLD |
| NB08 | 27.078–31.922 | L14 + music tail | 失去的不只是一段关系，而是曾经真实的自己；歌词结束后让后果继续存在 | 重、静、不可逆，最后进入余韵 | FINAL RELEASE |

## Beat boundaries locked to lyric clock

- NB01 start uses L01 `0.841s`; no visual/edit action may assume lyric begins at 0.000s.
- NB04 is intentionally a single long semantic unit because L07 itself carries the complete promise→disappearance turn.
- NB08 lyric content ends at `29.780s`; `29.780–31.921625s` is retained as music-tail breathing room rather than inventing another lyric beat.
- No Natural Beat boundary changes `line_timeline.csv` or `lyrics_exact.srt`.

## Director handoff

Director allocation should preserve the eight semantic jobs above but is free to use fewer or more production segments. `Natural Beat != first-frame count != dynamic-source count != final edit fragment count`.
