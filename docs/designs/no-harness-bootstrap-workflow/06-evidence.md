# Evidence

## Residual Risks
- The implementation wave may still need one more decision on how much CLI scaffolding is worth adding beyond docs and templates.
- No end-to-end fixture for Python cold-start entry exists yet; that validation remains follow-up work.
- `pytest` as a minimum floor is intentionally weaker than runtime tests, so implementation must state clearly when runtime tests are required now versus recommended next.

## Manual Steps
- None yet. If Python cold-start behavior is later validated manually against a fixture repository, record the exact sequence here.

## Files
- `docs/designs/no-harness-bootstrap-workflow/README.md`
- `docs/designs/no-harness-bootstrap-workflow/STATUS.yaml`
- `docs/designs/no-harness-bootstrap-workflow/01-requirements.md`
- `docs/designs/no-harness-bootstrap-workflow/02-overview-design.md`
- `docs/designs/no-harness-bootstrap-workflow/03-detailed-design.md`
- `docs/designs/no-harness-bootstrap-workflow/05-verification.md`
- `docs/designs/no-harness-bootstrap-workflow/06-evidence.md`
- `docs/designs/harness-completion-roadmap/README.md`
- `docs/designs/harness-completion-roadmap/STATUS.yaml`
- `docs/designs/harness-completion-roadmap/02-overview-design.md`
- `docs/designs/harness-completion-roadmap/03-detailed-design.md`
- `docs/designs/harness-completion-roadmap/05-verification.md`
- `docs/designs/harness-completion-roadmap/06-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-design no-harness-bootstrap-workflow OH-007 "No-Harness Bootstrap Workflow" --owner codex --summary "Define how OpenHarness should enter a repository with no harness, no package history, and no established verification loop, while still producing a usable first-round package and verification path."`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run pytest`
- `uv run python skills/using-openharness/scripts/openharness.py check-designs`
- `uv run pytest`

## Follow-ups
- Implement the first Python cold-start support wave in docs, templates, and any minimal CLI help defined by this package.
- Decide whether Python cold start needs a dedicated fixture repository or can be validated with repository-local temp fixtures inside `skills/using-openharness/tests/`.
