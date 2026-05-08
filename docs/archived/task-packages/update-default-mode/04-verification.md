# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先运行新增 update 行为测试，确认默认模式配置相关断言在实现前失败。
  - 实现后运行 update targeted 测试、帮助页测试、相关 CLI/协议测试和 task package 协议校验。
- Executed Path:
  - 已执行 red 测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，结果为 3 failed、7 passed、21 deselected；失败原因是当前实现忽略默认模式配置，设置默认值时仍执行 update，配置为 `force-sync` 时仍走 `git pull`。
  - 已执行 green targeted 测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，结果为 10 passed、21 deselected。
  - 已执行帮助页测试：`uv run pytest tests/openharness_cases/test_entrypoint.py -q`，结果为 3 passed。
  - 已执行相关完整测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q`，结果为 86 passed。
  - 已执行协议校验：`uv run openharness check-tasks`，结果为通过，输出为 validated 48 task package(s)。
- Path Notes:
  - 没有真实执行 `git pull`、`git reset` 或 `uv tool upgrade openharness`；本轮通过 monkeypatch 观察命令序列，避免破坏当前工作树，同时覆盖 handler 的模式选择和失败中断契约。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`
- `uv run pytest tests/openharness_cases/test_entrypoint.py -q`
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q`
- `uv run openharness check-tasks`

## Expected Outcomes
- 未配置默认模式时，`openharness update` 仍执行 `git pull` 后 `uv tool upgrade openharness`。
- `--set-default-mode force-sync` 写入配置并退出，不执行 update。
- 配置默认模式为 `force-sync` 后，无参数 update 执行强制同步路径。
- `--mode pull` 和 `--force-sync` 能覆盖保存的默认模式。
- 非法配置模式返回 1，且不执行 `git` 或 `uv`。

## Traceability
- 需求 1 由 `test_update_set_default_mode_writes_config_without_running_update` 覆盖。
- 需求 2 由 parser `choices` 和帮助页断言覆盖。
- 需求 3 由 `test_update_uses_configured_force_sync_default` 及既有默认路径测试覆盖。
- 需求 4 由 `test_update_mode_overrides_configured_force_sync_default` 和 `test_update_force_sync_overrides_configured_pull_default` 覆盖。
- 需求 5 由 `test_update_invalid_configured_default_mode_stops_before_commands` 覆盖。

## Risk Acceptance
- 接受没有真实运行破坏性同步命令的风险；命令序列和失败中断是本轮可自动验证的核心契约。
- 接受没有新增通用配置命令；当前只有一个配置项，先保持局部 helper，避免过早扩大 API。

## Latest Result
- 截至 2026-05-08T16:51:02+08:00，pytest 相关验证和 `check-tasks` 均通过。
- Latest Artifact: `.harness/artifacts/OH-046/verification-runs/latest.json`
