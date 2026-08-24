# WEB R3｜Camera Calibration Matrix v1

Status: `EXPERIMENTAL / R3-B`
Song: `如果风会替我说话`
Model target: `Seedance 2 mini`
Source duration: `5s each`

## Goal
R3 不把“导演能力升级”等同于增加镜头数量，而是验证一组可复用、可稳定执行、与歌词语义一致的摄影机运动。

每个5秒源素材：
- 只允许一个主摄影机运动；
- 人物/环境事件仍只有一个主事件；
- 运镜必须服务歌词与情绪；
- 结束时必须有 clean endpoint；
- 先稳定，再复杂；
- 不为了炫技机械运镜。

## Calibration Matrix

| Seg | Lyric role | Primary camera grammar | Motion budget | Risk | Director reason |
|---|---|---|---|---|---|
| S01 | HOOK / wind speaks | MICRO DOLLY-IN | framing enlargement <= 5% | LOW-MED | 风把未说的话推近观众，但不变成人像广告式推脸 |
| S02 | rain answers | LATERAL SLIDER PARALLEL TO GLASS | 8–15cm-equivalent | LOW-MED | 利用雨滴/玻璃/人物三层视差，让“回答”发生在空间里 |
| S03 | memory / absence | SLOW DOLLY-OUT REVEAL | framing reduction 8–12% | LOW-MED | 从人物退开，逐渐让空椅/空门成为“他”的缺席 |
| S04 | home / hold | FOREGROUND OCCLUSION SLIDE / REVEAL | 10–20cm-equivalent lateral | MED | 借门框完整前景遮挡与横移揭示走廊和远端暖光，强化“路出现了” |
| S05 | dream / ambiguity | MINI ARC / ORBIT AROUND MIRROR AXIS | 6–10 degrees only | MED-HIGH | 用小弧线改变实体与倒影重合关系，物理表达真假偏移 |
| S06 | healing / MMP-01 | LOCKED-OFF PERFORMANCE SHOT | none | LOW | 微表演、手与面纱受力优先；此段故意不运镜，作为稳定对照组 |
| S07 | imperfect us | DIAGONAL SLIDER + RACK FOCUS | 8–15cm-equivalent | MED | 前景两个风物产生视差，焦点从物体回到人物，让“我们”先于“我”被看到 |
| S08 | release | SLOW CRANE-RETREAT | retreat <= 12%, rise small | MED-HIGH | 镜头后撤并轻升，让世界逐渐大于人物，完成真正的情绪释放 |

## Stability constraints

### LOW / LOW-MED
可直接作为当前生成首选：
- micro dolly-in / dolly-out；
- 单轴 lateral slider；
- rack focus；
- locked-off。

### MED
必须限制位移：
- foreground reveal；
- diagonal slider；
- small parallax move。

### MED-HIGH
只做小幅度能力测试：
- mini arc / orbit；
- crane-retreat compound move。

若模型出现身份漂移、镜像错脸、空间拓扑重建、镜头突然加速，立即判为 `CAMERA_GRAMMAR_FAIL`，不通过增加提示词复杂度强救；回退到最近一级稳定摄影语法。

## Evaluation after generation
每条素材记录：
1. CAMERA_EXECUTION: PASS / PARTIAL / FAIL
2. IDENTITY_STABILITY: PASS / FAIL
3. VEIL_STABILITY: PASS / FAIL
4. SPACE_TOPOLOGY: PASS / FAIL
5. LYRIC_FIT: 1–5
6. EDITABILITY: 1–5
7. CLEAN_ENDPOINT: YES / NO
8. REUSABLE_CAMERA_GRAMMAR: YES / NO

## Promotion policy
R3 一次成功只标记 `POSITIVE_EVIDENCE`。
只有跨至少两种不同场景/歌曲仍稳定，才允许晋升到长期 `MV Camera Library` 或 `04_HARNESS` runtime rule。
