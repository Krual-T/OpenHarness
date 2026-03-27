# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 模板仍然只有短提示，不会主动重复 guidance 的问题清单；新作者仍需通过 skill 或 reference 进入完整写法说明。
- 当前测试主要覆盖 guidance 存在和 skill 引用，尚未把更多“问题清单级”约束提升为自动校验。

## Manual Steps
- 无

## Files
- docs/task-packages/task-package-writing-methodology/README.md
- docs/task-packages/task-package-writing-methodology/STATUS.yaml
- docs/task-packages/task-package-writing-methodology/02-overview-design.md
- docs/task-packages/task-package-writing-methodology/03-detailed-design.md
- docs/task-packages/task-package-writing-methodology/04-verification.md
- docs/task-packages/task-package-writing-methodology/05-evidence.md
- skills/using-openharness/references/requirements-writing-guidance.md
- skills/using-openharness/references/overview-design-writing-guidance.md
- skills/using-openharness/references/detailed-design-writing-guidance.md
- skills/using-openharness/references/verification-writing-guidance.md
- skills/using-openharness/references/evidence-writing-guidance.md
- tests/openharness_cases/test_protocol_docs.py

## Commands
- uv run pytest tests/openharness_cases/test_protocol_docs.py -q
- uv run openharness check-tasks

## Artifact Paths
- 无独立文件产物；关键证据来自最近一次测试与校验命令输出。

## Follow-ups
- 如后续发现模板过于轻量，可单独开包讨论模板提示增强，而不是回到总指南。
- 如后续继续出现形式主义空壳文档，可单独开包讨论把部分 guidance contract 提升为更强校验。
