# Verification

## Verification Path
- Planned Path:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'skill_hub_uses_protocol_status_plus_stage_model or readme_describes_plug_and_play_harness_and_python_pytest_floor'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Executed Path:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'skill_hub_uses_protocol_status_plus_stage_model or readme_describes_plug_and_play_harness_and_python_pytest_floor'`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model requirements_ready`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model overview_ready`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model detailed_ready`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model in_progress`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model verifying`
  - `uv run python skills/using-openharness/scripts/openharness.py verify skill-taxonomy-and-stage-model`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model archived`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
- Path Notes:
  - The package changes task docs, live repository docs, skill docs, and repository tests, so targeted pytest plus full repository validation is the minimum credible path.

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- The new package validates cleanly during design and implementation.
- Repository tests pin the new two-layer skill model and Python verification baseline.
- The full suite stays green after live docs and skill wording are updated.

## Latest Result
- Passed on 2026-03-23:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'skill_hub_uses_protocol_status_plus_stage_model or readme_describes_plug_and_play_harness_and_python_pytest_floor'`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model verifying`
  - `uv run python skills/using-openharness/scripts/openharness.py verify skill-taxonomy-and-stage-model`
  - `uv run python skills/using-openharness/scripts/openharness.py transition skill-taxonomy-and-stage-model archived`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
  - `uv run pytest`
  - Result: the live repository now exposes the two-layer skill model, the Python-first pytest baseline is documented, the package recorded a structured verification artifact, the package archived cleanly, post-archive `check-tasks` validated the repository cleanly, `bootstrap` returned to a single active package (`OH-004`), and the full suite passed with `44 passed`.
- Latest Artifact:
  - `.harness/artifacts/OH-012/verification-runs/20260322T164921906572Z.json`
