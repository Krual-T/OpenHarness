# Evidence

## Residual Risks
- The implementation wave may still need one more decision on how much guidance belongs in docs/templates versus mechanical enforcement.
- No end-to-end fixture yet proves the new baseline-versus-runtime wording against a realistic Python task package; that validation remains follow-up work.
- `pytest` as a minimum floor is intentionally weaker than runtime tests, so implementation must state clearly when runtime tests are required now versus recommended next.

## Manual Steps
- None yet. If the verification-maturity behavior is later validated manually against a fixture repository or task package, record the exact sequence here.

## Files
- `docs/archived/task-packages/python-verification-maturity/README.md`
- `docs/archived/task-packages/python-verification-maturity/STATUS.yaml`
- `docs/archived/task-packages/python-verification-maturity/01-requirements.md`
- `docs/archived/task-packages/python-verification-maturity/02-overview-design.md`
- `docs/archived/task-packages/python-verification-maturity/03-detailed-design.md`
- `docs/archived/task-packages/python-verification-maturity/05-verification.md`
- `docs/archived/task-packages/python-verification-maturity/06-evidence.md`
- `docs/archived/task-packages/harness-completion-roadmap/README.md`
- `docs/archived/task-packages/harness-completion-roadmap/STATUS.yaml`
- `docs/archived/task-packages/harness-completion-roadmap/02-overview-design.md`
- `docs/archived/task-packages/harness-completion-roadmap/03-detailed-design.md`
- `docs/archived/task-packages/harness-completion-roadmap/05-verification.md`
- `docs/archived/task-packages/harness-completion-roadmap/06-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task no-harness-bootstrap-workflow OH-007 "No-Harness Bootstrap Workflow" --owner codex --summary "Define how OpenHarness should enter a repository with no harness, no package history, and no established verification loop, while still producing a usable first-round package and verification path."`
- `mv docs/task-packages/no-harness-bootstrap-workflow docs/task-packages/python-verification-maturity`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`
- `mv docs/task-packages/python-verification-maturity docs/archived/task-packages/python-verification-maturity`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`

## Follow-ups
- Implement the first Python verification-maturity support wave in docs, templates, and completion guidance.
- Decide whether the baseline-versus-runtime distinction needs a dedicated fixture repository or can be validated with repository-local temp fixtures inside `skills/using-openharness/tests/`.
