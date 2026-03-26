# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 没有覆盖真实 `git pull` 网络、冲突或鉴权失败场景。
- 没有覆盖用户把 OpenHarness 安装在非常规目录且包文件位置无法映射到 git clone 的场景。

## Manual Steps
- 已安装用户升级到本版本后，可直接执行 `openharness update` 替代原手工更新步骤。

## Files
- openharness_cli/__init__.py
- openharness_cli/cli.py
- openharness_cli/commands.py
- openharness_cli/main.py
- skills/using-openharness/scripts/openharness.py
- INSTALL.codex.md
- skills/using-openharness/SKILL.md
- skills/using-openharness/tests/openharness_cases/test_cli_workflows.py
- skills/using-openharness/tests/openharness_cases/test_protocol_docs.py

## Commands
- uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py -k update
- uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k update
- uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py
- uv run pytest skills/using-openharness/tests/openharness_cases/test_cli_workflows.py
- uv run python skills/using-openharness/scripts/openharness.py check-tasks

## Artifact Paths
- docs/archived/task-packages/openharness-update-command/04-verification.md

## Follow-ups
- 如果后续要支持 `openharness self-update`、`openharness doctor` 或更丰富的安装诊断，可以在此基础上继续扩展安装层子命令。
