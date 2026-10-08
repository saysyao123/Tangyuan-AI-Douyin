# P5 · Actual Huashu engine receives GPT-native illustration layers

### What is implemented
- The original repository engine `render.py` and `engine.js` are preserved as the rendering backend. The engine's `index.html` gets only one new allowed film identifier `gpt`.
- New `eras_gpt.js` and `scenes/gpt_images.js` register four approved picture shots in the source Huashu `SCENES` API. No rewriting the engine renderer or silent fallback to old art.
- Five prepared PNGs are required: `L01_clean.png`, `L04_hero.png`, `L07_clean.png`, `L07_photo.png`, `L08_hero.png`.
- Dynamic layer events: L01 red thread snap, L07 independent photo drift, L04 steam/glow, restrained rain all scenes. **Actors remain static** pending new GPT action poses.
- `stage_assets.py` verifies exact SHA256 of each file; refuses missing/mismatched images.
- `render_one.py` runs actual Huashu `render.py --film gpt --solo lXX` and muxes music/audio from the correct original-song time range.
- GitHub Action exports the original source snapshot on push, and offers browser-triggered single-shot cloud rendering **ONLY after actual PNG binaries are uploaded**.

### Honest limitations
The source images were generated in ChatGPT (four genuine single-frame artworks). Earlier image generation subsequently produced repeated multi-panel boards, NOT acceptable replacements. This P5 does not claim full 8-shot picture coverage, animation of L07 arm or L08 scarf-touch hand, or that PNGs already exist inside the public repo.

### Import instructions
Upload only the 5 prepared PNG assets to `mv_web_stable/p5/assets/prepared/` from the downloadable deliverable ZIP; keep matching byte-identical SHA256. Do **not** commit the licensed original audio. After import, start the workflow manually at `.github/workflows/mv_web_stable_p5.yml`, select L01 for first proof. A source snapshot will be downloadable even while production images are missing.
