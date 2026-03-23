# Evidence

## Residual Risks
- The repository now ships the runtime-surface-map reference and starter template, but it still does not ship a concrete project runtime helper example.
- Real repositories may still reveal a need for a small machine-readable layer if doc-first routing proves too weak in practice.

## Manual Steps
- None in this round.

## Files
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/README.md`
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/STATUS.yaml`
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/01-requirements.md`
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/02-overview-design.md`
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/03-detailed-design.md`
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/05-verification.md`
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/06-evidence.md`
- `README.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/runtime-capability-contract.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/references/project-runtime-surface-map.md`
- `skills/using-openharness/references/templates/project-runtime-surface-map.md`
- `skills/using-openharness/tests/test_openharness.py`
- `docs/task-packages/harness-completion-roadmap/*`
- `docs/archived/task-packages/adding-project-runtime-helper/06-evidence.md`
- `.project-memory/facts/project_runtime_surface_map_protocol.yaml`
- `.project-memory/aliases.yaml`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task project-runtime-surface-map-and-helper-skills OH-014 "Project Runtime Surface Map And Helper Skills" --owner codex --summary "Define how a repository should map its runtime surfaces and attach multiple project-specific runtime helper skills to the OpenHarness workflow without collapsing them into one generic debug skill."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_surface_map or runtime_capability or capability_contract'`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/project-memory/scripts/query_memory.py "运行时表面图 runtime surface map"`
- `uv run python skills/project-memory/scripts/save_fact.py project_runtime_surface_map_protocol --title "OpenHarness 项目运行时表面图已产品化" --statement "OpenHarness 通过 skills/using-openharness/references/project-runtime-surface-map.md 定义项目运行时表面图；仓库应为每个运行时表面声明用途、前置条件、驱动方式、观察点、成功标准、失败证据，以及关联的 helper skill 或 bootstrap package，并把执行结果回写到 03、05、06。" --alias "运行时表面图在哪里" --alias "runtime surface map 怎么写" --alias "项目运行时表面图包含什么" --applies-to skills/using-openharness/SKILL.md --applies-to skills/using-openharness/references/project-runtime-surface-map.md --applies-to skills/using-openharness/references/templates/project-runtime-surface-map.md --evidence skills/using-openharness/references/project-runtime-surface-map.md --evidence skills/using-openharness/references/templates/project-runtime-surface-map.md --tag runtime --tag protocol --tag onboarding`
- `uv run python skills/using-openharness/scripts/openharness.py transition project-runtime-surface-map-and-helper-skills in_progress`
- `uv run python skills/using-openharness/scripts/openharness.py transition project-runtime-surface-map-and-helper-skills verifying`
- `uv run python skills/using-openharness/scripts/openharness.py verify project-runtime-surface-map-and-helper-skills`
- `uv run python skills/using-openharness/scripts/openharness.py transition project-runtime-surface-map-and-helper-skills archived`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Artifact Paths
- `docs/archived/task-packages/project-runtime-surface-map-and-helper-skills/05-verification.md`

## Follow-ups
- Archived `OH-016 Adding Project Runtime Helper` now carries the focused helper-addition workflow on top of archived `OH-014`.
- Decide later whether the repository should add one concrete project runtime helper example on top of the starter runtime surface map template.
