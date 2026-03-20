# Evidence

## Files
- `AGENTS.md`
- `README.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/manifest.yaml`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/references/templates/design-package.README.md`
- `skills/using-openharness/references/templates/design-package.STATUS.yaml`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/brainstorming/SKILL.md`

## Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `mv docs/designs/workflow-redesign docs/archived/designs/workflow-redesign`

## Follow-ups
- Decide later whether `writing-plans`, `executing-plans`, and `subagent-driven-development` should be retired, fully repurposed, or kept as optional compatibility skills.
- Update the remaining non-core skills that still describe `04-implementation-plan.md` so optional compatibility wording is explicit and not misleading.
