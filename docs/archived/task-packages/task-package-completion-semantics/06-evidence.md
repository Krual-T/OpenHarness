# Evidence

## Residual Risks
- Older archived packages outside the explicitly updated hotspot set may still use pre-migration wording and should be treated as historical records, not as current protocol examples.

## Manual Steps
- None.

## Files
- `AGENTS.md`
- `skills/using-openharness/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/brainstorming/references/spec-document-reviewer-prompt.md`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/using-openharness/references/templates/task-package.README.md`
- `skills/using-openharness/references/templates/task-package.STATUS.yaml`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.05-verification.md`
- `docs/task-packages/harness-completion-roadmap/README.md`
- `docs/task-packages/harness-completion-roadmap/01-requirements.md`
- `docs/task-packages/harness-completion-roadmap/02-overview-design.md`
- `docs/task-packages/harness-completion-roadmap/03-detailed-design.md`
- `docs/archived/task-packages/python-verification-maturity/README.md`
- `docs/archived/task-packages/python-verification-maturity/03-detailed-design.md`
- `docs/archived/task-packages/python-verification-maturity/05-verification.md`
- `docs/archived/task-packages/task-package-completion-semantics/*`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task task-package-completion-semantics OH-008 "Task Package Completion Semantics" --owner codex --summary "Rename design packages to task packages and tighten completion semantics so archive only means implemented, verified, and no longer active."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `mv docs/task-packages/task-package-completion-semantics docs/archived/task-packages/task-package-completion-semantics`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Follow-ups
- Audit older archived packages incrementally when they are touched, so historical wording does not get mistaken for current protocol.
