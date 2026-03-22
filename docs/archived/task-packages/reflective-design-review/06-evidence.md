# Evidence

## Residual Risks
- Reflection quality still depends on agent honesty and skill wording; this package did not add a separate reflection runner or stronger machine enforcement.

## Files
- `docs/archived/task-packages/reflective-design-review/*`
- `skills/subagent-driven-development/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/using-openharness/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/brainstorming/SKILL.md`
- `README.md`
- `AGENTS.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task reflective-design-review OH-003 "Reflective Design Review Loop" --owner codex --summary "Add explicit reflection and optional subagent discussion loops around overview design and detailed design so architecture choices are challenged before implementation."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap && uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Follow-ups
- Decide whether the reflection loop should become a dedicated skill, a review prompt, or a lightweight section inside existing core skills.
- If bounded subagent design review becomes common enough, extract a dedicated prompt or skill instead of keeping it implicit inside the core workflow text.
