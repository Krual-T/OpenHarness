# Verification

## Verification Path
- Planned Path:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Executed Path:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
- Path Notes:
  - This package now includes live skill retirement, live-doc cleanup, archived-history cleanup, and test updates.

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- The new task package validates cleanly.
- Repository tests pass after taxonomy wording and test expectations are aligned.

## Latest Result
- Passed on 2026-03-22 after retiring the old plan-oriented skill surface and cleaning live plus archived references:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
  - Result: the repository validates cleanly, the full test suite passes, and `bootstrap` shows only `OH-004` in the active set after archival.
- Passed again on 2026-03-23 after adding duplicate-task-id protection and cleaning remaining archive inconsistencies:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'design_packages_validate_cleanly or find_duplicate_task_ids_reports_conflicts'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
  - Result: duplicate task ids are now guarded by tests and `check-tasks`, `OH-008` remains archived cleanly, and `bootstrap` still shows only `OH-004` as active.
