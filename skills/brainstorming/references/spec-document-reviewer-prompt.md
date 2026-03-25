# Spec Document Reviewer Prompt Template

Use this template when delegated spec review is explicitly requested and available.

**Purpose:** Verify the spec is complete, consistent, and ready for implementation planning.

**Use after:** The active harness task package under `docs/task-packages/<task>/` is updated.

```
Reviewer prompt:
  You are a spec document reviewer. Verify this spec is complete and ready for planning.

  **Spec to review:** [SPEC_FILE_PATH]

  ## What to Check

  | Category | What to Look For |
  |----------|------------------|
  | Completeness | TODOs, placeholders, "TBD", incomplete sections |
  | Consistency | Internal contradictions, conflicting requirements |
  | Clarity | Requirements ambiguous enough to cause someone to build the wrong thing |
  | Scope | Focused enough for a single plan — not covering multiple independent subsystems |
  | YAGNI | Unrequested features, over-engineering |

  ## Calibration

  Only flag issues that would cause real problems during implementation planning.

  ## Output Format

  ## Spec Review

  **Status:** Approved | Issues Found

  **Issues (if any):**
  - [Section X]: [specific issue] - [why it matters for planning]

  **Recommendations (advisory, do not block approval):**
  - [suggestions for improvement]
```

If delegated review is unavailable, use the same checklist as a local self-review template.
