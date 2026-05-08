# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 先用 TDD 新增 CLI 测试锁定 active 根目录下 `status: archived` 包会自动移动；确认测试先失败后，再实现 discovery 规范化；最后执行完整测试和 task package 校验。
- Executed Path: 已执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py::test_check_tasks_auto_moves_archived_status_from_active_root -q`，先观察到失败，失败点是 archived 目录不存在；实现后同一测试通过。随后执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py -q`，第一次发现旧 validation 测试仍按旧 discovery 语义取包；迁移该测试为直接调用 validation 后，第二次执行通过。最后执行 `uv run pytest -q` 和 `uv run openharness check-tasks`，结果通过。
- Path Notes: 本轮验证覆盖新自动移动行为、显式 `transition <task> archived` 既有路径、validation 位置不变量、完整测试套件和当前仓库 task package 协议校验。`verify` 成功后不会自动归档仍是有意保留的非目标行为。

## Required Commands
- `uv run pytest -q`
- `uv run openharness check-tasks`

## Expected Outcomes
- active 根目录中的 `status: archived` 包在 `cmd_check_tasks` 过程中被移动到 `docs/archived/task-packages/<task>/`。
- 包内 `docs/task-packages/<task>/...` 引用被重写为 `docs/archived/task-packages/<task>/...`。
- 显式 `transition <task> archived` 的现有测试继续通过。
- 全量测试和 task package 校验返回 0。

## Traceability
- 需求 1 由 `test_check_tasks_auto_moves_archived_status_from_active_root` 覆盖，该测试观察 active 路径消失、archived 路径存在和 `cmd_check_tasks` 返回 0。
- 需求 2 由同一测试中的 `STATUS.yaml`、`04-verification.md`、`05-evidence.md` 路径断言覆盖。
- 需求 3 由完整 `test_cli_workflows.py` 回归覆盖，其中既有 `test_transition_to_archived_moves_package_and_rewrites_paths` 继续通过。
- 设计约束“validation 保持最终不变量”由 `test_validate_task_package_directly_rejects_archived_status_in_active_root` 覆盖。

## Risk Acceptance
- 接受 discovery 现在具备窄范围副作用的风险，因为触发条件只限 active 根目录里已经明确写成 `status: archived` 的包，且移动复用事务式 helper。
- 接受没有新增 `verify` 自动归档行为；如果后续要让验证通过触发归档，应另开任务重新设计完成闭环。

## Latest Result
- `uv run pytest -q` 通过，结果为 208 passed。
- `uv run openharness check-tasks` 通过，结果为 Validated 46 task package(s)。
- Latest Artifact: `.harness/artifacts/OH-044/verification-runs/latest.json`
