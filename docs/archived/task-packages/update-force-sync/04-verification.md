# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - 先运行新增 update 行为测试，确认 `--force-sync` 在实现前失败。
  - 实现后运行 update targeted 测试、帮助页测试、相关 CLI/协议测试和 task package 协议校验。
- Executed Path:
  - 已执行 red 测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，结果为 3 failed、2 passed、21 deselected；失败原因是当前 handler 忽略 `force_sync`，仍执行 `git pull`。
  - 已执行 green targeted 测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`，结果为 5 passed、21 deselected。
  - 已执行帮助页测试：`uv run pytest tests/openharness_cases/test_entrypoint.py -q`，结果为 3 passed。
  - 已执行相关完整测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q`，结果为 81 passed。
  - 已执行协议校验：`uv run openharness check-tasks`，首次结果为 failed，因为 `STATUS.yaml.verification.last_run_result` 误写为自由文本，不符合允许值 `passed`、`failed`、`insufficient_verification`。
  - 修正状态值后重跑 `uv run openharness check-tasks`，结果为通过，输出为 validated 47 task package(s)。
  - 已执行归档前正式验证：`uv run openharness verify update-force-sync`，结果为通过，并生成 JSON verification artifact。
- Path Notes:
  - 没有真实执行 `git fetch`、`git reset --hard` 或 `uv tool upgrade openharness`，因为真实强制同步会破坏当前开发工作树；本轮用 monkeypatch 观察命令序列和失败中断，覆盖 CLI handler 契约。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest tests/openharness_cases/test_cli_workflows.py -k update -q`
- `uv run pytest tests/openharness_cases/test_entrypoint.py -q`
- `uv run pytest tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_entrypoint.py tests/openharness_cases/test_protocol_docs.py -q`
- `uv run openharness check-tasks`
- 归档前执行 `uv run openharness verify update-force-sync`，由 CLI 运行上述 required commands 并记录 JSON artifact。

## Expected Outcomes
- update targeted 测试应观察到默认路径仍为 `git pull` 后 `uv tool upgrade openharness`。
- `--force-sync` 测试应观察到 `git fetch --prune`、`git reset --hard '@{u}'`、`uv tool upgrade openharness` 的顺序。
- 强制同步任一步失败时，不应继续执行工具升级。
- `update --help` 应包含 `--force-sync` 和 discard local changes 风险说明。

## Traceability
- 需求 1 由 `test_parser_help_includes_overview_and_update_behavior` 覆盖，证明参数和帮助文案可见。
- 需求 2 由 `test_update_runs_git_pull_then_uv_tool_upgrade_in_repo_root` 覆盖，证明默认路径兼容。
- 需求 3 由三个 `test_update_force_sync_*` 覆盖，证明强制同步顺序和失败中断。
- 需求 4 由 `INSTALL.codex.md` 更新和帮助页断言覆盖，证明用户可见风险提示。

## Risk Acceptance
- 接受没有真实执行强制同步命令的风险，因为真实命令会修改当前仓库；handler 的可验证契约是命令顺序、repo root 和失败中断。
- 接受没有处理无上游跟踪分支的风险；该情况下 `git reset --hard '@{u}'` 会失败，并且 handler 会停止，不会继续工具升级。

## Latest Result
- 截至 2026-05-08T08:43:31Z，`uv run openharness verify update-force-sync` 通过；pytest 相关验证和 `check-tasks` 均为 exit code 0。
- Latest Artifact: `.harness/artifacts/OH-045/verification-runs/20260508T084331295546Z.json`
