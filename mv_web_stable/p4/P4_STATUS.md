# P4 · GPT independent-image asset acceptance checkpoint

Updated 2026-10-08. **P4 ART PRODUCTION NOT PASSED**.

## Facts
- P1 cloud 2s animation smoke PASS (existing Huashu-derived engine).
- P2 L03 cloud independent rehearsal PASS; legacy art only.
- P3 genuinely generated and delivered four stand-alone GPT-native 941×1672 hero PNG images for L01, L04, L07, L08, not uploaded as binaries to this public GitHub repo.
- Latest attempts to generate L02, L03, L05, L06 instead returned several **eight-shot collage/storyboard posters**. These were *not accepted* as independent hero frames.
- L07 and L08 are only one completed-pose still each; no new independent hand/arm keyframe sequences were successfully generated.
- Local asset validator check: 4/8 geometry PASS; expected --require-all FAIL; portrait poster 1024×1536 was rejected for incorrect 9:16 aspect.
- Geometry alone cannot detect montage, inconsistent character, hand distortions or physically implausible image-layer movements. Human creative gate still required.
- Local deliverable: `若爱有尽头_P4_素材验收包.zip`, containing the four true originals, review report, independent per-shot prompt instructions and a demonstration of a rejected collage.
- Actual GitHub binary art import: NOT DONE; no cloud new-art render claimed.

## Correct next execution
1. In Work or a clean, single-image creation chat, execute **one shot per native image call**, with reference to L01 and L07 as character anchors. First L02, L03, L05, L06 then true 3-frame action poses L07/L08.
2. Save original PNG (not croppings of contact sheet) into assets/Lxx_hero.png. Re-run `validate_p4_assets.py` and perform manual scene/character/motion visual gate.
3. Transfer approved original PNG files into actual storage connected to GitHub Actions. Current conversation files are not magically GitHub asset binaries. Do not merge public copyrighted music.
4. Only then run an **image-driven Huashu scene** cloud test against genuine uploaded assets; avoid reverting to old Run01 stills as purported final art.
5. Lock transitions by the eight actual lyric boundaries and retime motion peaks after listening to the real audio. Current cue hints are provisional.

## Status evidence
Local source images and SHA256 already enumerated in `mv_web_stable/p3/four_anchor_manifest.json`. No new image SHA256 for the missing four is available because independent pictures were not successfully generated.
