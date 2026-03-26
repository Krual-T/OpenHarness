# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- archived package 的旧正文内容仍然大量提到旧测试路径和脚本路径，但它们现在由 `docs/archived/legacy/` 快照兜住，不影响协议校验。
- 本轮没有去规范 legacy 快照的长期裁剪策略，后续如果历史镜像继续增大，需要单独治理。

## Manual Steps
- 无。

## Files
- pyproject.toml
- openharness_cli/validation.py
- skills/using-openharness/SKILL.md
- tests/test_openharness.py
- tests/openharness_cases/common.py
- tests/openharness_cases/test_cli_workflows.py
- tests/openharness_cases/test_entrypoint.py
- tests/openharness_cases/test_protocol_docs.py
- tests/openharness_cases/test_task_package_core.py
- docs/archived/legacy/skills/using-openharness/scripts/openharness.py
- docs/archived/legacy/skills/using-openharness/tests/test_openharness.py
- docs/archived/legacy/skills/using-openharness/tests/openharness_cases/__init__.py
- docs/archived/legacy/skills/using-openharness/tests/openharness_cases/common.py
- docs/archived/legacy/skills/using-openharness/tests/openharness_cases/test_cli_workflows.py
- docs/archived/legacy/skills/using-openharness/tests/openharness_cases/test_entrypoint.py
- docs/archived/legacy/skills/using-openharness/tests/openharness_cases/test_protocol_docs.py
- docs/archived/legacy/skills/using-openharness/tests/openharness_cases/test_task_package_core.py

## Commands
- openharness new-task openharness-top-level-tests-and-cli-entry --auto-id --title "Move OpenHarness Tests To Top Level And Remove Script Compatibility Entry" --owner codex --summary "Move OpenHarness self-tests to the repository top-level tests tree and remove the legacy skill script entrypoint in favor of the packaged CLI module."
- uv run pytest tests/openharness_cases/test_entrypoint.py -q
- uv run pytest tests/openharness_cases/test_protocol_docs.py -q
- uv run pytest tests/openharness_cases/test_task_package_core.py -q
- uv run pytest tests/openharness_cases/test_cli_workflows.py -q
- uv run openharness check-tasks

## Artifact Paths
- No generated artifact files.

## Follow-ups
- 如果后续需要进一步简化 archived 证据校验，可以单独定义“legacy snapshot retention”策略，而不是继续扩散到运行时结构。
