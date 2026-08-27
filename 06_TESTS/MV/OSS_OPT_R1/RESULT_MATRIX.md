# OSS MV Optimization Result Matrix v1.5

Status: `IN_PROGRESS / P1 LIGHTWEIGHT LYRIC TIMELINE VALIDATED`

## Test identity

- Experiment branch: `test/mv-oss-optimization-r1`
- Runtime baseline fork SHA: `89852ec5314e7579853683ef5eb40adb09f25753`
- Test MV slot: `D02-B / Lane S`
- HG01 song family: `有几次想你了 / LOCKED`
- HG02 BGM: `B variant / exact Douyin music object 7670104695834282815 / 0.8s soft tail fade / LOCKED`
- Locked BGM SHA-256: `6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4`
- Canonical Runtime state: `S02_HG02_BGM_LOCKED / BGM_LOCKED`
- External OSS source: `penposs/mvmaker-h3-skills@796797030275fe57afaba736771e8510c848799d`

## A/B creative comparison

| Dimension | Baseline Runtime | Runtime + OSS Overlay | Delta | Evidence |
|---|---:|---:|---:|---|
| Lyric visual hit | TBD | TBD | TBD | Director A/B not started |
| Director / camera quality | TBD | TBD | TBD | Director A/B not started |
| Shot diversity | TBD | TBD | TBD | TBD |
| Visual coherence | TBD | TBD | TBD | TBD |
| First-frame performability | TBD | TBD | TBD | TBD |
| Dynamic stability | TBD | TBD | TBD | TBD |
| Character / identity continuity | TBD | TBD | TBD | TBD |
| Edit-source usability | TBD | TBD | TBD | TBD |
| Regeneration count | TBD | TBD | TBD | TBD |
| Manual intervention count | TBD | TBD | TBD | TBD |
| Production time / burden | TBD | TBD | TBD | TBD |
| Runtime compatibility | Baseline | TBD | TBD | Executor-first audit completed |
| Zero-context reproducibility | Baseline | Improved | Positive | 19/19 executor registry CI PASS |

## Gate-by-gate findings

### HG01 / Song

`PROCESS CORRECTION / VALIDATED IN EXPERIMENT`

Accepted strategy:
`CORE BENCHMARK ACCOUNTS -> DATA CENTER -> SONG_FAMILY RANKING -> SIMPLE DIRECT MV HANDOFF -> USER HG01`

Retained hardening:
`DELIVERED URL MUST OPEN THE CITED MV ITSELF`.

Rejected:
`WEB-WIDE SEARCH -> CANDIDATES CHOSEN BY PUBLIC EVIDENCE AVAILABILITY -> HEAVY EVIDENCE TAXONOMY`.

HG01 is locked to `有几次想你了`.

### HG02 / BGM

`PASS / LOCKED`

Two core works resolved to the same Douyin music object `7670104695834282815`. User accepted B: same exact source with final `0.8s` soft fade-out.

### Audio Timeline

`P1 LIGHTWEIGHT ROUTE VALIDATED / ONE HUMAN LYRIC AUDIT STILL REQUIRED BEFORE CANONICAL S03 LOCK`

#### Defect A｜Executor discovery gap

The agent initially rebuilt tooling even though canonical Audio Timeline tooling already existed.

Remediation completed:
- stage executor registry with 19/19 coverage;
- Executor-First rule;
- startup/JIT loads executor routing before any new implementation;
- slot-specific core helpers and per-song production-model installs rejected by default.

#### Defect B｜Partial caption mistaken for complete lyrics

The first D02-B lyric set contained only four lines because a creator caption was treated as complete lyric truth.
The locked BGM actually contains seven sung lines.

Hard rule:
`creator caption / description / hashtag / lyric quote != complete lyric truth`.

The incorrect four-line downstream Audio Timeline/Natural Beat state was formally rolled back and archived via the Runtime revision mechanism. Canonical D02-B remains at S02.

#### Re-audit of proven D01 production paths

D01-A used `SAME_VERSION_LRC`, not Xingyu.
D01-B used `faster-whisper==1.2.1 / small / CPU int8 / zh word timestamps + trusted-text character mapping`, not Xingyu.

This changed the experimental route priority to:

`P0 SAME_VERSION_LRC`
-> `P1 D01B_LIGHTWEIGHT_FASTER_WHISPER`
-> `P2 XINGYU_CTC_FALLBACK`

Policy:
`06_TESTS/MV/OSS_OPT_R1/AUDIO_TIMELINE_ROUTE_POLICY_v1.md`

#### P1 D02-B validation

Workflow run `33059906090` — unprompted full-clip Faster-Whisper small:
- exact B audio SHA verified;
- complete seven-line song structure recovered in one pass;
- two normal ASR wording errors appeared (`想念` vs audited `想你`; `几场风` vs audited `几阵风`), proving the value of one lyric-text audit;
- model init `3.097s`;
- transcript `4.426s`;
- total model work `7.523s`;
- lightweight cache created: `573,157,329 bytes` (~547 MB).

Workflow run `33060055071` — audited trusted text + D01-B mapping:
- cache hit;
- model init `1.227s`;
- transcript `4.775s`;
- total model work `6.002s`;
- recognized normalized text exactly equals audited trusted text;
- sequence ratio `1.0`;
- `7/7` lines mapped;
- `100%` character coverage on every line;
- line starts strictly monotonic;
- decision `LIGHTWEIGHT_ALIGNMENT_PASS`.

Validated P1 line timing candidate:

| Line | Lyric | Start | End | Coverage |
|---|---|---:|---:|---:|
| 1 | 有几次想你了 | 0.000 | 1.880 | 100% |
| 2 | 有几次忍住了 | 2.020 | 3.640 | 100% |
| 3 | 有几句想说的 | 3.780 | 5.400 | 100% |
| 4 | 都变成算了 | 5.600 | 7.180 | 100% |
| 5 | 有几场雨停了 | 7.320 | 8.940 | 100% |
| 6 | 有几阵风过了 | 9.120 | 10.700 | 100% |
| 7 | 有多舍不得也该放下了 | 10.860 | 14.260 | 100% |

Conclusion:
`D01B_LIGHTWEIGHT_FASTER_WHISPER = P1 PASS / DEFAULT AI ROUTE CANDIDATE`.

#### P2 Xingyu archive

Xingyu remains validated but is now fallback-only.
Archive:
`06_TESTS/MV/OSS_OPT_R1/XINGYU_FALLBACK_ARCHIVE_v1.md`

Validated Xingyu capabilities on corrected D02-B:
- 7/7 lines aligned;
- 45/45 normalized characters timed;
- no missing character timestamps;
- monotonic line timing;
- high precision.

Reason for fallback classification:
- shared Xingyu/WhisperX environment cache roughly `5.8 GB`;
- substantially heavier startup/restore burden than P1;
- no demonstrated production benefit on this D02-B case once P1 reached 100% coverage.

P2 triggers only on concrete P1 failure or explicit high-precision word/character timing need.

#### Minimal normal production logic

`P0 reliable same-version LRC? -> PASS and stop`

otherwise:
`P1 exact BGM -> one Faster-Whisper full-clip pass -> one lyric-text audit -> trusted-text timing map -> one automatic QA -> PASS and stop`

only if P1 concretely fails:
`P2 Xingyu CTC forced alignment`.

No default second-model verification.
No Web-wide lyric evidence sweep.
No waveform/BPM lyric guessing.
No per-song helper/toolchain.
No Anchor/Music Events before lyric timeline lock.

### Director

TBD. First major stage where `mvmaker-h3-skills` creative overlay is intentionally allowed.

### HG03 / First Frames
TBD

### Dynamic / Dynamic QA
TBD

### Normalization / Edit
TBD

### HG04 / Picture Edit
TBD

### Subtitle / Final QA
TBD

### HG05 / Final Acceptance
TBD

## Final decisions

| Optimization ID | Decision | Reason | Promotion target / next action |
|---|---|---|---|
| CORE-DATABASE-HG01-RESTORE | `PROMOTE_RULE` candidate | Restores proven R3 candidate authority | retain |
| DIRECT-LINK-IDENTITY-GUARD | `PROMOTE_RULE` candidate | Prevents incorrect MV handoff | retain |
| WEB-WIDE-EVIDENCE-DRIVEN-DISCOVERY | `REJECT` | Evidence availability started driving song choice | do not promote |
| EXECUTOR-DISCOVERY-GAP | `PROMOTE_RUNTIME` candidate | Runtime must route HOW as well as WHAT | retain |
| SLOT-SPECIFIC-CORE-HELPER | `REJECT` | Duplicates canonical paths | keep history only |
| PER-SLOT-PRODUCTION-MODEL-INSTALL | `REJECT AS DEFAULT` | Production should reuse established route/runtime | environment setup only |
| PARTIAL-CAPTION-AS-LYRIC-TRUTH | `REJECT` | Caption may be only an excerpt | hard reject |
| P0-SAME-VERSION-LRC | `PROMOTE_RULE` candidate | Proven D01-A fastest path | first priority when reliable |
| P1-D01B-LIGHTWEIGHT-FW | `PROMOTE_RULE` candidate | Proven D01-B and validated D02-B; fast + 100% coverage | default AI route |
| P2-XINGYU-CTC-FALLBACK | `KEEP AS FALLBACK` | High precision but heavy runtime; valuable for exceptions | archived and retained |
| MULTI-SOURCE-BY-DEFAULT-LYRIC-QA | `REJECT` | Adds cost without failure signal | exception only |
| ANCHOR-MUSIC-EVENTS-BLOCK-S03 | `REJECT IN SIMPLE PATH` | These are downstream director enrichment | move downstream |
| OSS-VISUAL-OVERLAY | `KEEP_EXPERIMENTAL` | Creative A/B not started | begin after S03 lock |

## Current experiment verdict

The lyric timing experiment now has a much simpler validated production policy:

`P0 same-version timed lyric -> P1 D01-B lightweight Faster-Whisper -> P2 Xingyu fallback`.

For D02-B, P1 has passed technically. The only remaining normal human action before locking the final Audio Timeline is the single lyric-text audit of the seven-line trusted text. After that, build line timeline/SRT from the validated P1 evidence and advance S03; do not invoke Xingyu unless a new concrete P1 failure appears.
