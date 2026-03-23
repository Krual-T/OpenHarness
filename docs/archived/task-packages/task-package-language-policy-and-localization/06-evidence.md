# Evidence

## Residual Risks
- 本轮只完成第一阶段，仍未实现中文章节标题支持。
- 现有历史 task package 还没有整体迁移到中文正文，后续只会先从新包和增量更新开始生效。

## Manual Steps
- 本轮无额外人工步骤。

## Files
- `AGENTS.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/templates/task-package.README.md`
- `skills/using-openharness/references/templates/task-package.01-requirements.md`
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.05-verification.md`
- `skills/using-openharness/references/templates/task-package.06-evidence.md`
- `skills/using-openharness/tests/test_openharness.py`
- `.project-memory/decisions/task_package_language_policy_phase_one.yaml`
- `docs/archived/task-packages/task-package-language-policy-and-localization/README.md`
- `docs/archived/task-packages/task-package-language-policy-and-localization/STATUS.yaml`
- `docs/archived/task-packages/task-package-language-policy-and-localization/01-requirements.md`
- `docs/archived/task-packages/task-package-language-policy-and-localization/02-overview-design.md`
- `docs/archived/task-packages/task-package-language-policy-and-localization/03-detailed-design.md`
- `docs/archived/task-packages/task-package-language-policy-and-localization/05-verification.md`
- `docs/archived/task-packages/task-package-language-policy-and-localization/06-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py transition task-package-language-policy-and-localization in_progress`
- `uv run python skills/using-openharness/scripts/openharness.py transition task-package-language-policy-and-localization verifying`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'language_policy or chinese_narrative or repo_protocol_documents_task_package_language_policy'`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py transition task-package-language-policy-and-localization archived`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/project-memory/scripts/query_memory.py "task package 语言策略"`
- `uv run python skills/project-memory/scripts/save_decision.py task_package_language_policy_phase_one ...`

## Artifact Paths
- `.harness/artifacts/OH-015/verification-runs/latest.json`

## Follow-ups
- 如需把章节标题也本地化，单独开启第二阶段实现包，同时修改模板、校验器与测试。
- 视实际使用情况决定是否要逐步把现有高频 task package 正文补成中文。
