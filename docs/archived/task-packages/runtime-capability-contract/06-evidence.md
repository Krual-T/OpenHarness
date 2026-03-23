# Evidence

## Residual Risks
- The contract is now productized in live docs and tests, but repositories still do not get a standard runtime surface map example until `OH-014` lands.
- The eventual implementation may still need a small machine-readable declaration surface if doc-only routing proves too weak.

## Manual Steps
- None in this round.

## Files
- `docs/archived/task-packages/runtime-capability-contract/README.md`
- `docs/archived/task-packages/runtime-capability-contract/STATUS.yaml`
- `docs/archived/task-packages/runtime-capability-contract/01-requirements.md`
- `docs/archived/task-packages/runtime-capability-contract/02-overview-design.md`
- `docs/archived/task-packages/runtime-capability-contract/03-detailed-design.md`
- `docs/archived/task-packages/runtime-capability-contract/05-verification.md`
- `docs/archived/task-packages/runtime-capability-contract/06-evidence.md`
- `README.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/skill-hub.md`
- `skills/using-openharness/references/runtime-capability-contract.md`
- `skills/using-openharness/tests/test_openharness.py`
- `docs/archived/task-packages/harness-completion-roadmap/*`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task runtime-capability-contract OH-013 "Runtime Capability Contract" --owner codex --summary "Define how OpenHarness should describe, route, verify, and write back project-specific runtime capabilities without assuming a single universal runtime debugging skill."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'runtime_capability or capability_contract'`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py transition runtime-capability-contract in_progress`
- `uv run python skills/using-openharness/scripts/openharness.py transition runtime-capability-contract verifying`
- `uv run python skills/using-openharness/scripts/openharness.py verify runtime-capability-contract`
- `uv run python skills/using-openharness/scripts/openharness.py transition runtime-capability-contract archived`

## Artifact Paths
- `docs/archived/task-packages/runtime-capability-contract/05-verification.md`

## Follow-ups
- `OH-014` should now productize the repository-facing runtime surface map that consumes this contract.
- `OH-016` should now define the helper-addition workflow on top of this archived baseline.
- Decide later whether the declaration shape should stay docs-first or gain a small machine-readable schema.
