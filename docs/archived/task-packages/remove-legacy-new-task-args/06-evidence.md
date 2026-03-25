# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 若仓库外有人仍依赖旧位置参数，需要自行更新调用方式。

## Manual Steps
- 无。

## Files
- `skills/using-openharness/scripts/openharness_cli/cli.py`
- `skills/using-openharness/scripts/openharness_cli/commands.py`
- `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py`
- `skills/using-openharness/tests/openharness_cases/test_task_package_core.py`
- `docs/archived/task-packages/remove-legacy-new-task-args/README.md`
- `docs/archived/task-packages/remove-legacy-new-task-args/STATUS.yaml`
- `docs/archived/task-packages/remove-legacy-new-task-args/01-requirements.md`
- `docs/archived/task-packages/remove-legacy-new-task-args/02-overview-design.md`
- `docs/archived/task-packages/remove-legacy-new-task-args/03-detailed-design.md`
- `docs/archived/task-packages/remove-legacy-new-task-args/05-verification.md`
- `docs/archived/task-packages/remove-legacy-new-task-args/06-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task --auto-id "remove-legacy-new-task-args" --title "Remove legacy new-task positional compatibility"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k "new_task or legacy_positional or task_package_commands_use_current_handlers_only"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py new-task --help`

## Artifact Paths
- `docs/archived/task-packages/remove-legacy-new-task-args/05-verification.md`
- `docs/archived/task-packages/remove-legacy-new-task-args/06-evidence.md`

## Follow-ups
- 可以后续再单独优化 argparse 错误文案，使旧调用失败时更容易看懂。
