# Template｜Director Segment Contract

```yaml
segment_id:
time_range:
voiceover:
narrative_task:
evidence_ref:
visual_function: REAL | HYPERFRAMES | REMOTION | AI | REAL_OUTPUT
teaching_truth:
primary_visual:
main_action:
camera:
on_screen_text:
assets:
  - id:
    status: REAL | EXTRACTABLE | PROGRAMMATIC | GENERATABLE
transition_in:
transition_out:
fallback:
qa_focus:
status: DRAFT | QA | APPROVED | LOCKED
```

规则：一个Segment只承担一个主要叙事任务；`MISSING/ASSUMED` 不允许进入 LOCKED。
