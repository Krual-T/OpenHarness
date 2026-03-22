# Evidence

## Residual Risks
- The package defines policy but does not yet productize it in templates or validators.
- If the repository later insists on Chinese section titles, a focused implementation wave will still be required.

## Manual Steps
- None in this round.

## Files
- `docs/task-packages/task-package-language-policy-and-localization/README.md`
- `docs/task-packages/task-package-language-policy-and-localization/STATUS.yaml`
- `docs/task-packages/task-package-language-policy-and-localization/01-requirements.md`
- `docs/task-packages/task-package-language-policy-and-localization/02-overview-design.md`
- `docs/task-packages/task-package-language-policy-and-localization/03-detailed-design.md`
- `docs/task-packages/task-package-language-policy-and-localization/05-verification.md`
- `docs/task-packages/task-package-language-policy-and-localization/06-evidence.md`

## Commands
- `uv run python skills/using-openharness/scripts/openharness.py new-task task-package-language-policy-and-localization OH-015 "Task Package Language Policy And Localization" --owner codex --summary "Define whether OpenHarness task packages should be Chinese-first, which repository surfaces stay English, and how localization should interact with templates, validation, and readability for the human maintainer."`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- `uv run pytest`

## Artifact Paths
- `docs/task-packages/task-package-language-policy-and-localization/05-verification.md`

## Follow-ups
- If the policy is accepted, open a focused implementation package for template and validator rollout.
- Decide later whether title localization should support dual titles, Chinese titles, or permanent English titles.
