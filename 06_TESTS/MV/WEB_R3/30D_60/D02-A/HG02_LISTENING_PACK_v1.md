# 汤圆音乐映像｜30天60条｜D02-A HG02 Listening Pack v1

Status: `HG02_READY / USER_LISTENING_REQUIRED`
Slot: `D02-A`
Lane: `P / Primary-Trend`
Song family: `做她的大地别做她的天`

## Exact Douyin-native version

Locked candidate recording family for HG02:

`做她的大地别做她的天（r&b）（氛围片段） / 大眼仔`

Discovery route:
`P1_VERIFIED_DOUYIN_WORKS`

Independent core samples:
1. 火乐烁 / aweme `7674182052884173553`
2. Aura / aweme `7673796884212895016`

Both works resolved to byte-identical direct music assets:

`sha256 = b5c951cfd1a5d1ab8cf67c093ca0ab1242e9a9be116785588074d768eba9621d`

Direct asset duration:
`26.423991s`

Audio:
- AAC-LC
- 44.1 kHz
- stereo
- ~128 kbps

Classification:
`EXACT_ASSET_CONTENT_IDENTITY_CONFIRMED`

Numeric asset ID is not visible in the current opaque signed URL format; content identity is confirmed by identical direct-asset hashes plus independent-work acoustic comparison.

## Machine QA

- two independent core works: PASS
- displayed title/author consistency: PASS
- direct music asset download: PASS x2
- direct asset byte identity: PASS
- video-side Chromaprint comparison: `0.946403 / same recording`
- source decode: PASS
- target duration fits Lane-P 20–30s typical range: PASS
- no manual crop has been applied to Option A
- no visual work / timeline work started before this Gate

## Listening options

### Option A｜Trend-native exact asset

- duration: `26.423991s`
- transform: `NONE`
- purpose: preserve the exact Douyin-native short music asset first, per BGM discovery rules.

### Option B｜Same asset + soft tail fade

- source: same exact asset as Option A
- structure/cut: unchanged
- transform: only a `1.2s` tail fade starting at approximately `25.224s`
- purpose: test whether the native end feels too abrupt for an MV hold/release.

## User decision｜HG02

Please judge only:
1. whether the opening feels right;
2. whether this is the section we actually want to build the MV around;
3. whether the ending is comfortable;
4. Option A natural end vs Option B soft fade.

PASS condition:
`USER_APPROVES_OPTION_A_OR_B = YES`

After PASS:
- freeze selected BGM bytes/transform/hash;
- set `BGM_LOCKED`;
- build trusted Audio Timeline Package;
- only after timeline QA enter lyric beats / director allocation / first frames.
