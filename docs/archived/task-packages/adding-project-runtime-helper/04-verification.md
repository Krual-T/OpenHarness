# Verification

## Verification Path
- Planned Path:
  - 先运行 `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or runtime_surface_map or runtime_helper_reference or readme_describes_runtime_capability_contract or skill_hub_describes_runtime_capability_layer or openharness_skill_routes_runtime_work_through_capability_contract'`，确认 helper-addition 断言已经覆盖到 live docs。
  - 再运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 与 `uv run pytest`，确认仓库整体仍然通过。
  - 完成归档后再运行 `uv run python skills/using-openharness/scripts/openharness.py bootstrap`，确认 `OH-016` 不再出现在 active task package 列表中。
- Executed Path:
  - 已经先执行过目标化测试 `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or runtime_surface_map or runtime_helper_reference or readme_describes_runtime_capability_contract or skill_hub_describes_runtime_capability_layer or openharness_skill_routes_runtime_work_through_capability_contract'`，确认新增断言在实现前失败、实现后通过。
  - 运行 `uv run python skills/using-openharness/scripts/openharness.py verify adding-project-runtime-helper`，用包级验证记录 `check-tasks` 与全量 `pytest` 的 fresh artifact。
  - 完成 `archived` 迁移与目录移动后，再运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`、`uv run python skills/using-openharness/scripts/openharness.py bootstrap` 与 `uv run pytest`，确认归档后的仓库状态仍然一致。
- Path Notes:
  - 这一轮验证的是文档与协议产品化，不是某个具体项目 runtime helper 的真实运行时闭环。
  - 目标化红绿测试负责证明新增断言不是空断言；`check-tasks`、全量 `pytest` 与归档后的 `bootstrap` 负责证明仓库协议、测试面和 active-package 视图仍然一致。

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- live docs、参考文档、模板、测试与项目记忆对 “reuse / add / bootstrap” 三岔决策保持一致。
- 仓库在归档前后都能通过 task-package 校验与测试套件。
- 归档完成后，`bootstrap` 默认 active 列表里不再出现 `OH-016`。

## Latest Result
- 2026-03-23 通过：
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or runtime_surface_map or runtime_helper_reference or readme_describes_runtime_capability_contract or skill_hub_describes_runtime_capability_layer or openharness_skill_routes_runtime_work_through_capability_contract'`
  - `uv run python skills/using-openharness/scripts/openharness.py verify adding-project-runtime-helper`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
  - 结果：目标化 helper-addition 断言通过，`verify` 记录了 `.harness/artifacts/OH-016/verification-runs/20260323T100004667275Z.json`，归档后 `check-tasks` 仍验证了 `16 task package(s)`，`bootstrap` 只显示 `OH-004` 为 active package，全量测试保持 `53 passed`。
- Latest Artifact:
  - `.harness/artifacts/OH-016/verification-runs/20260323T100004667275Z.json`
