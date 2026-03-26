# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 还没有为每个子命令都写单独的帮助页快照测试，目前覆盖的是顶层、`bootstrap` 和 `update` 这类代表性命令。

## Manual Steps
- 无。

## Files
- openharness_cli/cli.py
- skills/using-openharness/tests/openharness_cases/test_entrypoint.py
- docs/archived/task-packages/openharness-help-polish/STATUS.yaml

## Commands
- uv run pytest skills/using-openharness/tests/openharness_cases/test_entrypoint.py
- uv run pytest skills/using-openharness/tests/openharness_cases/test_protocol_docs.py -k help
- uv run python skills/using-openharness/scripts/openharness.py check-tasks
- openharness update --help
- openharness bootstrap --help

## Artifact Paths
- docs/archived/task-packages/openharness-help-polish/05-verification.md

## Follow-ups
- 如果后续新增更多安装层命令，可以继续沿用现在的 description + example 模式，并补对应帮助测试。
