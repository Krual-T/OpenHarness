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
