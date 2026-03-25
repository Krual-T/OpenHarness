# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k "new_task or legacy_positional or task_package_commands_use_current_handlers_only"`
  - `uv run pytest skills/using-openharness/tests/test_openharness.py`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Executed Path:
  - 已执行 `uv run pytest skills/using-openharness/tests/test_openharness.py -k "new_task or legacy_positional or task_package_commands_use_current_handlers_only"`，结果为 5 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，结果为 75 passed。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，结果为通过，校验了 28 个任务包。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py new-task --help`，确认帮助输出中不再出现 `legacy_task_id` 与 `legacy_title`。
- Path Notes:
  - 聚焦测试先覆盖 `new-task` 的接口收紧，再用完整 harness 测试和任务包校验确认没有破坏其他协议行为。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k "new_task or legacy_positional or task_package_commands_use_current_handlers_only"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 聚焦测试通过。
- 完整 harness 测试通过。
- `check-tasks` 通过。
- 旧位置参数形式不再被 parser 接受。

## Traceability
- `01-requirements.md` 定义了删除旧位置参数兼容的完成条件。
- `02-overview-design.md` 说明为什么必须在 parser 层切断旧接口。
- `03-detailed-design.md` 具体化了测试和实现落点。
- 本文件承接执行结果。

## Risk Acceptance
- 当前接受的风险是：若外部还有未更新的旧脚本，它们会立即失败。
- 这个风险可以接受，因为显式失败优于静默误建目录。

## Latest Result
- 2026-03-25 已完成本轮全部必需验证，结果通过。
- Latest Artifact:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py new-task --help`
