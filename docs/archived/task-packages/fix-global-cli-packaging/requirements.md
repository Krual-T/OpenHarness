# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
修复 OpenHarness 全局 CLI 安装包缺少子包的问题，让 `uv tool install --force .` 安装出的 `openharness` 命令可以正常导入 `openharness_cli.models`、`openharness_cli.core` 和 `openharness_cli.commands`。

单一成功指标：全局 `/home/Shaokun.Tang/.local/bin/openharness` 重新安装后能正常运行，并且 `transition` 不再因旧代码尝试补建 `task-package.README.md`。

## Problem Statement
当前仓库源码已经移除了任务包 README 协议，但全局 `openharness` 曾加载旧克隆代码，导致旧代码读取当前仓库的新模板时仍尝试创建 `README.md`，最终报 `task-package.README.md` 缺失。

尝试用当前仓库重新安装全局工具后，又暴露出 packaging 问题：`pyproject.toml` 只声明了 `openharness_cli` 和 `openharness` 两个顶层包，没有包含 `openharness_cli.models`、`openharness_cli.core`、`openharness_cli.commands` 子包，导致全局入口启动时报 `ModuleNotFoundError: No module named 'openharness_cli.models'`。

目标用户是通过 PATH 上的全局 `openharness` 命令操作任务包的维护者和 agent。核心场景是从任意目录执行 `openharness --repo <repo> task-package ...`。

## Required Outcomes
1. 修正 Python 包发现配置。
   - acceptance criteria：安装包包含 `openharness_cli` 的所有子包。
2. 验证全局工具使用当前仓库代码。
   - acceptance criteria：全局工具 Python 环境中 `TaskPackageDocument` 不包含 `README.md`。
3. 验证全局 transition 不再补建 README。
   - acceptance criteria：从仓库外目录运行全局 `openharness --repo <repo> task-package transition TASK-004 overview_designing` 不再报 `task-package.README.md` 缺失；验证后把 `TASK-004` 状态恢复到原 gate 值。

## Non-Goals
- 不修改任务包 README 协议本身；它已由 `TASK-006` 处理。
- 不修改 `update` 命令的同步策略。
- 不清理或删除 `/home/Shaokun.Tang/.agents/skill-hub/openharness` 旧克隆。

Counterexample：改回 `task-package.README.md` 模板能绕过报错，但会恢复已删除的协议，不能作为本轮修复。

## Constraints
- 不覆盖用户在 `workflow-docs-skill-sharpening` 的未提交改动。
- 全局重装只能从当前仓库构建，不做 `git reset --hard`。
- cost cap：只改 packaging 配置和本任务包文档。
