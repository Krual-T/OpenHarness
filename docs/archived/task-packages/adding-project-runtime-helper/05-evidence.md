# Evidence

## Residual Risks
- 仓库现在已经有 helper-addition 决策流程，但还没有提供一个具体项目 runtime helper 的完整示例或模板。
- 如果真实仓库在采用时仍频繁误用这一流程，后续可能还需要补一个更强的脚手架或轻量机器可读层。

## Manual Steps
- None in this round.

## Files
- `docs/archived/task-packages/adding-project-runtime-helper/README.md`
- `docs/archived/task-packages/adding-project-runtime-helper/STATUS.yaml`
- `docs/archived/task-packages/adding-project-runtime-helper/01-requirements.md`
- `docs/archived/task-packages/adding-project-runtime-helper/02-overview-design.md`
- `docs/archived/task-packages/adding-project-runtime-helper/03-detailed-design.md`
- `docs/archived/task-packages/adding-project-runtime-helper/04-verification.md`
- `docs/archived/task-packages/adding-project-runtime-helper/05-evidence.md`
- `README.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/runtime-capability-contract.md`
- `skills/using-openharness/references/project-runtime-surface-map.md`
- `skills/using-openharness/references/templates/project-runtime-surface-map.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/references/adding-project-runtime-helper.md`
- `skills/using-openharness/tests/test_openharness.py`
- `docs/archived/task-packages/harness-completion-roadmap/*`
- `.project-memory/facts/project_runtime_helper_addition_protocol.yaml`
- `.project-memory/aliases.yaml`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task adding-project-runtime-helper OH-016 "Adding Project Runtime Helper" --owner codex --summary "Define when and how a repository should add a new project runtime helper skill under the OpenHarness runtime capability workflow."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or runtime_surface_map or runtime_helper_reference or readme_describes_runtime_capability_contract or skill_hub_describes_runtime_capability_layer or openharness_skill_routes_runtime_work_through_capability_contract'`
- `uv run python skills/project-memory/scripts/query_memory.py "什么时候新增 project runtime helper"`
- `uv run python skills/project-memory/scripts/save_fact.py project_runtime_helper_addition_protocol --title "OpenHarness 项目运行时 helper 新增流程已产品化" --statement "OpenHarness 通过 skills/using-openharness/references/adding-project-runtime-helper.md 定义项目运行时 helper 的新增流程；当运行时表面已映射且现有 helper 不匹配时，应新增一个窄 helper 并回写运行时表面图、03、05、06；只有在表面、前置条件、驱动方式或证据流仍不清晰时才先开 bootstrap package。" --alias "什么时候新增 project runtime helper" --alias "什么时候新增 runtime helper" --alias "runtime helper 怎么新增" --applies-to skills/using-openharness/SKILL.md --applies-to skills/using-openharness/references/adding-project-runtime-helper.md --applies-to skills/using-openharness/references/project-runtime-surface-map.md --evidence skills/using-openharness/references/adding-project-runtime-helper.md --evidence docs/archived/task-packages/adding-project-runtime-helper/README.md --tag runtime --tag protocol --tag onboarding --tag helper`
- `uv run python skills/using-openharness/scripts/openharness.py transition adding-project-runtime-helper in_progress`
- `uv run python skills/using-openharness/scripts/openharness.py transition adding-project-runtime-helper verifying`
- `uv run python skills/using-openharness/scripts/openharness.py verify adding-project-runtime-helper`
- `uv run python skills/using-openharness/scripts/openharness.py transition adding-project-runtime-helper archived`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`

## Artifact Paths
- `docs/archived/task-packages/adding-project-runtime-helper/04-verification.md`
- `.harness/artifacts/OH-016/verification-runs/20260323T100004667275Z.json`

## Follow-ups
- Decide later whether OpenHarness should ship one concrete project runtime helper example or starter template on top of the helper-addition workflow.
- Watch real repository adoption to see whether doc-first helper-addition guidance is enough or needs a small machine-readable companion later.
