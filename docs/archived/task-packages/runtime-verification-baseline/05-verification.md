# Verification

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- The new child package is structurally valid.
- Existing repository tests continue to pass after adding the child package scaffolding and early design content.

## Latest Result
- Passed on 2026-03-20:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-20 after exploration refined the rollout strategy to docs-first, CLI-assisted semantics and after restoring `AGENTS.md` to the repository's tested workflow baseline:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-20 after implementing the first runtime-verification rollout wave in templates and verification-oriented skills:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Passed again on 2026-03-20 after implementing the second rollout wave in `openharness.py verify` and its targeted tests:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'declared_manual_scenarios or no_declared_verification_path'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- Passed again on 2026-03-20 after archiving the completed package under `docs/archived/task-packages/runtime-verification-baseline`:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
