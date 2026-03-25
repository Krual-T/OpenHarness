# Implementer Subagent Prompt Template

Use this template when delegated implementation is explicitly requested and available.

```
Implementer prompt:
  You are implementing Task N: [task name]

  ## Task Description

  [FULL TEXT of task from plan - paste it here]

  ## Context

  [Scene-setting: where this fits, dependencies, architectural context]

  ## Before You Begin

  Ask questions now if requirements, constraints, or assumptions are unclear.

  ## Your Job

  1. Implement exactly what the task specifies
  2. Write tests when the task changes behavior
  3. Verify the implementation
  4. Self-review
  5. Report back

  Work from: [directory]

  ## Report Format

  - Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
  - What you implemented
  - What you tested and the results
  - Files changed
  - Self-review findings
  - Remaining concerns
```
