# Upstream Skill Lock

- Upstream: https://github.com/alchaincyf/huashu-art-motion
- Commit: `26dba25b2b495c2138848c29a2c90df356a20325`
- License: MIT (code/documentation); fonts separately OFL and source illustrations demo-only.
- Source entry: `SKILL.md`.
- Role split: the Skill determines animation/staging/Canvas compositing, GPT native image generation supplies new character/scene sprites, and audio timeline is project-controlled.
- Project P1 path: existing Run01 fork pinned to this Skill, `08_AGENT_CONTROL_LAYER/pilots/CODE_MOTION_MV_RUN01_2026-10-06/engine/`.
- P1 explicitly does **not** validate new art assets or native browser installation inside ChatGPT: it validates hosted GitHub Actions execution of the Skill-renderer code.
- For P2+ the source engine and project overlays should be maintained as separate modules rather than rewriting `engine.js` for each MV.
