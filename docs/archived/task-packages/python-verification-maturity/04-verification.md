# Verification

## Verification Path
- Planned Path:
  - Task-package validation with `check-tasks`
  - Active-package inventory check with `bootstrap`
  - Repository regression check with `pytest`
- Executed Path:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
- Path Notes:
  - This round verifies the package documents and repository behavior after reframing `OH-007` around Python verification maturity instead of bootstrap routing.
  - This archive round was performed under earlier repository semantics that treated a completed design baseline as ready to leave the active set.
  - A later implementation round should add evidence that the new baseline-versus-runtime wording is carried through docs, templates, and completion rules.

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`

## Expected Outcomes
- `OH-007` validates as a complete historical design-baseline package before archive under the earlier semantics used at that time.
- After the move, `bootstrap` no longer lists `OH-007` as active work.
- Repository tests still pass after adding the reframed child package and updating roadmap docs.

## Latest Result
- Passed on 2026-03-21 after scaffolding `OH-007` and completing the first bootstrap task package:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
- Passed again on 2026-03-22 after narrowing `OH-007` to Python-only cold start with `pytest` as the minimum verification floor:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Passed again on 2026-03-22 after reframing `OH-007` as Python verification maturity and updating roadmap references:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
- Passed again on 2026-03-22 after archiving the completed `OH-007 Python Verification Maturity` package and updating roadmap references:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
