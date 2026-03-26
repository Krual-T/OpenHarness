# Evidence

## Residual Risks
- The first wave only checks minimum semantic anchors. A package can still be weakly designed and pass if it fills the required sections honestly.
- Status transitions are still edited directly in `STATUS.yaml`; this package did not add a dedicated `transition` command.
- Verification execution is still documented in task packages rather than recorded as structured run artifacts under `.harness/artifacts/`.

## Manual Steps
- None.

## Files
- `docs/archived/task-packages/task-package-semantic-validation/*`
- `docs/archived/task-packages/harness-completion-roadmap/README.md`
- `docs/archived/task-packages/harness-completion-roadmap/02-overview-design.md`
- `docs/archived/task-packages/harness-completion-roadmap/03-detailed-design.md`
- `docs/archived/task-packages/harness-completion-roadmap/05-evidence.md`
- `docs/archived/task-packages/reflective-design-review/02-overview-design.md`
- `docs/archived/task-packages/reflective-design-review/03-detailed-design.md`
- `docs/archived/task-packages/reflective-design-review/04-verification.md`
- `docs/archived/task-packages/reflective-design-review/05-evidence.md`
- `docs/archived/task-packages/runtime-verification-baseline/03-detailed-design.md`
- `docs/archived/task-packages/runtime-verification-baseline/04-verification.md`
- `docs/archived/task-packages/runtime-verification-baseline/05-evidence.md`
- `docs/archived/task-packages/self-hosting-bootstrap/02-overview-design.md`
- `docs/archived/task-packages/self-hosting-bootstrap/03-detailed-design.md`
- `docs/archived/task-packages/self-hosting-bootstrap/04-verification.md`
- `docs/archived/task-packages/self-hosting-bootstrap/05-evidence.md`
- `docs/archived/task-packages/workflow-redesign/02-overview-design.md`
- `docs/archived/task-packages/workflow-redesign/03-detailed-design.md`
- `docs/archived/task-packages/workflow-redesign/04-verification.md`
- `docs/archived/task-packages/workflow-redesign/05-evidence.md`
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task task-package-semantic-validation OH-009 "Task Package Semantic Validation" --owner codex --summary "Strengthen check-tasks so status readiness is anchored to minimum document semantics instead of file existence alone."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'placeholder_requirements or overview_ready_without_reflection or archived_without_evidence_anchors or accepts_detailed_ready_with_filled_semantic_anchors'`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'declared_manual_scenarios or no_declared_verification_path or later_stage_statuses_only or explicit_package_target_before_in_progress'`
- `uv run pytest`
- `mv docs/task-packages/task-package-semantic-validation docs/archived/task-packages/task-package-semantic-validation`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Follow-ups
- Decide in a later focused package whether to add a `transition` subcommand that enforces legal state moves instead of relying on direct `STATUS.yaml` edits.
- Decide in a later focused package whether to record verification runs under `.harness/artifacts/` and tie `04-verification.md` to those artifacts.
