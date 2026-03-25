---
name: subagent-driven-development
description: Use when a task package is detailed enough to execute and its tasks are independent enough to dispatch subagents in the current session
---

# Subagent-Driven Development

## Skill Role

- Protocol status: optional helper skill
- Primary stage: implementation execution
- Trigger: use only when the task package is already detailed enough, the subtasks are mostly independent, and the user explicitly wants delegated execution

Use this skill to execute a detailed task package through bounded subagents. The task package remains authoritative; the controller owns coordination, verification, and task-package writeback.

**Core principle:** bounded delegation, bounded context, controller-owned verification.

## When to Use

Use this skill only when all of the following are true:

- `using-openharness` has already routed the task and the package is ready to execute.
- The work can be split into mostly independent subtasks.
- The user explicitly wants subagents or parallel agent work.
- Delegation will not create shared-write conflicts that are harder than doing the work locally.

If any of these are false, stay in the main session and execute manually.

## Process

1. Read the task package once and extract the executable tasks into a local checklist.
2. For each task, prepare bounded context:
   - the exact task text
   - the relevant file paths
   - constraints and acceptance criteria
   - any architectural context the worker needs
3. Dispatch one implementer subagent for one bounded task.
4. Answer questions before the subagent proceeds; do not let it guess through ambiguity.
5. Review the result against the task package and declared verification path.
6. If there are gaps, send the task back with concrete corrections.
7. Mark the task complete in your local checklist only after the delegated result is verified.
8. After all tasks are complete, run package-level verification, then update `05-verification.md`, `06-evidence.md`, and `STATUS.yaml`.

## Model Selection

- Mechanical, tightly scoped edits: fast model.
- Multi-file integration work: standard model.
- Architectural judgment or review-heavy work: strongest model available.

Do not use a more capable model as a substitute for a vague task description.

## Handling Implementer Status

**DONE:** Review the result against the task package and run the relevant verification.

**DONE_WITH_CONCERNS:** Read the concerns before proceeding. Resolve correctness or scope doubts before treating the task as complete.

**NEEDS_CONTEXT:** Provide the missing context and re-dispatch.

**BLOCKED:** Change something real before retrying: context, task size, or model. Do not blindly retry the same prompt.

## Prompt Templates

- `./references/implementer-prompt.md` - bounded implementer prompt
- `./references/spec-reviewer-prompt.md` - optional bounded compliance review prompt when delegated review is explicitly requested
- `./references/code-quality-reviewer-prompt.md` - optional bounded quality review prompt when delegated review is explicitly requested

## Red Flags

- Using this skill when the user did not ask for delegation.
- Making subagents discover the task package on their own when you could hand them the exact task text.
- Dispatching multiple workers that edit the same files.
- Treating subagent self-report as proof of completion.
- Marking the package done before package verification and evidence writeback are complete.

## Integration

- `using-openharness` is required before this skill.
- `using-git-worktrees` is optional when isolated workspace helps.
- `test-driven-development` remains the preferred execution discipline for behavior changes.
- `finishing-a-development-branch` closes the package after verification.
