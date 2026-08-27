# D02-B｜WEB Source Rough-Cut QA v1

Status: `WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`

- Raw sources preserved unchanged.
- S1/S3/S4 use the previously validated R2 1.25x center-crop watermark-safe geometry: `crop=576:1024:72:128 -> scale=720:1280`.
- Current uploaded S2 file reports `720x960 / 3:4`; it is normalized without stretching using a centered 9:16 crop, then the same prior safe-crop concept is applied: `crop=432:768:144:96 -> scale=720:1280`.
- All proxies: `720x1280 / 24fps / SAR 1:1`, source audio removed.
- Representative proxy frames checked after render: no visible `豆包AI生成` corner mark remains.
- Composition remains usable in all four proxies; S2 is tighter than the others but does not cut the head, core gesture, or boundary-column relationship.
- No regeneration requested for geometry alone.

Proxy SHA256 identities from this run:
- S1 `078f72758eb1d3522b29210c54758f7c04e246c686a01a5b9df52e845b609794`
- S2 `61a46b2ce27d3a420e5cb173bd7d4285f3d935f8334c29b871a37413da4db7b7`
- S3 `2868498eea7802b36f64acd6a5a12c91899a106de2731168b1e86a95fe8fdef0`
- S4 `12d36eee5938113402e8bbbb5fccdf663e585ff1f72ea22fe3ef2e95daeac8bd`
