# P2: Eight-lyric isolation + GPT art gate
P1 has proved GitHub cloud export of a real 2-second H.264/AAC MP4.

## Executable in this revision
- shot_contract.json = eight independent lyric scene IDs, global time spans and provisional primary-event markers.
- validate.py = strict eight-shot/timing/frame-coverage gate; --require-assets fails closed if real GPT-native images are absent/unapproved.
- render_shot.py = isolate and render a chosen global-time scene using proven Huashu Canvas. Uses legacy art ONLY as ENGINE REHEARSAL.
- verify_clip.py = verify full decode, 1080x1920/30fps, frame count, AAC and a middle preview.
- GitHub Actions / mv_web_stable_p2.yml = browser choice L01–L08 to test one scene.
- GPT_NATIVE_ART_BRIEF.md / assets_manifest.json = production image prompt and per-shot source/visual QA contract.
- EXPLAINROO_ADOPTION.md = study notes, explicitly separate reusable marker/QA methodology from irrelevant TTS.

## P2 acceptance
1. Score validated = PASS (8 IDs, 641 exact global frames).
2. At least one Lxx independently rendered in Actions, its MP4 and PNG artifact downloadable.
3. Art readiness separate = PENDING until genuine GPT-native assets are generated and reviewed.
4. Full eight-shot high-art MV remains PENDING; no fallback to old art is allowed for production.

Public repo: no copyrighted raw music and no API keys.
