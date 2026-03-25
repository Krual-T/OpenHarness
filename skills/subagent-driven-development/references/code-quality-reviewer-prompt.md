# Code Quality Reviewer Prompt Template

Use this template when delegated code-quality review is explicitly requested and available.

**Purpose:** Verify that an implementation is clean, tested, and maintainable.

```
Reviewer prompt:
  Use template at ../requesting-code-review/references/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from implementer or controller]
  PLAN_OR_REQUIREMENTS: [relevant requirements or task text]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]
```

In addition to the standard checklist, review:

- whether each file has one clear responsibility
- whether the implementation follows the planned structure
- whether the change made file growth worse in ways that matter
