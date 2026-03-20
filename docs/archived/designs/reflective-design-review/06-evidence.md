# Evidence

## Files
- `docs/archived/designs/reflective-design-review/*`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
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
- `uv run python skills/using-openharness/scripts/openharness.py new-design reflective-design-review OH-003 "Reflective Design Review Loop" --owner codex --summary "Add explicit reflection and optional subagent discussion loops around overview design and detailed design so architecture choices are challenged before implementation."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap && uv run python skills/using-openharness/scripts/openharness.py check-designs`

## Follow-ups
- Decide whether the reflection loop should become a dedicated skill, a review prompt, or a lightweight section inside existing core skills.
- If bounded subagent design review becomes common enough, extract a dedicated prompt or skill instead of keeping it implicit inside the core workflow text.
