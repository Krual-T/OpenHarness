# 需求

## 目标

`openharness init` 命令一次性创建项目运行所需的所有基本目录结构，用户无需依赖其他命令的按需创建行为。

**单一成功指标**：在新项目中执行 `openharness init` 后，`.harness/rwp/`、`.harness/locks/`、`docs/task-packages/`、`docs/archived/task-packages/` 及其子文件全部存在且结构完整。

## 问题陈述

当前 `openharness init` 只创建 `.harness/` 和 `.harness/.gitignore`，其余目录（`rwp/rwplib/`、`rwp/workflows/`、`locks/`、`docs/task-packages/`、`docs/archived/task-packages/`）依赖 `rwp create`、`task-package new` 等命令按需 `mkdir(parents=True, exist_ok=True)` 创建。

这导致可发现性差：用户 `init` 之后看不到完整的项目骨架，不知道 OpenHarness 会用到哪些目录。`rwplib/__init__.py` 作为 PYTHONPATH 注入目标，在运行时才被感知到存在。

目标用户是任何在新项目中执行 `openharness init` 的开发者。核心场景：克隆仓库 → `openharness init` → 直接看到完整的 `.harness/` 和 `docs/` 目录树。

## 必须交付的结果

1. `init` 命令创建 `.harness/rwp/rwplib/__init__.py`（空文件）
   - 验收标准：`init` 后该文件存在，rwplib 可作为 Python 包导入
2. `init` 命令创建 `.harness/rwp/workflows/` 目录
   - 验收标准：`init` 后该目录存在（空目录）
3. `init` 命令创建 `.harness/locks/` 目录
   - 验收标准：`init` 后该目录存在（空目录）
4. `init` 命令创建 `docs/task-packages/` 目录
   - 验收标准：`init` 后该目录存在（空目录）
5. `init` 命令创建 `docs/archived/task-packages/` 目录
   - 验收标准：`init` 后该目录存在（空目录）
6. 所有创建操作保持幂等性 — 重复执行 `init` 不会报错
   - 验收标准：对已初始化的项目再次执行 `init` 不会报错

## 非目标

- 不创建 `.harness/settings.yaml`（settings.yaml 属于 OpenHarness 全局配置，位于 `~/.agents/skill-hub/openharness/.harness/settings.yaml`，由 `update --set-default-mode` 管理）
- 不创建任何其他配置文件
- 不修改已有命令的按需创建逻辑（保留作为防御性保障）

## 约束

- 改动范围限定于 `openharness_cli/commands/init_cmd.py` 一个文件
- 所有目录创建必须使用 `exist_ok=True`，确保幂等
- 不改变 `init` 命令的现有参数和行为签名
