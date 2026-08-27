# D02-B｜Release Package v1

Status: `READY`

## Internal identity
- `slot_id`: `D02-B`
- `lane`: `S`
- `internal_project_title`: `D02-B｜《有几次想你了》｜OSS_OPT_R1 Accepted Final`
- `final_render`: `D02-B_有几次想你了_最终候选_字幕版_v1.mp4`
- `final_render_sha256`: `7f77a41a68db47d4f7992cb77161c86414eeb0fd1cf8233322956b4025bf43d9`
- `duration`: `15.375s`
- `packaging`: `MUSIC_FIRST`

## Douyin caption

有几次想你了。
有些话忍住了，有些舍不得，也该慢慢放下了。
这次把想念拍成靠近、停住、转身，最后让风把世界打开。

## Hashtags

`#有几次想你了 #音乐推荐 #治愈系 #氛围感 #音乐MV`

## Pinned comment

`这段里，你更喜欢“忍住”的那一下，还是最后“放下”的那一下？`

## Cover
- `cover_family`: `SONG_NAME_ONLY_CINEMATIC_STILL`
- `cover_text`: `有几次想你了`
- `cover_frame_source`: accepted final render around `00:00:00.900`, L01 approach / male-lead hero frame.
- cover rule: one song-name line only; no AI / DAY / 30天60条 / English decoration / emotion subtitle.
- composition rule: keep the male lead and seaside light as dominant visual; place title in available negative space away from eyes and bottom lyric-safe area.

## Audio attachment / sync note
- HG02 locked source: Douyin music object `7670104695834282815`, accepted B variant with soft tail fade.
- The accepted final render already contains the locked production audio.
- If the platform music object is associated at publish time, do not create a second audible duplicate music layer; preserve the accepted final mix/timing.

## Final acceptance chain
- HG04 picture rhythm: PASS.
- Subtitle implementation QA: PASS.
- Final Technical QA: PASS.
- HG05 final human acceptance: PASS.

## Publish-state boundary
This package is publish-ready metadata only.
The MV has **not** been marked `PUBLISHED` and no publish timestamp is invented here.
Only after the user confirms the real post is live may Runtime execute the post-publish sync transaction and update Tracker / DATA_COLLECTION_ACTIVE state.
