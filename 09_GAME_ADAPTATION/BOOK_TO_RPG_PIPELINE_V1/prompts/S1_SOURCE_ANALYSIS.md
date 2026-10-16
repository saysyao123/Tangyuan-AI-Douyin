# S1 小说事实抽取提示（可直接复制给GPT）

读取用户提供且允许使用的全部章节/文件；若太长则按章节分块，不跳读结局或时间线。输出可检索的 fact_ledger.json、chapter_index.json、timeline.json、characters.json、locations.json，每条事实给 chapter_id 和精确到场景/短引文位置的 source_ref。明确 source_fact / reasonable_inference / game_adaptation 三类；矛盾事实进入 unresolved，不得自动取舍。

抽取角色身份、欲望、关系变化、入场/退场、地点、道具、线索、战斗、转折、因果顺序，并标识可操作章节候选。不要在这一阶段制作游戏地图或私自改原著剧情；只有证据门禁通过后才进入 S2。
