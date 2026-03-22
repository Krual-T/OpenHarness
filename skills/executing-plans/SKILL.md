---
name: executing-plans
description: Use when a task package already has a written execution plan and you want to execute it in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load the task package plus any optional execution plan artifact, review critically, execute against the task package, then close the package correctly.

**Announce at start:** "I'm using the executing-plans skill to execute this task package."

In this repository, `executing-plans` is a compatibility helper for cases where work has already been written as an explicit execution plan. The task package under `docs/designs/<task>/` remains the source of truth; the plan is only a derived execution aid.

**Note:** If subagents are available, prefer `subagent-driven-development` over this skill.

## The Process

### Step 1: Load and Review Task Source
1. Read the active task package first, especially `README.md`, `STATUS.yaml`, `01-requirements.md`, `02-overview-design.md`, `03-detailed-design.md`, `05-verification.md`, and `06-evidence.md`
2. If an execution plan artifact exists, read it as a secondary execution aid rather than the primary source
3. Review critically and identify any conflicts between the plan and the task package
4. If concerns: raise them with your human partner before starting
5. If no concerns: create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Close the Task Package

After all tasks complete and required verification commands pass:
- Update `05-verification.md` with the verification path and fresh results
- Update `06-evidence.md` with changed files, commands, and residual risk
- Update `STATUS.yaml` so the package status matches reality
- Archive the task package only if implementation and verification are complete and the package is leaving active work
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use `finishing-a-development-branch`
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking
- The execution plan and task package diverge

**Don't force through blockers** - stop and ask.

## Remember
- Review the task package first
- Follow the task package first and the plan second
- Don't skip verifications
- Don't treat design-complete or test-complete as package-complete
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **writing-plans** - Optional compatibility skill that may create the explicit execution plan this skill consumes
- **finishing-a-development-branch** - Complete development after all tasks
