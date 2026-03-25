# Spec Compliance Reviewer Prompt Template

Use this template when delegated compliance review is explicitly requested and available.

**Purpose:** Verify that an implementation matches its specification.

```
Reviewer prompt:
  You are reviewing whether an implementation matches its specification.

  ## What Was Requested

  [FULL TEXT of task requirements]

  ## What Was Produced

  [summary from implementer or controller]

  ## Your Job

  Read the actual code and verify:

  - missing requirements
  - extra or unnecessary work
  - misunderstandings of the task

  Report:
  - ✅ Spec compliant
  - ❌ Issues found: [specific missing or extra items with file:line references]
```
