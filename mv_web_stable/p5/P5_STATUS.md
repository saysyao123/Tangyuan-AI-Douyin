# P5 · GPT-native illustration scenes inside original Huashu engine

Updated 2026-10-08.

## Actual engineering and proof
- GitHub commit c68bfffcad6b9395f01dcd95f9c11eaa0e10a8f9 adds the Huashu `gpt` scene profile. Original Huashu `render.py` and `engine.js` are unmodified.
- GitHub Actions source export RUN **37734709478 PASS**, archive artifact **11531231907**. Engine files were downloaded back and verified in the current session.
- The current container browser blocks **both localhost and file://** navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. This is a runtime sandbox policy and does NOT imply the Huashu script itself failed.
- Fallback local test executes **the exact exported original Huashu scene module** `scenes/gpt_images.js` with Node/skia-canvas; it renders actual four previously generated GPT-native picture assets and masks separate red-thread/photo object layers.
- Local preview MP4: 1080×1920 30fps, H.264/AAC, **310 video frames / 10.333 seconds**, complete decode **PASS**; original source song excerpts selected at frozen **global frame boundaries**.
- Local L01 independent 2.5-second MP4 complete decode **PASS**.
- Four shots and global frame intervals: L01 [0,75), L04 [240,322), L07 [488,562), L08 [562,641).
- Original sound recording and actual GPT PNGs are contained only in private conversation outputs, NOT the public GitHub repository.

## Deliberate technical and visual distinctions
- The cloud **source-export** workflow passed. A true cloud **NEW GPT ART RENDER** with original Huashu Chromium `render.py` is **NOT PASSED** yet because the five PNGs have not been uploaded to GitHub.
- Existing GPT stills do not have complete actor keyframes: L07 and L08 contain a frozen hand posture. The background and object layers can move, but cannot pass a physically natural human movement gate.
- L01 thread separation is technically animated but subtle in the review frames; needs art correction/stronger hand thread visual peak.
- No image asset exists for L02/L03/L05/L06; only four-shot sampler produced.
- Current main user intent remains a full lyric-specific, dynamic, coherent 21.36-second MV. This P5 stage is **an engine-image integration milestone**, not final delivery.

## How to use cloud production runtime
1. From the private P5 download ZIP, upload only `assets/prepared/L01_clean.png`, `L04_hero.png`, `L07_clean.png`, `L07_photo.png`, `L08_hero.png` to **mv_web_stable/p5/assets/prepared/** in the GitHub repo; do not upload the source song or lyrics raw-media file.
2. Each asset SHA256 must match `prepared_assets_expected_sha.json`; `stage_assets.py` refuses to render on mismatch or absent files.
3. Open [Actions / MV P5 Huashu GPT Art Runtime](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/workflows/mv_web_stable_p5.yml), select `L01`, and trigger workflow_dispatch.
4. Successful proof requires GitHub runner result, delivered MP4 Artifact and decoded full-video checks. Running a source-export alone is insufficient.

## Next visual work
One **single image generation request per new original frame**. Correct the image-generation drift into contact sheets; do not crop them for main artwork. Generate missing L02 L03 L05 L06 standalone 9:16 heroes, then stable, consistent L07 and L08 start/middle/end real keyposes. Score human-motion smoothness only when pose evidence exists. Avoid pointless whole-frame pans/zooms.


## 2026-10-08 Cloud follow-up
- Huashu **real Chromium renderer** synthetic engine QA RUN 37737780845 = SUCCESS, 75 frames, 1080x1920, H.264/AAC, frame delta/nonstatic verified.
- The original five GPT art PNG files were not in the GitHub repo and were NOT used in that cloud fixture. P5 real-art cloud render still PENDING.
- An upload-once ZIP contract with exact manifest and SHA pin was added in `P5_SINGLE_UPLOAD.md`: a user can upload ONE ~10MB ZIP in the GitHub browser. Push will auto-detect it and trigger production.
- The prior incorrect stage-assets root was fixed. Artistically reviewed story footage requires other four lyric heroes and true actor action keyframes.
