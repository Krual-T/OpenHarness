# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 入口兼容面可能比当前识别的顶层符号更多，需要在测试拆分与重构过程中持续补齐。
- 测试拆分后的命名如果处理不好，可能出现重复收集或漏收集；本轮通过保留单一入口聚合文件规避了这类风险。

## Manual Steps
- 当前无额外人工步骤；实现完成后如需人工检查 CLI 文本输出，再补充。

## Files
- docs/archived/task-packages/openharness-cli-modularization/README.md
- docs/archived/task-packages/openharness-cli-modularization/STATUS.yaml
- docs/archived/task-packages/openharness-cli-modularization/01-requirements.md
- docs/archived/task-packages/openharness-cli-modularization/02-overview-design.md
- docs/archived/task-packages/openharness-cli-modularization/03-detailed-design.md
- docs/archived/task-packages/openharness-cli-modularization/05-verification.md
- docs/archived/task-packages/openharness-cli-modularization/06-evidence.md
- skills/using-openharness/scripts/openharness.py
- skills/using-openharness/scripts/openharness_cli/__init__.py
- skills/using-openharness/scripts/openharness_cli/cli.py
- skills/using-openharness/scripts/openharness_cli/commands.py
- skills/using-openharness/scripts/openharness_cli/constants.py
- skills/using-openharness/scripts/openharness_cli/lifecycle.py
- skills/using-openharness/scripts/openharness_cli/models.py
- skills/using-openharness/scripts/openharness_cli/repository.py
- skills/using-openharness/scripts/openharness_cli/validation.py
- skills/using-openharness/tests/test_openharness.py
- skills/using-openharness/tests/openharness_cases/__init__.py
- skills/using-openharness/tests/openharness_cases/common.py
- skills/using-openharness/tests/openharness_cases/test_cli_workflows.py
- skills/using-openharness/tests/openharness_cases/test_entrypoint.py
- skills/using-openharness/tests/openharness_cases/test_protocol_docs.py
- skills/using-openharness/tests/openharness_cases/test_task_package_core.py

## Commands
- uv run python skills/using-openharness/scripts/openharness.py bootstrap
- uv run python skills/using-openharness/scripts/openharness.py new-task openharness-cli-modularization --title "Openharness CLI Modularization" --auto-id --owner codex --summary "拆分 using-openharness CLI 与测试，降低集中度并保持两个入口文件稳定"
- git log --oneline -5 -- skills/using-openharness
- rg --files skills/using-openharness | sort
- rg -n "^def |^class " skills/using-openharness/scripts/openharness.py
- rg -n "^def test_" skills/using-openharness/tests/test_openharness.py
- uv run pytest skills/using-openharness/tests/test_openharness.py -k entrypoint_re_exports_package_main_and_parser
- uv run pytest skills/using-openharness/tests/test_openharness.py
- uv run python -m py_compile skills/using-openharness/scripts/openharness.py skills/using-openharness/scripts/openharness_cli/*.py skills/using-openharness/tests/openharness_cases/*.py skills/using-openharness/tests/test_openharness.py
- uv run python skills/using-openharness/scripts/openharness.py check-tasks
- uv run python skills/using-openharness/scripts/openharness.py transition openharness-cli-modularization in_progress
- uv run python skills/using-openharness/scripts/openharness.py transition openharness-cli-modularization verifying
- uv run python skills/using-openharness/scripts/openharness.py verify OH-019

## Artifact Paths
- .harness/artifacts/OH-019/verification-runs/latest.json

## Follow-ups
- 如果拆分后共享 fixture 明显重复，再评估是否补 `conftest.py`。
- 如果未来要继续压缩复杂度，可以把 task package 构造样例提炼成测试辅助工厂。
