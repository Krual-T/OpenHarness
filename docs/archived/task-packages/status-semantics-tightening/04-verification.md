# Verification

## Verification Path
- Planned Path: repository automation
- Executed Path: repository automation
- Path Notes:
  - This package ended with both design clarification and repository implementation alignment.
  - Verification covers the CLI behavior change, the added semantic validation, the template and skill wording updates, and the final archive move.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Expected Outcomes
- The settled status contract remains documented and internally consistent after archive.
- Repository tests continue to pass after the status-semantics implementation waves and archive move.
- `bootstrap` no longer shows `OH-006` in the active package list once it lives under `docs/archived/task-packages/`.

## Latest Result
- Passed on 2026-03-21:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after implementing the first CLI behavior wave for status semantics:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'later_stage_statuses_only or explicit_package_target_before_in_progress'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after implementing lightweight semantic validation for `verifying` and `archived`:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'verifying_without_verification_path or archived_without_verification_path'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after adding lightweight status guidance to task-package templates:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'include_status_guidance'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after adding matching status guidance to workflow skills:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'workflow_skills_include_status_guidance'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after archiving `OH-006 Status Semantics Tightening` and updating repository references:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
