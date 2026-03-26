# Verification

## Verification Path
- Planned Path: repository automation
- Executed Path: repository automation
- Path Notes: this package changed validation logic, templates, archived fact-source docs, and tests, so `check-tasks` plus `pytest` were the right completion path

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- `check-tasks` rejects obvious status-to-document contradictions without breaking current repository packages.
- The new semantic checks are covered by repository tests.
- The archived task-package fact sources that remain in scope validate cleanly under the stronger semantics.

## Latest Result
- Passed on 2026-03-22 after landing semantic-anchor validation, updating historical archived fact sources, and aligning templates:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'placeholder_requirements or overview_ready_without_reflection or archived_without_evidence_anchors or accepts_detailed_ready_with_filled_semantic_anchors'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'declared_manual_scenarios or no_declared_verification_path or later_stage_statuses_only or explicit_package_target_before_in_progress'`
  - `uv run pytest`
