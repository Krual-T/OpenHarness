---
name: using-git-worktrees
description: Use when starting implementation work that needs isolation from the current workspace or before executing a task package in a separate worktree
---

# Using Git Worktrees

## Skill Role

- Protocol status: optional helper skill
- Primary stage: implementation execution
- Trigger: use when execution needs an isolated workspace or branch context

Git worktrees create isolated workspaces that share one repository history. Use them when isolation is genuinely helpful, not as a default ritual.

**Core principle:** choose the location deliberately, verify ignore safety first, then run the repository's documented bootstrap and verification path.

## Directory Selection Process

Follow this priority order:

### 1. Check Existing Directories

```bash
ls -d .worktrees 2>/dev/null
ls -d worktrees 2>/dev/null
```

If both exist, `.worktrees` wins.

### 2. Check Repository Guidance

- Read `AGENTS.md`.
- Read the active task package if it mentions isolation or branch strategy.
- If the repository already defines a preferred location, follow it.

### 3. Ask User

If no directory exists and repository guidance does not define a preference, ask where the worktree should live.

## Safety Verification

For project-local directories (`.worktrees` or `worktrees`), verify the directory is ignored before creating a worktree:

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

If the directory is not ignored:

1. Add the ignore rule.
2. Re-check ignore status.
3. Only then create the worktree.

## Creation Steps

### 1. Detect Project Name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. Create Worktree

```bash
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. Run Project Setup

Run the repository's documented bootstrap path. For Python repositories in this workspace, prefer the `uv run ...` commands documented in `AGENTS.md` or the task package instead of assuming `pip` or `poetry`.

### 4. Verify Clean Baseline

Run the repository's verification command before starting implementation.

If the baseline fails, report that failure before continuing so new breakage is not mixed with old breakage.

## Common Mistakes

- Creating a project-local worktree before verifying the directory is ignored.
- Assuming a directory location without checking repository guidance.
- Assuming an installer or setup tool when the repository already documents its own workflow.
- Starting implementation on top of a failing baseline without recording it.

## Integration

- `using-openharness` decides whether isolated execution is warranted.
- `subagent-driven-development` may use this skill when the user explicitly wants delegated work in an isolated workspace.
- `finishing-a-development-branch` handles cleanup once the work is complete.
