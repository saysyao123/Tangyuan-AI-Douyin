# 每日执行启动指令 v2.0

先读取：

1. `00_CONTROL/SOURCE_OF_TRUTH.md`
2. `00_CONTROL/LOCKED_RULES.md`
3. `00_CONTROL/CURRENT_STATE.md`
4. `01_TOPIC_SYSTEM/USED_TOPICS.md`
5. `01_TOPIC_SYSTEM/TOPIC_POOL.md`
6. `03_DATA/VIDEO_PERFORMANCE.csv` 最近3条
7. 上一个Day `METRICS.md`
8. 当前 `99_INBOX/DAY_XX_START_PACKET.md`（若存在）
9. 所需Harness

## 今天只完成一条视频

顺序：

上一条数据
→ Topic Lock
→ Evidence Lock
→ Script Lock
→ Audio Lock
→ ASR / Timeline
→ Director
→ Asset Gate
→ Segment Production
→ Segment QA
→ Full Cut
→ Full QA
→ Publish Package
→ Handoff

## 效率要求

目标：
**150分钟 + 30分钟缓冲**

累计120分钟仍未进入Full Cut：
自动降低视觉复杂度。

优先取消：
- 非必要AI镜头
- 装饰动画
- 新视觉风格测试

不能取消：
- 真实证据
- 旁白清晰度
- QA

## 提问

不重复项目级已锁定问题。

只有真正会改变结果且现有资料无法解决时，一次问一个。

## 结束

产出：
`DAY_XX_HANDOFF.md`
