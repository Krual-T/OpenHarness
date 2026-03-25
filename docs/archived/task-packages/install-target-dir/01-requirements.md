# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
调整 OpenHarness 的 Codex 安装说明，让安装目标目录由用户显式决定，而不是默认把仓库克隆与技能链接路径都写死到 `~` 下。

## Problem Statement
当前 `README.md` 和 `INSTALL.codex.md` 都把安装路径直接写成 `~/.codex/openharness` 与 `~/.agents/skills/openharness`。这会让 Agent 在执行安装时跳过“询问安装目录”这个必要步骤，也会把示例路径误传达成默认标准路径。用户要求取消这种默认行为，并改成先询问目标目录，再生成诸如 `<target dir>/.agents/skills/openharness` 的安装结果。

## Required Outcomes
1. `INSTALL.codex.md` 明确要求 Agent 在执行安装前先询问用户要安装到哪个目标目录。
2. `INSTALL.codex.md` 不再把 `~` 作为默认安装位置，而是统一使用 `<target dir>` 占位符描述安装命令。
3. `README.md` 中的安装说明与 `INSTALL.codex.md` 保持一致，不再把默认写死到 `~` 的命令作为主路径。
4. 文档中保留清晰示例，说明技能安装结果应为 `<target dir>/.agents/skills/openharness`。

## Non-Goals
- 不引入新的交互式安装脚本。
- 不修改 Codex 的技能发现机制。
- 不扩展到其他 Agent 或编辑器的安装流程。

## Constraints
- 本轮只改安装说明与任务包，不新增执行程序。
- 仍然保留 “Fetch and follow instructions from ...” 这一安装入口。
- 完成前至少执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`。
- requirements gate：
- target user：希望把 OpenHarness 装到自定义目录的 Codex 用户。
- core scenario：用户让 Codex 按 `INSTALL.codex.md` 安装 OpenHarness 时，Agent 会先询问目标目录，再执行对应命令。
- single success metric：安装文档主路径不再把 `~` 当作默认目标目录。
- cost cap：只做文档与任务包改动，不开发安装器。
- acceptance criteria：README 与 INSTALL 都清楚表达“先询问目录，再基于 `<target dir>` 安装”。
- counterexample：如果文档仍保留 `git clone ... ~/.codex/openharness` 作为默认主命令，即使补充一句“也可以自定义”，也不满足本需求。
