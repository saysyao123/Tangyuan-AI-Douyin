# 当前 run 的 S0/S1 修复实现

先看 `REPAIR_REPORT_2026-09-30.md`，正式执行状态以父目录 `RUN_CURRENT_STATE.yaml` 为准。

在 run 根目录运行（只依赖 Python 标准库）：

```sh
python validate_fresh_run.py
python -m unittest discover -s s0_s1_repair -p 'test_*.py' -v
```

第一条命令也会运行回归检查。PASS 表示当前状态一致、回归通过；不是歌曲、音频或 S1 封存 PASS。GitHub 现有 `Fresh S0 S1 Validator` workflow 通过本轮 `VALIDATE_TRIGGER.txt` 变更执行同一入口。

复现真实来源测试需要网络、ffmpeg/ffprobe，以及公开 SenseVoice 模型。以下适配器专门针对已确认的补充测试曲《一个人在家》，不是所有平台的通用抓取器：

```sh
python s0_s1_repair/acquire_validation_source.py
python -m pip install sherpa-onnx==1.13.8 numpy soundfile opencc-python-reimplemented
python s0_s1_repair/scan_validation_source.py --model-dir /absolute/path/to/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17
python s0_s1_repair/run_validation.py --media s0_s1_repair/validation_full.mp3
```

模型应来自 [k2-fsa/sherpa-onnx 的官方预训练模型](https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models)，目录内包含 `model.int8.onnx` 和 `tokens.txt`。脚本在其自身目录生成临时完整音频、歌词和原始识别稿；这些不提交仓库。

`DIRECTION_INPUT.json` 来源于本轮已复核的历史核心队列；`trusted_pool.csv` 和 `trusted_used_ledger.csv` 为这次读取的仓库历史快照，不能冒充实时来源。新方向须重新提供真实 provenance、中文内容依据和当前历史策略，调用 `rank_directions`；新实际来源须使用新的身份验证和媒体报告。当前 `run_validation.py` 的固定身份只用于本次测试源，不应改标题后复用旧哈希或识别证据。

缺失或更改媒体时，真实验证脚本会非零退出；不退化成静默回放旧 PASS。补充测试结果不自动回填正式选歌、S1 封存或 S2 放行。
