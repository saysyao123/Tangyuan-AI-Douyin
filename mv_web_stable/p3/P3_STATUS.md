# P3 result · 4 GPT native hero stills verified (art unfinished)

Date 2026-10-08

## Verified local artifacts
- Four genuine, newly generated GPT-native hero PNGs: L01, L04, L07, L08; each 941×1672. Per-image SHA256 in four_anchor_manifest.json.
- A 10.366667s, 311-frame, 1080×1920, 30fps H.264 + original-song-fragments AAC **local aesthetic sampler** was actually rendered, full decode passed.
- The sampler source song is the already provided/approved 21.36s song slice, SHA256 42c8fd3ce982b54d6792c66eebff6edd1406a823e53cf2a9c93b03d772ccebfe. It was not uploaded into this PUBLIC repository.
- All images and sampler are delivered as ChatGPT conversation attachments/ZIP, NOT stored in GitHub yet. The hashes here make the re-import auditable.
- Local sample MP4 SHA256 03c3ad0b4a052d0ed242c82100ce989d8d87d4cecdfd1a88674731f6b02018bd.

## Artistic review
The new GPT-native imagery is substantially more detailed than the earlier primitive code animations. But each is **one baked full-frame illustration**, so the motion pass is limited to synthetic rain, lamplight, thread and some photo drift. The actor's reaching motion (L07) and scarf hand contact motion (L08) are illustrated at a single pose and cannot legitimately be scored as animated motion.

Do not conflate this local lightweight compositing test with a Huashu-native GitHub Actions render or with the finished eight-lyric music video. The previous P1/P2 cloud gate stays passed, but new-art skill-native integration is an unmet test.

## Current state
- P0 cloud runtime: PASS
- P1 two-second Skill engine cloud proof: PASS
- P2 isolated one-lyric Huashu cloud test: PASS (old art rehearsal)
- P3 4 GPT image hero anchors: CREATED / LOCAL ART ONLY
- P3 new-art cloud ingestion & layer-separated animation: NOT TESTED
- P3 image hero for L02/L03/L05/L06: MISSING
- P3 real L07/L08 multi-pose keyframes: MISSING
- human aesthetic approval: PENDING

## Next 3 implementable steps
1. In a Work/browser image-generation session, make four missing lyric hero images and 2–3 motion keyframes for L07 and L08. Generate full-frame scene and subject layers separately when possible. Do not assert transparent backgrounds without inspecting alpha.
2. Import the four existing PNGs from the artifact ZIP with `python mv_web_stable/p3/ingest.py /path/to/assets`, inspect the import receipt, then upload approved assets to proper storage with copyright/private-song policy intact.
3. Build a true layer-based `mv_web_stable/p3/shot_renderer.js` for Huashu Canvas and a GitHub Actions partial MP4 run using first new assets; score natural motion and cut timing independently of codec QA.

Work project hint: the referenced GitHub repo cannot consume images automatically from a transient ChatGPT conversation; the actual PNG files must be transferred and hashes verified.
