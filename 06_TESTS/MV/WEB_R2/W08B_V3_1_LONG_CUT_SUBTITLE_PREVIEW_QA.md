# WEB R2｜V3.1 Long-Cut + Subtitle Diagnostic Preview QA

- external edit fragments: 9 (V3 was 17)
- video: 891 frames / 24fps / 37.125s / 720x1280 / SAR 1:1
- locked audio content: 37.120s
- preview-vs-locked-audio best global lag: 0.000000s
- audio correlation: 0.999043
- preview SHA-256: `9088dc30c06bc65cacf50dd0b28bbd2042de95ea9a7dcf5a461aef9e903d3c0e`
- subtitle timing source: canonical `AUDIO_TIMELINE_PACKAGE/line_timeline.csv`
- subtitle fade: disabled for diagnostic viewing
- subtitle rendering: exact locked timestamps, subject only to 24fps display quantization (<41.667ms)
- max subtitle start quantization observed: 37.000ms
- long breathing segment: S5 one-take stretched to 6.792s with blend interpolation; no lyric clock change
- safe crop: `630:1120:45:0 -> 720:1280`, lower-right platform mark removed in spot checks
- edit status: `CANDIDATE / USER AESTHETIC + ALIGNMENT VIEWING PENDING`
- W09 subtitle style is NOT locked by this diagnostic overlay.

## Intent

User feedback on V3: technically much better but external cutting still felt too fragmented / visually busy.

V3.1 therefore changes only the picture-edit grammar:
- external fragments reduced from 17 to 9;
- no external fragment below 2.0s;
- canonical lyric/anchor/music clocks unchanged;
- Anchor Word no longer automatically means picture cut;
- S6 internal person→bird→person structure is allowed to carry the `鸟儿` hit inside one external segment;
- S5 becomes the longest breathing shot and carries the title line without external cuts;
- final S9 remains an uninterrupted 4.292s release.

The embedded subtitles are a diagnostic alignment overlay requested by the user. They use the canonical W02A timeline directly and intentionally have no fade so timing can be judged by ear/eye. Final W09 style remains pending human acceptance.
