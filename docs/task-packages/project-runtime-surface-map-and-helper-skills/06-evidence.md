# Evidence

## Residual Risks
- The package defines onboarding structure but does not yet ship live examples or templates.
- Real repositories may reveal an additional need for lightweight examples before full helper-skill guidance is easy to adopt.

## Manual Steps
- None in this round.

## Files
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/README.md`
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/STATUS.yaml`
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/01-requirements.md`
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/02-overview-design.md`
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/03-detailed-design.md`
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/05-verification.md`
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/06-evidence.md`
- `docs/task-packages/harness-completion-roadmap/*`
- `docs/archived/task-packages/runtime-verification-baseline/*`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task project-runtime-surface-map-and-helper-skills OH-014 "Project Runtime Surface Map And Helper Skills" --owner codex --summary "Define how a repository should map its runtime surfaces and attach multiple project-specific runtime helper skills to the OpenHarness workflow without collapsing them into one generic debug skill."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Artifact Paths
- `docs/task-packages/project-runtime-surface-map-and-helper-skills/05-verification.md`

## Follow-ups
- Productize this structure in live docs, examples, or templates.
- Decide later whether repositories should get a default runtime surface map example artifact.
