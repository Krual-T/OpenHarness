# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 没有真实运行 `openharness update --force-sync`，避免对当前 OpenHarness 工作树执行破坏性 reset；本轮证据覆盖的是 CLI 编排契约。
- 如果用户的 OpenHarness clone 没有 upstream tracking branch，`git reset --hard '@{u}'` 会失败；本轮接受这个失败并停止的行为，不做自动修复。

## Manual Steps
- 无。

## Files
- `openharness_cli/cli.py`：新增 `--force-sync` 参数和帮助文案。
- `openharness_cli/commands.py`：新增强制同步命令编排和失败中断。
- `tests/openharness_cases/test_cli_workflows.py`：覆盖默认 update、强制同步顺序和失败路径。
- `tests/openharness_cases/test_entrypoint.py`：覆盖帮助页参数和风险说明。
- `INSTALL.codex.md`：记录用户可见的强制同步更新入口。
- `docs/archived/task-packages/update-force-sync/*`：记录本轮需求、设计、验证和证据。

## Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，red run: 3 failed, 2 passed, 21 deselected。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，green run: 5 passed, 21 deselected。
- `uv run pytest tests/openharness_cases/test_entrypoint.py -q`，3 passed。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q`，81 passed。
- `uv run openharness check-tasks`，first run failed because `verification.last_run_result` used free text instead of an allowed result value。
- `final verification command`: `uv run openharness check-tasks`，passed, validated 47 task package(s)。
- `uv run openharness verify update-force-sync`，passed, recorded `.harness/artifacts/OH-045/verification-runs/20260508T084331295546Z.json`。

## Artifact Paths
- `.harness/artifacts/OH-045/verification-runs/20260508T084331295546Z.json`
- `.harness/artifacts/OH-045/verification-runs/latest.json`

## Follow-ups
- 如果未来要支持未跟踪文件清理、stash 或无 upstream 的自动修复，应单独建任务包设计更强的恢复流程和风险确认。
