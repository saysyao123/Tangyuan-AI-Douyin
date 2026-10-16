# S4官方Type PAL canonical编译器任务

读取现有 S1原著账本、S2游戏节拍、S3授权素材，**不得**仅凭V1游戏 `terrain` 数组或map name伪造完成。
固定 Type PAL commit f98d0ddd89ebdee7b04502ee35de26ee82c6d246、content22/SAVE12。输出内容工程规范根目录：
- `manifest.json`：完整entryPoints，startWorld，不重复当前HP/MP之外的静态角色定义
- `content/scenes/index.json` 及每个场景正文
- `content/maps/index.json` 及真正 ProjectMap v4
- `content/actors.json`, `items.json`, `skills.json`, `locale.json`、battle与NPC脚本条目
- `assets/index.json` 和真正的原创瓦片、头像、人物精灵、战斗资源文件（或合法占位）
然后调用上游 `@type-pal/content` 的当前校验与 `@type-pal/editor check:project`，依序输出负例测试记录，做到零遗失路径/引用、零非法版本/超目录资源；再运行真正的Reforge交互回归。
制作后若用户通过网页编辑器改动工程，之后AI再次生成应先对作者改动做显式合并而非直接覆盖。
失败就写STATUS=BLOCKED，不得拿 Type PAL第一阶段Pal游戏的可通关成绩充当此新书通过证据。
