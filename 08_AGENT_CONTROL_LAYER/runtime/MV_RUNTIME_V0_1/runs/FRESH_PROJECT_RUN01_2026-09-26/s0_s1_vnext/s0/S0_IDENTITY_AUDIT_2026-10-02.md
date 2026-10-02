# S0 Song Family identity audit — 2026-10-02

## Purpose

Separate the song title, performer and recommending account before any S0 lock. This audit records discovery leads only; it does not claim a match without exact-source proof.

| Stored label | Recommending account | Current discovery | Decision |
|---|---|---|---|
| 向山河林响 | 火乐烁 | A catalog result exists for [《向山河》—林响](https://open.spotify.com/intl-vi/track/4sM2oL0S9ilxDRNf6qqncP). This suggests the stored label may concatenate title and performer, but it is not yet bound to the original Douyin item. | UNRESOLVED |
| 听见月亮的歌 | XIANGJISHI | Same-title catalog results exist, including [《听见月亮的歌》—生特吾姬](https://www.youtube.com/watch?v=WYUz6YFZ6zM). The recommending account is not proof of performer identity, and a same-title result is not proof of the same Song Family. | UNRESOLVED |
| 遇见爱的人 | XIANGJISHI | No stable exact catalog identity was recovered from the stored phrase and account. Search results were dominated by unrelated songs or lyric phrases. | UNRESOLVED |

The three original Douyin item URLs remain the primary identity leads, but current automated access produced an HTML shell or an inaccessible page rather than auditable media/metadata. Do not use third-party same-title results as silent replacements.

## Required resolution record

For each candidate retained, record:

- normalized song title;
- performer/creator;
- recommending or curator account separately;
- original item ID and URL;
- current playable reference;
- evidence that the playable reference is the same Song Family;
- date checked and reviewer.

Until at least one record is resolved, the correct S0 route is `SONG_IDENTITY_REFRESH_REQUIRED`.

