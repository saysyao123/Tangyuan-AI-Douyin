# D02-B｜NATURAL_BEAT

> Stage: `S03_AUDIO_TIMELINE_LOCKED -> S04_NATURAL_BEAT_LOCKED`
> Status: `READY_FOR_RUNTIME_PREFLIGHT`
> Executor: `NATURAL_BEAT_SYNTHESIS`
> Scope: semantic / emotional / music structure only. **No world, character, palette, camera, prop, composition or production-segment allocation is decided here.**

## 1. Locked input truth

- Song family: `有几次想你了`
- Exact HG02 audio: Douyin asset `7670104695834282815`, option B, 0.8s soft tail fade
- Locked audio SHA-256: `6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4`
- Canonical timeline duration: `15.386083s`
- Lyric evidence: `ASR_FORCED_ALIGNMENT`, Ground-truth QA PASS
- Lyric clock:
  - L01 `有几次想你了` — `0.300–2.061s`
  - L02 `有几次忍住了` — `2.061–3.802s`
  - L03 `有几句想说的` — `3.802–5.602s`
  - L04 `都变成算了` — `5.602–6.983s`
- Director-relevant lyric anchors:
  - `想你` — `1.120–1.641s`
  - `忍住` — `2.921–3.561s`
  - `想说` — `4.642–5.182s`
  - `算了` — `6.503–6.983s`
- Music-event clock highlights:
  - opening onset `0.163s`
  - mid-vocal onset `3.170s`
  - final-line onset `5.619s`
  - vocal release `6.983s`
  - first post-vocal onset `7.767s`
  - late buildup `11.122s`
  - detected energy peak `12.214s`
  - late accent `13.398s`
  - fade start `14.586s`
  - content end `15.386s`

## 2. Core semantic arc

The excerpt is a compressed emotional sequence of **admission -> restraint -> unsaid speech -> self-cancellation -> emotional afterimage -> release**.

The key dramatic fact is not simply “missing someone.” Every lyric line weakens the speaker's permission to act:

1. `想你` admits an internal impulse.
2. `忍住` actively suppresses that impulse.
3. `想说` reveals communication almost becoming action.
4. `算了` cancels that action at the last moment.
5. After `6.983s`, language disappears but the music continues for more than eight seconds; the unresolved feeling therefore survives the words instead of ending with them.

This post-vocal duration is structurally important. It is **not dead tail** and must remain available to the Director as emotional continuation / transformation / release space.

## 3. Natural Beats

| Beat | Time window | Locked trigger | Semantic / emotional task | Energy role | Anchor opportunity | Boundary reason |
|---|---:|---|---|---|---|---|
| NB01 | `0.163–2.061s` | opening onset -> L01 | **Admission / recurrence.** The thought of the other person has returned more than once; the speaker finally names the private impulse: `想你`. | HOOK / inward opening | `想你 1.120–1.641` | Ends exactly when the lyric changes from feeling to active suppression. |
| NB02 | `2.061–3.802s` | L02; onset at 3.170 | **Restraint.** The emotion is not merely felt; it is deliberately held back. `忍住` is the first clear action verb and introduces internal resistance. | TENSION / compression | `忍住 2.921–3.561` | Ends when the suppressed action changes from feeling-control to blocked communication. |
| NB03 | `3.802–5.602s` | L03 | **Almost-speaking.** The emotional pressure seeks an external channel: there are words that nearly leave the speaker but remain unsaid. | RISE / near-action | `想说 4.642–5.182` | Ends at the final semantic reversal: expression gives way to cancellation. |
| NB04 | `5.602–6.983s` | strong onset 5.619; L04 | **Cancellation / resignation.** `都变成算了` converts accumulated longing, restraint and unsaid speech into a chosen retreat. The phrase `算了` is the semantic landing, not a casual filler. | LYRIC PEAK / semantic release | `算了 6.503–6.983` | Ends on the final aligned vocal token; language stops here. |
| NB05 | `6.983–12.214s` | vocal release -> post-vocal onset 7.767 -> buildup 11.122 | **Afterimage / feeling outlives language.** No new lyric arrives, so the music carries what the speaker could not say. The emotional state should be allowed to continue, change scale or accumulate rather than being treated as empty outro. | POST-VOCAL BUILD / expansion | none; music clock only | Ends at the strongest detected energy peak, which creates a natural non-verbal culmination. |
| NB06 | `12.214–15.386s` | energy peak 12.214 -> accent 13.398 -> fade 14.586 -> end | **Non-verbal culmination -> letting go.** The excerpt reaches its strongest acoustic accent after the lyrics are already gone, then releases into the locked fade. | MUSIC PEAK -> RELEASE / tail | none; music clock only | Ends at canonical content end. No new semantic event should be introduced after fade start. |

## 4. Hook / Peak / Release map

- **Semantic Hook:** NB01, especially `想你 1.120–1.641s`.
- **Internal tension pivot:** NB02 `忍住 2.921–3.561s`.
- **Near-action pivot:** NB03 `想说 4.642–5.182s`.
- **Lyric semantic peak / landing:** NB04 `算了 6.503–6.983s`.
- **Music-only expansion:** NB05 `6.983–12.214s`.
- **Acoustic peak:** NB06 entry at `12.214s`.
- **Final release:** `14.586–15.386s` fade zone.

Important distinction: the lyric peak occurs around `算了`, while the strongest detected music-event peak occurs much later at `12.214s`. Director Allocation must coordinate these two different clocks rather than pretending they are the same moment.

## 5. Energy contour

`quiet admission`
-> `compression / restraint`
-> `pressure toward expression`
-> `semantic resignation`
-> `post-vocal expansion`
-> `non-verbal peak`
-> `fade / release`

This contour argues against equal-duration visual blocks. It also argues against ending the meaningful visual story at `6.983s`: more than half of the locked excerpt remains after the last lyric.

## 6. Director handoff constraints

The next stage may design visual language, but it must preserve these truths:

1. **No second lyric clock.** All lyric timing comes from `03_AUDIO_TIMELINE/line_timeline.csv`.
2. Natural Beat is a semantic unit, **not a required first-frame count, dynamic-source count or edit-fragment count**.
3. Anchor words are visual opportunities, not mandatory cut points.
4. `NB04` must make `算了` read as the culmination of accumulated suppression, not as an isolated lyric illustration.
5. `NB05–NB06` must have a purposeful post-vocal role; they cannot be generic filler or merely hold the last lyric image for eight seconds without a reason.
6. The acoustic peak at `12.214s` may drive a non-verbal visual culmination, but it cannot rewrite the lyric meaning already landed at `6.983s`.
7. After fade start `14.586s`, prefer release/residue; do not introduce a brand-new narrative proposition that cannot resolve before `15.386s`.
8. No visual world, character identity, palette, object, camera recipe or composition from D01-A/D01-B/other prior MVs is inherited by this Beat map.

## 7. Stage conclusion

`NATURAL_BEAT_SYNTHESIS = PASS`

`NATURAL_BEAT_READY = YES`

The locked audio truth has been converted into six semantic/music Natural Beats without introducing visual design or altering either lyric or music-event clocks.
