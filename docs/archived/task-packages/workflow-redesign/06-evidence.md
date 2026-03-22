# Evidence

## Residual Risks
- This package established the fixed protocol shape, but optional compatibility helpers and later status/verification semantics still required follow-up work.

## Files
- `AGENTS.md`
- `README.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/manifest.yaml`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/references/templates/task-package.README.md`
- `skills/using-openharness/references/templates/task-package.STATUS.yaml`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/brainstorming/SKILL.md`

## Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `mv docs/task-packages/workflow-redesign docs/archived/task-packages/workflow-redesign`

## Follow-ups
- Decide later whether `writing-plans`, `executing-plans`, and `subagent-driven-development` should be retired, fully repurposed, or kept as optional compatibility skills.
- Update the remaining non-core skills that still describe `04-implementation-plan.md` so optional compatibility wording is explicit and not misleading.
