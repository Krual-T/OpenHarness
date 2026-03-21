# Verification

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`

## Expected Outcomes
- The roadmap package validates cleanly.
- The existing repository tests continue to pass with the new active package added.

## Latest Result
- Passed on 2026-03-20:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - Result after tightening exploration-to-design workflow wording in the core skill docs.
- Passed again on 2026-03-20 after splitting `OH-005 Runtime Verification Baseline`:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-20 after removing mandatory user approval pauses from the default brainstorming flow:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
- Passed again on 2026-03-20 after archiving the completed `OH-005 Runtime Verification Baseline` package and updating roadmap references:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after scaffolding `OH-006 Status Semantics Tightening` and promoting it to an active child package:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after `OH-006` completed the first status-semantics CLI tightening wave:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after `OH-006` added lightweight semantic validation for later-stage status contradictions:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after `OH-006` added lightweight status guidance to design-package templates:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after `OH-006` added matching status guidance to workflow skills:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-21 after archiving `OH-006 Status Semantics Tightening` and updating roadmap references:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed on 2026-03-21 after scaffolding `OH-007 No-Harness Bootstrap Workflow` and updating roadmap references:
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
