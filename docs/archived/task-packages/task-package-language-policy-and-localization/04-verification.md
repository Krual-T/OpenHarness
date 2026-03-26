# Verification

## Verification Path
- Planned Path:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'language_policy or chinese_narrative or repo_protocol_documents_task_package_language_policy'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Executed Path:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'language_policy or chinese_narrative or repo_protocol_documents_task_package_language_policy'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Path Notes:
  - 本轮是第一阶段语言策略的真实落地，不再只是设计验证；需要同时验证新增约束、仓库协议校验和全量回归。

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'language_policy or chinese_narrative or repo_protocol_documents_task_package_language_policy'`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- 新增的模板与协议文档测试通过。
- `check-tasks` 仍能正常校验 task package 结构。
- 仓库测试套件在引入第一阶段语言策略后仍然通过。

## Latest Result
- 2026-03-23 验证通过：
  - 定向测试通过，结果为 `2 passed, 44 deselected`
  - `check-tasks` 成功校验 `16` 个 task package
  - 全量测试通过，结果为 `46 passed`
  - 归档后再次执行 `bootstrap`，active 列表中不再出现 `OH-015`
- Latest Artifact:
  - `.harness/artifacts/OH-015/verification-runs/latest.json`
