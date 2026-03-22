# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest`
- Fallback Path:
  - if repo-local path discovery or dependency bootstrapping breaks, record the blocking command and keep the package below any completion claim
- Planned Evidence:
  - a self-hosting package tree the CLI can discover
  - passing repository validation and tests
  - updated top-level docs with corrected repository identity and paths

## Files Added Or Changed
- Add `pyproject.toml` with runtime dependency `PyYAML` and dev dependency `pytest`.
- Update `skills/using-openharness/scripts/openharness.py` to resolve repo-local manifests and templates from `skills/using-openharness/...`.
- Add the initial task package under `docs/archived/task-packages/self-hosting-bootstrap/`.
- Rewrite `skills/using-openharness/tests/test_openharness.py` to validate the real repo layout and a minimal self-hosting package inventory.
- Fix small doc mistakes in `AGENTS.md` and `README.md`.

## Interfaces
- `openharness.py bootstrap` must work against the current repository root with no undeclared Python packages.
- `load_manifest()` must prefer repo-local `skills/using-openharness/references/manifest.yaml` when present.
- `create_design_package()` must prefer repo-local `skills/using-openharness/references/templates/` when present.
- The package `STATUS.yaml` for this round declares the commands used for self-host verification.

## Error Handling
- If no task packages exist, `bootstrap` may still succeed with an empty inventory, but after this round `check-tasks` and tests should have a valid package to inspect.
- Repo-local path discovery must keep existing fallback paths so installed/global skill layouts still work.

## Migration Notes
- This round intentionally focused on self-hosting bootstrap; protocol simplification is tracked separately in `OH-002`.
- The rewritten tests should stop depending on inherited historical packages from other repositories.

## Detailed Reflection
- I checked whether the self-hosting package should also solve later workflow semantics. It should not; that would have mixed bootstrap and redesign into one unstable round.
- I checked whether the repository needed a custom verification harness immediately. It did not; standard bootstrap, package validation, and tests were enough to prove self-host viability.
