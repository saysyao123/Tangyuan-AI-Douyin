# P2 · Eight-shot deterministic MV execution contract

Status: **READY / NOT EXECUTED**. Prerequisite P1 cloud media output PASSED on run 37723404840.

## Inputs

- `lyric_timeline.json`: 8 lyric intervals and approved approximate timings. Their boundaries are not newly verified word-level alignment.
- A typed `shots/Lxx.json` per line, with `start`, `end`, `intent`, `image_refs`, `character_frames`, `primary_action`, `secondary_loops`, `camera`, `cut_reason`, `motion_peak_at`, `qa_state`.
- A single locked audio checksum; do not commit copyrighted source audio into the public repo.

## Deliverables

1. Eight separately callable/deterministic scene entries, named L01 through L08.
2. Script to render one scene by `--shot Lxx` with exact global frame boundaries, preserving absolute source-time semantics.
3. Cloud workflow allows single-shot render or full assembly without editing code.
4. Each line has an independently downloadable short MP4 and a PNG keyframe. One failed line does not invalidate sealed upstream outputs.
5. Joining outputs must preserve one continuous master audio layer and no duplicate or dropped frames.
6. Per-scene comparison checks: starting pose, end pose, on-lyric main event, no spatial jumps, visually motivated cut. Human visual Gate after technical checks.

## Shot intent for this song (current provisional artistic direction)

| ID | Lyric | Visual action |
|---|---|---|
| L01 | 如果爱有尽头 | red thread tension and snap |
| L02 | 怎么想念没有 | loss/absence becomes readable |
| L03 | 我该如何拼凑 | photographic fragments reassemble |
| L04 | 没有你的以后 | photo and empty paired seats/cups |
| L05 | 你随时光远走 | wind lifts paper away with ease-in/settle |
| L06 | 回忆却总逗留 | paper slows and lingers without teleporting |
| L07 | 怪我太过念旧 | woman tries to catch it, fails by inches |
| L08 | 迟迟不肯退后 | hand contacts scarf, rests, no repeated zoom |

## Quality gating

- Primary motion event must coincide with each actual lyric onset/peak; if the approved ±0.25s lyric boundaries are inadequate, reopen only timing verification (do not invent precision).
- Foot movement requires planted steps and weight shifts (avoid sliding).
- A camera move is permitted only with named motivation and at most one meaningful continuous move per shot; static is valid.
- Still-image animation vs video generation must be stated as such; optical flow cannot be counted as new human pose evidence.
- Artwork needed after P2 uses GPT native image generation in ChatGPT/Work, not an assumed GitHub API integration.
