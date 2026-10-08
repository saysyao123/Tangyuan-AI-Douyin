# P5 · One-upload GPT asset pipeline

## Source and integrity
The images originate from the four actual ChatGPT-native single-illustration generations for L01/L04/L07/L08. Five prepared PNG files are derived from them: one red-thread clean plate, the room hero, a reaching figure clean plate plus an independent photo cutout, and the scarf hero. All five SHA256 values are pinned in `prepared_assets_expected_sha.json`.

**No audio is contained in the ZIP.** This is a public repo and the song remains outside it. The resulting cloud clip is paired with a test tone, not the original song.

## One-click browser upload (one user action)
1. Obtain `GPT_NATIVE_ANCHORS_UPLOAD.zip` from the ChatGPT P5 delivery.
2. At [mv_web_stable/p5/assets](https://github.com/saysyao123/Tangyuan-AI-Douyin/tree/main/mv_web_stable/p5/assets) select **Add file → Upload files**.
3. Drag the **single unmodified ZIP file**, preserving its name `GPT_NATIVE_ANCHORS_UPLOAD.zip`, and commit it to **main**.
4. That commit automatically triggers the [MV P5 Huashu GPT Art Runtime](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/workflows/mv_web_stable_p5.yml); the job detects the archive and switches from synthetic fixture to `production`.
5. Download the latest job artifact. The result is labeled `huashu-p5-production-L01-<run-id>` and must contain an MP4 + verification JSON.
6. If necessary, manually Run workflow choosing L04, L07, L08, and `production` after the first success.

## Fail-closed safety
- `stage_assets.py` checks exactly five known PNG names and one manifest, SHA256 for all five files, PNG signature and no audio flag.
- If any source PNG is missing or altered, **no legacy art fallback** is allowed and the production job fails with a specific error.
- `make_fixture.py` writes an obvious watermark and a separate fixture marker, and is used only when real art has not yet been uploaded.
- `render_one.py` only accepts `production` or `synthetic-fixture` art modes. The final technical report retains the mode so fixtures cannot be mislabeled as finished art.

## Acceptance
- Already proven: Huashu Chromium on GitHub Actions rendered a **75-frame** L01 synthetic test MP4 and decoded it correctly (run 37737780845). This is ENGINE PASS.
- Not yet proven: **actual GPT PNG binaries** traveling through the GitHub Actions production pipeline. This requires the ZIP upload.
- Not yet completed: remaining four standalone images L02/L03/L05/L06 and natural keyframe motion for L07/L08. Production single-shot video is a separate milestone from the finished MV.

## Image generation issue
Repeated attempts at L02 produced **eight-panel storyboard posters instead of one portrait frame**. Those are rejected and must not be cropped and represented as native standalone GPT stills. In a clean Work/new image chat, request one single scene output only, keeping P3 L01/L07 as role references.
