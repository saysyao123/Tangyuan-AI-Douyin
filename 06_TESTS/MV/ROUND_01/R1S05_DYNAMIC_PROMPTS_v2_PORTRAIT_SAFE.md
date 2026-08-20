# R1S05 Dynamic Prompts v2｜Portrait-safe image-to-video revision

## Why this revision exists

User QA correction:
- PASSED and kept: `S1 / S2 / S4 / S6`
- needs revision: `S3 / S5 / S7 / S8`
- `S3 / S5 / S7`: Seedance portrait-protection block occurred before generation; keep **image-to-video**, but restore the proven dynamic-wallpaper prompt framing that explicitly classifies the reference as an AI-generated fictional character image rather than a real-person photo.
- `S8`: generation completed, but the moving paper was hallucinated into a torn hole/window revealing the heroine; revise the occlusion mechanism.

## Proven identity framing restored from earlier dynamic-wallpaper workflow

Place this at the very beginning of each blocked image-to-video prompt:

> 人物为AI生成动画人物，无真人出现。当前上传图片是AI生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。当前图片仅用于锁定虚构角色外观、服装、场景、构图和第0秒状态。严格以当前图片作为视频第0秒首帧。

Prompt-language corrections:
- keep `电影级写实质感`, but avoid repeatedly describing the source as `真人摄影 / 真实人脸 / 真人肖像`;
- do not over-emphasize facial biometric details such as exact face shape;
- keep veil / costume / scene continuity as fictional-character attributes;
- retain first-frame character-closure: no new human can appear in a 5s segment;
- restore the previously successful `2–3 shot nodes inside 5 seconds` grammar when appropriate instead of defaulting every segment to one continuous slow push.

---

## S3 / KF05｜我有什么错｜IMAGE-TO-VIDEO RETRY

```text
人物为AI生成动画人物，无真人出现。当前上传图片是AI生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。当前图片仅用于锁定虚构角色外观、服装、面纱、雨夜水面场景、构图和第0秒状态。严格以当前图片作为视频第0秒首帧。

9:16竖版，时长严格5秒。保持当前首帧里的虚构女主、黑色半透明面纱、深墨绿色长衣、旧黯金发簪、雨夜旧宅、水面和倒影完全连续；首帧里只有这一名虚构角色，5秒内绝不新增任何真人或第二角色。倒影始终只是同一AI虚构角色的同步水面镜像，不能变成第二个人。

这段不要一镜到底慢推，采用3个连续镜头节点，镜头之间自然切换，整体动作连续。

镜头1｜0.0–1.4秒｜半近景固定构图：
延续首帧，女主低头看自己的水中倒影，食指停在水面上方约1厘米。细雨在水面留下轻微波纹。人物只保持克制呼吸，面纱和少量发丝有极轻风动。

镜头2｜1.4–2.8秒｜手指与水面的近特写：
自然切到指尖近特写。指尖轻轻触水一次，不用力戳入水中。接触点产生一圈清晰、真实的涟漪。焦点跟着波纹向外扩散，水光和倒影开始被拉开。

镜头3｜2.8–5.0秒｜贴近水面的低机位：
自然切到接近水面的低角度，让水中倒影成为画面主体。涟漪经过倒影中的双眼与面纱，使她自己的镜像短暂被拉伸、打散、错位，但始终明确还是同一虚构角色。约4秒时指尖离水，一滴水重新落下形成第二圈很小的波纹；最后0.6秒只保留倒影缓慢恢复与雨点余韵。

主视觉事件：指尖触水，自己的倒影被涟漪打散。
次级余韵：指尖离水后的水滴 + 倒影缓慢恢复。
镜头语法：固定半近景 → 手部近特写 → 低机位倒影重构；不要常规慢推。

禁止：新增人物、倒影生成陌生脸、倒影独立行动、面纱消失、角色换装、张嘴说话、夸张哭泣、魔法水波、快速推拉、字幕、logo、水印。
声音：禁止AI对白、歌声、旁白、BGM；如必须生成声音，只保留极轻雨声、水面轻响、风声。
```

---

## S5 / KF02｜你有没有真的爱过我｜IMAGE-TO-VIDEO RETRY

```text
人物为AI生成动画人物，无真人出现。当前上传图片是AI生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。当前图片仅用于锁定虚构角色外观、黑色面纱、服装、湿纸、雨夜场景、构图和第0秒状态。严格以当前图片作为视频第0秒首帧。

9:16竖版，时长严格5秒。保持当前首帧中同一个AI虚构女主、黑色半透明面纱、深墨绿色服装、黑发、旧黯金发簪和湿纸完全连续；首帧没有第二人物，5秒内禁止新增任何人。面纱始终完整遮住鼻口与下半脸。

这段是全片情绪中心，但不要做成一张脸5秒慢推。采用3个克制的情绪镜头节点，用手部、眼神和空间完成发问。

镜头1｜0.0–1.3秒｜湿纸与手部插镜：
从首帧延续，先保持人物三分之二近景约0.3秒，随后自然切到她手里被雨水浸软的旧纸边角近特写。手指轻轻收紧，湿纸产生细小褶皱，不撕裂。背景里她的身影保持柔焦。

镜头2｜1.3–3.0秒｜眼部近景：
自然切到面纱上方双眼的近景，不要完整正脸身份证式构图。女主原本微垂的视线先保持短暂停顿，然后缓慢抬起。眼睛有压抑情绪但不流泪；一缕湿发和面纱边缘被轻风带动。摄影机基本稳定，只允许极轻的焦点呼吸，不做明显慢推。

镜头3｜3.0–5.0秒｜三分之二侧正面半近景：
切回比首帧略宽一点的半近景。她把视线停在镜头旁边的空位置，像向一个缺席的人真正问出去。手仍捏着湿纸，但身体不大动。背景雨光轻微流动。最后0.7秒完全停住人物，只让发丝、面纱与雨光保留微余韵。

主视觉事件：由手中湿纸的紧张过渡到双眼真正抬起发问。
次级余韵：湿纸褶皱 + 面纱与发丝微动。
镜头语法：手部插镜 → 眼部近景 → 略宽半近景，采用情绪碎片化剪辑，不做5秒单一慢推。

禁止：新增人物、完整露嘴、面纱掉落、换脸、换装、夸张哭喊、人物突然冲向镜头、镜头环绕、强闪光、纸张撕裂、字幕、logo、水印。
声音：禁止AI对白、歌声、旁白、BGM；只允许极轻雨声、布料声、纸张轻响。
```

---

## S7 / KF07｜落款第几页 / 第几次临摹｜IMAGE-TO-VIDEO RETRY

```text
人物为AI生成动画人物，无真人出现。当前上传图片是AI生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。当前图片仅用于锁定虚构角色的手部、袖口、黑色面纱轮廓、旧毛笔、层叠湿纸、湿木桌面、墨迹、构图和第0秒状态。严格以当前图片作为视频第0秒首帧。

9:16竖版，时长严格5秒。当前首帧中的人物是AI虚构角色，5秒内不新增任何人；人物脸始终只在后景柔焦中保持原有虚构角色轮廓，重点只拍手、笔、纸与墨。不得生成可读汉字、名字、英文、数字或清晰印章文字。

这段不要单一微距一镜到底，采用3个连续细节镜头，让“重复临摹”通过旧痕层层被揭开。

镜头1｜0.0–1.5秒｜笔尖微距：
延续首帧，旧毛笔缓慢完成当前抽象笔划最后一小段。笔尖压过湿纸纤维，新墨边缘真实向外渗开。另一只手继续压住层叠薄纸。

镜头2｜1.5–3.0秒｜侧向层叠纸张近特写：
自然切到纸层侧面与手指近景。毛笔离开画面主体，压纸的手慢慢松开并掀起最上层纸角。摄影机做很短的横向滑动与焦点切换，先看新墨，再穿过半透明上层纸看到下方相似但更淡的旧墨痕和圆形旧印痕；所有痕迹必须不可阅读。

镜头3｜3.0–5.0秒｜新旧痕迹重叠特写：
切到更靠近桌面的斜侧微距。两三层薄纸被轻风带出几毫米错位，半透明纸层短暂重叠，新墨与旧墨在视觉上叠在一起。约4秒时最上层纸缓慢落回一部分，镜头最后停在“新痕覆盖旧痕”的细节，新墨仍在纸纤维里慢慢扩散。

主视觉事件：写完当前一笔后，掀开纸层看见下面重复过的旧痕。
次级余韵：新墨扩散 + 多层湿纸轻微错位并回落。
镜头语法：笔尖微距 → 层叠纸侧面揭示 → 新旧痕迹叠合特写；不用人物脸部慢推。

禁止：生成任何可读文字、真实签名、清晰印章、第二人物、毛笔高速挥舞、纸张飞散、人物脸突然占满画面、魔法墨水、字幕、logo、水印。
声音：禁止AI对白、歌声、旁白、BGM；只允许笔尖摩擦纸面、湿纸轻响、远雨声。
```

---

## S8 / KF08｜还是匆匆一瞥就略过｜IMAGE-TO-VIDEO QUALITY RETRY

Problem in v1: the model treated the moving full sheet as a torn paper window and created a hole that revealed the heroine.

Fix strategy: **do not ask the paper to deform across the whole frame**. Keep the foreground paper physically intact and nearly stationary; move the CAMERA laterally behind its solid edge to create a natural wipe. Once the heroine is occluded, cut to a wet-paper detail shot. This removes the incentive to invent a hole.

```text
人物为AI生成动画人物，无真人出现。当前上传图片是AI生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。当前图片仅用于锁定远处虚构女主背影、完整前景旧纸、长廊、湿地、冷雾、灯光、构图和第0秒状态。严格以当前图片作为视频第0秒首帧。

9:16竖版，时长严格5秒。保持远处同一个AI虚构女主、深墨绿色长衣、黑发、旧黯金发簪、长廊、湿地、冷雾和前景巨大旧纸完全连续；首帧只有这一名角色，禁止新增任何人物。

最重要的物理规则：前景旧纸在整个视频中必须始终是一整张完整连续的纸面。绝对禁止破洞、撕裂、烧穿、裂口、镂空、窗洞、透明洞口。不要让人物从纸上的任何孔洞中出现。

这次不要让纸页大幅翻卷穿过镜头。采用“完整纸页固定前景 + 摄影机横移到纸后完成自然遮挡 + 遮挡后切纸面细节”的两镜结构。

镜头1｜0.0–3.2秒｜横向遮挡式运镜：
延续首帧。前景巨大湿纸只做很小的风动和边缘轻颤，整体形状保持完整稳定，不翻卷、不拉伸、不变形。远处女主背向镜头，只向前走一小步，绝不回头。摄影机本身缓慢向右横移，让完整纸页的实体边缘从画面上方/右侧逐渐进入更多区域，像摄影机移动到一堵柔软的前景屏风后面一样，持续遮住远处人物。人物只能在纸页“边缘以外”的空间被看见，绝不能通过纸面内部看到。

镜头1末尾：到约3.2秒时，完整纸页的实体边缘已经把女主完全挡住。遮挡来自摄影机位置变化，不来自纸张开洞或撕裂。

镜头2｜3.2–5.0秒｜湿纸纹理近特写：
利用完整遮挡做自然切镜，切到同一张湿纸表面的极近特写。只看到旧纸纤维、抽象墨痕、水珠、微弱冷色反光；不再出现人物。风势逐渐减弱，纸面只保留很小的呼吸式起伏。最后0.6秒几乎静止，方便接音频淡出或黑场。

主视觉事件：摄影机横向移到完整纸页后方，人物被完整前景自然遮住。
次级余韵：遮挡后切到湿纸纹理，风和水珠运动逐渐衰减。
镜头语法：横向遮挡式运镜 → 完整遮挡匹配切镜 → 湿纸极近特写；不是一镜到底，也不追人物。

严禁：纸张破洞、纸张撕裂、镂空、人物从洞里露出、女主回头、人物凭空消失、第二人物、纸张变成碎片或鸟、强风卷纸、镜头360度旋转、暖色日出、字幕、logo、水印。
声音：禁止AI对白、歌声、旁白、BGM；只允许极轻风翻纸声、远雨声、极轻脚步和衣料声。
```

## Current retry set

Retry only:
1. `S3 / KF05` — image-to-video with restored AI-character declaration + 3-shot reflection grammar.
2. `S5 / KF02` — image-to-video with restored AI-character declaration + 3-shot emotional fragments.
3. `S7 / KF07` — image-to-video with restored AI-character declaration + 3-shot macro grammar.
4. `S8 / KF08` — image-to-video with camera-based solid-paper occlusion instead of paper deformation.

Keep current successful outputs unchanged:
- `S1 / KF01`
- `S2 / KF04`
- `S4 / KF06`
- `S6 / KF03`
