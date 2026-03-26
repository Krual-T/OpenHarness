# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 目前只在当前 Linux 环境验证了 `uv tool install --editable` 与 `openharness` 命令，尚未补做其他平台的真实安装证据。
- 仓库历史文档中仍保留大量旧脚本命令示例，这是兼容保留而不是功能问题；后续如要统一文案，可再做单独清理。

## Manual Steps
- 新用户需要先克隆仓库，再执行 `uv tool install --editable ~/.agents/skill-hub/openharness` 和技能软链接安装。
- 已安装过技能的用户只需额外执行一次 `uv tool install --editable ~/.agents/skill-hub/openharness`。

## Files
- pyproject.toml
- openharness_cli/__init__.py
- openharness_cli/main.py
- openharness_cli/cli.py
- openharness_cli/commands.py
- openharness_cli/constants.py
- openharness_cli/lifecycle.py
- openharness_cli/models.py
- openharness_cli/repository.py
- openharness_cli/validation.py
- skills/using-openharness/scripts/openharness.py
- INSTALL.codex.md
- AGENTS.md
- skills/using-openharness/SKILL.md
- skills/using-openharness/tests/openharness_cases/test_entrypoint.py
- skills/using-openharness/tests/openharness_cases/test_protocol_docs.py
- docs/archived/task-packages/openharness-cli-modularization/STATUS.yaml
- docs/archived/task-packages/new-task-auto-id-concurrency-fix/STATUS.yaml
- docs/archived/task-packages/remove-legacy-new-task-args/STATUS.yaml

## Commands
- uv run python skills/using-openharness/scripts/openharness.py new-task openharness-global-cli --auto-id --title "为 OpenHarness 提供全局命令入口" --owner codex --summary "将长路径 uv run python 调用收敛为可安装的 openharness 全局命令，并补充安装与迁移说明。" --status proposed
- uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py
- uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py
- uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py
- uv tool install --editable /home/Shaokun.Tang/Projects/openharness --force
- openharness bootstrap
- uv run python skills/using-openharness/scripts/openharness.py check-tasks

## Artifact Paths
- docs/archived/task-packages/openharness-global-cli/04-verification.md

## Follow-ups
- 可后续补一个面向 Windows 和 macOS 的安装验证 task package，确认 `uv tool` 安装、PATH 与文档示例完全一致。
- 如果后续继续统一其他技能脚本入口，可以把 `project-memory` 等零散脚本也收拢到 `openharness` 子命令树下。
