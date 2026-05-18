# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 `openharness update` 刷新全局工具的方式改为 `uv tool upgrade --reinstall openharness`，确保从当前 tool 记录的安装来源重新安装，而不是使用普通 upgrade 语义。

单一成功指标：`update` 命令执行工具刷新时调用 `uv tool upgrade --reinstall openharness`。

## Problem Statement
OpenHarness 的全局安装来源应是 skill-hub 下的 OpenHarness 克隆。普通 `uv tool upgrade openharness` 可能只做升级解析，不明确表达“按当前安装来源重装一次”的意图；而 `uv tool install --force .` 又会把安装来源改成当前开发仓库，破坏 skill-hub 作为真实来源的约定。

目标用户是使用 `openharness update` 刷新全局 CLI 的维护者和 agent。核心场景是 skill-hub 源更新后，update 应从该来源重新构建并安装全局 tool。

## Required Outcomes
1. 修改 update 的工具刷新命令。
   - acceptance criteria：`openharness_cli/commands/update.py` 使用 `["uv", "tool", "upgrade", "--reinstall", "openharness"]`。
2. 更新测试覆盖。
   - acceptance criteria：update 命令测试断言 subprocess 调用包含 `--reinstall`。

## Non-Goals
- 不把 update 改成 `uv tool install --force .`。
- 不改变 skill-hub 作为真实安装来源的约定。
- 不改 update 的 pull / force-sync 模式选择逻辑。

Counterexample：从当前开发仓库执行 `uv tool install --force .` 可以临时修好本地 CLI，但会改变安装来源，不属于本轮目标。

## Constraints
- 保持 update 先同步源克隆、再刷新 tool 的顺序。
- cost cap：只改 update 刷新命令和相关测试。
