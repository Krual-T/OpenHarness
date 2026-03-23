# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - run `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - run `uv run pytest`
  - add targeted tests that exercise the new semantic-anchor failures and a passing package case
- Fallback Path:
  - if a proposed anchor is too noisy against current repository packages, narrow the rule before landing code rather than keeping a flaky validator
  - if doc-template changes are needed to keep the validator honest, land those in the same round so validation and guidance stay aligned
- Planned Evidence:
  - updated `OH-009` design docs
  - `openharness.py` semantic-anchor helpers and validation wiring
  - template updates for any newly required reflection or evidence headings
  - tests that pin both passing and failing status/readiness combinations

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Files Added Or Changed
- `docs/task-packages/task-package-semantic-validation/*`
- `docs/archived/task-packages/harness-completion-roadmap/*`
- `skills/using-openharness/scripts/openharness.py`
- `skills/using-openharness/tests/test_openharness.py`
- `skills/using-openharness/references/templates/task-package.02-overview-design.md`
- `skills/using-openharness/references/templates/task-package.03-detailed-design.md`
- `skills/using-openharness/references/templates/task-package.05-verification.md`
- `skills/using-openharness/references/templates/task-package.06-evidence.md`

## Interfaces
- Add a small internal representation in `openharness.py` for markdown semantic anchors:
  - document path
  - required headings or labeled bullets
  - placeholder patterns that should count as empty
- Extend `validate_design_package` to:
  - map status to required anchor set
  - report targeted errors like `overview_ready requires non-placeholder section '## Key Flows'`
- Keep `STATUS.yaml` unchanged in this round; status-to-anchor mapping should live in repository code and docs, not in per-package bespoke metadata.
- Tests should cover both:
  - repository fixtures that fail because docs are still placeholder shells
  - current real packages that continue to validate after templates and docs are aligned

## Error Handling
- Treat empty headings, single placeholder bullets such as `-` or `1.`, and unchanged default template text as missing semantic content.
- Do not fail packages for stylistic differences, paragraph length, or alternate markdown formatting that still conveys the required anchor honestly.
- If a check would require parsing arbitrary prose semantics, stop and narrow it; the first wave should remain deterministic.
- Keep archived historical packages valid by updating their docs only if the new rules intentionally apply to them; otherwise scope checks to active semantics in a way that does not rewrite history gratuitously.

## Migration Notes
- `OH-006` already established the shared status meanings and some late-stage contradiction checks; this package should build on that implementation rather than redefining the model.
- If this first wave succeeds, the likely next packages are:
  - a `transition` command that enforces allowed state moves
  - verification-artifact recording under `.harness/artifacts/`
- `OH-004` should be updated to list this package as the active follow-up for stronger transition enforcement and semantic validation.

## Detailed Reflection
- I challenged whether `requirements_ready` should stay out of scope because early statuses are more common. I rejected that concern because the `01-requirements.md` template is stable and the required anchors are minimal.
- I challenged whether requiring reflection headings in `02` and `03` would be too coupled to current prose. I kept them because the repository already treats reflection as part of design readiness, so not checking it would leave an obvious honesty gap.
- I checked whether placeholder detection should be regex-heavy. It should not. The implementation should prefer a short list of explicit placeholder patterns derived from current templates.
- I checked whether archived packages should be grandfathered entirely. They should not by default, because `archived` is exactly where false completion claims are most damaging. If one historical package breaks for a justified reason, fix that package or narrow the specific rule with evidence.
- I checked whether runtime verification is concrete enough. It is, because the repository already uses `check-tasks` and `pytest` as the canonical baseline for protocol changes.
