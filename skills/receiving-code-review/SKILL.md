---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Code Review Reception

## Skill Role

- Protocol status: optional helper skill
- Primary stage: debugging and repair
- Trigger: use when review feedback arrives and needs technical validation before implementation

Code review requires technical evaluation, not social performance.

**Core principle:** verify before implementing, ask before assuming, push back when the feedback is wrong.

## The Response Pattern

1. Read the full feedback without reacting line by line.
2. Restate the technical requirement in your own words.
3. Verify it against the codebase and current constraints.
4. Decide whether it is correct for this repository.
5. Implement or push back with technical reasoning.
6. Test each accepted fix.

## Forbidden Responses

Never lead with performative agreement or commit to changes before verification.

Bad examples:

- "You're absolutely right!"
- "Great point!"
- "Let me implement that now."

Good alternatives:

- Restate the technical issue.
- Ask a precise clarifying question.
- Verify locally and then state the result.

## Handling Unclear Feedback

If any item is unclear, stop and clarify before implementing anything that depends on it. Partial understanding leads to wrong implementation.

## Source-Specific Handling

### From your human partner

- Trusted, but still clarify scope when needed.
- Prefer action or technical acknowledgment over performative phrasing.

### From external reviewers

Check all of the following before implementing:

1. Is the suggestion technically correct here?
2. Does it break existing behavior?
3. Is there a reason the current code looks this way?
4. Does the reviewer have enough context?

If you cannot verify the claim, say so explicitly and state what evidence is missing.

## YAGNI Check

When feedback asks for a more "proper" implementation, first check whether the feature is actually needed. If the code path is unused, challenge the requirement instead of automatically building more.

## Acknowledging Correct Feedback

State the result factually:

- `Fixed. [brief description]`
- `Verified. [issue] was real; corrected in [location]`

The code and verification should do the talking.

## When To Push Back

Push back when the feedback:

- breaks working behavior
- conflicts with repository constraints
- adds unused scope
- is technically incorrect
- lacks enough context to justify the change

Push back with technical reasoning, not defensiveness.
