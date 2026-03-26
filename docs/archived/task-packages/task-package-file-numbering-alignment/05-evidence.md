# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 这轮会造成大量 archived task package 文本 diff，因为真实文件名和路径引用都改了；这是结构收敛的直接成本。
- 如果后续仍有人在仓库外部工具里硬编码旧文件名，需要他们单独跟进切换。

## Manual Steps
- 无。

## Files
- AGENTS.md
- skills/using-openharness/references/manifest.yaml
- skills/using-openharness/references/runtime-capability-contract.md
- skills/using-openharness/references/project-runtime-surface-map.md
- skills/using-openharness/references/adding-project-runtime-helper.md
- skills/using-openharness/references/templates/task-package.README.md
- skills/using-openharness/references/templates/task-package.STATUS.yaml
- skills/using-openharness/references/templates/task-package.04-verification.md
- skills/using-openharness/references/templates/task-package.05-evidence.md
- openharness_cli/constants.py
- tests/openharness_cases/test_protocol_docs.py
- tests/openharness_cases/test_task_package_core.py
- tests/openharness_cases/test_cli_workflows.py
- docs/task-packages/
- docs/archived/task-packages/

## Commands
- openharness new-task task-package-file-numbering-alignment --auto-id --title "Align Task Package File Numbering" --owner codex --summary "Renumber task package verification and evidence files to a continuous sequence and update the harness protocol accordingly."
- uv run pytest tests/openharness_cases/test_protocol_docs.py -q
- uv run pytest tests/openharness_cases/test_task_package_core.py -q
- uv run pytest tests/openharness_cases/test_cli_workflows.py -q
- uv run openharness check-tasks
- uv run pytest -q

## Artifact Paths
- No generated artifact files.

## Follow-ups
- 如果后续要进一步减少 archived task package 的大规模路径改动，可以单独定义“历史叙述与现行路径分离”的归档策略，但这不是本轮目标。
