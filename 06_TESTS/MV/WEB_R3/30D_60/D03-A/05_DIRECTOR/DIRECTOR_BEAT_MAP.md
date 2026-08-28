# D03-A｜Director Beat Map v1

Status: `READY_FOR_S05`
Song: `爱让人脑袋空空`
Timing authority: `03_AUDIO_TIMELINE/line_timeline.csv`
Natural Beat authority: `04_BEATS/NATURAL_BEAT.md`

## Director Thesis

在一个**盛夏临近闭馆的现代主义室内游泳馆**里，一个人不断在水、玻璃和镜面里追到自己的倒影；外面的夏天始终灼亮，馆内却随歌词逐段关灯、降温、变空，直到他亲手盖住最后一面还能映出自己的镜子。

## Primary Visual Engine

`REFLECTION -> DISPLACEMENT -> EXTINCTION`

倒影不是装饰，而是“还认不认得自己”的持续视觉机制：
1. 开场还能直视并试图修补；
2. 受伤时倒影被水纹/红泳道切开；
3. 承诺消失时倒影被风和水汽扰散；
4. 失控时人物与镜面关系不断错位；
5. 真相出现时属于他的灯熄灭，而另一处成对暖光仍在；
6. 结尾他主动覆盖镜面，终止自己的倒影。

Secondary engine: `SUMMER OUTSIDE / WINTER INSIDE`。暖黄玻璃砖、日晒白光和湿热空气始终证明“盛夏”真实存在；冷青只在馆内逐步增加，不做突然换世界。

## Production allocation

8 Natural Beats 不机械等于 8 个首帧。正式生产压成 **6 个 production segments**，目标约 6 条 5s 级 raw sources，后续通过 atom/arc 剪辑覆盖 31.921625s。

| Seg | Time responsibility | Natural Beats / lyrics | Audiovisual relationship | Dominant visual event | Camera-subject-space relation | Final edit role | WHY CUT HERE |
|---|---:|---|---|---|---|---|---|
| P01 | 0.841–4.983 | NB01 / L01-L02 | spatial metaphor + direct title hit | 男主在空更衣室镜前撕下贴在裂纹上的透明防水修补膜；镜里只剩他和成排空柜 | `HOLD -> mild DOLLY-IN`; intimate medium, mirror gives depth | HOOK | L02“脑袋空空”落下时，从狭窄镜面心理空间切到巨大泳池空间，完成“空”的尺度升级 |
| P02 | 4.983–8.686 | NB02 / L03-L04 | direct hit + kinetic answer | 俯视浅蓝水面，他胸口位置的倒影被一个扩开的圆形水纹切开，水纹下方正好掠过一条深红泳道线；随后本人沿湿池边快速走开 | `OVERHEAD REVEAL -> SIDE FOLLOW`; subject travel carries urgency | HIT / BRIDGE | “见了红”完成后动作方向建立；切在他真正加速离开的一步，进入下一段关系回忆 |
| P03 | 8.686–15.631 | NB03-NB04 / L05-L07 | emotional echo -> physical release | 暖光池畔，一条很细的白色无字腕带/系带系在金属扶手上；他先轻压住它，玻璃水汽在他的倒影上形成泪痕感，通风气流最终把系带从指间拉走 | `SIDE HOLD + short YIELD`; hand/ribbon one fragile anchor only | RISE -> RELEASE-1 | 系带真正脱手、越过画面边缘就是“承诺无影无踪”的物理完成点，之后不再追它 |
| P04 | 15.631–19.753 | NB05 / L08-L09 | subjective pressure / spatial metaphor | 长更衣通道内，男主持续向前走；相机从后侧追随、加速超过他，再在前侧领拍，前景挂着的湿毛巾短暂遮挡镜头，人物始终没有真正走出这条重复空间 | `FOLLOW -> OVERTAKE -> LEAD`, translational, not orbit | PEAK-A | 相机完成超越后，他却仍被相同柜门包围；在“心事重重”落点切到静态远景，让失控突然变成事实 |
| P05 | 19.753–23.436 | NB06 / L10-L11 | environmental reveal, no literal second actors | 泳池大厅远景，他所在一侧的顶灯/水下灯熄灭；隔着整池的另一侧，两盏相邻暖灯与两张靠近的空躺椅仍亮着，人物只在冷暗一侧看过去 | `DISCOVER / slow LATERAL REVEAL`; protagonist small, architecture carries meaning | PEAK-B / REVEAL | “和她情意浓浓”不出现第二真人；切点放在成对暖光被完整揭示后，进入冷热反转句 |
| P06 | 23.436–31.922 | NB07-NB08 / L12-L14 + tail | counterpoint -> identity extinction | 更衣室尽头的玻璃砖外仍是强烈金色盛夏；馆内已转冷青。男主站在全身镜前，亲手把一条干净白浴巾从镜顶缓慢放下，直到自己的倒影完全消失；随后相机沿柜道后退，让他和被覆盖的镜子越来越小 | `HOLD -> WORLD-OPENING RETREAT`; full/wide endpoint, summer stays visible | CONTRAST -> FINAL RELEASE | 不再切出新信息；29.780s歌词结束后保留镜面已被覆盖、夏光仍存在的余韵直到 31.922s |

## Shot-scale differentiation

`P01 intimate medium / P02 overhead-wide + travel / P03 medium side / P04 moving medium-wide / P05 architectural wide / P06 full-to-wide retreat`

No all-close-up sequence. No repeated centered portrait template.

## Character / world lock

- One fictional East Asian adult male protagonist, attractive but natural rather than fashion-ad posing.
- Same identity, short dark hair with slightly damp texture, clean understated styling.
- Wardrobe: off-white lightweight short-sleeve knit or thin shirt + charcoal loose trousers; progressively damp but no wardrobe change.
- No visible branded sportswear, text, logos, pool signage or readable numbers.
- Main world materials: pale aqua ceramic tile, stainless steel, amber glass brick, wet concrete, clear water, warm summer daylight, cool interior fluorescents/underwater light.
- No beach, no seaside architecture, no pale-stone resort, no rain-after exterior, no D02-B linen-curtain vocabulary.

## Optional-element controls

| Element | Trigger | Function | Allowed range | Stop condition |
|---|---|---|---|---|
| water ripple | P02 one small disturbance | cut reflection + reveal red lane | one expanding ring family | once red line is readable; no ongoing magical water behavior |
| white wristband/tie | P03 ventilation gust | promise made physical then released | one thin unbranded strip | exits frame; never returns in later segments |
| condensation | P03 warm pool glass | tear-like emotional echo | sparse vertical trails | stays background; never becomes literal rain |
| hanging towels | P04 camera passage | foreground depth / pressure | 1-2 brief occlusions | stop after camera overtakes subject |
| lights | P05-P06 | relationship truth + inner cooling | simple off/on state only | no flicker, no strobe, no color cycling |

## Creative Drift QA checkpoints

At `Director -> K0 -> Dynamic Prompt -> Generated Source` verify:
- reflection function is still readable, not just decorative mirror beauty;
- red in P02 comes from pool lane/environment, never injury/blood;
- P03 contains only one fragile hand/tie interaction;
- P04 actually translates `FOLLOW -> OVERTAKE -> LEAD`, not an orbit/reframe;
- P05 never invents a second/third human to literalize “她”;
- P06 covering the mirror remains the dominant event and the summer exterior stays visibly warm.

Accepted actual first-frame pixels will outrank this prose if HG03 accepts a useful deviation.
