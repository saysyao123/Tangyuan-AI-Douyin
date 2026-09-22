# 02 — Stage Contracts, Seal, Handoff, Reopen

## 1. Stage contract

Every stage must explicitly define:

```yaml
stage_id:
version:

goal:

input_contract:
  required:
  optional:

locked_rules:

acceptance_criteria:

output_contract:

evidence_requirements:

failure_routes:
```

The contract should be stable even when the internal Skill implementation changes.

## 2. Stage result package

Before review, a stage produces:

```yaml
result:
  artifacts:

decisions:

locked_rules_forward:

evidence:

open_issues:

next_input:
```

The result package is not yet the next-stage input until it passes review and is sealed.

## 3. Seal rule

A stage can enter `SEALED` only if:

- deterministic required fields are present;
- required evidence exists;
- all critical Judge criteria pass;
- no unresolved blocking issue remains;
- required human gate is approved when applicable.

Model prose such as "looks complete" cannot create a sealed state.

## 4. Compact handoff

After sealing, compile only the information needed downstream.

Example:

```yaml
FIRST_FRAME_HANDOFF:
  contract_version: 1

  asset:
    shot_03: shot03_v8.png

  character:
    identity_version: C04
    costume_version: C02

  composition:
    framing: medium_wide
    camera_angle: low_three_quarter

  continuity:
    facing: camera_right
    end_pose: ready_step

  locked_rules:
    preserve_identity: true
    preserve_costume: true

  evidence_refs:
    - user_approval
    - image_asset

  open_issues: []
```

Do not include:
- discarded image versions;
- old face-cover rules that were superseded;
- full discussion transcript;
- irrelevant reasons for choices.

## 5. Archive policy

When a stage is sealed, move its process history conceptually into archive:

```text
Archive/
  stage_version/
    discussion
    failed_artifacts
    judge_report
    diagnostics
    superseded_rules
```

This may remain in repository/history storage. The rule is about **active context**, not data deletion.

## 6. Reopen policy

A sealed stage cannot be silently edited.

```text
SEALED v7
   |
 REOPEN
   |
OPEN v8
   |
REVIEW
   |
SEALED v8
```

The new version must be reviewed again.

## 7. Dependency invalidation

Each stage declares dependencies by contract version.

Example:

```yaml
MOTION:
  depends_on:
    DIRECTOR: 5
    FIRST_FRAME: 8
```

When `FIRST_FRAME` changes from v8 to v9:

- compare handoff fields used by MOTION;
- if relevant fields changed, mark MOTION DIRTY;
- if irrelevant internal implementation changed, leave MOTION sealed.

This is selective rebuild.

## 8. Normal path vs fault path

### Normal path
```text
Stage A
-> Review
-> Seal
-> Compact Handoff
-> Stage B
```

### Fault path
```text
Stage B failure
-> localize failure
-> inspect B inputs
-> if necessary inspect A handoff/evidence
-> reopen only originating stage
-> selectively rebuild dependents
```

Never default to "reload the whole project."

## 9. Recommended MV stage boundaries

Initial candidate boundaries:

1. Audio / lyric segment lock
2. Story / visual interpretation
3. Director / shot plan
4. Character and first-frame assets
5. Dynamic prompt / motion design
6. Video generation
7. Video QA and retry routing
8. Edit / continuity assembly
9. Final delivery

These are starting points, not immutable. Real project testing should determine whether any stage is too broad or too narrow.
