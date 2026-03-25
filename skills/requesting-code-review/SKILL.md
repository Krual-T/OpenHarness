---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

## Skill Role

- Protocol status: optional helper skill
- Primary stage: verification and closure
- Trigger: use before merge or after major implementation waves when bounded review adds value

Prepare a bounded review context before merge or closure. If the current session permits delegated review and the user explicitly wants it, use that context for a reviewer subagent. Otherwise perform the same review checklist yourself in the current session.

## When to Request Review

**Mandatory:**
- After a major feature or refactor
- Before merge to main
- Before claiming a broad change is safe

**Optional but valuable:**
- When stuck
- Before risky refactoring
- After fixing a subtle bug

## How to Request

**1. Get the diff range:**

```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Build review context:**

Use the template at `references/code-reviewer.md` to capture:

- what changed
- what it was supposed to do
- the diff range to inspect
- any known risks or constraints

**3. Run the review and act on feedback:**

- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later when appropriate
- Push back with technical reasoning if a review conclusion is wrong

## Integration

- In delegated workflows, review each substantial result before moving on.
- In manual workflows, use the same checklist before merge or closure.

## Red Flags

- Skipping review because the change feels small.
- Treating delegated review as mandatory when delegation is unavailable or not requested.
- Proceeding with unfixed Important issues.
- Arguing with valid technical feedback instead of checking it.

See template at: `references/code-reviewer.md`
