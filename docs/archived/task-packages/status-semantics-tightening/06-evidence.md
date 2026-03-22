# Evidence

## Residual Risks
- The repository still lacks machine-enforced checks for most transition rules; this package currently defines the semantics rather than fully enforcing them.
- Validation now catches missing verification paths for `verifying` and `archived`, but earlier status/readiness mismatches are still documentation-level rules.
- Template and skill guidance now repeat the same late-stage boundaries, but there is still no machine validation for earlier design-ready statuses.

## Manual Steps
- None in this round.

## Files
- `docs/archived/task-packages/status-semantics-tightening/README.md`
- `docs/archived/task-packages/status-semantics-tightening/STATUS.yaml`
- `docs/archived/task-packages/status-semantics-tightening/01-requirements.md`
- `docs/archived/task-packages/status-semantics-tightening/02-overview-design.md`
- `docs/archived/task-packages/status-semantics-tightening/03-detailed-design.md`
- `docs/archived/task-packages/status-semantics-tightening/05-verification.md`
- `docs/archived/task-packages/status-semantics-tightening/06-evidence.md`
- `docs/task-packages/harness-completion-roadmap/02-overview-design.md`
- `docs/task-packages/harness-completion-roadmap/05-verification.md`
- `docs/task-packages/harness-completion-roadmap/06-evidence.md`
- `skills/exploring-solution-space/SKILL.md`
- `skills/using-openharness/SKILL.md`
- `skills/using-openharness/references/templates/task-package.README.md`
- `skills/using-openharness/references/templates/task-package.STATUS.yaml`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.05-verification.md`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py new-task status-semantics-tightening OH-006 "Status Semantics Tightening" --owner codex --summary "Define stronger status meanings, transition rules, and evidence gates for OpenHarness task packages."`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'later_stage_statuses_only or explicit_package_target_before_in_progress'`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'verifying_without_verification_path or archived_without_verification_path'`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'include_status_guidance'`
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'workflow_skills_include_status_guidance'`
- `mv docs/task-packages/status-semantics-tightening docs/archived/task-packages/status-semantics-tightening`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`

## Follow-ups
- Decide whether `validate_design_package` should gain lightweight semantic checks for earlier statuses such as `overview_ready` and `detailed_ready`, or whether those should remain documentation-driven.
- Feed the settled status contract back into the no-harness bootstrap and maintenance streams once the first implementation wave is verified.
- Decide whether additional workflow skills beyond `using-openharness` and `exploring-solution-space` need explicit status cues, or whether the current coverage is already sufficient.
