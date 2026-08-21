# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W04`
- STAGE_NAME: `Director concept + production-unit allocation`
- STATE: `READY_TO_START`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Golden Quality Floor

R1 Golden Sample remains the minimum quality floor: frame beauty, lyric hit, directing/camera diversity, dynamic QA and edit/subtitle accuracy must not regress.

## W00 Result — LOCKED

Actual state: `AUTO`. GitHub/Web/Files/Image interface/local ffmpeg stack verified. Dedicated Whisper/faster-whisper and direct Seedance execution are unavailable in the current exposed toolset.

## W01 Result — LOCKED

Research: `AUTO`; stage total: `HUMAN_GATE / PASSED`.
Selected song: `如果你也刚好抬头看树` — `孙天宇` official vocal version.

## W02 Result — LOCKED

Actual state: `PARTIAL`.
Locked production source: `如果你也刚好抬头看树-孙天宇.mp3`, 196.127s, MP3 320 kbps / 44.1 kHz / stereo.
Locked BGM excerpt: `139.930s–177.050s`, rendered duration `37.120s`, fade in `0.020s`, fade out `0.950s`.
Final preview v3 passed user gate.

W02 one-shot clipping failed in this round and required two avoidable boundary corrections. `04_HARNESS/workflows/mv.md` was upgraded to v1.1 with the mandatory Audio Boundary Gate. Future W02 must prove this improvement by first-pass acceptance.

## W03 Result — LOCKED

Actual state: `AUTO`.

### Evidence / timing method

- Dedicated Whisper/faster-whisper is unavailable and was **not** claimed.
- No trustworthy public same-version timed LRC was found.
- Lyric sequence was cross-checked against multiple same-song sources; full-version identity remains the locked 3:16 Sun Tianyu master.
- Timing/structure uses the locked v3 audio, waveform/RMS/onset evidence, repeated-chorus alignment from W02 and beat tracking.
- Local beat estimate for the locked clip: approximately `103.36 BPM`.
- Harmonic-color estimate is bright major-leaning (automatic chroma estimate near E-flat major); this is descriptive only, not a hard production dependency.
- Exact subtitle timestamps are **not** being invented here; W08 must use verifiable same-version timing evidence.

### Exact lyric sequence in locked excerpt

1. 如果你也刚好抬头看树
2. 我要学着树叶翩翩起舞
3. 喊几声布谷布谷
4. 或许少有人知道
5. 有鸟儿是这样叫
6. 好吧哎哟哎哟
7. 一颗心叽叽喳喳飞过了树梢
8. 如果你也刚好抬头看树
9. 向一朵白云学习如何漂浮

### Natural Beat Map

Timing below is structural/energy grouping for directing, not subtitle timing.

| Beat | Approx clip range | Lyric / function | Energy | Visual opportunity |
|---|---:|---|---|---|
| B1 | `0.0–5.9s` | 标题句 + 树叶起舞入口 | medium → bright | `抬头`必须成为第一个空间事件；叶片动作不是背景装饰 |
| B2 | `5.9–10.7s` | 布谷布谷 | playful rise | 声音可转译为枝叶震动 / 鸟的空间定位 / 微距事件 |
| B3 | `10.7–15.9s` | 少有人知道 / 鸟儿这样叫 | medium, curious | 从“听见”转为“发现”，适合隐藏→揭示 |
| B4 | `15.9–23.1s` | 哎哟哎哟 + 心飞过树梢 | **primary motion peak** | 最适合整段最大动作与向上运动，禁止只拍风吹叶子 |
| B5 | `23.1–27.7s` | 标题句复现 | release/reset | 重新获得“抬头看树”的完整空间关系，为天空段换层级 |
| B6 | `27.7–37.12s` | 向白云学习漂浮 + tail | airy release | 从树冠释放到天空；结尾应轻，不再制造第二高潮 |

### Emotional / Strength Curve

`好奇停驻 → 轻快游戏 → 发现生命 → 顽皮上扬 → 心的飞升 → 抬头确认 → 漂浮释放`

Strongest dynamic opportunity: `B4 一颗心叽叽喳喳飞过了树梢`.
Strongest recognition opportunity: title-line openings in `B1 / B5`.
Best ending opportunity: `B6` cloud/air release.

### Opening Hook candidates from W03

These are opportunities only; W04 selects one concept:
1. one leaf lifts against gravity and drags the camera rapidly up the trunk into the canopy;
2. extreme low-angle canopy opening where a branch/leaf passes the lens and reveals the sky in the first second;
3. hidden bird-call event that physically disturbs dew/leaf texture before the bird is seen.

## W03 Automation Conclusion

W03 can be completed automatically without user work. The missing dedicated ASR affects exact subtitle-level timing, not the ability to establish lyrics, musical structure, Natural Beats, emotional curve and director opportunities.

## Next Allowed Action

Run `W04` automatically.

W04 must:
- perform a focused 3–5 work benchmark relevant to this song;
- choose one unified visual concept/world/material system;
- set character policy;
- lock one Opening Hook;
- assign dominant visual event per Beat;
- calculate conceptual visual units, first-frame count and 5s production clips separately;
- explicitly verify raw dynamic coverage versus the `37.120s` locked BGM;
- design camera diversity and run a Camera Repetition Gate;
- then stop at the designed `AESTHETIC_GATE` for user director approval before W05.