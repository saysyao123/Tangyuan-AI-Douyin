# D03-A｜HG02 BGM Excerpt Listening Gate v1

Status: `READY FOR HUMAN REVIEW`
Song family: `爱让人脑袋空空`
Upstream: `HG01 PASS / S01_HG01_SONG_LOCKED`
Discovery route: `P1_VERIFIED_DOUYIN_WORKS / DIRECT_MUSIC_ASSET_FIRST`

## 1. Machine result

Two independent core-account Douyin works were resolved through the existing Douyin-first asset path:

### Option A｜火乐烁 direct music asset
- aweme: `7673830659274810033`
- displayed music: `@火乐烁创作的原声`
- duration: `31.477542s`
- sample rate: `44.1kHz`
- channels: `2`
- bitrate: `192kbps`
- SHA-256: `06002970e402cf2b7d0e200fc026e5c2b54b771441f8186dfed190ea7a154917`

### Option B｜乐青春 work / 乐乐动画 direct music asset
- aweme: `7672476381650263962`
- displayed music: `@乐乐动画创作的原声`
- duration: `31.921625s`
- sample rate: `44.1kHz`
- channels: `2`
- bitrate: `192kbps`
- SHA-256: `f298e1c7d99fe3cba9a2beed2fc6ecab406f946a3427895e5aad1aa4dfdf4769`

## 2. Acoustic comparison

Direct-asset Chromaprint comparison:
- similarity: `0.992623`
- best shift: `0`
- overlap: `233`

Interpretation:
- these are acoustically near-identical recordings from the same starting point;
- they are still separate asset bytes/hashes and have a ~`0.444s` duration difference;
- therefore HG02 keeps A/B separate rather than silently treating them as one immutable asset.

Canonical provenance:
`BGM_DISCOVERY/asset_probe_report.json`

## 3. Machine QA completed before HG02

- direct Douyin music assets successfully resolved: `2/2`;
- no generic full-track substitution used;
- both files decode successfully;
- both are 44.1kHz stereo MP3 at 192kbps;
- direct-asset fingerprint comparison completed;
- no second lyric timeline has been created;
- HG01 remains locked and was not reopened after the first probe failure;
- video CDN 403 was patched at nearest cause by making video a fallback rather than a prerequisite.

## 4. Human decision｜HG02

User only judges listening comfort:
1. which opening feels cleaner/more natural;
2. which ending/release feels more complete;
3. whether either option has an audible cut/contamination that makes it unsuitable.

If both sound effectively identical, prefer the one whose ending feels more natural; machine evidence alone does not choose the aesthetic winner.

PASS requires explicit selection of `A` or `B` (or an explicit statement that one exact asset should be locked).

After PASS:
- record HG02 durable receipt;
- lock the selected BGM identity/hash;
- advance to `S02_HG02_BGM_LOCKED`;
- immediately enter the Lean Audio Timeline priority router (`P0 -> P1 -> P2 only on failure`).
