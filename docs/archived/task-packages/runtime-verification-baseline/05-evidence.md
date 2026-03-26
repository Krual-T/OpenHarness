# Evidence

## Residual Risks
- The repository now has a shared verification vocabulary, but it still relies on documentation and lightweight CLI behavior rather than a richer execution-artifact system.

## Files
- `AGENTS.md`
- `docs/archived/task-packages/runtime-verification-baseline/README.md`
- `docs/archived/task-packages/runtime-verification-baseline/STATUS.yaml`
- `docs/archived/task-packages/runtime-verification-baseline/01-requirements.md`
- `docs/archived/task-packages/runtime-verification-baseline/02-overview-design.md`
- `docs/archived/task-packages/runtime-verification-baseline/03-detailed-design.md`
- `docs/archived/task-packages/runtime-verification-baseline/04-verification.md`
- `docs/archived/task-packages/runtime-verification-baseline/05-evidence.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.04-verification.md`
- `skills/using-openharness/references/templates/task-package.05-evidence.md`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/verification-before-completion/SKILL.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task runtime-verification-baseline OH-005 "Runtime Verification Baseline" --owner codex --summary "Define the minimum verification protocol and evidence contract for OpenHarness tasks in repositories that may not have an existing runtime harness."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'verification_path_sections or manual_and_insufficient_paths'`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'declared_manual_scenarios or no_declared_verification_path'`
- `mv docs/task-packages/runtime-verification-baseline docs/archived/task-packages/runtime-verification-baseline`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Follow-ups
- Decide in a downstream status-semantics package whether `insufficient verification` should become an explicit status-transition restriction in addition to the current CLI/documentation rule.
- Revisit machine-readable verification-path metadata in `STATUS.yaml.verification` only after more packages exercise the docs-first contract.
- Feed this completed baseline into the next focused package selection under `OH-004`, most likely `status semantics tightening` or `no-harness bootstrap workflow`.
