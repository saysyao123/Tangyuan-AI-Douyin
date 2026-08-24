# WEB R3｜First-frame Set QA v1

Song: `如果风会替我说话`
Round: `WEB_R3`
Stage: `R3-B / FIRST-FRAME SET QA`

## Result
`PASS`

## Set under review
Canonical sequence:
1. S01 `如果风会替我说话`
2. S02 `如果雨会替我回答`
3. S03 `如果我还会想起他`
4. S04 `如果还能一起回家`
5. S05 `如果梦能模糊真假`
6. S06 `如果痛能随之融化`
7. S07 `如果我们还是傻瓜`
8. S08 `如果爱不只是童话`

## QA summary

### Character identity / eye region
PASS. Same fictional East Asian woman remains visually coherent. Eye-region design keeps elongated almond geometry, defined brow-eye depth and wet catchlight without reproducing a real celebrity identity.

### Veil integrity
PASS. Smoke-charcoal veil remains present and fully covers the lower face in all human frames.

### Shot-scale diversity
PASS after full-set regeneration.
The set now breathes as:
`EXTREME CLOSE -> CLOSE/REFLECTION -> MEDIUM -> WIDE -> MEDIUM/REFLECTION -> CLOSE -> MEDIUM -> MEDIUM-WIDE/WIDE`.
This corrects the previous near-shot compression problem.

### Lyric visual hit
PASS.
- S01 wind visibly owns the unsaid sentence.
- S02 rain/reflection acts as an answering layer.
- S03 absence is expressed through empty warm domestic space, not a second human.
- S04 home becomes a distant warm coordinate in architecture.
- S05 truth/dream is expressed by a single-person reflection geometry.
- S06 pain/healing is carried by eyes + hand + veil tension.
- S07 'we' is represented by two imperfect wind objects rather than another person.
- S08 release is expressed through open post-rain warm sky and enlarged world space.

### Environment storytelling
PASS. Warm practical lamps, rain glass, lived-in interior, corridor depth, reflection geometry and open exterior all carry narrative function rather than serving as generic beauty backgrounds.

### Dynamic executability
PASS. Every frame contains one clear 0-second anchor and a feasible first motion entrance. No frame requires a new human to enter.

### Set-level repetition
PASS. Strong close-up shots are concentrated at S01/S06; other segments deliberately hand visual priority to rain, space, absence, architecture, reflection, objects or landscape.

## Notes for dynamic stage
- Keep Seedance 2 mini source generation at ~5s per source.
- Do not force every source into multi-shot. Default 1–2 shots.
- Preserve first-frame identity and veil.
- S04 and S08 should remain space-led; do not push the camera back into a beauty close-up.
- S06 is the MMP-01 core test; facial performance must remain subtle and asynchronous.
- Source audio is REMOVE by default; prompts must prohibit BGM/voice/music.

State:
`FIRST_FRAME_SET_QA_PASS = YES`
