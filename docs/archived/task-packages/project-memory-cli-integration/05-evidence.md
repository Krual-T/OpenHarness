# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- `project-memory` 目前仍通过脚本桥接接入 CLI，未来如果这些脚本路径发生结构变化，需要同步更新包装层。
- `--repo` 目前要求放在 `project-memory` 命令组上；如果维护者强烈期待叶子命令级别的自由位置支持，还需要后续单独收口。

## Manual Steps
- 无。

## Files
- openharness_cli/cli.py
- openharness_cli/commands.py
- openharness_cli/main.py
- openharness_cli/__init__.py
- skills/project-memory/SKILL.md
- tests/openharness_cases/test_cli_workflows.py
- tests/openharness_cases/test_protocol_docs.py
- docs/archived/task-packages/project-memory-cli-integration/README.md
- docs/archived/task-packages/project-memory-cli-integration/STATUS.yaml
- docs/archived/task-packages/project-memory-cli-integration/01-requirements.md
- docs/archived/task-packages/project-memory-cli-integration/02-overview-design.md
- docs/archived/task-packages/project-memory-cli-integration/03-detailed-design.md
- docs/archived/task-packages/project-memory-cli-integration/04-verification.md
- .project-memory/facts/project_memory_official_cli_entrypoint.yaml
- .project-memory/aliases.yaml

## Commands
- uv run openharness bootstrap --json
- uv run python skills/project-memory/scripts/query_memory.py "project-memory cli 收拢 openharness 子命令"
- uv run openharness new-task project-memory-cli-integration --auto-id --title "Integrate Project Memory Into OpenHarness CLI" --owner codex --summary "Add project-memory subcommands to the official openharness CLI and align live skills, docs, and tests with the new entrypoint."
- uv run openharness transition project-memory-cli-integration requirements_ready
- uv run openharness transition project-memory-cli-integration overview_ready
- uv run openharness transition project-memory-cli-integration detailed_ready
- uv run pytest tests/openharness_cases/test_protocol_docs.py -k 'single_cli_supports_all_subcommands or task_package_commands_use_current_handlers_only'
- uv run pytest tests/openharness_cases/test_cli_workflows.py -k 'project_memory_query_runs_wrapped_script_in_target_repo or project_memory_parser_accepts_nested_subcommands'
- uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_task_package_core.py
- uv run openharness check-tasks
- uv run openharness project-memory query "project-memory cli 收拢 openharness 子命令" --include-unusable
- uv run openharness project-memory save-fact project_memory_official_cli_entrypoint ...
- final verification command: uv run openharness verify project-memory-cli-integration

## Artifact Paths
- docs/archived/task-packages/project-memory-cli-integration/04-verification.md
- docs/archived/task-packages/project-memory-cli-integration/05-evidence.md
- .harness/artifacts/OH-039/verification-runs/

## Follow-ups
- 如果后续还要把更多 helper skill 收口进 `openharness` CLI，可以考虑抽出一个通用的脚本桥接辅助层，减少命令包装重复。
- 如果维护者反馈 `--repo` 的位置限制不够直观，再单独评估更灵活的参数解析方案。
