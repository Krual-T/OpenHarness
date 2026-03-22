# Evidence

## Residual Risks
- OpenHarness still cannot stop a human from bypassing the CLI and editing files directly; the new contract makes the supported path much stronger, but repository discipline still matters.
- Repository-wide reference scanning currently reports lingering active-root references after archive rather than rewriting every external reference automatically.

## Manual Steps
- None for the automated verification path in this round.

## Files
- `docs/archived/task-packages/workflow-transition-and-verification-artifacts/*`
- `docs/task-packages/harness-completion-roadmap/*`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/using-openharness/references/templates/task-package.STATUS.yaml`
- `skills/using-openharness/references/templates/task-package.05-verification.md`
- `skills/using-openharness/references/templates/task-package.06-evidence.md`

## Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'single_cli_supports_all_subcommands or task_package_commands_use_current_handlers_only or transition_rejects_skipped_forward_moves or verify_records_artifact_and_status_metadata or transition_to_archived_moves_package_and_rewrites_paths'`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-transition-and-verification-artifacts requirements_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-transition-and-verification-artifacts overview_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-transition-and-verification-artifacts detailed_ready`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-transition-and-verification-artifacts in_progress`
- `uv run python skills/using-openharness/scripts/openharness.py verify workflow-transition-and-verification-artifacts`
- `uv run python skills/using-openharness/scripts/openharness.py transition workflow-transition-and-verification-artifacts verifying`
- `uv run python skills/using-openharness/scripts/openharness.py verify workflow-transition-and-verification-artifacts`

## Artifact Paths
- `.harness/artifacts/OH-010/verification-runs/20260322T145529623928Z.json`
- `.harness/artifacts/OH-010/verification-runs/20260322T145640065490Z.json`
- `.harness/artifacts/OH-010/verification-runs/latest.json`

## Follow-ups
- Consider whether a later package should productize repository-wide external-reference repair after archive instead of only scanning and reporting it.
