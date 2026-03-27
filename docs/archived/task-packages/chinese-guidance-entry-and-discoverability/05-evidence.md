# Evidence

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Residual Risks
- 目前主要残余风险不是“未实现”，而是缺少正式人工 walkthrough 证据。
- 中文作者入口已经进入 bootstrap、`AGENTS.md` 和关键 skill，但真实用户反馈仍可能暴露入口文案需要进一步收紧。

## Manual Steps
- 建议后续由中文用户从“首次进入仓库”的视角走一遍 `AGENTS.md` -> `openharness bootstrap` -> `author-entry.md` 的路径，确认发现成本是否明显下降。

## Files
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/README.md
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/STATUS.yaml
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/01-requirements.md
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/02-overview-design.md
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/03-detailed-design.md
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/04-verification.md
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/05-evidence.md
- AGENTS.md
- openharness_cli/commands.py
- skills/using-openharness/SKILL.md
- skills/brainstorming/SKILL.md
- skills/exploring-solution-space/SKILL.md
- skills/verification-before-completion/SKILL.md
- skills/using-openharness/references/author-entry.md
- skills/using-openharness/references/skill-hub.md
- skills/using-openharness/references/templates/task-package.01-requirements.md
- skills/using-openharness/references/templates/task-package.02-overview-design.md
- skills/using-openharness/references/templates/task-package.03-detailed-design.md
- skills/using-openharness/references/templates/task-package.04-verification.md
- skills/using-openharness/references/templates/task-package.05-evidence.md
- tests/openharness_cases/test_cli_workflows.py
- tests/openharness_cases/test_protocol_docs.py

## Commands
- uv run openharness bootstrap
- uv run openharness new-task chinese-guidance-entry-and-discoverability --auto-id --title "Chinese Guidance Entry And Discoverability" --owner codex --summary "Improve Chinese-first discoverability of task-package guidance and reduce protocol-only friction for new maintainers."
- uv run pytest tests/openharness_cases/test_cli_workflows.py -k 'author_entry or stage_guidance' -q
- uv run pytest tests/openharness_cases/test_protocol_docs.py -k 'author_entry_reference_exists or stage_skills_and_hub_expose_split_task_package_writing_guidance' -q
- uv run pytest tests/openharness_cases/test_cli_workflows.py -q
- uv run pytest tests/openharness_cases/test_protocol_docs.py -q
- uv run openharness check-tasks
- final verification command: uv run openharness verify --design chinese-guidance-entry-and-discoverability

## Artifact Paths
- docs/archived/task-packages/chinese-guidance-entry-and-discoverability/
- .harness/artifacts/

## Follow-ups
- 通过状态流把该包推进到 `archived`。
- 如果后续中文用户反馈入口仍然不够直观，再另开 task package 优化入口文案与 walkthrough 证据。
