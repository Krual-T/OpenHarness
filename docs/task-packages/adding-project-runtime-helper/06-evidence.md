# Evidence

## Files
- `docs/task-packages/adding-project-runtime-helper/README.md`
- `docs/task-packages/adding-project-runtime-helper/STATUS.yaml`
- `docs/task-packages/adding-project-runtime-helper/01-requirements.md`
- `docs/task-packages/adding-project-runtime-helper/02-overview-design.md`
- `docs/task-packages/adding-project-runtime-helper/03-detailed-design.md`
- `docs/task-packages/adding-project-runtime-helper/05-verification.md`
- `docs/task-packages/adding-project-runtime-helper/06-evidence.md`
- `docs/task-packages/harness-completion-roadmap/README.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task adding-project-runtime-helper OH-016 "Adding Project Runtime Helper" --owner codex --summary "Define when and how a repository should add a new project runtime helper skill under the OpenHarness runtime capability workflow."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Follow-ups
- Productize this package into live routing guidance after `OH-013` and `OH-014` move into implementation.
- Decide whether the repository should ship a runtime helper example template together with the runtime surface map example.
