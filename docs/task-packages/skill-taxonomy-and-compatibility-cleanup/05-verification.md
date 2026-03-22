# Verification

## Verification Path
- Planned Path:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Executed Path:
  - Pending implementation.
- Path Notes:
  - This package is currently design-only. Fresh results should be recorded when taxonomy wording and tests are actually updated.

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- The new task package validates cleanly.
- Repository tests pass after taxonomy wording and test expectations are aligned.

## Latest Result
- Passed on 2026-03-22 for the design-package handoff state:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - Result: package validates cleanly, appears in the active package list as `detailed_ready`, and repository tests continue to pass.
- Passed on 2026-03-22 for the direct removal surface:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'retired_skills_are_not_shipped_live or key_repo_skills_are_vendored_locally or optional_execution_skills_are_not_described_as_core_protocol or skill_hub_declares_no_parallel_entry_skill or openharness_skill_is_repo_entry_skill'`
  - Result: 5 passed, confirming the two skills are no longer shipped live and the updated hub / routing docs are internally consistent.
- Passed again on 2026-03-22 after the repository-wide semantic-validation wave landed:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - Result: `check-tasks` validated 11 task packages, `bootstrap` showed `OH-004` and `OH-008` as the active set, and the full test suite passed with `41 passed`.
- Passed on 2026-03-22 for the staged commit snapshot of this removal wave:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
  - Result: `check-tasks` validated 9 task packages, `bootstrap` showed `OH-004` and `OH-008` as the active set, and the staged snapshot test suite passed with `33 passed`.
