# WEB R3｜HG04 Picture Edit Lock v1

Status: `HG04 PASS / PICTURE EDIT LOCKED WITH FINAL-POLISH TODO`
Song: `如果风会替我说话`
Candidate: `如果风会替我说话_R3_PictureEdit_v1.mp4`

## Human decision
User review:
- overall result is good;
- rhythm and musical hit-point / cut-point feeling are good;
- no request to reopen picture rhythm or regenerate current source pool;
- visible source watermark / provenance-mark handling was not solved in the rough-cut and is explicitly deferred into the next stage.

## Gate decision
HG04 reviews picture rhythm / lyric fit / flow. These are accepted.

Therefore:
- `HG04_PASS = YES`
- `PICTURE_EDIT_LOCKED = YES`
- do not reopen edit structure unless final-polish work reveals a concrete continuity problem.

## Deferred final-polish item: source watermark / provenance mark
This is NOT treated as a picture-rhythm failure.

Handling priority in next stage:
1. prefer platform-provided clean / no-overlay export when legitimately available;
2. otherwise use composition-safe crop / reframe where it does not damage 9:16 framing or subject balance;
3. where crop would harm the shot, prefer alternate clean source region / alternate accepted take if available;
4. do not regenerate an otherwise strong shot solely because of watermark until the above paths are exhausted.

The watermark task must be verified shot-by-shot after subtitle-safe-area planning, because crop/reframe and subtitle placement can interact.

## Next stage
`R3-C / FINAL VISUAL POLISH + SUBTITLE INTEGRATION`

Tasks:
- clean-source / watermark handling;
- frame-level trim refinements only if necessary;
- subtitle integration from locked audio timeline / exact SRT;
- final visual consistency pass;
- source-audio removal verification;
- export final candidate;
- HG05 final acceptance.

`HG04_PASS = YES`
`PICTURE_EDIT_LOCKED = YES`
`WATERMARK_POLISH_PENDING = YES`
