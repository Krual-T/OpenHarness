---
name: finishing-a-development-branch
description: 当任务状态是 archived（验证通过、任务包已完成）时使用
---

# 完成开发分支

## 概述

任务完成后关闭任务包，提供清晰的整合选项并执行用户选择。

## 步骤

### 1. 验证任务证据

确保任务包反映已完成的工作：
- `verification_design.md` 有最新的验证结果
- `evidence.md` 有变更文件、执行的命令和残留风险
- `STATUS.yaml` 与实际工作状态一致

运行项目测试套件。验证或测试不通过→停止，不能继续。

### 2. 确定基础分支

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

### 3. 提供 4 个选项

```
1. 合并到 <base-branch>（本地）
2. 推送并创建 Pull Request
3. 保持分支不动（稍后自行处理）
4. 丢弃这些工作
```

### 4. 执行选择

- **选项 1**：切到基础分支 → pull → merge → 测试通过 → `git branch -d`
- **选项 2**：推送分支 → `gh pr create` 创建 PR
- **选项 3**：报告保留状态，不清理 worktree
- **选项 4**：要求输入 `discard` 确认后，强制删除分支

### 5. 清理 Worktree

选项 1、2、4 完成后清理 worktree；选项 3 保留。

## 要点

- 必须在验证和测试通过后才能提供选项
- 选项 1（本地合并）和选项 2（创建 PR）执行前，确认代码审查已完成（Critical/Important 问题已修复）
- 丢弃工作必须先确认再执行
- 不要画蛇添足给选项加解释文字
