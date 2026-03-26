# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
为 OpenHarness 提供一个即插即用的全局命令 `openharness`，让仓库技能和维护者能够直接运行 `openharness <cmd>`，同时不要求接入仓库的用户修改自己项目的 `pyproject.toml`。

## Problem Statement
当前 `using-openharness` 相关命令只能通过长路径脚本调用，例如 `uv run python /path/to/skills/using-openharness/scripts/openharness.py bootstrap`。这有三个问题：

- 调用路径过长，难以记忆，也不利于技能文档稳定引用。
- 用户虽然通过 `INSTALL.codex.md` 安装了技能软链接，但并没有同步获得系统级的 `openharness` 命令。
- 现有仓库已经具备成型 CLI 代码，却缺少正式的打包入口，导致安装体验和复用体验都停留在脚本级别。

## Required Outcomes
1. OpenHarness 仓库自身暴露稳定的 CLI 入口，使用户安装后可以直接运行 `openharness bootstrap`、`openharness check-tasks` 等子命令。
2. 该 CLI 的安装方式不要求业务项目修改自身 `pyproject.toml`；命令安装应发生在 OpenHarness 仓库或用户工具环境层。
3. 现有脚本入口 `skills/using-openharness/scripts/openharness.py` 保持兼容，避免破坏已有技能文档、测试和手工工作流。
4. `INSTALL.codex.md` 需要明确说明新装用户和已安装用户分别如何启用全局 `openharness` 命令。
5. 至少提供一条可持续维护的安装路径，优先使用 `uv tool install --editable <repo>` 这一类可编辑工具安装，而不是要求用户自行维护 shell alias。

## Non-Goals
- 不在本轮实现 Rust、Go 或其他原生语言的独立二进制程序。
- 不要求每个接入 OpenHarness 的用户项目增加 Python 打包配置。
- 不在本轮重写所有技能脚本，只覆盖 `using-openharness` 现有 CLI 入口和相关文档。
- 不承诺发布到 PyPI 或做跨平台安装包分发。

## Constraints
- 必须遵守现有 task package 协议，并回写设计、验证和证据。
- 仓库内 Python 命令统一使用 `uv run ...`，但最终用户命令体验应优先是 `openharness <cmd>`。
- 已有测试大量直接导入 `skills/using-openharness/scripts/openharness.py`，实现时必须保留兼容层或同步调整测试而不破坏外部入口。
- 安装方案必须是即插即用的，不能依赖用户修改目标项目的 `pyproject.toml`。
- 成本上限是一次聚焦改动，优先复用现有 CLI 代码结构，而不是重写命令系统。
