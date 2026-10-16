# 仙剑98机制基线：源码已核与下一步缺口

状态标签：
- A=用户上传包字节静态核实
- B=SDLPAL代码存在（不等于此特定原程序行为一致）
- C=Type PAL仓库自述、代码与 schema
- D=设计抽象/待实测

| 模块 | 学到且优先保留的规则 | 证据 |
|---|---|---|
| 明雷敌人 | 原作地图中可见敌人，玩家可避让或接触进入战斗，不默认替换为随机暗雷 | Steam社区版本差异资料；B script.c/play.c NPC追逐和碰触机制（本包待运行确认） |
| 世界场景 | 斜视角场景、瓦片和遮挡、地图/进出场景、碰撞检查 | B map.c,scene.c,global.h SCENE |
| 玩家操作 | 方向移动与NPC交互、位置触发、角色跟随 | B play.c,scene.c |
| NPC | triggerScript和autoScript、朝向和动画帧、出现/消失与脚本绑定 | B global.h EVENTOBJECT,script.c |
| 剧情 | 操作码+3操作数的8字节脚本记录，触发/自动脚本双通路、对话与过场 | B global.h SCRIPTENTRY, script.c,text.c,ending.c |
| 角色 | 姓名/头像/地图精灵/战斗精灵/音效，等级HP/MP，攻击/魔力/防御/身法等 | B global.h PLAYERROLES |
| 队伍 | 战斗同时最多三名；剧情改变队伍，地图跟随 | B palcommon.h MAX_PLAYERS_IN_PARTY=3,script.c |
| 装备 | 六装备槽位与相关战斗状态影响 | B palcommon.h MAX_PLAYER_EQUIPMENTS=6,global.c |
| 技能/魔法 | 单体/全体/战场特效/恢复/变身/召唤、MP消耗、学习表 | B global.h MAGIC_TYPE, global.c |
| 五灵/异常 | 五系抗性、毒、混乱、睡眠、沉默、强化等 | B global.h STATUS/NUM_MAGIC_ELEMENTAL, fight.c |
| 战斗 | 经典命令 Attack/Magic/Co-op/Misc，使用/投掷道具、守备、逃跑 | B uibattle.h, fight.c,battle.c |
| 行动模式 | SDLPAL有 PAL_CLASSIC 分支，须针对98柔情版实测选用正确行动队列，不得直接套新式ATB | B fight.c |
| 伤害/敌人 | 物理/法术单独公式，敌人有攻击、魔力、速度、概率、双行动等 | B fight.c PAL_Calc*Damage;global.h ENEMY |
| 奖励/经济 | 战胜获经验与钱；装备、背包、商店、卖物 | B battle.c,global.h INVENTORY/STORE,script.c |
| UI | 状态、仙术、物品、系统四大菜单及战斗界面状态 | B uigame.c,uibattle.h |
| 保存 | 主角与世界状态可保存/恢复，原代码区分Win/DOS存档路径 | B global.c |
| 表现 | 320×200底图，像素精灵、配色，RNG/AVI、音乐音效、过场与结局 | B scene.c,battle.c,rngplay.c,aviplay.c,ending.c |

### 额外只读用户包结构观察（A）
- Sss.mkf chunk长度: 162464/2360/7910/54056/348456 B。
- scene段 2360 / 8=295 个记录；SCRIPTENTRY段 348456 / 8=43557 个记录。
- Map.mkf 和 Gop.mkf 各226块，223块非空。
- 数据规模≠完整理解：事件 opcode 分类与跳转、角色技能数值、各关卡地图连接、战场环境效果、全部主线序列及本包运行均仍需验证。

### 锁定源代码
- https://github.com/sdlpal/sdlpal/blob/f6236a0d0839b1cc8918e2abc54017e223938f1d/global.h
- https://github.com/sdlpal/sdlpal/blob/f6236a0d0839b1cc8918e2abc54017e223938f1d/scene.c
- https://github.com/sdlpal/sdlpal/blob/f6236a0d0839b1cc8918e2abc54017e223938f1d/script.c
- https://github.com/sdlpal/sdlpal/blob/f6236a0d0839b1cc8918e2abc54017e223938f1d/fight.c
- https://github.com/sdlpal/sdlpal/blob/f6236a0d0839b1cc8918e2abc54017e223938f1d/uigame.c

以上是“有实现锚点的机制目录”，不是“完整剧情和全机制已100%反编译”的声明。
