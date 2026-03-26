# Verification

## Verification Path
- Planned Path:
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
- Executed Path:
  - Ran `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or capability_contract'` first to confirm the new runtime-capability contract assertions failed before implementation and passed after the live-doc updates.
  - Ran `uv run python skills/using-openharness/scripts/openharness.py check-tasks` after productizing the live docs and task-package updates.
  - Ran `uv run pytest` to confirm the full repository suite still passes with the new runtime-capability contract surface.
- Path Notes:
  - This round verifies documentation-backed protocol productization rather than a concrete project runtime helper.
  - The targeted red/green test proves the new contract assertions are real, while `check-tasks` plus the full suite confirm the repository still validates cleanly.

Use `verifying` only when implementation is complete enough to gather fresh evidence for the declared verification path.
Do not use `archived` while implementation is still deferred to a future wave.

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Expected Outcomes
- The updated task package validates cleanly.
- The live docs, reference contract, and repository tests agree on the runtime-capability routing model.
- The repository test suite still passes after productizing the contract.

## Latest Result
- Passed on 2026-03-23:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or capability_contract'`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - `uv run pytest`
  - Result: targeted runtime-capability assertions passed, `check-tasks` validated `16 task package(s)`, and the full suite passed with `50 passed`.
- Latest Artifact:
  - `openharness.py verify runtime-capability-contract` should record the latest JSON artifact under `.harness/artifacts/OH-013/verification-runs/`.
