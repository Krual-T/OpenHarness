# Evidence

## Residual Risks
- The package currently defines protocol shape but does not yet productize it in live skills or templates.
- The eventual implementation may still need a small machine-readable declaration surface if doc-only routing proves too weak.

## Manual Steps
- None in this round.

## Files
- `docs/task-packages/runtime-capability-contract/README.md`
- `docs/task-packages/runtime-capability-contract/STATUS.yaml`
- `docs/task-packages/runtime-capability-contract/01-requirements.md`
- `docs/task-packages/runtime-capability-contract/02-overview-design.md`
- `docs/task-packages/runtime-capability-contract/03-detailed-design.md`
- `docs/task-packages/runtime-capability-contract/05-verification.md`
- `docs/task-packages/runtime-capability-contract/06-evidence.md`
- `docs/task-packages/harness-completion-roadmap/*`
- `docs/archived/task-packages/runtime-verification-baseline/*`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task runtime-capability-contract OH-013 "Runtime Capability Contract" --owner codex --summary "Define how OpenHarness should describe, route, verify, and write back project-specific runtime capabilities without assuming a single universal runtime debugging skill."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Artifact Paths
- `docs/task-packages/runtime-capability-contract/05-verification.md`

## Follow-ups
- Productize the contract in live `using-openharness` routing and reference docs.
- Decide later whether the declaration shape should stay docs-first or gain a small machine-readable schema.
