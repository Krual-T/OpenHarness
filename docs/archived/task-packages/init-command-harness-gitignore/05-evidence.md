# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 如果后续希望 `.harness/.gitignore` 保留用户已有自定义规则，需要另起任务设计合并或不覆盖策略。

## Manual Steps
- 已在当前仓库执行 `uv run openharness init`，生成 `.harness/.gitignore`。无额外人工步骤。

## Files
- `.harness/.gitignore`：当前仓库实际初始化产物，内容为 `*`。
- `openharness_cli/cli.py`：注册 `init` 子命令。
- `openharness_cli/commands.py`：实现 `.harness/.gitignore` 写入。
- `openharness_cli/main.py`：暴露 `cmd_init` 包装。
- `openharness_cli/__init__.py`：导出 `cmd_init`。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖 parser 与文件生成行为。
- `tests/openharness_cases/test_protocol_docs.py`：覆盖公开子命令集合和 handler 集合。

## Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -q`：先确认新增测试失败，后确认聚焦测试通过。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_protocol_docs.py -q`：相关测试通过，`74 passed in 0.34s`。
- `uv run openharness init`：在当前仓库生成 `.harness/.gitignore`。
- `uv run openharness check-tasks`：归档后协议检查通过，验证 43 个 task package。
- `uv run pytest -q`：final verification command，通过，`205 passed in 1.47s`。

## Artifact Paths
- 无独立日志文件。

## Follow-ups
- 后续如果要扩展 `openharness init`，应单独定义更多初始化项和幂等规则。
