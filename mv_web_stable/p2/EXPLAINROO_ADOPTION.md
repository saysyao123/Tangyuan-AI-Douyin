# Explainroo adoption review
Original: https://github.com/vincentsch/explainroo
Pinned review: 53479053ffd659984394f8ee79c00eb89a5690af (MIT).
Checked files: AGENTS.md; skills/explainroo/SKILL.md; src/timeline.js; src/render.js; src/qa.js; src/images.js.

**Useful architecture**
- script.md with #marker and scenes.js maps spoken cues to drawing changes; adapt to L01–L08 lyric source-time plus provisional peak markers.
- Each scene can be separately rendered and inspected through stills and contact sheets.
- QA checks frame layouts, subtitle readability, black frames and final A/V codec/length.
- On-demand image asset registry with references and provenance.

**Do not adopt**
- Kokoro creates synthetic voice-over, inappropriate for existing music.
- Whisper/forced alignment is not reliable enough to lock Chinese singing lyrics without listening.
- Explainroo uses optional OpenRouter image generation and paid API tokens, not the user's chosen ChatGPT native image-generation workflow.
- Its default explanatory flat-icon style should not replace the established cinematic illustrated MV identity.
- Keep Huashu-art-motion as the master Canvas animation renderer; adapt Explainroo's cue and review ideas only.

**State**
No Explainroo packages installed in production and no Explainroo TTS invoked. This is source study and architecture adaptation, not a claim of native Explainroo MV execution.
