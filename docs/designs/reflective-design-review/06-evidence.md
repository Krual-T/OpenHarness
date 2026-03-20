# Evidence

## Files
- `docs/designs/reflective-design-review/*`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/using-openharness/tests/test_openharness.py`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-design reflective-design-review OH-003 "Reflective Design Review Loop" --owner codex --summary "Add explicit reflection and optional subagent discussion loops around overview design and detailed design so architecture choices are challenged before implementation."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Follow-ups
- Decide whether the reflection loop should become a dedicated skill, a review prompt, or a lightweight section inside existing core skills.
- Thread the reflection/subagent discussion requirement into the core workflow docs and skills in a follow-up implementation round.
