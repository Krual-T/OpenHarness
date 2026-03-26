# Requirements

## Goal
Implement a first wave of semantic validation for OpenHarness task packages so readiness statuses are backed by minimum document meaning, not only by file existence and a manually edited `STATUS.yaml`.

## Problem Statement
OpenHarness already validates the fixed task-package structure and some late-stage status constraints:

- required files must exist
- required `STATUS.yaml` keys must exist
- `archived` must live under the archive root
- `verifying` and `archived` must declare at least one verification path

That baseline is useful, but it still leaves a large honesty gap between what the repository says and what the package docs actually contain.

Today a package can still pass validation while claiming a stronger readiness state than its docs justify. Examples:

- `requirements_ready` while `01-requirements.md` is still a placeholder shell
- `overview_ready` while `02-overview-design.md` does not actually describe system boundary or architecture
- `detailed_ready` while `03-detailed-design.md` lacks implementation landing points or runtime verification planning
- `verifying` while `04-verification.md` has not recorded an executed path yet
- `archived` while `05-evidence.md` does not record the concrete evidence a later reader would need

This creates several concrete risks:

- later agents trust a status claim and skip work that was never really completed
- archived packages look more complete than they actually are
- verification becomes a declaration in `STATUS.yaml` rather than a claim tied to document evidence
- the repository feels strict while still relying on human interpretation for the most important contradictions

Archived `OH-006 Status Semantics Tightening` deliberately stopped at lightweight contradiction checks for `verifying` and `archived`. This package is the next implementation wave: strengthen semantic validation without jumping straight to a new transition engine, artifact format, or broader workflow redesign.

## Required Outcomes
1. Define the minimum semantic anchors that must exist in package docs for key readiness statuses to be credible.
2. Extend `check-tasks` so it validates those anchors mechanically, using simple and durable checks rather than brittle prose interpretation.
3. Keep the first wave narrow enough to improve honesty immediately without turning task packages into a heavyweight schema-first system.
4. Update docs, templates, and tests so the new validation behavior is explicit and future drift is caught automatically.
5. Record which adjacent ideas remain intentionally out of scope for a later package, especially status-transition commands and execution-artifact recording.

## Success Conditions
- A package cannot claim `requirements_ready`, `overview_ready`, `detailed_ready`, `verifying`, or `archived` while the corresponding doc is still missing its minimum required semantic sections.
- The new checks fail for obvious placeholder or structurally incomplete docs, but avoid trying to judge nuanced design quality.
- Future agents can predict the validation rules from repository docs and templates rather than discovering them only by trial and error.
- The implementation leaves room for later `transition` and verification-artifact work without forcing that design in this round.

## Non-Goals
- Add a full status-transition command or machine-enforced workflow engine in this package.
- Introduce mandatory execution artifacts under `.harness/artifacts/` as part of the same change.
- Score document quality or semantic correctness beyond minimum structural anchors.
- Re-open the meaning of the shared status vocabulary already defined by `OH-006`.

## Constraints
- Preserve the single `openharness.py` CLI and the existing task-package filesystem model.
- Prefer cheap, predictable checks over natural-language heuristics that are likely to be noisy.
- Reuse existing template section headings where practical so validation rules align with the docs agents already write.
- Keep the first wave compatible with archived `OH-005` and `OH-006` semantics instead of inventing a second protocol.
