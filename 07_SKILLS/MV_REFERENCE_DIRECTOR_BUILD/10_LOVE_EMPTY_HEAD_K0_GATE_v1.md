# 《爱让人脑袋空空》｜K0 Gate v1

> Upstream Director: `08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v3_LOCKED.md`
> K0 Spec: `09_LOVE_EMPTY_HEAD_K0_SPEC_v1.md`
> Status: `K0_GATE_PASSED / GENERATION_NOT_YET_VALIDATED`

## 1. K0 role

K0 = `first-shot anchor + persistent asset contract`。

本轮已经实际生成 K0-A / K0-B，并由用户在当前对话中查看后确认继续进入下一阶段。

## 2. K0-A

- Role: Segment A first-shot anchor / persistent asset declaration.
- Establishes: same original female adventurer, red-orange short cloak, readable legs/ground, highland-lake world, small blue-white wind spirit, sunset/wind direction.
- Visual function: supports later close-up / wide / follow / detail shots without requiring new core assets.
- Conversation generation artifact: `/mnt/data/a_highly_detailed_anime_style_illustration_a_lone.png` (conversation-local evidence, not repository binary asset).

## 3. K0-B

- Role: Segment B hard-cut restart / same persistent asset declaration.
- Establishes: same character/world/wind spirit and motion-capable terrain; allows a new camera sentence for B.
- Visual function: supports close facial peak, hand detail, environment takeover, and final wide ending using already established assets.
- Conversation generation artifact: `/mnt/data/a_wide_cinematic_anime_ghibli_style_fantasy_land.png` (conversation-local evidence, not repository binary asset).

## 4. Gate result

PASS for current project.

Accepted constraints:

- no extra protagonist / crowd / new large creature / new large prop system;
- later richness comes from shot language, action, framing, camera and environment motion;
- local close-ups must derive from established character/world assets;
- K0 does not imply one-take; each generated clip remains multi-shot.

## 5. Next stage

Enter `Phase I｜Multi-shot Dynamic Prompt`.

Compile:

- Segment A: Generation 12s, core maps to BGM 0.000–8.700s;
- Segment B: Generation 10s, core maps to BGM 8.700–15.370998s;
- explicit `Shot / time / CUT` structure;
- lyric/beat alignment;
- character movement + camera movement + environment movement;
- physical footwork / no sliding;
- post-handle residue;
- no asset-count inflation.

K0 is not yet promoted as a general Skill rule; real Seedance generation and cross-project validation are still required.