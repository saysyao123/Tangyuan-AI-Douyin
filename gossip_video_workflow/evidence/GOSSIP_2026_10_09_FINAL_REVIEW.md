# 2026-10-09 Chinese Gossip Video | Final encoded MP4 recovery

## Final episode
- Original editorial edition: 2026-10-09, Asia/Shanghai, three subjects; not a same-day breaking news headline.
- Encoded file: `2026-10-09_中文吃瓜集锦_1080P.mp4` (saved as a ChatGPT conversation download, not in this public Git repo).
- SHA256: `53c1ad447bbf707c245b134b8caf126645cc53140a138e7ab38c490e969a786d`.
- True encoded format: 1080x1920 / H.264 / AAC / 30fps / 220.833333 seconds.

## Verified execution history
- Full render [37906181163](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/37906181163): rendered real MP4, cover, 45 shot keyframes; job concluded failure because source-frame JPEG hash flags were treated as fatal *before* independent STT / contact sheets.
- Independent encoded-AAC STT [38019320039](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38019320039): succeeded and produced `independent_stt.json` and `independent_qa.json` artifacts.
- All 45 rows independently transcribed. 6 phonetic similarity review flags (00,03,05,06,07,08) match Chinese numeric pronunciation versus Arabic numeric notation (e.g. 二零二五/2025, 三十九块九/39.9); no conflicting numbers found by manual text comparison. STT may misrecognize proper names/near homophones, and is not human listening.
- Final AAC vs master 45 spoken row correlations: minimum 0.999879, median 0.999977. EBU loudness about -16.0 LUFS, true peak -3.2 dBFS.
- Re-extracted 2208 10fps sampled frames from **final encoded MP4**; 5 x full-film contact sheets at 2fps and 44 x 10fps transition strips visually inspected; 45 keyframe layouts observed. No missing images, blank frames, font overflow, or black video sections spotted.
- All 39 video rows showed motion in the decoded final media-well samples (lowest mean frame difference about 2.93/255 per 0.5s). This does not prove no perceptually similar footage; there is visibly repeated subject/framing because one stock shot was sectioned into many adjacent rows.
- Source film temporal ranges in JSON are nonoverlapping, but source sample JPEG hashes may repeat at adjacent boundaries; legacy test recorded that ambiguity. Corrected QA now records `sourceSampleReview=review_required` and continues encoded evidence generation/STT; manual visual review remains mandatory.
- Human qualitative listening: **not independently completed**. Listener should confirm the naturalness and specific pronunciation, including English acronym `IT` in the newspaper name.
- All three film assets are contextual Pexels licensed footage, **not** the event participants, damaged ceramic, or 2026 Hengdian reporters' field video. On-screen metadata clarifies this. Original poster and source links remain in the episode JSON.
- No external post, publication, account action, or upload of raw video to public GitHub was performed.

## Scope note
This round fulfills the user's narrowed **1080P Chinese MP4 delivery**. No 720P file was included in the delivery. Reuse the repository JSON, workflows, and QA evidence for later edits; the encoded MP4 lives in user-deliverable conversation storage, not permanently in the GitHub source tree.
