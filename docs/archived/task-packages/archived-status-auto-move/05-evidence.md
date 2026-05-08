# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- discovery 带有自动移动副作用；本轮通过窄触发条件和事务式 helper 控制风险，但未来如果有人把 `status: archived` 当作临时草稿状态使用，会触发移动。
- 自动移动不检查 latest verification artifact；这是本轮刻意保留的差异，因为触发依据是用户已经写入 `status: archived`，而不是 `transition` 的完成前置校验。

## Manual Steps
- 无。

## Files
- `openharness_cli/repository.py`：新增 discovery 期间自动移动 active archived 包的逻辑。
- `tests/openharness_cases/test_cli_workflows.py`：新增自动移动的 CLI 回归测试。
- `tests/openharness_cases/test_task_package_core.py`：迁移旧位置不变量测试，让它直接验证 validation 而不是经过 discovery。
- `docs/archived/task-packages/archived-status-auto-move/*`：记录本轮需求、设计、验证和证据。

## Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py::test_check_tasks_auto_moves_archived_status_from_active_root -q`，先失败后通过，用于 TDD red/green。
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py -q`，最终结果 45 passed。
- `uv run pytest -q`，最终结果 208 passed。
- `uv run openharness check-tasks`，最终结果 Validated 46 task package(s)。
- Final verification command: `uv run openharness verify archived-status-auto-move`。

## Artifact Paths
- `.harness/artifacts/OH-044/verification-runs/latest.json`：由 `uv run openharness verify archived-status-auto-move` 生成的最新验证 artifact。

## Follow-ups
- 暂无。`verify` 成功后自动归档不属于本轮范围；如需该行为，应另行设计它和证据写回之间的顺序关系。
