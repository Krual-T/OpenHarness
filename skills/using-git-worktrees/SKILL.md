---
name: using-git-worktrees
description: 当实现工作需要隔离工作空间或需要在单独 worktree 中执行任务包时使用
triggers_on: [implementing]
requires: []
next_skills: []
---

# 使用 Git Worktrees

## 概述

Git worktree 创建共享同一仓库历史的隔离工作空间。在隔离确实有帮助时使用，不要作为默认仪式。

## 目录选择

按以下优先级：

1. 检查已有目录：`ls -d .worktrees worktrees 2>/dev/null`，两个都有则 `.worktrees` 优先
2. 检查仓库指引：读 `AGENTS.md` 和当前任务包中关于隔离或分支策略的说明
3. 都没有则问用户

## 安全检查

项目本地目录（`.worktrees` 或 `worktrees`）创建前验证已被 gitignore：
```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```
未忽略则先添加忽略规则，再验证，然后才创建 worktree。

## 创建步骤

1. 检测项目名：`project=$(basename "$(git rev-parse --show-toplevel)")`
2. 创建 worktree：`git worktree add "$path" -b "$BRANCH_NAME"`；`cd "$path"`
3. 运行仓库文档化的启动流程（Python 仓库优先 `uv run ...` 命令）
4. 实现前运行验证命令确认基线干净。基线失败则先报告，避免新旧损坏混淆

## 集成

- `using-openharness` 决定是否需要隔离执行
- `subagent-driven-development` 在用户要求隔离工作空间时使用此技能
- `finishing-a-development-branch` 完成工作后处理清理
