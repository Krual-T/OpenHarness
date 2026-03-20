# Verification

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`

## Expected Outcomes
- The repository validates design packages against the new required-file set.
- Tests pass with the exploration-centric workflow wording.

## Latest Result
- 2026-03-20: PASS
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run pytest`
- 2026-03-20: PASS after archival
  - `uv run python skills/using-openharness/scripts/openharness.py check-designs`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
