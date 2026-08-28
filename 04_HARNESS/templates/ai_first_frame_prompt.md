# Template｜AI First Frame Prompt v2

> This template is structural only. Before generation, the final prompt MUST comply with `04_HARNESS/rules/mv_first_frame_prompt_optimization.md` and the locked Director Plan.
>
> Do not send the placeholders or raw Director prose directly to the image model. Convert them into one complete generation-ready cinematic instruction.

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

【LYRIC VISUAL HIT / Narrative Role】
当前歌词/Beat：{LYRIC_OR_BEAT}
这张图不可替代的视觉命中：{LYRIC_SPECIFIC_VISUAL_ANSWER}

【K0 PERFORMANCE STATE】
0秒必须清楚看到：{BODY_ORIENTATION_WEIGHT_HANDS_GAZE_CURRENT_ACTION_PHASE}

【CHARACTER PHYSIOLOGY / IDENTITY LOCK】
{AGE_BUILD_BODY_PROPORTION_HEAD_FACE_STRUCTURE_HAIR_STABLE_IDENTITY_CUES_NO_CELEBRITY_LIKENESS}

【FACE PRIVACY / COMPLETION GRID｜CURRENT WEB/SEEDANCE PATH】
人物可见面部特征区域采用标准二维正交黑色方格：笔直水平线 + 垂直线形成规则方格，高对比、密集、平面化；不是贴合脸部轮廓的3D网格，不是像素马赛克、模糊、黑条、整块黑面罩、头盔或随机涂抹。头发、头型、耳朵/下颌线（可见时）、身体、服装、光线和环境保持完整高清。若自然机位本来就看不清脸，不要为了展示方格强行生成正脸。

【SKIN / HUMAN REALISM】
{VISIBLE_SKIN_MICROTEXTURE_NATURAL_TONAL_VARIATION_MOISTURE_SPECULAR_BEHAVIOR_NO_PLASTIC_CGI}

【WARDROBE MATERIAL】
{GARMENT_CUT_FIBER_WEIGHT_SEAMS_FOLDS_DRAPE_HUMIDITY_WIND_RESPONSE_CONTINUITY}

【PRIMARY VISUAL EVENT】
画面唯一主事件：{DOMINANT_EVENT}

【ACTION ENTRANCE / STATIC BASE / MOTION SPACE / RESIDUE】
下一秒自然继续：{ACTION_ENTRANCE}
必须保持稳定不动：{STATIC_BASE}
为动作保留的空间：{AVAILABLE_MOTION_SPACE}
动作结束后可持续余韵：{PHYSICAL_RESIDUE}
可稳定收束的终态：{SETTLED_END}

【CAMERA OPTICS / COMPOSITION】
{SHOT_SCALE_FOCAL_LANGUAGE_CAMERA_HEIGHT_ANGLE_PERSPECTIVE_PURPOSE_DOF_FOREGROUND_MIDGROUND_BACKGROUND_NEGATIVE_SPACE}

【LIGHTING PHYSICS】
{LIGHT_SOURCE_DIRECTION_SOFTNESS_HIGHLIGHT_SHADOW_EXPOSURE_REFLECTION_LOGIC}

【ENVIRONMENT / MATERIAL DEPTH】
{WORLD_CONTINUITY_FOREGROUND_MIDGROUND_BACKGROUND_MATERIAL_HIERARCHY_PHYSICAL_STATE}

【QUALITY / NEGATIVE GUARD】
人物解剖、双手、镜面/水面反射、建筑几何必须真实一致；不要额外人物或把倒影生成第二人；不要随机新增道具；不要商业模特摆拍；不要塑料CG皮肤；不要低清、过曝、严重磨皮；不要文字/UI/品牌；不要让多个主事件同时抢焦；不要裁断关键动作空间；不要用“masterpiece/8K”等形容词替代真实镜头、材质和光照描述。
```

## Required pre-generation check

A prompt is not production-ready unless it resolves all applicable items:

`OUTPUT CONTRACT + LYRIC HIT + K0 PERFORMANCE + CHARACTER PHYSIOLOGY + SKIN REALISM + WARDROBE MATERIAL + CAMERA OPTICS + LIGHTING PHYSICS + ENVIRONMENT DEPTH + ACTION/RESIDUE + QUALITY/NEGATIVE + FACE GRID`.
