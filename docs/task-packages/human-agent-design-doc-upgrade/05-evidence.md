# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 当前还没有自动校验 `PlantUML` 图是否存在、是否语法正确。
- 新 contract 解决的是“写作 guidance 和脚手架提示”，并不保证每个未来 package 都会把设计写得足够好。
- 当前仓库还有一个无关 active package `project-memory-cli-integration` 的 `STATUS.yaml` 解析失败，会阻塞整仓级 harness 验证。

## Manual Steps
- 无。

## Files
- docs/task-packages/human-agent-design-doc-upgrade/STATUS.yaml
- docs/task-packages/human-agent-design-doc-upgrade/01-requirements.md
- docs/task-packages/human-agent-design-doc-upgrade/02-overview-design.md
- docs/task-packages/human-agent-design-doc-upgrade/03-detailed-design.md
- docs/task-packages/human-agent-design-doc-upgrade/04-verification.md
- docs/task-packages/human-agent-design-doc-upgrade/05-evidence.md
- skills/using-openharness/references/overview-design-writing-guidance.md
- skills/using-openharness/references/detailed-design-writing-guidance.md
- skills/using-openharness/references/templates/task-package.02-overview-design.md
- skills/using-openharness/references/templates/task-package.03-detailed-design.md
- skills/using-openharness/references/author-entry.md
- tests/openharness_cases/test_protocol_docs.py
- tests/openharness_cases/test_task_package_core.py
- .project-memory/decisions/human_agent_design_docs_require_structured_collaboration_contracts.yaml

## Commands
- openharness bootstrap
- openharness new-task human-agent-design-doc-upgrade --auto-id --title "Human-Agent Design Doc Upgrade" --summary "Strengthen overview and detailed design guidance for human-agent collaboration, including diagram guidance."
- uv run pytest tests/openharness_cases/test_protocol_docs.py -k "task_package_writing_guidance_references_define_stage_contracts or design_package_templates_include_verification_path_sections"
- uv run pytest tests/openharness_cases/test_task_package_core.py -k live_templates_scaffold_human_agent_design_prompts
- uv run pytest tests/openharness_cases/test_protocol_docs.py tests/openharness_cases/test_cli_workflows.py tests/openharness_cases/test_task_package_core.py  `final verification command`
- openharness verify human-agent-design-doc-upgrade
- uv run scripts/query_memory.py "overview detailed design guidance human agent PlantUML"
- uv run scripts/save_decision.py human_agent_design_docs_require_structured_collaboration_contracts ...

## Artifact Paths
- .harness/artifacts/OH-038/verification-runs/20260330T080539614631Z.json

## Follow-ups
- 如果后续多个 task package 依旧缺图或图文关系混乱，可以再开一轮任务，决定是否把 `PlantUML` 提示升级为更强约束或校验。
- 如果未来发现 overview/detailed 仍有边界重叠，再依据真实使用样本细化 guidance，而不是重新合并文档。
- 等 `project-memory-cli-integration` 或其他无关坏包修复后，应重跑 `openharness verify human-agent-design-doc-upgrade` 与 `openharness check-tasks`，再决定是否归档 `OH-038`。
