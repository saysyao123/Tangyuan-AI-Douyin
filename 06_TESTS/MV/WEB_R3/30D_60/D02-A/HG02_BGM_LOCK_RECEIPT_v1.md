# D02-A｜HG02 BGM Lock Receipt v1

Status: `HG02_PASS / BGM_LOCKED`
Slot: `D02-A`
Lane: `P`
Song family: `做她的大地别做她的天`

## User decision

User explicitly selected **Option B** at HG02 because the tail fade is more comfortable.

## Locked audio

- Source family: `DOUYIN_NATIVE / 做她的大地别做她的天（r&b）（氛围片段） / 大眼仔`
- Source asset content identity: `EXACT_ASSET_CONTENT_IDENTITY_CONFIRMED`
- Source direct-asset SHA256: `b5c951cfd1a5d1ab8cf67c093ca0ab1242e9a9be116785588074d768eba9621d`
- Source decoded duration: `26.423991s`
- Selected transform: `tail fade only`
- Fade start on source-content timeline: `25.223991s`
- Fade duration: `1.2s`
- Structural trim: `NONE`
- Selected listening/locked file: `D02-A_HG02_B_尾部1.2s柔和淡出_26.424s.mp3`
- Locked rendered-file SHA256: `2e7d74c6abbee709bb94bf337684ee742c79c9532228b6b487e1facbb870446e`
- Locked rendered container duration: `26.462041s` (MP3 encoder padding included; musical content remains the 26.423991s source asset)
- Sample rate: `44100 Hz`
- Channels: `2`

## Consequence

`BGM_LOCKED = YES`.

From this point forward:
- do not change song family;
- do not change recording/version;
- do not alter start point;
- do not alter fade unless HG02 is explicitly reopened by the user;
- all lyric timing, beat mapping, directing, subtitles and picture edit must reference this locked BGM identity.

Next machine stage:
`Trusted Audio Timeline Package -> alignment QA -> Natural Beat / Director planning`.

No additional human gate is required unless alignment evidence conflicts strongly enough to trigger CHG-A.
