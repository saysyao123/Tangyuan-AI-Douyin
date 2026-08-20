# Rules｜Production Core v1.0

> 权威范围：已经被生产过程验证的跨模块硬规则。

1. **Audio Before Final Timing**：未锁最终旁白音频前，导演秒数只能是 `DRAFT_TIMING`。
2. **Independent ASR**：录音可能偏离原稿时必须 `Audio → ASR → Transcript Confirm → Cleanup`，禁止旧稿诱导听写。
3. **One Master Narration**：最终成片只保留一个Master Narration Track；AI视频源音轨默认移除。
4. **Multi-session Match**：多场录音匹配响度、动态、轻微音色差，不改变真实音高/声线。
5. **HD Source for Zoom**：高清Source负责放大；低清Motion只负责运动。
6. **Directed Motion**：镜头运动必须有起点、单一主方向、终点；默认禁止随机漂移、呼吸Zoom、左右摇摆、无意义浮动。
7. **Segment Lock**：`Produce → QA → Approve → Lock`；已批准段落不因其他局部问题随意重做。
8. **Generated != Done**：Technical / Visual / Narrative / Evidence QA 全部通过才允许交付。
9. **Exact Data Outside Generative AI**：准确数字、DAY编号、平台文字不交给生成模型伪造。
10. **Artifact Verify**：输出文件宣称完成前必须 `exists → probe → QA → deliver`。
11. **Material Coverage**：`MISSING / ASSUMED` 不得进入最终Director Lock。
12. **Evidence Integrity**：程序化/AI示意不得冒充真实平台、真实截图、真实结果。

任何新增生产硬规则必须通过 `knowledge/PROMOTION_POLICY.md` 的 PRODUCTION_VALIDATED 门槛。
