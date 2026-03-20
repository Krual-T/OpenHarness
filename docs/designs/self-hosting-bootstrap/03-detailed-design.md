# Detailed Design

## Files Added Or Changed
- Add `pyproject.toml` with runtime dependency `PyYAML` and dev dependency `pytest`.
- Update `skills/using-openharness/scripts/openharness.py` to resolve repo-local manifests and templates from `skills/using-openharness/...`.
- Add the active design package under `docs/designs/self-hosting-bootstrap/`.
- Rewrite `skills/using-openharness/tests/test_openharness.py` to validate the real repo layout and a minimal self-hosting package inventory.
- Fix small doc mistakes in `AGENTS.md` and `README.md`.

## Interfaces
- `openharness.py bootstrap` must work against the current repository root with no undeclared Python packages.
- `load_manifest()` must prefer repo-local `skills/using-openharness/references/manifest.yaml` when present.
- `create_design_package()` must prefer repo-local `skills/using-openharness/references/templates/` when present.
- The package `STATUS.yaml` for this round declares the commands used for self-host verification.

## Error Handling
- If no design packages exist, `bootstrap` may still succeed with an empty inventory, but after this round `check-designs` and tests should have a valid package to inspect.
- Repo-local path discovery must keep existing fallback paths so installed/global skill layouts still work.

## Migration Notes
- This round intentionally leaves `writing-plans` and `04-implementation-plan.md` in place; protocol simplification can happen in a later package.
- The rewritten tests should stop depending on inherited historical packages from other repositories.
