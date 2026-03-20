# Overview Design

## System Boundary
This round only covers the minimal repository machinery needed for OpenHarness to operate on itself:

- repo-local Python dependency declaration
- repo-local design package tree
- harness CLI repo-path discovery for the current `skills/` layout
- tests aligned with the actual repository structure
- small documentation corrections required for self-hosting legibility

## Proposed Structure
- Add `pyproject.toml` so `uv run` can provision `PyYAML` and `pytest`.
- Scaffold `docs/designs/self-hosting-bootstrap/` using the existing harness templates and use it as the first active package.
- Adjust the harness CLI so repo-local `skills/using-openharness/...` manifests and templates are discoverable when operating inside this repository.
- Rewrite the harness tests to validate the actual repository instead of inherited `openrelay` / `.codex/skills` assumptions.
- Fix the most obvious stale identity/path mistakes in top-level docs so the repo describes itself correctly.

## Key Flows
1. Fresh checkout runs `uv run python skills/using-openharness/scripts/openharness.py bootstrap`.
2. `uv` installs declared dependencies and the CLI finds `skills/using-openharness/references/manifest.yaml`.
3. The CLI discovers `docs/designs/self-hosting-bootstrap/` as the active package.
4. `check-designs` validates the package and `pytest` validates the self-hosting assumptions.

## Trade-offs
- This keeps the current package protocol, including `04-implementation-plan.md`, even though the workflow likely evolves later.
- The first round focuses on repository operability, not on finishing the higher-level workflow redesign discussed earlier.
- Rewriting tests to current reality is lower risk than forcing the repository to mimic the old `.codex/skills` fixture layout internally.
