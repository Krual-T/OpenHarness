# Evidence

## Files
- `AGENTS.md`
- `docs/designs/runtime-verification-baseline/README.md`
- `docs/designs/runtime-verification-baseline/STATUS.yaml`
- `docs/designs/runtime-verification-baseline/01-requirements.md`
- `docs/designs/runtime-verification-baseline/02-overview-design.md`
- `docs/designs/runtime-verification-baseline/03-detailed-design.md`
- `docs/designs/runtime-verification-baseline/05-verification.md`
- `docs/designs/runtime-verification-baseline/06-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-design runtime-verification-baseline OH-005 "Runtime Verification Baseline" --owner codex --summary "Define the minimum verification protocol and evidence contract for OpenHarness tasks in repositories that may not have an existing runtime harness."`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Follow-ups
- Implement the first rollout wave in this order: templates, verification-oriented skills, then CLI/test updates.
- Decide whether `insufficient verification` should map to a status restriction, a documentation-only rule, or both.
- Decide whether to add machine-readable verification-path metadata to `STATUS.yaml.verification` only after the docs-first contract is exercised in real packages.
