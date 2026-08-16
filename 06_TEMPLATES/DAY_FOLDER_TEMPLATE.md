# DAY_FOLDER_TEMPLATE v2.0

每个Day：

```text
DAY_XX/
├── SUMMARY.md
├── SCRIPT_FINAL.md
├── DIRECTOR_PLAN.md
├── ASSET_MANIFEST.md
├── PUBLISH.md
├── METRICS.md
└── PRODUCTION/
    ├── AUDIO_LOCK.md
    ├── TIMELINE_LOCK.md
    ├── PRODUCTION_LOG.md
    ├── QA_REPORT.md
    └── LESSONS_LEARNED.md
```

## 主文件

### SUMMARY
当天主题、核心观点、状态、最终结论。

### SCRIPT_FINAL
必须区分：
- Verbatim Transcript
- Clean Subtitle Transcript

### DIRECTOR_PLAN
音频锁定前：
`DRAFT_TIMING`

音频锁定后：
`FINAL_TIMING`

### ASSET_MANIFEST
字段至少包括：
- Asset ID
- Filename
- Type
- Resolution
- Primary Use
- Can Upscale
- Contains Audio
- QA
- Status
- Used in Final

### PUBLISH
- Cover
- Title
- Description
- Tags
- BGM
- Actual Publish Time

### METRICS
- 1h
- 3h
- 24h

## PRODUCTION

### AUDIO_LOCK
最终Master Narration信息。

### TIMELINE_LOCK
真实音频时间轴。

### PRODUCTION_LOG
只记录真正影响生产的变更和返工，不记录全部聊天。

### QA_REPORT
四层QA。

### LESSONS_LEARNED
每条经验标：
- ONE_OFF
- PRODUCTION_VALIDATED
- PERFORMANCE_PENDING
- PERFORMANCE_VALIDATED
