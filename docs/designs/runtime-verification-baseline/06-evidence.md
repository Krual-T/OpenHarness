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
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/templates/design-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/design-package.05-verification.md`
- `skills/using-openharness/references/templates/design-package.06-evidence.md`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/verification-before-completion/SKILL.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-design runtime-verification-baseline OH-005 "Runtime Verification Baseline" --owner codex --summary "Define the minimum verification protocol and evidence contract for OpenHarness tasks in repositories that may not have an existing runtime harness."`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'verification_path_sections or manual_and_insufficient_paths'`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`

## Follow-ups
- Decide whether `insufficient verification` should map to a status restriction, a documentation-only rule, or both.
- Decide whether to add machine-readable verification-path metadata to `STATUS.yaml.verification` only after the docs-first contract is exercised in real packages.
- Implement the second rollout wave in this order: `openharness.py verify`, CLI/tests, then status-semantics integration.
