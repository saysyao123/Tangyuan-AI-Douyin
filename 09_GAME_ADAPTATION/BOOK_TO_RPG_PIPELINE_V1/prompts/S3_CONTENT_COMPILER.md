# S3/S4 游戏数据与资源生成提示

输入 S2 beat_graph 和角色表，生成游戏JSON、资产需求清单和引用索引；不要直接更改游戏引擎源码。每个实体/场景/物品/事件/怪物/结局使用稳定ID；重要行为的反馈应写入事件effects，资源需要路径与来源状态。先以原创最小故事运行 `node tools/pipeline.mjs validate`；再构建可玩HTML和测试日志。若要升级Type PAL，必须先根据其官方content22 schema制作单独adapter并通过官方引擎实机回归，不得混用本项目的示例JSON。
